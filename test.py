import requests
import json

# The raw URL of your JSON file
RAW_URL = "https://raw.githubusercontent.com/SingularityNET-Archive/SingularityNET-Archive/main/Data/Snet-Ambassador-Program/Meeting-Summaries/2025/meeting-summaries-by-id.json"

response = requests.get(RAW_URL)
response.raise_for_status()  # Checks for errors

# Load JSON data
data = json.loads(response.text)

# Now you can use 'data' as a Python dictionary or list
print(data)

# Example: Access a specific meeting summary by ID, if your JSON structure is like { "123": {...}, ... }
meeting_id = "123"
if meeting_id in data:
    print("Meeting summary for ID 123:")
    print(data[meeting_id])
else:
    print(f"No summary found for ID {meeting_id}")