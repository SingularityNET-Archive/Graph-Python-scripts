import requests
import json
import networkx as nx
import matplotlib.pyplot as plt

# --- CONFIG ---
url = "https://raw.githubusercontent.com/SingularityNET-Archive/SingularityNET-Archive/refs/heads/main/Data/Snet-Ambassador-Program/Meeting-Summaries/2025/meeting-summaries-array.json"  # Replace with your URL
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

# --- NEW: Count top-level values ---
top_level_count = len(workgroups)
print(f"🔹 Number of top-level workgroup entries: {top_level_count}")

# --- 2. Helper functions ---
def safe_get(d, keys, default=None):
    """Safely walk nested dict keys."""
    for key in keys:
        if isinstance(d, dict) and key in d:
            d = d[key]
        else:
            return default
    return d

def sanitize_value(v):
    """
    Return a GEXF-safe representation of v:
      - keep str/int/float/bool
      - convert lists/dicts/other -> json string
      - drop None -> return None
    """
    if v is None:
        return None
    if isinstance(v, (str, int, float, bool)):
        return v
    try:
        # Prefer JSON representation for lists/dicts
        return json.dumps(v, ensure_ascii=False)
    except Exception:
        # Fallback to string
        return str(v)

def find_invalid_attrs(G):
    """Return list of (node_or_edge, attr_name, value_type) that are invalid for GEXF."""
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

for wg_data in workgroups:
    workgroup = safe_get(wg_data, ["workgroup"], "Unknown Workgroup")
    meeting_id = safe_get(wg_data, ["workgroup_id"], f"MeetingID_{workgroup}")
    meeting_info = safe_get(wg_data, ["meetingInfo"], {})

    # Workgroup & Meeting
    G.add_node(workgroup, type="Workgroup")
    # Provide attributes using sanitize_value where appropriate (we'll sanitize later too)
    G.add_node(meeting_id, type="Meeting",
               date=meeting_info.get("date", "") or "",
               typeOfMeeting=meeting_info.get("typeOfMeeting", "") or "")
    G.add_edge(workgroup, meeting_id, relation="has_meeting")

    # Host & Documenter
    host = meeting_info.get("host", "Unknown Host")
    documenter = meeting_info.get("documenter", "Unknown Documenter")
    for person in [host, documenter]:
        G.add_node(person, type="Person")
    G.add_edge(meeting_id, host, relation="hosted_by")
    G.add_edge(meeting_id, documenter, relation="documented_by")

    # Attendees
    people_present = meeting_info.get("peoplePresent", "")
    for person in [p.strip() for p in people_present.split(",") if p.strip()]:
        G.add_node(person, type="Person")
        G.add_edge(meeting_id, person, relation="attended_by")

    # Working Docs
    for doc in meeting_info.get("workingDocs", []):
        title = doc.get("title", "Untitled Document")
        link = doc.get("link", "")
        G.add_node(title, type="Document", link=link or "")
        G.add_edge(meeting_id, title, relation="references_doc")

    # Agenda Items -> ActionItems & DecisionItems
    for agenda in wg_data.get("agendaItems", []):
        agenda_status = agenda.get("status", "unknown")
        agenda_id = f"Agenda_{agenda_status}_{meeting_id}"
        G.add_node(agenda_id, type="AgendaItem", status=agenda_status)
        G.add_edge(meeting_id, agenda_id, relation="has_agenda")

        # ActionItems
        for action in agenda.get("actionItems", []):
            action_text = action.get("text", "Unnamed Action")
            action_id = action_text[:40] + "..."
            G.add_node(action_id, type="ActionItem", dueDate=action.get("dueDate", "") or "")
            G.add_edge(agenda_id, action_id, relation="has_actionItem")
            assignee = action.get("assignee")
            if assignee:
                G.add_node(assignee, type="Person")
                G.add_edge(action_id, assignee, relation="assigned_to")

        # DecisionItems
        for decision in agenda.get("decisionItems", []):
            dec_text = decision.get("decision", "Unnamed Decision")
            dec_id = dec_text[:40] + "..."
            G.add_node(dec_id, type="DecisionItem",
                       effect=decision.get("effect"),
                       rationale=decision.get("rationale"))
            G.add_edge(agenda_id, dec_id, relation="has_decisionItem")

    # Tags & Emotions
    tags = safe_get(wg_data, ["tags"], {})
    for topic in tags.get("topicsCovered", "").split(","):
        topic = topic.strip()
        if topic:
            G.add_node(topic, type="Tag")
            G.add_edge(meeting_id, topic, relation="tagged_with")
    for emotion in tags.get("emotions", "").split(","):
        emotion = emotion.strip()
        if emotion:
            G.add_node(emotion, type="Emotion")
            G.add_edge(meeting_id, emotion, relation="tagged_with")

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
    # Replace attributes atomically
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

# --- 8. Optional: visualize quickly in Python ---
plt.figure(figsize=(18, 12))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=1500, font_size=8, arrows=True)
edge_labels = nx.get_edge_attributes(G, "relation")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)
plt.show()
