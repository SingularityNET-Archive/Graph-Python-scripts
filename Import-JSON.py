import requests
import json

url = "https://raw.githubusercontent.com/SingularityNET-Archive/SingularityNET-Archive/refs/heads/main/Data/Snet-Ambassador-Program/Meeting-Summaries/2025/meeting-summaries-array.json"  # replace with your remote JSON URL

response = requests.get(url)
data = response.json()

# Handle if JSON is a list
if isinstance(data, list):
    data = data[0]

workgroup = data.get("workgroup", "Unknown Workgroup")
print(workgroup)

