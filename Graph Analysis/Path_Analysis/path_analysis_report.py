import json
import requests
import networkx as nx
from collections import Counter
from datetime import datetime
import os


def load_json_remote(url):
    """Load JSON data from a remote URL."""
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def extract_json_paths(obj, prefix=""):
    """
    Recursively extract all JSON paths in dot notation.
    Example: {"a": {"b": 1}} -> ["a", "a.b"]
    """
    paths = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            path = f"{prefix}.{k}" if prefix else k
            paths.append(path)
            paths.extend(extract_json_paths(v, path))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            path = f"{prefix}[{i}]"
            paths.append(path)
            paths.extend(extract_json_paths(item, path))
    return paths


def build_path_graph(paths):
    """Build a directed graph from JSON paths (parent → child relationships)."""
    G = nx.DiGraph()
    for path in paths:
        if "." in path:
            parent = path.rsplit(".", 1)[0]
            G.add_edge(parent, path)
        elif "[" in path:
            parent = path.rsplit("[", 1)[0]
            G.add_edge(parent, path)
        else:
            G.add_node(path)
    return G


def path_analysis(paths):
    """Compute path metrics and structural statistics."""
    depths = [p.count(".") + p.count("[") for p in paths]
    max_depth = max(depths) if depths else 0
    avg_depth = sum(depths) / len(depths) if depths else 0

    # Find deepest paths
    deepest_paths = [p for p, d in zip(paths, depths) if d == max_depth]

    # Count parent prefixes
    parent_counts = Counter([p.rsplit(".", 1)[0] if "." in p else p for p in paths])

    return {
        "total_paths": len(paths),
        "max_depth": max_depth,
        "avg_depth": avg_depth,
        "deepest_paths": deepest_paths[:10],
        "parent_counts": parent_counts.most_common(10),
    }


def write_markdown_report(analysis, output_file):
    """Generate Markdown report summarizing JSON path analysis."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# JSON Path Analysis Report\n")
        f.write(f"**Generated on:** {timestamp}\n\n")

        f.write("## Summary Statistics\n")
        f.write(f"- Total Unique Paths: {analysis['total_paths']}\n")
        f.write(f"- Maximum Depth: {analysis['max_depth']}\n")
        f.write(f"- Average Depth: {analysis['avg_depth']:.2f}\n\n")

        f.write("## Deepest JSON Paths\n")
        for p in analysis["deepest_paths"]:
            f.write(f"- `{p}`\n")
        f.write("\n")

        f.write("## Most Common Parent Paths\n")
        f.write("| Rank | Parent Path | Count |\n|------|--------------|--------|\n")
        for i, (parent, count) in enumerate(analysis["parent_counts"], 1):
            f.write(f"| {i} | `{parent}` | {count} |\n")
        f.write("\n")

        f.write("## Interpretation\n")
        f.write(
            "This report analyzes the structural complexity of the JSON file. "
            "Each path represents a unique traversal route through nested keys and arrays. "
            "The **maximum depth** indicates how deeply nested certain fields are, "
            "while the **most common parent paths** reveal recurring structural patterns.\n"
        )

    print(f"✅ Path analysis report saved to: {output_file}")


def main():
    url = (
        "https://raw.githubusercontent.com/SingularityNET-Archive/"
        "SingularityNET-Archive/refs/heads/main/Data/Snet-Ambassador-Program/"
        "Meeting-Summaries/2025/meeting-summaries-array.json"
    )
    output_dir = "reports"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "path_analysis_report.md")

    print("📡 Fetching JSON data from remote source...")
    data = load_json_remote(url)
    print("✅ JSON file downloaded.")

    print("🔍 Extracting all JSON paths...")
    all_paths = extract_json_paths(data)
    print(f"📊 Extracted {len(all_paths)} unique paths.")

    print("🔧 Performing path analysis...")
    analysis = path_analysis(all_paths)

    print("🧩 Building path graph...")
    G = build_path_graph(all_paths)
    print(f"✅ Graph built with {len(G.nodes)} nodes and {len(G.edges)} edges.")

    write_markdown_report(analysis, output_file)


if __name__ == "__main__":
    main()
