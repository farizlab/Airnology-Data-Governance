# Airnology 2026 Data Dictionary

## 1. Purpose

This data dictionary defines the main entities and attributes used in the Airnology 2026 Data Management & Governance prototype.

The dictionary provides a common reference for understanding the meaning and role of each data field.

---

## 2. Competition

| Field | Description |
|---|---|
| competition_id | Unique identifier for a competition |
| competition_name | Full name of the competition |
| competition_code | Short code used to identify the competition |
| description | Description of the competition |
| status | Current status of the competition |

---

## 3. Team

| Field | Description |
|---|---|
| team_id | Unique identifier for a team |
| team_name | Registered team name |
| competition_id | Competition selected by the team |
| institution_id | Identifier of the institution associated with the team |
| created_at | Timestamp when the team record was created |
| is_active | Indicates whether the team is active in operational data |

---

## 4. Participant

| Field | Description |
|---|---|
| participant_id | Unique identifier for a participant |
| full_name | Participant's full name |
| email | Participant email address |
| whatsapp | Participant WhatsApp number |
| institution | Participant's institution |
| faculty | Participant's faculty |
| study_program | Participant's study program |

---

## 5. Team Member

| Field | Description |
|---|---|
| team_member_id | Unique identifier for the team-member relationship |
| team_id | Identifier of the associated team |
| participant_id | Identifier of the associated participant |
| role | Participant's role within the team |
| joined_at | Timestamp when the participant joined the team |

---

## 6. Registration

| Field | Description |
|---|---|
| registration_id | Unique identifier for a registration record |
| team_id | Team associated with the registration |
| submitted_at | Registration submission timestamp |
| version | Registration version number |
| is_latest | Indicates whether the record is the latest registration version |
| supersedes_registration_id | Previous registration record replaced by the current version |
| revision_reason | Reason for registration revision |

### Important Business Rule

A resubmission is not automatically considered a duplicate.

Participants may submit a new registration to correct information from a previous submission. Previous versions are therefore retained for traceability.

---

## 7. Submission

| Field | Description |
|---|---|
| submission_id | Unique identifier for a submission |
| team_id | Team submitting the work |
| competition_id | Competition associated with the submission |
| submitted_at | Submission timestamp |
| work_file_url | Link to the submitted work |
| attachment_url | Link to supporting attachments |
| requirement_status | Administrative submission status |
| verification_notes | Notes related to requirement verification |

---

## 8. Judge

| Field | Description |
|---|---|
| judge_id | Unique identifier for a judge |
| judge_name | Judge's name |
| institution | Judge's institution |

---

## 9. Criterion

| Field | Description |
|---|---|
| criterion_id | Unique identifier for an assessment criterion |
| competition_id | Competition associated with the criterion |
| criterion_name | Name of the assessment criterion |
| weight | Weight assigned to the criterion |

---

## 10. Assessment

| Field | Description |
|---|---|
| assessment_id | Unique identifier for an assessment record |
| submission_id | Submission being assessed |
| judge_id | Judge associated with the assessment |
| criterion_id | Criterion used for the assessment |
| score | Score assigned to the submission |
| assessed_at | Assessment timestamp |

### Assessment Rule

Scores are stored at criterion level rather than only storing the final score. This allows the assessment result to be traced back to its individual scoring components.

---

## 11. Ranking

| Field | Description |
|---|---|
| ranking_id | Unique identifier for a ranking record |
| submission_id | Submission being ranked |
| final_score | Final calculated score |
| rank | Ranking position |
| result_status | Result classification associated with the ranking |

---

## 12. Key Relationships

```text
Competition
    │
    ├── Team
    │    │
    │    ├── Team Member ── Participant
    │    │
    │    └── Registration
    │
    └── Submission
             │
             └── Assessment ── Criterion
                       │
                       └── Judge

Submission
    │
    └── Ranking