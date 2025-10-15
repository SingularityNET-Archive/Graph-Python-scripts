# Unified Graph Analysis Report
**Generated on:** 2025-10-15 09:23:45

## Summary
- Co-attendance graph (nodes): 126
- Co-attendance graph (edges): 1848
- Path graph (nodes): 6833
- Path graph (edges): 6832
- Field graph (nodes): 44
- Field graph (edges): 149

## Degree (Co-attendance) Analysis
### Top Nodes by Degree
| Rank | Node | Degree |
|------|------|--------|
| 1 | AshleyDawn | 95 |
| 2 | PeterE | 91 |
| 3 | advanceameyaw | 87 |
| 4 | CallyFromAuron | 81 |
| 5 | Kateri | 81 |
| 6 | UKnowZork | 79 |
| 7 | Sucre n Spice | 78 |
| 8 | esewilliams | 76 |
| 9 | LordKizzy | 76 |
| 10 | Jeffrey Ndarake | 73 |

### Degree Distribution
| Degree | Count of Nodes |
|--------|-----------------|
| 4 | 1 |
| 6 | 2 |
| 8 | 4 |
| 9 | 6 |
| 10 | 6 |
| 11 | 8 |
| 12 | 5 |
| 13 | 17 |
| 15 | 2 |
| 16 | 5 |
| 17 | 4 |
| 18 | 2 |
| 19 | 3 |
| 20 | 4 |
| 21 | 4 |
| 23 | 2 |
| 24 | 1 |
| 26 | 2 |
| 27 | 2 |
| 29 | 1 |
| 30 | 3 |
| 31 | 1 |
| 33 | 1 |
| 34 | 2 |
| 35 | 1 |
| 36 | 2 |
| 40 | 1 |
| 43 | 2 |
| 44 | 1 |
| 45 | 1 |
| 46 | 3 |
| 47 | 1 |
| 48 | 1 |
| 49 | 1 |
| 51 | 1 |
| 57 | 1 |
| 58 | 1 |
| 60 | 1 |
| 62 | 4 |
| 63 | 1 |
| 65 | 1 |
| 66 | 1 |
| 71 | 2 |
| 72 | 1 |
| 73 | 1 |
| 76 | 2 |
| 78 | 1 |
| 79 | 1 |
| 81 | 2 |
| 87 | 1 |
| 91 | 1 |
| 95 | 1 |

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
| 1 | purpose | 0.256 | 0.001 | 0.256 | 0.309 |
| 2 | workingDocs | 0.256 | 0.001 | 0.256 | 0.309 |
| 3 | documenter | 0.256 | 0.001 | 0.256 | 0.309 |
| 4 | peoplePresent | 0.256 | 0.001 | 0.256 | 0.309 |
| 5 | date | 0.256 | 0.001 | 0.256 | 0.309 |
| 6 | typeOfMeeting | 0.256 | 0.001 | 0.256 | 0.309 |
| 7 | host | 0.256 | 0.001 | 0.256 | 0.309 |
| 8 | status | 0.256 | 0.030 | 0.256 | 0.000 |
| 9 | meetingVideoLink | 0.233 | 0.000 | 0.234 | 0.290 |
| 10 | tags | 0.209 | 0.000 | 0.209 | 0.000 |

## Clustering (Field Co-occurrence Graph)
- Average Clustering Coefficient: 0.882

### Top Nodes by Clustering Coefficient
| Rank | Field | Clustering |
|------|-------|------------|
| 1 | tags | 1.000 |
| 2 | workgroup | 1.000 |
| 3 | noSummaryGiven | 1.000 |
| 4 | workgroup_id | 1.000 |
| 5 | agendaItems | 1.000 |
| 6 | type | 1.000 |
| 7 | meetingInfo | 1.000 |
| 8 | canceledSummary | 1.000 |
| 9 | timestampedVideo | 1.000 |
| 10 | assignee | 1.000 |

## Connected Components (Field Co-occurrence Graph)
- Number of Components: 6
- Component Sizes (top 10): [12, 12, 10, 4, 4, 2]
- Sample of Largest Component Nodes (top 10):
  - meetingVideoLink
  - mediaLink
  - workingDocs
  - timestampedVideo
  - documenter
  - otherMediaLink
  - peoplePresent
  - date
  - miroBoardLink
  - host

