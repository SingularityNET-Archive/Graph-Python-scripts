# JSON Field Clustering Coefficient Report
**Generated on:** 2025-10-15 08:51:41

- Total Fields (Nodes): 44
- Total Relationships (Edges): 149

## Local Clustering Coefficients (Top 10 Fields)
| Rank | Field | Clustering Coefficient |
|------|--------|-------------------------|
| 1 | text | 0.680 |
| 2 | assignee | 0.674 |
| 3 | dueDate | 0.652 |
| 4 | workgroup_id | 0.297 |
| 5 | meetingInfo | 0.297 |
| 6 | canceledSummary | 0.297 |
| 7 | type | 0.297 |
| 8 | noSummaryGiven | 0.297 |
| 9 | workgroup | 0.297 |
| 10 | agendaItems | 0.291 |

## Interpretation of Clustering Results

The clustering coefficient measures how likely a node’s neighbors are to also be connected to one another. High clustering suggests that related fields consistently appear together in the JSON structure, forming tightly interconnected groups.


### Global Measures
- **Average Clustering Coefficient:** 0.164
- **Network Transitivity:** 0.903


### Fields with Highest Local Clustering

text (0.680), assignee (0.674), dueDate (0.652), workgroup_id (0.297), meetingInfo (0.297)


_Interpretation:_
If the **average clustering coefficient** is high (e.g., >0.5), it indicates that many JSON fields co-occur frequently, forming cohesive 'themes' or substructures (like `participants` + `summary` + `workgroups`). A **low value** (e.g., <0.2) would suggest a more modular or fragmented structure, where fields are grouped into separate contexts. Fields with **high local clustering** serve as 'cluster cores' — they often appear in tight-knit groups, while those with low clustering tend to bridge distinct sections.
