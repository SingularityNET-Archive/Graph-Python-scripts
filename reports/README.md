# Reports

Generated Markdown reports and their sources.

- `workgroup_analysis_report.md`
  - Source: `Scripts/Import-JSON.py` (summary of workgroups and meetings)

- `path_analysis_report.md`
  - Source: `Graph Analysis/Path_Analysis/path_analysis_report.py`

- `centrality_analysis_report.md`
  - Source: `Graph Analysis/Path_Analysis/Centrality_Analysis/json_centrality_analysis.py`

- `degree_analysis_by_field_with_interpretation.md`
  - Source: Analysis variants under `Graph Analysis/`

- `Graph Analysis/Degree_Analysis/degree_analysis_report.md`
  - Source: `Graph Analysis/Degree_Analysis/degree_analysis_to_md.py`

- `unified_analysis_report.md`
  - Source: `Graph Analysis/unified_analysis.py`
  - Command:
```bash
python "Graph Analysis/unified_analysis.py" --output reports/unified_analysis_report.md
```

Re-run the corresponding scripts to regenerate any report.
