import json
import requests
import networkx as nx
from itertools import combinations
from datetime import datetime
import statistics
import os


def load_json_remote(url):
    """Load JSON data from a remote URL."""
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def find_field_combinations(obj):
    """Recursively find sets of co-occurring JSON field names."""
    results = []

    if isinstance(obj, dict):
        keys = set(obj.keys())
        if len(keys) > 1:
            results.append(keys)
        for value in obj.values():
            results.extend(find_field_combinations(value))

    elif isinstance(obj, list):
        for item in obj:
            results.extend(find_field_combinations(item))

    return results


def build_field_graph(data):
    """Build a field co-occurrence graph."""
    G = nx.Graph()
    cooccurrence_sets = find_field_combinations(data)

    for field_set in cooccurrence_sets:
        for field in field_set:
            G.add_node(field)
        for u, v in combinations(field_set, 2):
            if G.has_edge(u, v):
                G[u][v]["weight"] += 1
            else:
                G.add_edge(u, v, weight=1)
    return G


def compute_centrality_measures(G):
    """Compute various centrality metrics for each node."""
    degree = nx.degree_centrality(G)
    betweenness = nx.betweenness_centrality(G)
    closeness = nx.closeness_centrality(G)
    try:
        eigenvector = nx.eigenvector_centrality(G, max_iter=1000)
    except nx.PowerIterationFailedConvergence:
        eigenvector = {n: 0 for n in G.nodes()}

    return {
        "degree": degree,
        "betweenness": betweenness,
        "closeness": closeness,
        "eigenvector": eigenvector,
    }


def interpret_centrality(centrality):
    """Generate an interpretation narrative."""
    degree = centrality["degree"]
    betweenness = centrality["betweenness"]
    closeness = centrality["closeness"]
    eigenvector = centrality["eigenvector"]

    def top_keys(metric_dict, n=5):
        return [f"{k} ({v:.3f})" for k, v in sorted(metric_dict.items(), key=lambda x: x[1], reverse=True)[:n]]

    interpretation = [
        "## Interpretation of Centrality Results\n",
        "Centrality measures identify the most structurally influential fields within the JSON schema. "
        "These indicate which fields are most central (high degree), which act as connectors (high betweenness), "
        "which can quickly reach others (high closeness), and which connect to other influential fields (high eigenvector).\n\n",
        f"### Most Connected Fields (Degree Centrality)\n{', '.join(top_keys(degree))}\n\n",
        f"### Key Bridge Fields (Betweenness Centrality)\n{', '.join(top_keys(betweenness))}\n\n",
        f"### Most Accessible Fields (Closeness Centrality)\n{', '.join(top_keys(closeness))}\n\n",
        f"### Most Influential Fields (Eigenvector Centrality)\n{', '.join(top_keys(eigenvector))}\n\n",
        "_Interpretation:_\n"
        "Fields with **high degree** appear alongside many others — they are structurally core. "
        "Fields with **high betweenness** link otherwise separate parts of the schema and may represent connectors "
        "(e.g., ‘meeting’, ‘summary’, or ‘participants’). "
        "Fields with **high closeness** are well-distributed across the structure, suggesting they can reach or influence many others easily. "
        "Finally, fields with **high eigenvector centrality** are not only connected but connected to other important fields — "
        "these represent high-level schema hubs or critical integration points."
    ]

    return "\n".join(interpretation)


def write_markdown_report(G, centrality, output_file):
    """Write all centrality results and interpretations to a Markdown file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# JSON Field Centrality Analysis Report\n")
        f.write(f"**Generated on:** {timestamp}\n\n")
        f.write(f"- Total Fields: {len(G.nodes)}\n")
        f.write(f"- Total Relationships: {len(G.edges)}\n\n")

        f.write("## Top 10 Fields by Centrality\n")
        f.write("| Rank | Field | Degree | Betweenness | Closeness | Eigenvector |\n")
        f.write("|------|--------|----------|--------------|-------------|-------------|\n")

        top_fields = sorted(centrality["degree"].keys(), key=lambda x: centrality["degree"][x], reverse=True)[:10]
        for i, node in enumerate(top_fields, 1):
            f.write(
                f"| {i} | {node} | "
                f"{centrality['degree'][node]:.3f} | "
                f"{centrality['betweenness'][node]:.3f} | "
                f"{centrality['closeness'][node]:.3f} | "
                f"{centrality['eigenvector'][node]:.3f} |\n"
            )
        f.write("\n")

        interpretation = interpret_centrality(centrality)
        f.write(interpretation)
        f.write("\n")

    print(f"✅ Centrality analysis report saved to: {output_file}")


def main():
    url = (
        "https://raw.githubusercontent.com/SingularityNET-Archive/"
        "SingularityNET-Archive/refs/heads/main/Data/Snet-Ambassador-Program/"
        "Meeting-Summaries/2025/meeting-summaries-array.json"
    )
    output_dir = "reports"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "centrality_analysis_report.md")

    print("📡 Fetching JSON data...")
    data = load_json_remote(url)
    print("✅ JSON file downloaded.")

    print("🔍 Building field co-occurrence graph...")
    G = build_field_graph(data)
    print(f"📊 Graph contains {len(G.nodes)} fields and {len(G.edges)} relationships.")

    print("📈 Computing centrality measures...")
    centrality = compute_centrality_measures(G)

    write_markdown_report(G, centrality, output_file)


if __name__ == "__main__":
    main()
