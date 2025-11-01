# Review Audit System Documentation

This document explains how the community review and audit system works for graph analysis results.

## Overview

The review system provides a human-audit layer for validating graph analysis results. Community members can submit reviews via GitHub Issues, which are automatically collected and aggregated into trust scores and metrics.

## System Architecture

### Components

1. **GitHub Issues** - Review submission interface
   - Users submit reviews via issue template
   - Issues are tagged with `review` label
   - Additional labels: `correct`, `needs-review`, `incorrect`

2. **Audit Script** (`scripts/audit_reviews.py`)
   - Fetches issues with `review` label using GitHub API
   - Parses issue body to extract method, rating, and comments
   - Computes trust scores and aggregates metrics
   - Outputs JSON to `docs/audit/reviews.json`

3. **GitHub Actions** (`.github/workflows/review_audit.yml`)
   - Runs nightly at 2 AM UTC
   - Executes audit script
   - Commits updated `reviews.json` if changed

4. **Audit Dashboard** (HTML tab)
   - Displays trust scores per method
   - Shows rating distribution charts
   - Lists all review comments
   - Located in "Audit" tab of main dashboard

## Trust Score Calculation

Trust scores are computed per analysis method:

```
trust_score = ((correct - incorrect) / total + 1) / 2
```

Where:
- `correct` = number of "Correct" ratings
- `incorrect` = number of "Incorrect" ratings
- `total` = total number of reviews

The score is normalized to the range [0, 1]:
- **1.0** = All reviews are "Correct"
- **0.5** = Equal "Correct" and "Incorrect" ratings
- **0.0** = All reviews are "Incorrect"
- **Needs Review** ratings are neutral (don't affect the score)

## Review Data Structure

Reviews are stored in `docs/audit/reviews.json`:

```json
{
  "last_updated": "2025-01-15T02:00:00Z",
  "total_issues_processed": 25,
  "methods": {
    "coattendance": {
      "total_reviews": 10,
      "correct": 7,
      "incorrect": 1,
      "needs_review": 2,
      "trust_score": 0.7,
      "reviews": [
        {
          "issue_number": 123,
          "rating": "correct",
          "comment": "Results look accurate",
          "author": "username",
          "created_at": "2025-01-10T10:00:00",
          "url": "https://github.com/..."
        }
      ]
    }
  }
}
```

## Methods Tracked

The following analysis methods can be reviewed:

- `coattendance` - Co-attendance Degree Analysis
- `field-degree` - JSON Field Degree Analysis
- `path-structure` - JSON Path Structure Analysis
- `centrality` - Field Centrality (Co-occurrence)
- `clustering` - Clustering (Field Co-occurrence Graph)
- `components` - Connected Components (Field Co-occurrence Graph)

## Governance

### Review Criteria

Reviews should evaluate:
- **Accuracy**: Do results match the underlying data?
- **Methodology**: Are analysis methods appropriate?
- **Completeness**: Are important patterns captured?
- **Presentation**: Are visualizations clear and informative?

### Disagreement Resolution

When reviews disagree:
- Multiple perspectives are valuable for identifying issues
- The audit dashboard shows all ratings transparently
- Trust scores reflect aggregate opinions
- Maintainers review flagged analyses for investigation

### Review Updates

- Reviews are collected automatically each night
- New reviews appear in the dashboard within 24 hours
- Trust scores update as new reviews are added
- Historical review data is preserved in issue history

## Automation

### Nightly Audit Collection

The GitHub Action workflow:
1. Checks out repository
2. Sets up Python environment
3. Installs dependencies (PyGithub)
4. Runs `scripts/audit_reviews.py`
5. Commits and pushes updated `reviews.json` if changed

### Manual Trigger

The workflow can also be triggered manually:
- Go to Actions tab in GitHub
- Select "Review Audit Collection"
- Click "Run workflow"

## Future Enhancements

Potential improvements to the system:

- **Reviewer Reputation**: Track reviewer history and reliability
- **Auto-classification**: Use ML to classify review sentiment
- **Visualization Overlays**: Flag disputed nodes/edges in visualizations
- **Review Templates**: Domain-specific review checklists
- **Review Notifications**: Notify maintainers of flagged analyses

## Technical Details

### Dependencies

- `PyGithub>=2.1.0` - GitHub API access
- `Chart.js` (CDN) - Chart rendering in dashboard

### API Rate Limits

GitHub API has rate limits:
- 5,000 requests/hour for authenticated requests
- Audit script processes issues in batches to respect limits

### Data Privacy

- Review author usernames are displayed in dashboard
- Review comments are public
- All data is stored in public repository

## Troubleshooting

### Audit Data Not Updating

- Check GitHub Actions workflow status
- Verify `GITHUB_TOKEN` is set correctly
- Check for errors in audit script logs

### Missing Reviews

- Ensure issues have `review` label
- Verify method name matches exactly
- Check issue template fields are filled correctly

### Chart Not Rendering

- Verify Chart.js CDN is loaded
- Check browser console for JavaScript errors
- Ensure `reviews.json` exists and is valid JSON

