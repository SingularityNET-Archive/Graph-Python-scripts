import requests
import networkx as nx
import matplotlib.pyplot as plt

# === 1. Fetch remote JSON ===
url = "https://raw.githubusercontent.com/SingularityNET-Archive/SingularityNET-Archive/refs/heads/main/Data/Snet-Ambassador-Program/Meeting-Summaries/2025/meeting-summaries-array.json"  # Replace with your URL
response = requests.get(url)

if response.status_code != 200:
    raise Exception(f"Failed to fetch JSON. Status code: {response.status_code}")

data = response.json()

# === 2. Handle JSON as list or dict ===
if isinstance(data, list):
    if len(data) == 0:
        raise Exception("JSON list is empty")
    data = data[0]  # Use the first object

if not isinstance(data, dict):
    raise Exception("Unexpected JSON structure, expected dict or list of dicts")

# === 3. Helper function to safely get nested keys ===
def safe_get(d, keys, default=None):
    """
    Safely navigate nested dictionaries.
    keys: list of keys to traverse
    """
    for key in keys:
        if isinstance(d, dict) and key in d:
            d = d[key]
        else:
            return default
    return d

# === 4. Create directed graph ===
G = nx.DiGraph()

# Workgroup & Meeting
workgroup = safe_get(data, ["workgroup"], "Unknown Workgroup")
meeting_id = safe_get(data, ["workgroup_id"], "MeetingID_Unknown")
meeting_info = safe_get(data, ["meetingInfo"], {})

G.add_node(workgroup, type="Workgroup")
G.add_node(meeting_id, type="Meeting", 
           date=meeting_info.get("date", ""),
           typeOfMeeting=meeting_info.get("typeOfMeeting", ""))
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
    G.add_node(title, type="Document", link=link)
    G.add_edge(meeting_id, title, relation="references_doc")

# Agenda Items → ActionItems & DecisionItems
for agenda in data.get("agendaItems", []):
    agenda_status = agenda.get("status", "unknown")
    agenda_id = f"Agenda_{agenda_status}"
    G.add_node(agenda_id, type="AgendaItem", status=agenda_status)
    G.add_edge(meeting_id, agenda_id, relation="has_agenda")
    
    # ActionItems
    for action in agenda.get("actionItems", []):
        action_text = action.get("text", "Unnamed Action")
        action_id = action_text[:40] + "..."  # shorten
        G.add_node(action_id, type="ActionItem", dueDate=action.get("dueDate", ""))
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
tags = safe_get(data, ["tags"], {})
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

# === 5. Visualize the graph ===
plt.figure(figsize=(18, 12))
pos = nx.spring_layout(G, seed=42)
node_font_size = 8  # Configurable font size for node labels
edge_font_size = node_font_size  # Match edge label font size to node label font size

nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=2000, font_size=node_font_size)
edge_labels = nx.get_edge_attributes(G, "relation")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=edge_font_size)
plt.savefig("graph.png")
print("Graph saved as graph.png")
# To open in browser from terminal:
# $BROWSER graph.png

