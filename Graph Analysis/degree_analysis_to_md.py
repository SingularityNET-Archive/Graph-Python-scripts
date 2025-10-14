import json
import requests
import networkx as nx
from itertools import combinations
from collections import Counter
from datetime import datetime


def load_json_remote(url):
    """Load JSON data from a remote URL."""
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def find_field_combinations(obj):
    """
    Recursively extract all field (key) names and record their co-occurrence within objects.
    Returns a list of sets — each set contains field names that appear together.
    """
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


def build_field_graph(meetings):
    """Build a co-occurrence graph where nodes are JSON field names."""
    G = nx.Graph()

    cooccurrence_sets = find_field_combinations(meetings)

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
    """Compute degree metrics for the graph."""
    degree_dict = dict(G.degree())
    degree_counts = Counter(degree_dict.values())
    return degree_dict, degree_counts


def write_markdown_report(degree_dict, degree_counts, output_file):
    """Write results to a Markdown file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# JSON Field Degree Analysis Report\n")
        f.write(f"**Generated on:** {timestamp}\n\n")

        # Summary
        f.write("## Summary Statistics\n")
        f.write(f"- Total Unique Fields: {len(degree_dict)}\n")
        f.write(f"- Maximum Degree: {max(degree_dict.values()) if degree_dict else 0}\n")
        f.write(f"- Minimum Degree: {min(degree_dict.values()) if degree_dict else 0}\n\n")

        # Top 15 fields by degree
        f.write("## Top 15 JSON Fields by Degree\n")
        f.write("| Rank | Field Name | Degree |\n|------|-------------|---------|\n")
        for i, (field, deg) in enumerate(sorted(degree_dict.items(), key=lambda x: x[1], reverse=True)[:15], 1):
            f.write(f"| {i} | {field} | {deg} |\n")
        f.write("\n")

        # Degree distribution
        f.write("## Degree Distribution\n")
        f.write("| Degree | Count of Fields |\n|---------|-----------------|\n")
        for degree, count in sorted(degree_counts.items()):
            f.write(f"| {degree} | {count} |\n")

    print(f"✅ Markdown report saved to: {output_file}")


def main():
    url = (
        "https://raw.githubusercontent.com/SingularityNET-Archive/"
        "SingularityNET-Archive/refs/heads/main/Data/Snet-Ambassador-Program/"
        "Meeting-Summaries/2025/meeting-summaries-array.json"
    )
    output_file = "degree_analysis_by_field.md"

    print("📡 Fetching JSON from remote source...")
    data = load_json_remote(url)
    print("✅ JSON file downloaded.")

    print("🔍 Building field co-occurrence graph...")
    G = build_field_graph(data)

    if len(G.nodes) == 0:
        print("⚠️ No JSON field structure detected.")
        return

    print(f"📊 Built graph with {len(G.nodes)} fields and {len(G.edges)} relationships.")

    degree_dict, degree_counts = degree_analysis(G)
    write_markdown_report(degree_dict, degree_counts, output_file)


if __name__ == "__main__":
    main()


