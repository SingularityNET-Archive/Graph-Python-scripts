import argparse
import json
import os
import urllib.parse
from datetime import datetime
from itertools import combinations
from typing import Any, Dict, Iterable, List, Tuple

import networkx as nx
import requests
from collections import Counter


DEFAULT_INPUT = (
    "https://raw.githubusercontent.com/SingularityNET-Archive/"
    "SingularityNET-Archive/refs/heads/main/Data/Snet-Ambassador-Program/"
    "Meeting-Summaries/2025/meeting-summaries-array.json"
)


def is_url(source: str) -> bool:
    return source.startswith("http://") or source.startswith("https://")


def load_json(source: str) -> Any:
    if is_url(source):
        resp = requests.get(source)
        resp.raise_for_status()
        return resp.json()
    with open(source, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------- Utility ----------------

def _truncate_label(text: str, max_len: int = 80) -> str:
    if text is None:
        return ""
    safe = str(text).replace("\n", " ").strip()
    return safe if len(safe) <= max_len else (safe[: max_len - 1] + "…")


# ---------------- Participant-only Degree (Co-attendance) ----------------

def extract_participants(record: Dict[str, Any]) -> List[str]:
    """Extract likely participants from a meeting record.
    - peoplePresent: comma-separated string under meetingInfo
    - host, documenter: added if present (deduped)
    """
    participants: List[str] = []
    meeting_info = {}
    if isinstance(record, dict):
        meeting_info = record.get("meetingInfo", {}) or {}
    # peoplePresent as comma-separated string
    pp = meeting_info.get("peoplePresent", "")
    if isinstance(pp, str) and pp.strip():
        participants.extend([p.strip() for p in pp.split(",") if p.strip()])
    # host/documenter as single names
    for key in ("host", "documenter"):
        val = meeting_info.get(key)
        if isinstance(val, str) and val.strip():
            participants.append(val.strip())
    # dedupe while preserving order
    seen = set()
    deduped: List[str] = []
    for p in participants:
        if p not in seen:
            seen.add(p)
            deduped.append(p)
    return deduped


def build_coattendance_graph(records: Iterable[Any]) -> nx.Graph:
    G = nx.Graph()
    for rec in records:
        participants = extract_participants(rec)
        if len(participants) < 2:
            continue
        for p in participants:
            G.add_node(p)
        for u, v in combinations(participants, 2):
            if G.has_edge(u, v):
                G[u][v]["weight"] += 1
            else:
                G.add_edge(u, v, weight=1)
    return G


def degree_analysis(G: nx.Graph) -> Tuple[Dict[str, int], Counter]:
    degree_dict = dict(G.degree())
    degree_counts = Counter(degree_dict.values())
    return degree_dict, degree_counts


# ---------------- JSON Path Structure ----------------

def extract_json_paths(obj: Any, prefix: str = "") -> List[str]:
    paths: List[str] = []
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


def path_metrics(paths: List[str]) -> Dict[str, Any]:
    depths = [p.count(".") + p.count("[") for p in paths]
    max_depth = max(depths) if depths else 0
    avg_depth = (sum(depths) / len(depths)) if depths else 0.0
    deepest_paths = [p for p, d in zip(paths, depths) if d == max_depth]
    parent_counts = Counter([p.rsplit(".", 1)[0] if "." in p else p for p in paths])
    return {
        "total_paths": len(paths),
        "max_depth": max_depth,
        "avg_depth": avg_depth,
        "deepest_paths": deepest_paths,
        "parent_counts": parent_counts,
    }


def build_path_graph(paths: List[str]) -> nx.DiGraph:
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


# ---------------- Field Co-occurrence (Degree, Centrality, Clustering, Components) ----------------

def find_field_combinations(obj: Any) -> List[set]:
    results: List[set] = []
    if isinstance(obj, dict):
        keys = set(obj.keys())
        if len(keys) > 1:
            results.append(keys)
        for v in obj.values():
            results.extend(find_field_combinations(v))
    elif isinstance(obj, list):
        for item in obj:
            results.extend(find_field_combinations(item))
    return results


def build_field_graph(data: Any) -> nx.Graph:
    G = nx.Graph()
    sets = find_field_combinations(data)
    for s in sets:
        for k in s:
            G.add_node(k)
        for u, v in combinations(s, 2):
            if G.has_edge(u, v):
                G[u][v]["weight"] += 1
            else:
                G.add_edge(u, v, weight=1)
    return G


def field_degree(G: nx.Graph) -> Tuple[Dict[str, int], Counter]:
    degree_dict = dict(G.degree())
    degree_counts = Counter(degree_dict.values())
    return degree_dict, degree_counts


def compute_centrality_measures(G: nx.Graph) -> Dict[str, Dict[str, float]]:
    degree = nx.degree_centrality(G) if G.number_of_nodes() else {}
    betweenness = nx.betweenness_centrality(G) if G.number_of_nodes() else {}
    closeness = nx.closeness_centrality(G) if G.number_of_nodes() else {}
    try:
        eigenvector = nx.eigenvector_centrality(G, max_iter=1000) if G.number_of_nodes() else {}
    except nx.PowerIterationFailedConvergence:
        eigenvector = {n: 0.0 for n in G.nodes()}
    return {
        "degree": degree,
        "betweenness": betweenness,
        "closeness": closeness,
        "eigenvector": eigenvector,
    }


def clustering_metrics(G: nx.Graph, top: int) -> Tuple[float, List[Tuple[str, float]]]:
    if G.number_of_nodes() == 0:
        return 0.0, []
    avg = nx.average_clustering(G)
    per_node = nx.clustering(G)
    top_nodes = sorted(per_node.items(), key=lambda x: x[1], reverse=True)[:top]
    return avg, top_nodes


def connected_components_info(G: nx.Graph, top: int) -> Dict[str, Any]:
    if G.number_of_nodes() == 0:
        return {"component_count": 0, "component_sizes": [], "largest_component_sample": []}
    components = sorted(nx.connected_components(G), key=len, reverse=True)
    sizes = [len(c) for c in components]
    largest = list(components[0]) if components else []
    sample = largest[:top]
    return {"component_count": len(components), "component_sizes": sizes, "largest_component_sample": sample}


# ---------------- Report Writer ----------------

def write_report(
    output_file: str,
    summary: Dict[str, Any],
    attend_deg: Tuple[Dict[str, int], Counter],
    attend_top: List[Tuple[str, int]],
    attend_dist: List[Tuple[int, int]],
    field_deg: Tuple[Dict[str, int], Counter],
    field_top: List[Tuple[str, int]],
    field_dist: List[Tuple[int, int]],
    path_info: Dict[str, Any],
    parent_top: List[Tuple[str, int]],
    centrality: Dict[str, Dict[str, float]],
    clustering: Tuple[float, List[Tuple[str, float]]],
    components: Dict[str, Any],
) -> None:
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Unified Graph Analysis Report\n")
        f.write(f"**Generated on:** {timestamp}\n\n")

        # Summary
        f.write("## Summary\n")
        f.write("These are high-level counts of nodes/edges for each graph constructed during analysis.\n\n")
        for k, v in summary.items():
            f.write(f"- {k}: {v}\n")
        f.write("\n")

        # Participant-only Degree (Co-attendance)
        f.write("## Degree (Co-attendance) Analysis\n")
        f.write("People are connected if they attend the same meeting; a person's degree is how many unique people they co-attended with.\n\n")
        f.write("### Top Nodes by Degree\n")
        f.write("These are the people connected to the most unique others across meetings.\n\n")
        f.write("| Rank | Node | Degree |\n|------|------|--------|\n")
        for i, (node, deg) in enumerate(attend_top, 1):
            label = _truncate_label(node, 80)
            f.write(f"| {i} | {label} | {deg} |\n")
        f.write("\n")
        f.write("### Degree Distribution\n")
        f.write("How many people fall into each degree (number of unique co-attendees) bucket.\n\n")
        f.write("| Degree | Count of Nodes |\n|--------|-----------------|\n")
        for d, c in attend_dist:
            f.write(f"| {d} | {c} |\n")
        f.write("\n")

        # JSON Field Degree Analysis
        f.write("## JSON Field Degree Analysis\n")
        f.write("Fields are connected when they appear together inside the same JSON object; a field's degree is the number of distinct fields it co-occurs with.\n\n")
        f.write("### Top Fields by Degree\n")
        f.write("These fields co-occur with the largest variety of other fields.\n\n")
        f.write("| Rank | Field | Degree |\n|------|-------|--------|\n")
        for i, (node, deg) in enumerate(field_top, 1):
            label = _truncate_label(node, 80)
            f.write(f"| {i} | {label} | {deg} |\n")
        f.write("\n")
        f.write("### Degree Distribution\n")
        f.write("How many fields have each degree (number of distinct co-occurring fields).\n\n")
        f.write("| Degree | Count of Fields |\n|--------|------------------|\n")
        for d, c in field_dist:
            f.write(f"| {d} | {c} |\n")
        f.write("\n")

        # Path Analysis
        f.write("## JSON Path Structure Analysis\n")
        f.write("Each JSON path represents a unique nested route (keys/array indices); depth shows how deeply information is nested.\n\n")
        f.write(f"- Total Unique Paths: {path_info['total_paths']}\n")
        f.write(f"- Maximum Depth: {path_info['max_depth']}\n")
        f.write(f"- Average Depth: {path_info['avg_depth']:.2f}\n\n")
        f.write("### Deepest JSON Paths (sample)\n")
        f.write("The deepest examples indicate where the data structure is most nested.\n\n")
        for p in path_info["deepest_paths"][:10]:
            f.write(f"- `{p}`\n")
        f.write("\n")
        f.write("### Most Common Parent Paths\n")
        f.write("Parents that appear most often, suggesting common structural hubs.\n\n")
        f.write("| Rank | Parent Path | Count |\n|------|-------------|-------|\n")
        for i, (parent, cnt) in enumerate(parent_top, 1):
            f.write(f"| {i} | `{parent}` | {cnt} |\n")
        f.write("\n")

        # Centrality
        f.write("## Field Centrality (Co-occurrence)\n")
        f.write("Centrality scores highlight fields that are well-connected (degree), act as bridges (betweenness), are close to others (closeness), or connect to other influential fields (eigenvector).\n\n")
        metrics = centrality
        top_fields = sorted(metrics["degree"].keys(), key=lambda x: metrics["degree"][x], reverse=True)[:10]
        f.write("| Rank | Field | Degree | Betweenness | Closeness | Eigenvector |\n")
        f.write("|------|-------|--------|-------------|-----------|------------|\n")
        for i, node in enumerate(top_fields, 1):
            f.write(
                f"| {i} | {node} | "
                f"{metrics['degree'].get(node, 0):.3f} | "
                f"{metrics['betweenness'].get(node, 0):.3f} | "
                f"{metrics['closeness'].get(node, 0):.3f} | "
                f"{metrics['eigenvector'].get(node, 0):.3f} |\n"
            )
        f.write("\n")

        # Clustering
        avg_clust, top_clust_nodes = clustering
        f.write("## Clustering (Field Co-occurrence Graph)\n")
        f.write("Clustering measures how tightly a field's neighbors are connected to each other (higher means more triads).\n\n")
        f.write(f"- Average Clustering Coefficient: {avg_clust:.3f}\n\n")
        f.write("### Top Nodes by Clustering Coefficient\n")
        f.write("Fields whose immediate neighborhoods are most tightly interlinked.\n\n")
        f.write("| Rank | Field | Clustering |\n|------|-------|------------|\n")
        for i, (node, val) in enumerate(top_clust_nodes, 1):
            f.write(f"| {i} | {node} | {val:.3f} |\n")
        f.write("\n")

        # Connected Components
        f.write("## Connected Components (Field Co-occurrence Graph)\n")
        f.write("Components are groups of fields that are all reachable from each other; multiple components suggest separate substructures.\n\n")
        f.write(f"- Number of Components: {components['component_count']}\n")
        f.write(f"- Component Sizes (top 10): {components['component_sizes'][:10]}\n")
        f.write("- Sample of Largest Component Nodes (top 10):\n")
        for n in components["largest_component_sample"][:10]:
            f.write(f"  - {n}\n")
        f.write("\n")


def ensure_iterable_records(data: Any) -> List[Any]:
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        return [data]
    return []


# ---------------- HTML Report Writer ----------------

def _review_button(method_name: str) -> str:
    """Generate HTML for a review button linking to GitHub Issues."""
    # GitHub Issue Forms: link to issues/new page
    # If template parameter works, it will load automatically
    # Otherwise, users will see template chooser and can select "Analysis Review"
    # Include method info in body as pre-fill for reference
    body_text = f"**Method:** {method_name}\n\n**File:** docs/index.html\n\n---\n\n"
    # URL encode the body text properly
    encoded_body = urllib.parse.quote(body_text)
    
    # Use template parameter (GitHub's documented format for Issue Forms)
    # Template name without .yml extension
    url = f"https://github.com/SingularityNET-Archive/Graph-Python-scripts/issues/new?template=analysis_review&body={encoded_body}"
    
    return f'<a href="{url}" class="review-button" target="_blank" title="Opens GitHub Issue template. If template doesn\'t load automatically, select \'Analysis Review\' from the template chooser.">Review This Analysis</a>'


def write_html_report(
    output_file: str,
    timestamp: str,
    summary: Dict[str, Any],
    attend_deg: Tuple[Dict[str, int], Counter],
    attend_top: List[Tuple[str, int]],
    attend_dist: List[Tuple[int, int]],
    attend_graph: nx.Graph,
    field_deg: Tuple[Dict[str, int], Counter],
    field_top: List[Tuple[str, int]],
    field_dist: List[Tuple[int, int]],
    path_info: Dict[str, Any],
    parent_top: List[Tuple[str, int]],
    centrality: Dict[str, Dict[str, float]],
    clustering: Tuple[float, List[Tuple[str, float]]],
    components: Dict[str, Any],
) -> None:
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Unified Graph Analysis Report</title>
    <link rel="stylesheet" href="style.css">
    <script type="text/javascript" src="https://unpkg.com/vis-network@latest/dist/vis-network.min.js"></script>
    <style type="text/css">
        #coattendance-network {
            width: 100%;
            height: 600px;
            border: 1px solid #e1e4e8;
            border-radius: 6px;
            background-color: #ffffff;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Unified Graph Analysis Report</h1>
            <p class="timestamp">Generated on: <strong>""" + timestamp + """</strong></p>
        </header>

        <div class="tabs">
            <button class="tab-button active" onclick="showTab('summary')">Summary</button>
            <button class="tab-button" onclick="showTab('coattendance')">Co-attendance Degree</button>
            <button class="tab-button" onclick="showTab('field-degree')">Field Degree</button>
            <button class="tab-button" onclick="showTab('path-structure')">Path Structure</button>
            <button class="tab-button" onclick="showTab('centrality')">Centrality</button>
            <button class="tab-button" onclick="showTab('clustering')">Clustering</button>
            <button class="tab-button" onclick="showTab('components')">Components</button>
            <button class="tab-button" onclick="showTab('audit')">Audit</button>
        </div>

        <div class="tab-content">
            <!-- Summary Tab -->
            <div id="summary" class="tab-pane active">
                <h2>Summary</h2>
                <p class="explanation">These are high-level counts of nodes/edges for each graph constructed during analysis.</p>
                <ul class="summary-list">
""")
        for k, v in summary.items():
            f.write(f"                    <li><strong>{k}:</strong> {v}</li>\n")
        f.write("""                </ul>
            </div>

            <!-- Co-attendance Degree Tab -->
            <div id="coattendance" class="tab-pane">
                <h2>Degree (Co-attendance) Analysis</h2>
                """ + _review_button("coattendance") + """
                <p class="explanation">People are connected if they attend the same meeting; a person's degree is how many unique people they co-attended with.</p>
                
                <h3>Interactive Network Visualization</h3>
                <p class="explanation">
                    Visual representation of the co-attendance graph. <strong>Nodes represent people</strong>, with size and color indicating degree (number of connections) - larger, darker nodes have more connections. <strong>Edges represent co-attendance</strong> - thicker, darker edges indicate more frequent co-attendance. 
                    <br><br>
                    <strong>Interactions:</strong> Use mouse wheel to zoom, click and drag to pan, drag nodes to reposition. Hover over nodes or edges to see detailed information. Click on a node to highlight its connections.
                </p>
                <div id="coattendance-network"></div>
                
                <h3>Top Nodes by Degree</h3>
                <p class="explanation">These are the people connected to the most unique others across meetings.</p>
                <table>
                    <thead>
                        <tr><th>Rank</th><th>Node</th><th>Degree</th></tr>
                    </thead>
                    <tbody>
""")
        for i, (node, deg) in enumerate(attend_top, 1):
            label = _truncate_label(node, 80)
            f.write(f"                        <tr><td>{i}</td><td>{label}</td><td>{deg}</td></tr>\n")
        f.write("""                    </tbody>
                </table>

                <h3>Degree Distribution</h3>
                <p class="explanation">How many people fall into each degree (number of unique co-attendees) bucket.</p>
                <table>
                    <thead>
                        <tr><th>Degree</th><th>Count of Nodes</th></tr>
                    </thead>
                    <tbody>
""")
        for d, c in attend_dist:
            f.write(f"                        <tr><td>{d}</td><td>{c}</td></tr>\n")
        f.write("""                    </tbody>
                </table>
            </div>

            <!-- Field Degree Tab -->
            <div id="field-degree" class="tab-pane">
                <h2>JSON Field Degree Analysis</h2>
                """ + _review_button("field-degree") + """
                <p class="explanation">Fields are connected when they appear together inside the same JSON object; a field's degree is the number of distinct fields it co-occurs with.</p>
                
                <h3>Top Fields by Degree</h3>
                <p class="explanation">These fields co-occur with the largest variety of other fields.</p>
                <table>
                    <thead>
                        <tr><th>Rank</th><th>Field</th><th>Degree</th></tr>
                    </thead>
                    <tbody>
""")
        for i, (node, deg) in enumerate(field_top, 1):
            label = _truncate_label(node, 80)
            f.write(f"                        <tr><td>{i}</td><td>{label}</td><td>{deg}</td></tr>\n")
        f.write("""                    </tbody>
                </table>

                <h3>Degree Distribution</h3>
                <p class="explanation">How many fields have each degree (number of distinct co-occurring fields).</p>
                <table>
                    <thead>
                        <tr><th>Degree</th><th>Count of Fields</th></tr>
                    </thead>
                    <tbody>
""")
        for d, c in field_dist:
            f.write(f"                        <tr><td>{d}</td><td>{c}</td></tr>\n")
        f.write("""                    </tbody>
                </table>
            </div>

            <!-- Path Structure Tab -->
            <div id="path-structure" class="tab-pane">
                <h2>JSON Path Structure Analysis</h2>
                """ + _review_button("path-structure") + """
                <p class="explanation">Each JSON path represents a unique nested route (keys/array indices); depth shows how deeply information is nested.</p>
                
                <ul class="summary-list">
                    <li><strong>Total Unique Paths:</strong> """ + str(path_info['total_paths']) + """</li>
                    <li><strong>Maximum Depth:</strong> """ + str(path_info['max_depth']) + """</li>
                    <li><strong>Average Depth:</strong> """ + f"{path_info['avg_depth']:.2f}" + """</li>
                </ul>

                <h3>Deepest JSON Paths (sample)</h3>
                <p class="explanation">The deepest examples indicate where the data structure is most nested.</p>
                <ul class="path-list">
""")
        for p in path_info["deepest_paths"][:10]:
            f.write(f"                    <li><code>{p}</code></li>\n")
        f.write("""                </ul>

                <h3>Most Common Parent Paths</h3>
                <p class="explanation">Parents that appear most often, suggesting common structural hubs.</p>
                <table>
                    <thead>
                        <tr><th>Rank</th><th>Parent Path</th><th>Count</th></tr>
                    </thead>
                    <tbody>
""")
        for i, (parent, cnt) in enumerate(parent_top, 1):
            f.write(f"                        <tr><td>{i}</td><td><code>{parent}</code></td><td>{cnt}</td></tr>\n")
        f.write("""                    </tbody>
                </table>
            </div>

            <!-- Centrality Tab -->
            <div id="centrality" class="tab-pane">
                <h2>Field Centrality (Co-occurrence)</h2>
                """ + _review_button("centrality") + """
                <p class="explanation">Centrality scores highlight fields that are well-connected (degree), act as bridges (betweenness), are close to others (closeness), or connect to other influential fields (eigenvector).</p>
                
                <table>
                    <thead>
                        <tr><th>Rank</th><th>Field</th><th>Degree</th><th>Betweenness</th><th>Closeness</th><th>Eigenvector</th></tr>
                    </thead>
                    <tbody>
""")
        metrics = centrality
        top_fields = sorted(metrics["degree"].keys(), key=lambda x: metrics["degree"][x], reverse=True)[:10]
        for i, node in enumerate(top_fields, 1):
            f.write(
                f"                        <tr><td>{i}</td><td>{node}</td>"
                f"<td>{metrics['degree'].get(node, 0):.3f}</td>"
                f"<td>{metrics['betweenness'].get(node, 0):.3f}</td>"
                f"<td>{metrics['closeness'].get(node, 0):.3f}</td>"
                f"<td>{metrics['eigenvector'].get(node, 0):.3f}</td></tr>\n"
            )
        f.write("""                    </tbody>
                </table>
            </div>

            <!-- Clustering Tab -->
            <div id="clustering" class="tab-pane">
                <h2>Clustering (Field Co-occurrence Graph)</h2>
                """ + _review_button("clustering") + """
                <p class="explanation">Clustering measures how tightly a field's neighbors are connected to each other (higher means more triads).</p>
                
                <p><strong>Average Clustering Coefficient:</strong> """)
        avg_clust, top_clust_nodes = clustering
        f.write(f"{avg_clust:.3f}")
        f.write("""</p>

                <h3>Top Nodes by Clustering Coefficient</h3>
                <p class="explanation">Fields whose immediate neighborhoods are most tightly interlinked.</p>
                <table>
                    <thead>
                        <tr><th>Rank</th><th>Field</th><th>Clustering</th></tr>
                    </thead>
                    <tbody>
""")
        for i, (node, val) in enumerate(top_clust_nodes, 1):
            f.write(f"                        <tr><td>{i}</td><td>{node}</td><td>{val:.3f}</td></tr>\n")
        f.write("""                    </tbody>
                </table>
            </div>

            <!-- Connected Components Tab -->
            <div id="components" class="tab-pane">
                <h2>Connected Components (Field Co-occurrence Graph)</h2>
                """ + _review_button("components") + """
                <p class="explanation">Components are groups of fields that are all reachable from each other; multiple components suggest separate substructures.</p>
                
                <ul class="summary-list">
                    <li><strong>Number of Components:</strong> """ + str(components['component_count']) + """</li>
                    <li><strong>Component Sizes (top 10):</strong> """ + str(components['component_sizes'][:10]) + """</li>
                </ul>

                <h3>Sample of Largest Component Nodes (top 10)</h3>
                <ul class="component-list">
""")
        for n in components["largest_component_sample"][:10]:
            f.write(f"                    <li>{n}</li>\n")
        f.write("""                </ul>
            </div>

            <!-- Audit Tab -->
            <div id="audit" class="tab-pane">
                <h2>Review Audit</h2>
                <p class="explanation">Community review scores and feedback for each analysis method.</p>
                
                <div id="audit-loading" style="text-align: center; padding: 20px;">
                    <p>Loading audit data...</p>
                </div>
                
                <div id="audit-content" style="display: none;">
                    <p id="audit-last-updated" class="explanation" style="font-weight: bold; margin-bottom: 20px;"></p>
                    
                    <h3>Trust Scores by Method</h3>
                    <p class="explanation">Percentage of reviews rated as "Correct" for each analysis method.</p>
                    <table id="trust-scores-table">
                        <thead>
                            <tr><th>Method</th><th>Trust Score</th><th>Total Reviews</th><th>Correct</th><th>Incorrect</th><th>Needs Review</th></tr>
                        </thead>
                        <tbody id="trust-scores-body">
                        </tbody>
                    </table>
                    
                    <h3>Rating Distribution</h3>
                    <p class="explanation">Overall distribution of review ratings across all methods.</p>
                    <div id="rating-chart-container" style="margin: 20px 0; text-align: center;">
                        <canvas id="rating-chart" width="400" height="400"></canvas>
                    </div>
                    
                    <h3>Review Comments</h3>
                    <p class="explanation">All review comments submitted by the community.</p>
                    <table id="review-comments-table">
                        <thead>
                            <tr><th>Method</th><th>Rating</th><th>Comment</th><th>Author</th><th>Date</th><th>Issue</th></tr>
                        </thead>
                        <tbody id="review-comments-body">
                        </tbody>
                    </table>
                    
                    <p style="margin-top: 20px;">
                        <a href="audit/reviews.json" target="_blank" class="review-button">View Raw JSON Data</a>
                    </p>
                </div>
                
                <div id="audit-error" style="display: none; color: #d73a49; padding: 20px; background-color: #ffeef0; border-radius: 6px;">
                    <p><strong>Error loading audit data:</strong> <span id="audit-error-message"></span></p>
                    <p>This may be because no reviews have been submitted yet, or the data file doesn't exist.</p>
                </div>
            </div>
        </div>
    </div>

    <script type="text/javascript">
        // Convert co-attendance graph to vis-network format
        const coattendanceGraphData = {
            nodes: """ + json.dumps([
                {
                    "id": node,
                    "label": _truncate_label(node, 30),
                    "value": deg,
                    "title": f"{node} - Degree: {deg}"
                }
                for node, deg in attend_graph.degree()
            ], ensure_ascii=False) + """,
            edges: """ + json.dumps([
                {
                    "from": u,
                    "to": v,
                    "value": attend_graph[u][v].get("weight", 1),
                    "title": f"Co-attended {attend_graph[u][v].get('weight', 1)} time(s)"
                }
                for u, v in attend_graph.edges()
            ], ensure_ascii=False) + """
        };
    </script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <script src="script.js"></script>
</body>
</html>
""")


def main() -> None:
    parser = argparse.ArgumentParser(description="Unified Graph Analysis")
    parser.add_argument(
        "--input",
        default=DEFAULT_INPUT,
        help="Local JSON file path or HTTP(S) URL",
    )
    parser.add_argument(
        "--output",
        default="reports/unified_analysis_report_explained.md",
        help="Markdown report output path",
    )
    parser.add_argument(
        "--limit-top",
        type=int,
        default=10,
        help="Top-N rows to include in tables",
    )
    parser.add_argument(
        "--html",
        action="store_true",
        help="Generate HTML report in addition to Markdown",
    )
    parser.add_argument(
        "--html-output",
        default="docs/index.html",
        help="HTML report output path",
    )
    args = parser.parse_args()

    data = load_json(args.input)
    records = ensure_iterable_records(data)

    # Participant-only co-attendance
    G_attend = build_coattendance_graph(records)
    attend_deg_dict, attend_deg_counts = degree_analysis(G_attend)
    attend_top = sorted(attend_deg_dict.items(), key=lambda x: x[1], reverse=True)[: args.limit_top]
    attend_dist = sorted(attend_deg_counts.items(), key=lambda x: x[0])

    # Path analysis
    all_paths = extract_json_paths(data)
    pmetrics = path_metrics(all_paths)
    parent_top = pmetrics["parent_counts"].most_common(args.limit_top)
    G_paths = build_path_graph(all_paths)

    # Field co-occurrence graph
    G_fields = build_field_graph(data)

    # Field degree (JSON Field Degree Analysis)
    fdeg_dict, fdeg_counts = field_degree(G_fields)
    field_top = sorted(fdeg_dict.items(), key=lambda x: x[1], reverse=True)[: args.limit_top]
    field_dist = sorted(fdeg_counts.items(), key=lambda x: x[0])

    # Centrality on field graph
    centrality = compute_centrality_measures(G_fields)

    # Clustering & components on field graph
    avg_clust, top_clust_nodes = clustering_metrics(G_fields, args.limit_top)
    components = connected_components_info(G_fields, args.limit_top)

    summary = {
        "Co-attendance graph (nodes)": len(G_attend.nodes),
        "Co-attendance graph (edges)": len(G_attend.edges),
        "Path graph (nodes)": len(G_paths.nodes),
        "Path graph (edges)": len(G_paths.edges),
        "Field graph (nodes)": len(G_fields.nodes),
        "Field graph (edges)": len(G_fields.edges),
    }

    write_report(
        output_file=args.output,
        summary=summary,
        attend_deg=(attend_deg_dict, attend_deg_counts),
        attend_top=attend_top,
        attend_dist=attend_dist,
        field_deg=(fdeg_dict, fdeg_counts),
        field_top=field_top,
        field_dist=field_dist,
        path_info=pmetrics,
        parent_top=parent_top,
        centrality=centrality,
        clustering=(avg_clust, top_clust_nodes),
        components=components,
    )
    print(f"✅ Unified report written to: {args.output}")

    if args.html:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        write_html_report(
            output_file=args.html_output,
            timestamp=timestamp,
            summary=summary,
            attend_deg=(attend_deg_dict, attend_deg_counts),
            attend_top=attend_top,
            attend_dist=attend_dist,
            attend_graph=G_attend,
            field_deg=(fdeg_dict, fdeg_counts),
            field_top=field_top,
            field_dist=field_dist,
            path_info=pmetrics,
            parent_top=parent_top,
            centrality=centrality,
            clustering=(avg_clust, top_clust_nodes),
            components=components,
        )
        print(f"✅ HTML report written to: {args.html_output}")


if __name__ == "__main__":
    main()
