# Unified Graph Analysis Report
**Generated on:** 2025-10-15 09:44:01

## Summary
- Path graph (nodes): 6833
- Path graph (edges): 6832
- Field graph (nodes): 44
- Field graph (edges): 149

## JSON Field Degree Analysis
### Top Fields by Degree
| Rank | Field | Degree |
|------|-------|--------|
| 1 | host | 11 |
| 2 | typeOfMeeting | 11 |
| 3 | date | 11 |
| 4 | documenter | 11 |
| 5 | workingDocs | 11 |
| 6 | purpose | 11 |
| 7 | peoplePresent | 11 |
| 8 | status | 11 |
| 9 | meetingVideoLink | 10 |
| 10 | tags | 9 |

### Degree Distribution
| Degree | Count of Fields |
|--------|------------------|
| 1 | 2 |
| 2 | 2 |
| 3 | 9 |
| 4 | 4 |
| 5 | 1 |
| 7 | 2 |
| 8 | 3 |
| 9 | 12 |
| 10 | 1 |
| 11 | 8 |

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
| 2 | typeOfMeeting | 0.256 | 0.001 | 0.256 | 0.309 |
| 3 | date | 0.256 | 0.001 | 0.256 | 0.309 |
| 4 | documenter | 0.256 | 0.001 | 0.256 | 0.309 |
| 5 | workingDocs | 0.256 | 0.001 | 0.256 | 0.309 |
| 6 | purpose | 0.256 | 0.001 | 0.256 | 0.309 |
| 7 | peoplePresent | 0.256 | 0.001 | 0.256 | 0.309 |
| 8 | status | 0.256 | 0.030 | 0.256 | 0.000 |
| 9 | meetingVideoLink | 0.233 | 0.000 | 0.234 | 0.290 |
| 10 | tags | 0.209 | 0.000 | 0.209 | 0.000 |

## Clustering (Field Co-occurrence Graph)
- Average Clustering Coefficient: 0.882

### Top Nodes by Clustering Coefficient
| Rank | Field | Clustering |
|------|-------|------------|
| 1 | tags | 1.000 |
| 2 | workgroup_id | 1.000 |
| 3 | meetingInfo | 1.000 |
| 4 | workgroup | 1.000 |
| 5 | noSummaryGiven | 1.000 |
| 6 | canceledSummary | 1.000 |
| 7 | type | 1.000 |
| 8 | agendaItems | 1.000 |
| 9 | timestampedVideo | 1.000 |
| 10 | assignee | 1.000 |

## Connected Components (Field Co-occurrence Graph)
- Number of Components: 6
- Component Sizes (top 10): [12, 12, 10, 4, 4, 2]
- Sample of Largest Component Nodes (top 10):
  - typeOfMeeting
  - host
  - mediaLink
  - documenter
  - workingDocs
  - purpose
  - peoplePresent
  - miroBoardLink
  - otherMediaLink
  - date

