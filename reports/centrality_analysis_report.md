# JSON Field Centrality Analysis Report
**Generated on:** 2025-10-15 08:28:29

- Total Fields: 44
- Total Relationships: 149

## Top 10 Fields by Centrality
| Rank | Field | Degree | Betweenness | Closeness | Eigenvector |
|------|--------|----------|--------------|-------------|-------------|
| 1 | documenter | 0.256 | 0.001 | 0.256 | 0.309 |
| 2 | date | 0.256 | 0.001 | 0.256 | 0.309 |
| 3 | peoplePresent | 0.256 | 0.001 | 0.256 | 0.309 |
| 4 | host | 0.256 | 0.001 | 0.256 | 0.309 |
| 5 | purpose | 0.256 | 0.001 | 0.256 | 0.309 |
| 6 | workingDocs | 0.256 | 0.001 | 0.256 | 0.309 |
| 7 | typeOfMeeting | 0.256 | 0.001 | 0.256 | 0.309 |
| 8 | status | 0.256 | 0.030 | 0.256 | 0.000 |
| 9 | meetingVideoLink | 0.233 | 0.000 | 0.234 | 0.290 |
| 10 | type | 0.209 | 0.000 | 0.209 | 0.000 |

## Interpretation of Centrality Results

Centrality measures identify the most structurally influential fields within the JSON schema. These indicate which fields are most central (high degree), which act as connectors (high betweenness), which can quickly reach others (high closeness), and which connect to other influential fields (high eigenvector).


### Most Connected Fields (Degree Centrality)
documenter (0.256), date (0.256), peoplePresent (0.256), host (0.256), purpose (0.256)


### Key Bridge Fields (Betweenness Centrality)
status (0.030), actionItems (0.003), decisionItems (0.003), discussionPoints (0.002), documenter (0.001)


### Most Accessible Fields (Closeness Centrality)
documenter (0.256), date (0.256), peoplePresent (0.256), host (0.256), purpose (0.256)


### Most Influential Fields (Eigenvector Centrality)
documenter (0.309), date (0.309), peoplePresent (0.309), host (0.309), purpose (0.309)


_Interpretation:_
Fields with **high degree** appear alongside many others — they are structurally core. Fields with **high betweenness** link otherwise separate parts of the schema and may represent connectors (e.g., ‘meeting’, ‘summary’, or ‘participants’). Fields with **high closeness** are well-distributed across the structure, suggesting they can reach or influence many others easily. Finally, fields with **high eigenvector centrality** are not only connected but connected to other important fields — these represent high-level schema hubs or critical integration points.
