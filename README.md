# Python-test

This repository is for testing Python Scripts

## Project Overview

This workspace contains Python scripts for visualizing meeting data as directed graphs using NetworkX and Matplotlib.

### Nodes-Edges.py

- **Purpose:**  
  Fetches a single meeting summary from a remote JSON file, parses its structure, and builds a directed graph representing relationships between workgroups, meetings, people, documents, agenda items, actions, decisions, tags, and emotions.
- **Key Steps:**  
  1. Downloads JSON data from a URL.
  2. Handles both list and dict JSON structures.
  3. Safely extracts nested fields.
  4. Adds nodes and edges for all relevant entities.
  5. Saves the resulting graph visualization as `graph.png`.

![graph.png](graph.png)

### Nodes-Edges2.py

- **Purpose:**  
  Processes an array of meeting summaries from a remote JSON file, building a directed graph that includes all workgroups and their associated meetings, people, documents, agenda items, actions, decisions, tags, and emotions.
- **Key Steps:**  
  1. Downloads JSON data from a URL.
  2. Handles both dict and list JSON structures, but always iterates through a list of workgroups.
  3. Safely extracts nested fields for each workgroup.
  4. Adds nodes and edges for all entities across all meetings.
  5. Saves the resulting graph visualization as `graph2.png`.

![graph2.png](graph2.png)

---

**Note:**  
Both scripts reference `meeting-summaries-array.json` as their data source, **not** `meeting-summaries-by-id.json`.  
They are designed for headless environments (such as dev containers). The graph images are saved to disk and can be viewed using the default browser with:

```bash
$BROWSER graph.png
$BROWSER graph2.png
```