import json
import requests
import networkx as nx
from itertools import combinations
from datetime import datetime


def load_json_remote(url):
    """Load JSON data from a remote URL."""
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def find_field_combinations(obj):
    """Recursively extract co-occurring field names (keys)."""
    cooccurrences = []

    if isinstance(obj, dict):
        keys = set(obj.keys())
        if len(keys) > 1:
            cooccurrences.append(keys)
        for value in obj.values():
            cooccurrences.extend(find_field_combinations(value))

    elif isinstance(obj, list):
        for item in obj:
            cooccurrences.extend(find_field_combinations(item))

    return cooccurrences


def build_field_graph(data):
    """Build a graph where nodes = field names and edges = co-occurrence in the same object."""
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


def degree_analysis(G):
    """Compute degree of each field in the graph."""
    return dict(G.degree())


def write_markdown_report(degree_dict, output_file):
    """Write the degree results to a Markdown report."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# JSON Field Degree Report\n")
        f.write(f"**Generated on:** {timestamp}\n\n")

        f.write(f"## Summary\n")
        f.write(f"- Total unique fields: {len(degree_dict)}\n")
        f.write(f"- Maximum degree: {max(degree_dict.values()) if degree_dict else 0}\n")
        f.write(f"- Minimum degree: {min(degree_dict.values()) if degree_dict else 0}\n\n")

        f.write("## Field Degrees (sorted by degree)\n")
        f.write("| Rank | Field Name | Degree |\n")
        f.write("|------|-------------|---------|\n")

        for i, (field, deg) in enumerate(sorted(degree_dict.items(), key=lambda x: x[1], reverse=True), start=1):
            f.write(f"| {i} | {field} | {deg} |\n")

    print(f"✅ Markdown report saved to: {output_file}")


def main():
    url = (
        "https://raw.githubusercontent.com/SingularityNET-Archive/"
        "SingularityNET-Archive/refs/heads/main/Data/Snet-Ambassador-Program/"
        "Meeting-Summaries/2025/meeting-summaries-array.json"
    )
    output_file = "json_field_degree_report.md"

    print("📡 Fetching JSON from remote source...")
    data = load_json_remote(url)
    print("✅ JSON file downloaded.")

    print("🔍 Building field co-occurrence graph...")
    G = build_field_graph(data)
    print(f"📊 Built graph with {len(G.nodes)} fields and {len(G.edges)} relationships.\n")

    degree_dict = degree_analysis(G)
    write_markdown_report(degree_dict, output_file)


if __name__ == "__main__":
    main()





