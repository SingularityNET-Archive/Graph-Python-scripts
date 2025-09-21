import requests
import json
from collections import Counter

# URL to the JSON file
url = "https://raw.githubusercontent.com/SingularityNET-Archive/SingularityNET-Archive/refs/heads/main/Data/Snet-Ambassador-Program/Meeting-Summaries/2025/meeting-summaries-array.json"

# Fetch JSON data from URL
response = requests.get(url)
data = response.json()

# --- Count workgroup values ---
workgroup_counts = Counter()

# If top-level JSON is a list:
if isinstance(data, list):
    for item in data:
        if isinstance(item, dict):
            workgroup = item.get("workgroup", "Unknown Workgroup")
            workgroup_counts[workgroup] += 1
# If top-level JSON is a dict:
elif isinstance(data, dict):
    workgroup = data.get("workgroup", "Unknown Workgroup")
    workgroup_counts[workgroup] += 1

# --- Save summary to a text file ---
summary_lines = ["Workgroup Counts Summary:\n"]
for workgroup, count in workgroup_counts.items():
    summary_lines.append(f"{workgroup}: {count}")

summary_text = "\n".join(summary_lines)

with open("workgroup_summary.txt", "w", encoding="utf-8") as f:
    f.write(summary_text)

print("Summary saved to workgroup_summary.txt")
