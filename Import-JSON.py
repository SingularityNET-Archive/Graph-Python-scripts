import requests
import json
from collections import defaultdict, Counter

# URL to the JSON file
url = "https://raw.githubusercontent.com/SingularityNET-Archive/SingularityNET-Archive/refs/heads/main/Data/Snet-Ambassador-Program/Meeting-Summaries/2025/meeting-summaries-array.json"

# Fetch JSON data from URL
response = requests.get(url)
data = response.json()

# --- Containers for counts and meeting lists ---
workgroup_counts = Counter()
workgroup_meetings = defaultdict(list)

# --- Process JSON ---
if isinstance(data, list):
    for item in data:
        if isinstance(item, dict):
            workgroup = item.get("workgroup", "Unknown Workgroup")
            workgroup_counts[workgroup] += 1

            # pull date from nested meetingInfo.date
            meeting_info_obj = item.get("meetingInfo", {})
            date = meeting_info_obj.get("date", "Unknown Date")

            # also capture typeOfMeeting or summary/title
            meeting_type = meeting_info_obj.get("typeOfMeeting", "")
            title = item.get("title") or item.get("summary") or meeting_type or ""

            meeting_info = f"{date} - {title}".strip(" -")
            workgroup_meetings[workgroup].append(meeting_info)
elif isinstance(data, dict):
    workgroup = data.get("workgroup", "Unknown Workgroup")
    workgroup_counts[workgroup] += 1
    meeting_info_obj = data.get("meetingInfo", {})
    date = meeting_info_ob


