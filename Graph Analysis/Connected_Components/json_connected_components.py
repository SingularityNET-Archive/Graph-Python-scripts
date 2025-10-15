import json
import requests
import networkx as nx
from itertools import combinations
from datetime import datetime
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


def connected_components_analysis(G):
    """Find all connected components (clusters) in the graph."""
    components = list(nx.connected_components(G))
    component_sizes = [len(c) for c in components]
    num_components = len(components)
    largest_component = max(component_sizes) if component_sizes else 0
    avg_size = sum(component_sizes) / len(component_sizes) if component_sizes else 0
    return components, num_components, largest_component, avg_size


def interpret_connected_components(num_components, largest_component, avg_size):
    """Interpretation narrative for connected components analysis."""
    interpretation = [
        "## Interpretation of Connected Components\n",
        "Connected components represent clusters of fields that are directly or indirectly linked — "
        "that is, they frequently co-occur in the same sections of the JSON structure.\n\n",
        f"- **Number of Components:** {num_components}\n"
        f"- **Largest Component Size:** {largest_component}\n"
        f"- **Average Component Size:** {avg_size:.2f}\n\n",
        "_Interpretation:_\n",
        "- A **small number of large components** suggests that many fields are interrelated, "
        "indicating a cohesive JSON schema.\n",
        "- A **large number of small components** implies that some parts of the data are isolated "
        "or used in specialized contexts.\n",
        "- The **largest component** can be viewed as the 'core schema' — the main structure tying most "
        "fields together.\n",
    ]
    return "\n".join(interpretation)


def write_markdown_report(G, components, num_components, largest_component, avg_size, output_file):
    """Write connected component results and interpretation to a Markdown file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# JSON Connected Components Report\n")
        f.write(f"**Generated on:** {timestamp}\n\n")
        f.write(f"- Total Fields (Nodes): {len(G.nodes)}\n")
        f.write(f"- Total Relationships (Edges): {len(G.edges)}\n\n")

        f.write("## Connected Components Summary\n")
        f.write(f"- Number of Components: {num_components}\n")
        f.write(f"- Largest Component Size: {largest_component}\n")
        f.write(f"- Average Component Size: {avg_size:.2f}\n\n")

        f.write("## Top 5 Largest Components\n")
        for i, comp in enumerate(sorted(components, key=len, reverse=True)[:5], 1):
            f.write(f"### Component {i} ({len(comp)} fields)\n")
            f.write(", ".join(sorted(comp)) + "\n\n")

        interpretation = interpret_connected_components(num_components, largest_component, avg_size)
        f.write(interpretation)

    print(f"✅ Connected Components report saved to: {output_file}")


def main():
    url = (
        "https://raw.githubusercontent.com/SingularityNET-Archive/"
        "SingularityNET-Archive/refs/heads/main/Data/Snet-Ambassador-Program/"
        "Meeting-Summaries/2025/meeting-summaries-array.json"
    )
    output_dir = "reports"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "connected_components_report.md")

    print("📡 Fetching JSON data...")
    data = load_json_remote(url)
    print("✅ JSON data successfully loaded.")

    print("🔍 Building field co-occurrence graph...")
    G = build_field_graph(data)
    print(f"📊 Graph contains {len(G.nodes)} fields and {len(G.edges)} edges.")

    print("🔗 Identifying connected components...")
    components, num_components, largest_component, avg_size = connected_components_analysis(G)
    print(f"✅ Found {num_components} connected components.")

    write_markdown_report(G, components, num_components, largest_component, avg_size, output_file)


if __name__ == "__main__":
    main()
