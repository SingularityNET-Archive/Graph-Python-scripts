# Unified Graph Analysis Report
**Generated on:** 2025-10-15 09:20:14

## Summary
- Co-attendance graph (nodes): 418
- Co-attendance graph (edges): 1336
- Path graph (nodes): 6833
- Path graph (edges): 6832
- Field graph (nodes): 44
- Field graph (edges): 149

## Degree (Co-attendance) Analysis
### Top Nodes by Degree
| Rank | Node | Degree |
|------|------|--------|
| 1 | We established the initial Q3 monthly roadmap and base expectations of what we … | 18 |
| 2 | Takes effort to find relevant information | 18 |
| 3 | What are Quarter 3 maintenance plans? | 18 |
| 4 | We went over the Progress Report, line by line | 18 |
| 5 | Organising videos is more challenging | 18 |
| 6 | Should we reward new feedback? | 18 |
| 7 | Organising Items gives a nice and logical framework to understand the Ambassado… | 18 |
| 8 | GPT is very helpful, providing useful information or triggering thoughts of imp… | 18 |
| 9 | [Insight](https://docs.google.com/document/d/1X1JC3Op5i4dGkthxHSYzwF-mSaKn8LZAr… | 18 |
| 10 | Uncertain when the time comes to contribute | 18 |

### Degree Distribution
| Degree | Count of Nodes |
|--------|-----------------|
| 1 | 14 |
| 2 | 30 |
| 3 | 56 |
| 4 | 70 |
| 5 | 61 |
| 6 | 48 |
| 7 | 32 |
| 9 | 12 |
| 10 | 22 |
| 11 | 13 |
| 12 | 13 |
| 13 | 28 |
| 18 | 19 |

## JSON Path Structure Analysis
- Total Unique Paths: 6832
- Maximum Depth: 6
- Average Depth: 4.20

### Deepest JSON Paths (sample)
- `[0].agendaItems[0].actionItems[0].text`
- `[0].agendaItems[0].actionItems[0].assignee`
- `[0].agendaItems[0].actionItems[0].dueDate`
- `[0].agendaItems[0].actionItems[0].status`
- `[0].agendaItems[0].decisionItems[0].decision`
- `[0].agendaItems[0].decisionItems[0].effect`
- `[0].agendaItems[0].decisionItems[1].decision`
- `[0].agendaItems[0].decisionItems[1].rationale`
- `[0].agendaItems[0].decisionItems[1].effect`
- `[0].agendaItems[0].decisionItems[2].decision`

### Most Common Parent Paths
| Rank | Parent Path | Count |
|------|-------------|-------|
| 1 | `[12].agendaItems[0]` | 26 |
| 2 | `[2].agendaItems[0]` | 21 |
| 3 | `[10].agendaItems[0]` | 21 |
| 4 | `[7].agendaItems[0]` | 19 |
| 5 | `[17].agendaItems[0]` | 19 |
| 6 | `[22].meetingInfo` | 19 |
| 7 | `[23].meetingInfo` | 19 |
| 8 | `[101].agendaItems[0]` | 19 |
| 9 | `[11].agendaItems[0]` | 18 |
| 10 | `[37].agendaItems[0]` | 18 |

## Field Centrality (Co-occurrence)
| Rank | Field | Degree | Betweenness | Closeness | Eigenvector |
|------|-------|--------|-------------|-----------|------------|
| 1 | host | 0.256 | 0.001 | 0.256 | 0.309 |
| 2 | documenter | 0.256 | 0.001 | 0.256 | 0.309 |
| 3 | typeOfMeeting | 0.256 | 0.001 | 0.256 | 0.309 |
| 4 | workingDocs | 0.256 | 0.001 | 0.256 | 0.309 |
| 5 | date | 0.256 | 0.001 | 0.256 | 0.309 |
| 6 | purpose | 0.256 | 0.001 | 0.256 | 0.309 |
| 7 | peoplePresent | 0.256 | 0.001 | 0.256 | 0.309 |
| 8 | status | 0.256 | 0.030 | 0.256 | 0.000 |
| 9 | meetingVideoLink | 0.233 | 0.000 | 0.234 | 0.290 |
| 10 | noSummaryGiven | 0.209 | 0.000 | 0.209 | 0.000 |

## Clustering (Field Co-occurrence Graph)
- Average Clustering Coefficient: 0.882

### Top Nodes by Clustering Coefficient
| Rank | Field | Clustering |
|------|-------|------------|
| 1 | noSummaryGiven | 1.000 |
| 2 | tags | 1.000 |
| 3 | agendaItems | 1.000 |
| 4 | workgroup | 1.000 |
| 5 | type | 1.000 |
| 6 | canceledSummary | 1.000 |
| 7 | workgroup_id | 1.000 |
| 8 | meetingInfo | 1.000 |
| 9 | timestampedVideo | 1.000 |
| 10 | dueDate | 1.000 |

## Connected Components (Field Co-occurrence Graph)
- Number of Components: 6
- Component Sizes (top 10): [12, 12, 10, 4, 4, 2]
- Sample of Largest Component Nodes (top 10):
  - host
  - meetingVideoLink
  - documenter
  - timestampedVideo
  - typeOfMeeting
  - workingDocs
  - otherMediaLink
  - mediaLink
  - date
  - purpose

