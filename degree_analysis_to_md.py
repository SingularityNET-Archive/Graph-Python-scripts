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

def find_participant_lists(obj):
    """
    Recursively find all lists of strings in a JSON-like object.
    Returns a list of lists (each list being a potential participant group).
    """
    results = []

    if isinstance(obj, dict):
        for value in obj.values():
            results.extend(find_participant_lists(value))
    elif isinstance(obj, list):
        # Check if this list looks like a participant list (all strings)
        if all(isinstance(x, str) for x in obj) and len(obj) > 1:
            results.append(obj)
        else:
            for item in obj:
                results.extend(find_participant_lists(item))

    return results

def build_coattendance_graph(meetings):
    """Build an undirected co-attendance graph from all detected participant lists."""
    G = nx.Graph()

    for meeting in meetings:
        participant_lists = find_participant_lists(meeting)
        # Merge all string lists found in this record
        participants = set()
        for lst in participant_lists:
            participants.update(lst)

        if len(participants) < 2:
            continue

        for p in participants:
            G.add_node(p)
        for u, v in combinations(participants, 2):
            if G.has_edge(u, v):
                G[u][v]['weight'] += 1
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
        f.write(f"# Degree Analysis Report\n")
        f.write(f"**Generated on:** {timestamp}\n\n")

        # Summary
        f.write("## Summary Statistics\n")
        f.write(f"- Total Nodes: {len(degree_dict)}\n")
        f.write(f"- Maximum Degree: {max(degree_dict.values()) if degree_dict else 0}\n")
        f.write(f"- Minimum Degree: {min(degree_dict.values()) if degree_dict else 0}\n\n")

        # Top 10 nodes
        f.write("## Top 10 Nodes by Degree\n")
        f.write("| Rank | Node | Degree |\n|------|-------|---------|\n")
        for i, (node, deg) in enumerate(sorted(degree_dict.items(), key=lambda x: x[1], reverse=True)[:10], 1):
            f.write(f"| {i} | {node} | {deg} |\n")
        f.write("\n")

        # Degree distribution
        f.write("## Degree Distribution\n")
        f.write("| Degree | Count of Nodes |\n|---------|----------------|\n")
        for degree, count in sorted(degree_counts.items()):
            f.write(f"| {degree} | {count} |\n")

    print(f"✅ Markdown report saved to: {output_file}")

def main():
    url = "https://raw.githubusercontent.com/SingularityNET-Archive/SingularityNET-Archive/refs/heads/main/Data/Snet-Ambassador-Program/Meeting-Summaries/2025/meeting-summaries-array.json"
    output_file = "degree_analysis_report.md"

    print("📡 Fetching data from remote source...")
    data = load_json_remote(url)
    print(f"✅ Downloaded {len(data)} meeting records.")

    print("🔍 Detecting participant lists recursively...")
    G = build_coattendance_graph(data)

    if len(G.nodes) == 0:
        print("⚠️ No participant lists found — please check JSON structure manually.")
        return

    print(f"📊 Built graph with {len(G.nodes)} nodes and {len(G.edges)} edges.")

    degree_dict, degree_counts = degree_analysis(G)
    write_markdown_report(degree_dict, degree_counts, output_file)

if __name__ == "__main__":
    main()

