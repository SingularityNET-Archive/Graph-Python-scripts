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


def clustering_analysis(G):
    """Compute clustering coefficients."""
    local_clustering = nx.clustering(G, weight="weight")
    avg_clustering = nx.average_clustering(G, weight="weight")
    transitivity = nx.transitivity(G)  # global measure
    return local_clustering, avg_clustering, transitivity


def interpret_clustering(local_clustering, avg_clustering, transitivity):
    """Generate interpretation narrative for clustering results."""
    sorted_nodes = sorted(local_clustering.items(), key=lambda x: x[1], reverse=True)
    top_nodes = [f"{k} ({v:.3f})" for k, v in sorted_nodes[:5]]

    interpretation = [
        "## Interpretation of Clustering Results\n",
        "The clustering coefficient measures how likely a node’s neighbors "
        "are to also be connected to one another. High clustering suggests "
        "that related fields consistently appear together in the JSON structure, "
        "forming tightly interconnected groups.\n\n",
        f"### Global Measures\n"
        f"- **Average Clustering Coefficient:** {avg_clustering:.3f}\n"
        f"- **Network Transitivity:** {transitivity:.3f}\n\n",
        "### Fields with Highest Local Clustering\n",
        ", ".join(top_nodes) + "\n\n",
        "_Interpretation:_\n"
        "If the **average clustering coefficient** is high (e.g., >0.5), "
        "it indicates that many JSON fields co-occur frequently, forming "
        "cohesive 'themes' or substructures (like `participants` + `summary` + `workgroups`). "
        "A **low value** (e.g., <0.2) would suggest a more modular or fragmented structure, "
        "where fields are grouped into separate contexts. "
        "Fields with **high local clustering** serve as 'cluster cores' — they often appear "
        "in tight-knit groups, while those with low clustering tend to bridge distinct sections."
    ]
    return "\n".join(interpretation)


def write_markdown_report(G, local_clustering, avg_clustering, transitivity, output_file):
    """Write clustering results and interpretation to a Markdown file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# JSON Field Clustering Coefficient Report\n")
        f.write(f"**Generated on:** {timestamp}\n\n")
        f.write(f"- Total Fields (Nodes): {len(G.nodes)}\n")
        f.write(f"- Total Relationships (Edges): {len(G.edges)}\n\n")

        f.write("## Local Clustering Coefficients (Top 10 Fields)\n")
        f.write("| Rank | Field | Clustering Coefficient |\n")
        f.write("|------|--------|-------------------------|\n")
        for i, (node, coeff) in enumerate(
            sorted(local_clustering.items(), key=lambda x: x[1], reverse=True)[:10], 1
        ):
            f.write(f"| {i} | {node} | {coeff:.3f} |\n")
        f.write("\n")

        interpretation = interpret_clustering(local_clustering, avg_clustering, transitivity)
        f.write(interpretation)
        f.write("\n")

    print(f"✅ Clustering coefficient report saved to: {output_file}")


def main():
    url = (
        "https://raw.githubusercontent.com/SingularityNET-Archive/"
        "SingularityNET-Archive/refs/heads/main/Data/Snet-Ambassador-Program/"
        "Meeting-Summaries/2025/meeting-summaries-array.json"
    )
    output_dir = "reports"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "clustering_analysis_report.md")

    print("📡 Fetching JSON data...")
    data = load_json_remote(url)
    print("✅ JSON data successfully loaded.")

    print("🔍 Building co-occurrence graph...")
    G = build_field_graph(data)
    print(f"📊 Graph contains {len(G.nodes)} fields and {len(G.edges)} edges.")

    print("📈 Computing clustering coefficients...")
    local_clustering, avg_clustering, transitivity = clustering_analysis(G)

    write_markdown_report(G, local_clustering, avg_clustering, transitivity, output_file)


if __name__ == "__main__":
    main()
