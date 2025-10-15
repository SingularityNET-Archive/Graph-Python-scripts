import argparse
import json
import os
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
        for k, v in summary.items():
            f.write(f"- {k}: {v}\n")
        f.write("\n")

        # Participant-only Degree (Co-attendance)
        f.write("## Degree (Co-attendance) Analysis\n")
        f.write("### Top Nodes by Degree\n")
        f.write("| Rank | Node | Degree |\n|------|------|--------|\n")
        for i, (node, deg) in enumerate(attend_top, 1):
            label = _truncate_label(node, 80)
            f.write(f"| {i} | {label} | {deg} |\n")
        f.write("\n")
        f.write("### Degree Distribution\n")
        f.write("| Degree | Count of Nodes |\n|--------|-----------------|\n")
        for d, c in attend_dist:
            f.write(f"| {d} | {c} |\n")
        f.write("\n")

        # JSON Field Degree Analysis
        f.write("## JSON Field Degree Analysis\n")
        f.write("### Top Fields by Degree\n")
        f.write("| Rank | Field | Degree |\n|------|-------|--------|\n")
        for i, (node, deg) in enumerate(field_top, 1):
            label = _truncate_label(node, 80)
            f.write(f"| {i} | {label} | {deg} |\n")
        f.write("\n")
        f.write("### Degree Distribution\n")
        f.write("| Degree | Count of Fields |\n|--------|------------------|\n")
        for d, c in field_dist:
            f.write(f"| {d} | {c} |\n")
        f.write("\n")

        # Path Analysis
        f.write("## JSON Path Structure Analysis\n")
        f.write(f"- Total Unique Paths: {path_info['total_paths']}\n")
        f.write(f"- Maximum Depth: {path_info['max_depth']}\n")
        f.write(f"- Average Depth: {path_info['avg_depth']:.2f}\n\n")
        f.write("### Deepest JSON Paths (sample)\n")
        for p in path_info["deepest_paths"][:10]:
            f.write(f"- `{p}`\n")
        f.write("\n")
        f.write("### Most Common Parent Paths\n")
        f.write("| Rank | Parent Path | Count |\n|------|-------------|-------|\n")
        for i, (parent, cnt) in enumerate(parent_top, 1):
            f.write(f"| {i} | `{parent}` | {cnt} |\n")
        f.write("\n")

        # Centrality
        f.write("## Field Centrality (Co-occurrence)\n")
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
        f.write(f"- Average Clustering Coefficient: {avg_clust:.3f}\n\n")
        f.write("### Top Nodes by Clustering Coefficient\n")
        f.write("| Rank | Field | Clustering |\n|------|-------|------------|\n")
        for i, (node, val) in enumerate(top_clust_nodes, 1):
            f.write(f"| {i} | {node} | {val:.3f} |\n")
        f.write("\n")

        # Connected Components
        f.write("## Connected Components (Field Co-occurrence Graph)\n")
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


def main() -> None:
    parser = argparse.ArgumentParser(description="Unified Graph Analysis")
    parser.add_argument(
        "--input",
        default=DEFAULT_INPUT,
        help="Local JSON file path or HTTP(S) URL",
    )
    parser.add_argument(
        "--output",
        default="reports/unified_analysis_report.md",
        help="Markdown report output path",
    )
    parser.add_argument(
        "--limit-top",
        type=int,
        default=10,
        help="Top-N rows to include in tables",
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


if __name__ == "__main__":
    main()
