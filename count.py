import requests
import json

url = "https://raw.githubusercontent.com/SingularityNET-Archive/SingularityNET-Archive/refs/heads/main/Data/Snet-Ambassador-Program/Meeting-Summaries/2025/meeting-summaries-array.json"

# Fetch the JSON from the URL
response = requests.get(url)
data = response.json()

# Ensure we’re always working with a list at the top level
if isinstance(data, list):
    top_level_items = data
else:
    top_level_items = [data]

# Print only the workgroup value for each top-level item
for index, item in enumerate(top_level_items, start=1):
    if isinstance(item, dict):
        workgroup = item.get("workgroup", "Unknown Workgroup")
        print(f"Item {index} workgroup: {workgroup}")
    else:
        print(f"Item {index} is not a dictionary (type: {type(item).__name__})")

