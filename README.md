# Graph-Python-scripts

This repository contains Python scripts for parsing meeting summaries and visualizing them as directed graphs using NetworkX and Matplotlib, plus exporting to GEXF for use in Gephi.

## Contents
- `Scripts/Nodes-Edges.py`: Build a directed graph from a single meeting summary and save `graph.png`.
- `Scripts/Nodes-Edges2.py`: Build a directed graph from multiple meeting summaries and save `graph2.png`.
- `Scripts/GEXF-export.py`: Build a comprehensive directed graph and export `all_workgroups_graph_sanitized.gexf`.
- `Scripts/count.py`: Print top-level workgroup names from the remote JSON.
- `Scripts/Import-JSON.py`: Generate `workgroup_meetings_summary.txt` with counts and meeting listings per workgroup.
- `graph.png`, `graph2.png`: Example rendered graphs.
- `Scripts/all_workgroups_graph_sanitized.gexf`: Example GEXF export ready for Gephi.

## Prerequisites
- Python 3.9+
- Packages:
  - `requests`
  - `networkx`
  - `matplotlib`

Install packages:

```bash
pip install requests networkx matplotlib
```

## Data Source
All scripts fetch JSON from a public URL:

- `https://raw.githubusercontent.com/SingularityNET-Archive/SingularityNET-Archive/refs/heads/main/Data/Snet-Ambassador-Program/Meeting-Summaries/2025/meeting-summaries-array.json`

The scripts handle both top-level list and dict JSON structures.

## Usage
Run scripts from the project root or the `Scripts/` directory.

### 1) Build a graph from a single meeting: `Scripts/Nodes-Edges.py`
- Purpose: Parse one meeting object and produce a directed graph of relationships among workgroup, meeting, people, documents, agenda items, action items, decision items, tags, and emotions.
- Output: Saves an image `graph.png` in the project root.

Command:
```bash
python Scripts/Nodes-Edges.py
```

### 2) Build a graph from multiple meetings: `Scripts/Nodes-Edges2.py`
- Purpose: Iterate all meetings/workgroups and build a combined directed graph.
- Output: Saves `graph2.png` in the project root.

Command:
```bash
python Scripts/Nodes-Edges2.py
```

### 3) Export a GEXF for Gephi: `Scripts/GEXF-export.py`
- Purpose: Build a comprehensive, sanitized directed graph across all workgroups and export to GEXF.
- Output: Writes `Scripts/all_workgroups_graph_sanitized.gexf`.

Notes:
- Ensures node IDs are strings and unique.
- Sanitizes node/edge attributes to primitive types for GEXF compatibility.
- Emits diagnostics (counts, sample nodes) before/after sanitization.

Command:
```bash
python Scripts/GEXF-export.py
```

Open the GEXF in Gephi to explore the network.

### 4) Quick inspection of workgroups: `Scripts/count.py`
- Purpose: Print the `workgroup` field for each top-level item in the JSON (list or dict).

Command:
```bash
python Scripts/count.py
```

### 5) Generate a text summary: `Scripts/Import-JSON.py`
- Purpose: Create `workgroup_meetings_summary.txt` listing counts per workgroup and meeting info (date + title/type).
- Output: `Scripts/workgroup_meetings_summary.txt`.

Command:
```bash
python Scripts/Import-JSON.py
```

## Outputs
- `graph.png`: Single-meeting graph.
- `graph2.png`: Multi-meeting graph.
- `Scripts/all_workgroups_graph_sanitized.gexf`: GEXF for Gephi.
- `Scripts/workgroup_meetings_summary.txt`: Human-readable summary.

To preview generated images on macOS/Linux:

```bash
$BROWSER graph.png
$BROWSER graph2.png
```

## Notes
- All scripts are designed to run headlessly; graphs are saved to files instead of opening GUI windows.
- The code uses defensive accessors and type checks to tolerate missing or differently shaped fields.
- For reproducible layouts, the drawing functions use a fixed seed for `spring_layout` where applicable.
