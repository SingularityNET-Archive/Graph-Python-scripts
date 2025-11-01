#!/usr/bin/env python3
"""
Audit script to collect and aggregate GitHub Issues reviews for graph analysis results.

Fetches issues with 'review' label, parses ratings and comments, and generates
a JSON report with trust scores and metrics.
"""

import json
import os
import re
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import defaultdict

try:
    from github import Github
except ImportError:
    print("Error: PyGithub not installed. Run: pip install PyGithub", file=sys.stderr)
    sys.exit(1)


# Repository configuration
REPO_OWNER = "SingularityNET-Archive"
REPO_NAME = "Graph-Python-scripts"
OUTPUT_FILE = "docs/audit/reviews.json"

# Method names to track
METHODS = [
    "coattendance",
    "field-degree",
    "path-structure",
    "centrality",
    "clustering",
    "components",
]

# Rating labels mapping
RATING_LABELS = {
    "correct": "correct",
    "needs-review": "needs-review",
    "needs_review": "needs-review",
    "incorrect": "incorrect",
}


def extract_method_from_body(body: str) -> Optional[str]:
    """Extract method name from issue body (markdown template or query param)."""
    if not body:
        return None

    # Try to find method from markdown template format: **Method:** method_name
    method_match = re.search(r'\*\*Method:\*\*\s*([^\n]+)', body, re.IGNORECASE)
    if method_match:
        method = method_match.group(1).strip().lower()
        # Remove markdown code blocks and normalize
        method = method.replace("`", "").replace("<!--", "").replace("-->", "").strip()
        method = method.replace(" ", "-").replace("_", "-")
        if method in METHODS:
            return method

    # Try to find from template field format (old YAML form): ### Analysis Method
    method_match = re.search(r'###\s*Analysis Method\s*\n\s*([^\n]+)', body, re.IGNORECASE)
    if method_match:
        method = method_match.group(1).strip().lower()
        method = method.replace(" ", "-").replace("_", "-")
        if method in METHODS:
            return method

    # Try to find from query parameter in body
    query_match = re.search(r'method=([^\s&]+)', body)
    if query_match:
        method = query_match.group(1).strip().lower()
        method = method.replace(" ", "-").replace("_", "-")
        if method in METHODS:
            return method

    return None


def extract_rating_from_labels(labels: List[Any]) -> Optional[str]:
    """Extract rating from issue labels."""
    for label in labels:
        label_name = label.name.lower()
        if label_name in RATING_LABELS:
            return RATING_LABELS[label_name]
        if label_name == "needs-review":
            return "needs-review"
    return None


def extract_rating_from_body(body: str) -> Optional[str]:
    """Extract rating from issue body (markdown template checkboxes)."""
    if not body:
        return None
    
    # Try to find rating from markdown template checkboxes
    # Format: - [x] Correct or - [x] Needs Review or - [x] Incorrect
    if re.search(r'-\s*\[x\]\s*Correct', body, re.IGNORECASE):
        return "correct"
    elif re.search(r'-\s*\[x\]\s*Incorrect', body, re.IGNORECASE):
        return "incorrect"
    elif re.search(r'-\s*\[x\]\s*Needs Review', body, re.IGNORECASE):
        return "needs-review"
    
    # Fallback: Try to find rating from old template field (dropdown)
    rating_match = re.search(r'###\s*Rating\s*\n\s*([^\n]+)', body, re.IGNORECASE)
    if rating_match:
        rating = rating_match.group(1).strip()
        return normalize_rating(rating)
    
    return None


def normalize_rating(rating: str) -> str:
    """Normalize rating value to standard format."""
    if not rating:
        return "needs-review"
    
    rating_lower = rating.lower().strip()
    # Handle dropdown format values (with spaces, title case)
    if "correct" in rating_lower:
        return "correct"
    elif "incorrect" in rating_lower:
        return "incorrect"
    elif "needs review" in rating_lower or "needs-review" in rating_lower or "needs_review" in rating_lower:
        return "needs-review"
    else:
        return "needs-review"  # Default


def extract_comment_from_body(body: str) -> str:
    """Extract comment text from issue body."""
    if not body:
        return ""

    # Try to find comment section
    comment_match = re.search(
        r'###\s*Comments?\s*\n\s*(.*?)(?=\n###|\n---|\Z)',
        body,
        re.IGNORECASE | re.DOTALL,
    )
    if comment_match:
        return comment_match.group(1).strip()

    # Fallback: return first substantial text block
    lines = body.split("\n")
    comment_lines = []
    in_comment = False
    for line in lines:
        if line.strip().startswith("###") or line.strip().startswith("---"):
            if in_comment:
                break
            if "comment" in line.lower():
                in_comment = True
                continue
        if in_comment and line.strip():
            comment_lines.append(line.strip())

    return " ".join(comment_lines) if comment_lines else ""


def compute_trust_score(correct: int, incorrect: int, needs_review: int, total: int) -> float:
    """Compute trust score: (correct - incorrect) / total, clamped to [0, 1]."""
    if total == 0:
        return 0.0
    score = (correct - incorrect) / total
    # Normalize to [0, 1] range
    return max(0.0, min(1.0, (score + 1.0) / 2.0))


def main() -> None:
    """Main function to fetch and aggregate review issues."""
    # Get GitHub token from environment
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        print("Error: GITHUB_TOKEN environment variable not set", file=sys.stderr)
        print("Note: For GitHub Actions, this is automatically set as GITHUB_TOKEN", file=sys.stderr)
        sys.exit(1)

    # Initialize GitHub client
    g = Github(github_token)
    repo = g.get_repo(f"{REPO_OWNER}/{REPO_NAME}")

    # Fetch all issues with 'review' label
    print(f"Fetching issues with 'review' label from {REPO_OWNER}/{REPO_NAME}...")
    issues = repo.get_issues(state="all", labels=["review"])

    # Aggregate data by method
    method_data: Dict[str, Dict[str, Any]] = defaultdict(
        lambda: {
            "total_reviews": 0,
            "correct": 0,
            "incorrect": 0,
            "needs_review": 0,
            "trust_score": 0.0,
            "reviews": [],
        }
    )

    issue_count = 0
    for issue in issues:
        issue_count += 1
        # Skip pull requests
        if issue.pull_request:
            continue

        method = extract_method_from_body(issue.body or "")
        if not method:
            # Skip issues without a valid method
            continue

        # Try to extract rating from body first (template field), then from labels
        rating = extract_rating_from_body(issue.body or "")
        if not rating:
            rating = extract_rating_from_labels(list(issue.labels))
        if not rating:
            rating = "needs-review"  # Default if no rating found

        comment = extract_comment_from_body(issue.body or "")

        # Add to method data
        method_data[method]["total_reviews"] += 1
        method_data[method][rating] += 1
        method_data[method]["reviews"].append(
            {
                "issue_number": issue.number,
                "rating": rating,
                "comment": comment,
                "author": issue.user.login if issue.user else "unknown",
                "created_at": issue.created_at.isoformat() if issue.created_at else "",
                "url": issue.html_url,
            }
        )

        print(f"  Processed issue #{issue.number}: {method} - {rating}")

    # Compute trust scores and sort reviews
    for method, data in method_data.items():
        total = data["total_reviews"]
        data["trust_score"] = compute_trust_score(
            data["correct"], data["incorrect"], data["needs_review"], total
        )
        # Sort reviews by creation date (newest first)
        data["reviews"].sort(key=lambda x: x["created_at"], reverse=True)

    # Create output structure
    output = {
        "last_updated": datetime.utcnow().isoformat() + "Z",
        "total_issues_processed": issue_count,
        "methods": dict(method_data),
    }

    # Ensure all methods are represented (even with zero reviews)
    for method in METHODS:
        if method not in output["methods"]:
            output["methods"][method] = {
                "total_reviews": 0,
                "correct": 0,
                "incorrect": 0,
                "needs_review": 0,
                "trust_score": 0.0,
                "reviews": [],
            }

    # Write output file
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Audit complete!")
    print(f"  Processed {issue_count} issues")
    print(f"  Methods reviewed: {len([m for m in method_data if method_data[m]['total_reviews'] > 0])}")
    print(f"  Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

