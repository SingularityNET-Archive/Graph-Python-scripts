PY=python

setup:
	python3 -m venv .venv
	. .venv/bin/activate && $(PY) -m pip install --upgrade pip && pip install -r requirements.txt

graphs:
	$(PY) Scripts/Nodes-Edges.py
	$(PY) Scripts/Nodes-Edges2.py

gexf:
	$(PY) Scripts/GEXF-export.py

summary:
	$(PY) Scripts/Import-JSON.py

degree-analysis:
	$(PY) "Graph Analysis/Degree_Analysis/degree_analysis_to_md.py"

path-report:
	$(PY) "Graph Analysis/Path_Analysis/path_analysis_report.py"

centrality-report:
	$(PY) "Graph Analysis/Path_Analysis/Centrality_Analysis/json_centrality_analysis.py"
