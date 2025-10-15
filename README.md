# Graph-Python-scripts

Scripts to fetch meeting summaries, generate graphs, and produce analysis reports.

## Quickstart
1. Create a virtual environment and install dependencies:
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

2. Run common tasks:
- Single-meeting graph → saves `graph.png`:
```bash
python Scripts/Nodes-Edges.py
```
- Multi-meeting graph → saves `graph2.png`:
```bash
python Scripts/Nodes-Edges2.py
```
- Export Gephi file → writes `Scripts/all_workgroups_graph_sanitized.gexf`:
```bash
python Scripts/GEXF-export.py
```
- Workgroup summary → writes `Scripts/workgroup_meetings_summary.txt`:
```bash
python Scripts/Import-JSON.py
```
- Degree (co-attendance) analysis → writes `Graph Analysis/Degree_Analysis/degree_analysis_report.md`:
```bash
python "Graph Analysis/Degree_Analysis/degree_analysis_to_md.py"
```
- JSON path structure report → writes `reports/path_analysis_report.md`:
```bash
python "Graph Analysis/Path_Analysis/path_analysis_report.py"
```
- Field centrality report → writes `reports/centrality_analysis_report.md`:
```bash
python "Graph Analysis/Path_Analysis/Centrality_Analysis/json_centrality_analysis.py"
```

## Repository Map
- `Scripts/` — data fetching and basic graph generation. See `Scripts/README.md`.
- `Graph Analysis/` — analysis utilities (degree, path, centrality). See `Graph Analysis/README.md`.
- `reports/` — generated Markdown reports. See `reports/README.md`.

## Data Source
All scripts read from a shared public JSON:
`https://raw.githubusercontent.com/SingularityNET-Archive/SingularityNET-Archive/refs/heads/main/Data/Snet-Ambassador-Program/Meeting-Summaries/2025/meeting-summaries-array.json`

## Outputs
- `graph.png`, `graph2.png` — rendered graphs
- `Scripts/all_workgroups_graph_sanitized.gexf` — Gephi import
- Markdown reports in `reports/`

Notes: Scripts run headlessly and save files to disk; images can be opened via your OS default viewer.
