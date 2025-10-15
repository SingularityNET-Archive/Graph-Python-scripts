# JSON Field Degree Analysis Report
**Generated on:** 2025-10-14 13:29:12

## Summary Statistics
- Total Unique Fields: 44
- Maximum Degree: 11
- Minimum Degree: 1

## Top 15 JSON Fields by Degree
| Rank | Field Name | Degree |
|------|-------------|---------|
| 1 | typeOfMeeting | 11 |
| 2 | host | 11 |
| 3 | peoplePresent | 11 |
| 4 | date | 11 |
| 5 | purpose | 11 |
| 6 | workingDocs | 11 |
| 7 | documenter | 11 |
| 8 | status | 11 |
| 9 | meetingVideoLink | 10 |
| 10 | workgroup | 9 |
| 11 | workgroup_id | 9 |
| 12 | meetingInfo | 9 |
| 13 | noSummaryGiven | 9 |
| 14 | type | 9 |
| 15 | canceledSummary | 9 |

## Degree Distribution
| Degree | Count of Fields |
|---------|-----------------|
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

## Interpretation of Degree Results

The **degree** of a field represents how many other fields it co-occurs with across the dataset. Fields with high degree are more central — they tend to appear together with many other fields, indicating they may be *core schema components*. Fields with low degree are more isolated or specialized.

- **Average degree:** 6.77
- **Maximum degree:** 11
- **Minimum degree:** 1


### Core (Highly Connected) Fields

typeOfMeeting (11), host (11), peoplePresent (11), date (11), purpose (11), workingDocs (11), documenter (11), status (11)


### Peripheral (Low-Connectivity) Fields

rationale (3), topicsCovered (3), emotions (3), opposing (3), other (2), gamesPlayed (2), link (1), title (1)


_Interpretation:_

The core fields likely represent the fundamental metadata elements that occur in nearly every record (e.g., identifiers, titles, timestamps). The peripheral fields may represent optional or contextual data used only in specific cases or submodules of the schema.
