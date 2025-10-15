# Scripts

Utilities for fetching meeting data and generating graphs/exports.

## Nodes-Edges.py
- Purpose: Build a directed graph from a single meeting entry and save an image.
- Output: `graph.png`
- Run:
```bash
python Scripts/Nodes-Edges.py
```

## Nodes-Edges2.py
- Purpose: Build a combined directed graph across all meetings and save an image.
- Output: `graph2.png`
- Run:
```bash
python Scripts/Nodes-Edges2.py
```

## GEXF-export.py
- Purpose: Build a comprehensive directed graph and export to GEXF (Gephi).
- Output: `Scripts/all_workgroups_graph_sanitized.gexf`
- Run:
```bash
python Scripts/GEXF-export.py
```

## Import-JSON.py
- Purpose: Generate a text summary of workgroups and meetings.
- Output: `Scripts/workgroup_meetings_summary.txt`
- Run:
```bash
python Scripts/Import-JSON.py
```

## count.py
- Purpose: Print the `workgroup` value for each top-level JSON item.
- Run:
```bash
python Scripts/count.py
```

All scripts fetch JSON from the shared data source referenced in the top-level README.
