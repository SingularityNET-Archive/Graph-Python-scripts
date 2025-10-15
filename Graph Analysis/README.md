# Graph Analysis

Analysis tools operating on meeting JSON data to derive structure and relationships.

## Degree Analysis (Co-attendance)
Script: `Degree_Analysis/degree_analysis_to_md.py`
- Finds participant string lists recursively and builds an undirected co-attendance graph.
- Computes degree per node and distribution, and writes a Markdown report.
- Output: `Graph Analysis/Degree_Analysis/degree_analysis_report.md`
- Run:
```bash
python "Graph Analysis/Degree_Analysis/degree_analysis_to_md.py"
```

## Path Analysis
Script: `Path_Analysis/path_analysis_report.py`
- Extracts all JSON paths (dot/array notation), computes depth statistics, and writes a report.
- Output: `reports/path_analysis_report.md`
- Run:
```bash
python "Graph Analysis/Path_Analysis/path_analysis_report.py"
```

## Centrality (Field Co-occurrence)
Script: `Path_Analysis/Centrality_Analysis/json_centrality_analysis.py`
- Builds a field co-occurrence graph and computes degree/betweenness/closeness/eigenvector centralities.
- Output: `reports/centrality_analysis_report.md`
- Run:
```bash
python "Graph Analysis/Path_Analysis/Centrality_Analysis/json_centrality_analysis.py"
```

See `reports/README.md` for example outputs.
