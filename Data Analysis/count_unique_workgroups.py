import json
import requests
from datetime import datetime
from collections import Counter

def load_json_remote(url):
    """Load JSON data from a remote URL."""
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def find_workgroups(obj, workgroup_keys=("workgroup", "workgroups")):
    """
    Recursively search for all workgroup names in a JSON object.
    Returns a list of strings (workgroup names).
    """
    found = []

    if isinstance(obj, dict):
        for key, value in obj.items():
            # Match case-insensitively
            if key.lower() in workgroup_keys:
                if isinstance(value, str):
                    found.append(value.strip())
                elif isinstance(value, list):
                    for v in value:
                        if isinstance(v, str):
                            found.append(v.strip())
            else:
                found.extend(find_workgroups(value, workgroup_keys))

    elif isinstance(obj, list):
        for item in obj:
            found.extend(find_workgroups(item, workgroup_keys))

    return found

def write_markdown_report(workgroup_counts, output_file):
    """Write results to a Markdown file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# Workgroup Analysis Report\n")
        f.write(f"**Generated on:** {timestamp}\n\n")

        total_unique = len(workgroup_counts)
        total_mentions = sum(workgroup_counts.values())

        f.write("## Summary\n")
        f.write(f"- Total Unique Workgroups: {total_unique}\n")
        f.write(f"- Total Mentions: {total_mentions}\n\n")

        f.write("## Workgroup Counts\n")
        f.write("| Rank | Workgroup | Mentions |\n|------|------------|-----------|\n")

        for i, (wg, count) in enumerate(workgroup_counts.most_common(), 1):
            f.write(f"| {i} | {wg} | {count} |\n")

    print(f"✅ Markdown report saved to: {output_file}")

def main():
    url = "https://raw.githubusercontent.com/SingularityNET-Archive/SingularityNET-Archive/refs/heads/main/Data/Snet-Ambassador-Program/Meeting-Summaries/2025/meeting-summaries-array.json"
    output_file = "workgroup_analysis_report.md"

    print("📡 Fetching data from remote source...")
    data = load_json_remote(url)
    print(f"✅ Downloaded {len(data)} top-level records.")

    print("🔍 Searching for workgroup mentions...")
    all_workgroups = find_workgroups(data)

    if not all_workgroups:
        print("⚠️ No workgroups found in the JSON.")
        return

    workgroup_counts = Counter(all_workgroups)

    print(f"📊 Found {len(workgroup_counts)} unique workgroups.")
    for wg, count in workgroup_counts.most_common(10):
        print(f"- {wg}: {count}")

    write_markdown_report(workgroup_counts, output_file)

if __name__ == "__main__":
    main()
