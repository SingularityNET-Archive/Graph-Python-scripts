import requests
import json
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter, defaultdict

# --- CONFIG ---
url = "https://raw.githubusercontent.com/SingularityNET-Archive/SingularityNET-Archive/refs/heads/main/Data/Snet-Ambassador-Program/Meeting-Summaries/2025/meeting-summaries-array.json"
output_gexf = "all_workgroups_graph_sanitized.gexf"

# --- 1. Fetch remote JSON safely ---
response = requests.get(url)
if response.status_code != 200:
    raise Exception(f"Failed to fetch JSON. Status code: {response.status_code}")

data = response.json()

# Normalize to list of workgroups
if isinstance(data, dict):
    workgroups = [data]
elif isinstance(data, list):
    workgroups = data
else:
    raise Exception("Unexpected JSON structure; expected dict or list")

# Debug: top-level count
top_level_count = len(workgroups)
print(f"🔹 Number of top-level workgroup entries: {top_level_count}")

# Quick check for repeated workgroup_id values (diagnostic)
ids = [ (wg.get("workgroup_id") or "") for wg in workgroups ]
c = Counter(ids)
print("Top repeated explicit workgroup_id values (empty string means missing):", c.most_common(10))

# --- 2. Helper functions ---
def safe_get(d, keys, default=None):
    for key in keys:
        if isinstance(d, dict) and key in d:
            d = d[key]
        else:
            return default
    return d

def sanitize_value(v):
    if v is None:
        return None
    if isinstance(v, (str, int, float, bool)):
        return v
    try:
        return json.dumps(v, ensure_ascii=False)
    except Exception:
        return str(v)

def find_invalid_attrs(G):
    bad = []
    for n, attrs in G.nodes(data=True):
        for k, v in attrs.items():
            if v is None or not isinstance(v, (str, int, float, bool)):
                bad.append(("node", n, k, type(v).__name__))
    for u, v, attrs in G.edges(data=True):
        for k, val in attrs.items():
            if val is None or not isinstance(val, (str, int, float, bool)):
                bad.append(("edge", (u, v), k, type(val).__name__))
    return bad

# --- 3. Build the directed graph for all workgroups ---
G = nx.DiGraph()

# Track seen meeting_ids to detect duplicates
meeting_id_counts = Counter()
for idx, wg_data in enumerate(workgroups, start=1):
    # Prefer explicit workgroup_id; fall back to unique generated id using index
    explicit_meeting_id = safe_get(wg_data, ["workgroup_id"], None)
    workgroup_name = safe_get(wg_data, ["workgroup"], "Unknown Workgroup")

    # ensure meeting_node_id is unique and string:
    if explicit_meeting_id:
        meeting_node_id = str(explicit_meeting_id)
        # Append index if this explicit id appears more than once
        if meeting_id_counts[meeting_node_id] > 0:
            meeting_node_id = f"{meeting_node_id}__{idx}"
    else:
        # No explicit meeting id -> generate one using workgroup + index to guarantee uniqueness
        meeting_node_id = f"Meeting_{workgroup_name}_{idx}"

    meeting_id_counts[meeting_node_id] += 1

    meeting_info = safe_get(wg_data, ["meetingInfo"], {})

    # Make sure node ids are strings
    workgroup_node_id = str(workgroup_name)
    meeting_node_id = str(meeting_node_id)

    # Workgroup & Meeting nodes
    G.add_node(workgroup_node_id, type="Workgroup", label=workgroup_node_id)
    G.add_node(meeting_node_id, type="Meeting",
               date=meeting_info.get("date", "") or "",
               typeOfMeeting=meeting_info.get("typeOfMeeting", "") or "",
               label=meeting_node_id)
    G.add_edge(workgroup_node_id, meeting_node_id, relation="has_meeting")

    # Host & Documenter
    host = meeting_info.get("host", "Unknown Host")
    documenter = meeting_info.get("documenter", "Unknown Documenter")
    for person in [host, documenter]:
        if person:
            G.add_node(str(person), type="Person", label=str(person))
    G.add_edge(meeting_node_id, str(host), relation="hosted_by")
    G.add_edge(meeting_node_id, str(documenter), relation="documented_by")

    # Attendees
    people_present = meeting_info.get("peoplePresent", "")
    for person in [p.strip() for p in people_present.split(",") if p.strip()]:
        G.add_node(str(person), type="Person", label=str(person))
        G.add_edge(meeting_node_id, str(person), relation="attended_by")

    # Working Docs
    for doc in meeting_info.get("workingDocs", []):
        title = doc.get("title", "Untitled Document")
        link = doc.get("link", "")
        # ensure document node id is unique-ish by combining title+index
        doc_node_id = f"Doc_{title}_{idx}"
        G.add_node(str(doc_node_id), type="Document", link=link or "", label=title)
        G.add_edge(meeting_node_id, str(doc_node_id), relation="references_doc")

    # Agenda Items -> ActionItems & DecisionItems
    for aindex, agenda in enumerate(wg_data.get("agendaItems", []), start=1):
        agenda_status = agenda.get("status", "unknown")
        agenda_id = f"Agenda_{agenda_status}_{idx}_{aindex}"
        G.add_node(agenda_id, type="AgendaItem", status=agenda_status, label=agenda_id)
        G.add_edge(meeting_node_id, agenda_id, relation="has_agenda")

        # ActionItems
        for action_index, action in enumerate(agenda.get("actionItems", []), start=1):
            action_text = action.get("text", "Unnamed Action")
            action_id = f"Action_{idx}_{aindex}_{action_index}"
            G.add_node(action_id, type="ActionItem", dueDate=action.get("dueDate", "") or "", label=action_text[:60])
            G.add_edge(agenda_id, action_id, relation="has_actionItem")
            assignee = action.get("assignee")
            if assignee:
                G.add_node(str(assignee), type="Person", label=str(assignee))
                G.add_edge(action_id, str(assignee), relation="assigned_to")

        # DecisionItems
        for decision_index, decision in enumerate(agenda.get("decisionItems", []), start=1):
            dec_text = decision.get("decision", "Unnamed Decision")
            dec_id = f"Decision_{idx}_{aindex}_{decision_index}"
            G.add_node(dec_id, type="DecisionItem",
                       effect=decision.get("effect"),
                       rationale=decision.get("rationale"),
                       label=dec_text[:60])
            G.add_edge(agenda_id, dec_id, relation="has_decisionItem")

    # Tags & Emotions
    tags = safe_get(wg_data, ["tags"], {})
    for topic in tags.get("topicsCovered", "").split(","):
        topic = topic.strip()
        if topic:
            G.add_node(str(topic), type="Tag", label=str(topic))
            G.add_edge(meeting_node_id, str(topic), relation="tagged_with")
    for emotion in tags.get("emotions", "").split(","):
        emotion = emotion.strip()
        if emotion:
            G.add_node(str(emotion), type="Emotion", label=str(emotion))
            G.add_edge(meeting_node_id, str(emotion), relation="tagged_with")

# Debug: counts BEFORE sanitization
print("DEBUG BEFORE SANITIZATION -> node count:", len(G.nodes()), "edge count:", len(G.edges()))
print("Sample nodes (first 50):", list(G.nodes())[:50])

# --- 4. (Optional) Inspect current invalid attributes BEFORE sanitization ---
bad_before = find_invalid_attrs(G)
if bad_before:
    print("Found attributes with potentially invalid types before sanitization (showing up to 20):")
    for item in bad_before[:20]:
        print(item)
else:
    print("No obviously invalid attributes detected before sanitization.")

# --- 5. Sanitize node attributes ---
for n, attrs in list(G.nodes(data=True)):
    new_attrs = {}
    for k, v in attrs.items():
        san = sanitize_value(v)
        if san is not None:
            new_attrs[k] = san
    # Keep label attr if present to increase clarity in Gephi
    G.nodes[n].clear()
    G.nodes[n].update(new_attrs)

# --- 6. Sanitize edge attributes ---
for u, v, attrs in list(G.edges(data=True)):
    new_attrs = {}
    for k, val in attrs.items():
        san = sanitize_value(val)
        if san is not None:
            new_attrs[k] = san
    G[u][v].clear()
    G[u][v].update(new_attrs)

# --- 7. Final check and write GEXF ---
bad_after = find_invalid_attrs(G)
if bad_after:
    print("⚠ After sanitization, still some problematic attributes (should not happen):")
    for item in bad_after:
        print(item)
    raise Exception("Graph still contains invalid attribute types for GEXF export.")
else:
    nx.write_gexf(G, output_gexf)
    print(f"✅ Graph exported to {output_gexf}")

# Final debug counts
print("DEBUG AFTER SANITIZATION -> node count:", len(G.nodes()), "edge count:", len(G.edges()))
print("Sample nodes (first 50):", list(G.nodes())[:50])

# --- 8. Optional: visualize quickly in Python ---
plt.figure(figsize=(18, 12))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_size=400, font_size=7, arrows=True)
edge_labels = nx.get_edge_attributes(G, "relation")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)
plt.show()
