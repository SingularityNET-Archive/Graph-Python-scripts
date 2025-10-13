# JSON Schema Report
**Generated on:** 2025-10-13 12:56:57

## Inferred Schema

- List of:
  - **workgroup**: `str`
  - **workgroup_id**: `str`
  - **meetingInfo**:
    - **typeOfMeeting**: `str`
    - **date**: `str`
    - **host**: `str`
    - **documenter**: `str`
    - **peoplePresent**: `str`
    - **purpose**: `str`
    - **meetingVideoLink**: `str`
    - **workingDocs**:
      - List of:
        - **title**: `str`
        - **link**: `str`
    - **timestampedVideo**:
  - **agendaItems**:
    - List of:
      - **status**: `str`
      - **actionItems**:
        - List of:
          - **text**: `str`
          - **assignee**: `str`
          - **dueDate**: `str`
          - **status**: `str`
      - **decisionItems**:
        - List of:
          - **decision**: `str`
          - **effect**: `str`
  - **tags**:
    - **topicsCovered**: `str`
    - **emotions**: `str`
  - **type**: `str`
  - **noSummaryGiven**: `bool`
  - **canceledSummary**: `bool`
