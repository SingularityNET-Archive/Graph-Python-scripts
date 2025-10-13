import json
import requests
from datetime import datetime

def load_json_remote(url):
    """Load JSON data from a remote URL."""
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def infer_schema(data, level=0):
    """
    Recursively infer schema of a JSON object.
    Returns a nested dict describing keys and their types.
    """
    if isinstance(data, dict):
        schema = {}
        for key, value in data.items():
            schema[key] = infer_schema(value, level + 1)
        return schema
    elif isinstance(data, list):
        if len(data) == 0:
            return ["empty_list"]
        # Infer schema from first element
        element_schema = infer_schema(data[0], level + 1)
        return [element_schema]
    else:
        return type(data).__name__

def format_schema(schema, indent=0):
    """Convert schema dictionary to formatted Markdown text."""
    lines = []
    prefix = "  " * indent
    if isinstance(schema, dict):
        for key, value in schema.items():
            if isinstance(value, (dict, list)):
                lines.append(f"{prefix}- **{key}**:")
                lines.extend(format_schema(value, indent + 1))
            else:
                lines.append(f"{prefix}- **{key}**: `{value}`")
    elif isinstance(schema, list):
        if len(schema) == 1:
            lines.append(f"{prefix}- List of:")
            lines.extend(format_schema(schema[0], indent + 1))
        else:
            lines.append(f"{prefix}- Mixed list elements: {schema}")
    else:
        lines.append(f"{prefix}- `{schema}`")
    return lines

def write_markdown(schema, output_file):
    """Write inferred schema to a Markdown file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# JSON Schema Report\n")
        f.write(f"**Generated on:** {timestamp}\n\n")
        f.write("## Inferred Schema\n\n")
        for line in format_schema(schema):
            f.write(line + "\n")
    print(f"✅ Schema written to {output_file}")

def main():
    url = "https://raw.githubusercontent.com/SingularityNET-Archive/SingularityNET-Archive/refs/heads/main/Data/Snet-Ambassador-Program/Meeting-Summaries/2025/meeting-summaries-array.json"
    output_file = "json_schema_report.md"

    print("📡 Fetching JSON from remote source...")
    data = load_json_remote(url)
    print(f"✅ Downloaded {len(data)} top-level records.")

    # If the file is a list, infer schema of the first element
    if isinstance(data, list) and len(data) > 0:
        schema = [infer_schema(data[0])]
    else:
        schema = infer_schema(data)

    print("🔍 Inferring JSON schema...")
    for line in format_schema(schema):
        print(line)

    write_markdown(schema, output_file)

if __name__ == "__main__":
    main()
