# Airnology 2026 Data Quality Report

## 1. Overview

This report documents the initial data quality assessment of Airnology 2026 operational data.

The assessment focuses on data completeness, uniqueness, consistency, validity, referential integrity, and traceability.

## 2. Dataset Summary

| Data Entity | Records |
|---|---:|
| Registration | 77 |
| Team | 67 |
| Participant | 171 |
| Team Member | 174 |
| Submission | 5 |
| Assessment | 45 |
| Ranking | 5 |

## 3. Data Quality Findings

### 3.1 Completeness

Several registration fields are conditional based on the competition selected by participants. Therefore, NULL values in conditional fields should not automatically be classified as missing data.

### 3.2 Uniqueness

There are 10 teams with more than one registration version.

Repeated registration records are not automatically treated as duplicates because participants may resubmit their registration to correct previous information.

The database preserves these records through registration versioning.

### 3.3 Consistency

Variations were identified in the formatting of team names, institution names, and WhatsApp numbers across registration records.

Normalization is required before performing exact-match joins between datasets.

### 3.4 Validity

An anomalous registration record was identified containing placeholder-like values.

The original record is preserved in the raw dataset, while the record is excluded from operational participant processing.

### 3.5 Referential Integrity

The database uses relational identifiers such as:

- team_id
- participant_id
- submission_id
- competition_id
- criterion_id

These identifiers connect operational entities and reduce dependency on manually matching names.

### 3.6 Traceability

Registration revisions are represented using:

- version
- is_latest
- supersedes_registration_id
- revision_reason

This allows historical registration records to be retained while identifying the latest version.

### 3.7 Assessment Auditability

Assessment data is stored at criterion level rather than only storing the final score.

For ECC, 5 submissions were assessed using 9 criteria each, resulting in 45 assessment records.

## 4. Governance Implications

The findings indicate the need for:

1. Standardized naming and formatting rules.
2. Stable identifiers for teams and participants.
3. Explicit registration versioning.
4. Defined data ownership and stewardship.
5. Standardized metadata and data dictionary.
6. Controlled access to confidential and restricted data.
7. Clear lineage between registration, submission, assessment, and ranking.

## 5. Overall Assessment

The current data can support operational analysis, but additional standardization and governance controls are required to improve consistency, traceability, and long-term maintainability.