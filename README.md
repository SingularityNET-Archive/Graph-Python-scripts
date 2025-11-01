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
- Unified analysis report (degree, path, centrality, clustering, components) → writes `reports/unified_analysis_report.md`:
```bash
python "Graph Analysis/unified_analysis.py" --output reports/unified_analysis_report.md
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
- HTML dashboard at `docs/index.html` (GitHub Pages)

Notes: Scripts run headlessly and save files to disk; images can be opened via your OS default viewer.

## Community Review System

This repository includes a community review system to validate graph analysis results. You can review analysis results and provide feedback through GitHub Issues.

### How to Review

1. Visit the [HTML dashboard](https://singularitynet-archive.github.io/Graph-Python-scripts/) (or open `docs/index.html` locally)
2. Navigate to any analysis tab (Co-attendance Degree, Field Degree, Path Structure, etc.)
3. Click the **"Review This Analysis"** button at the top of the section
4. Fill out the review form with:
   - Your rating (Correct / Needs Review / Incorrect)
   - Comments and feedback
   - Optional suggestions for improvements
5. Submit the issue - it will be automatically tagged with the `review` label

### View Review Results

- Click on the **"Audit"** tab in the dashboard to see:
  - Trust scores for each analysis method
  - Rating distribution charts
  - All review comments from the community

Reviews are collected nightly via GitHub Actions and displayed in the audit dashboard. See [CONTRIBUTING.md](CONTRIBUTING.md) and [REVIEWING.md](REVIEWING.md) for more details.
