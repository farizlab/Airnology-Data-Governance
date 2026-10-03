# Airnology 2026 Data Management & Governance Framework

### A Data Management and Governance Prototype for Event Operations

---

## 1. Project Overview

Airnology 2026 generates operational data from multiple sources, including registration forms, submission files, assessment spreadsheets, operational trackers, and other event documents.

The data is distributed across different spreadsheets, forms, and documents. This creates challenges related to consistency, traceability, data ownership, access control, and integration.

This project develops a prototype Data Management & Governance Framework to organize and govern selected Airnology 2026 data.

The project focuses on:

- Data Management
- Data Quality
- Data Governance
- Data Integration
- Data Lineage
- Data Classification
- Access Control

---

## 2. Objectives

The project aims to:

1. Organize Airnology operational data into a structured relational database.
2. Establish consistent data definitions.
3. Preserve registration history and resubmissions.
4. Improve data traceability.
5. Identify data quality issues.
6. Define data ownership and stewardship.
7. Establish data classification and access control principles.
8. Demonstrate a governance-oriented data architecture using real event data.

---

## 3. Data Sources

The prototype uses selected Airnology 2026 operational datasets, including:

- Registration data
- Submission data
- Assessment data
- Certificate data
- Operational trackers
- Financial records
- Marketing analytics
- Event documentation

The current database integration focuses primarily on:

**Registration → Team → Submission → Assessment → Ranking**

---

## 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data processing and ETL |
| Pandas | Spreadsheet processing |
| SQLite | Relational database |
| SQL | Data modeling and querying |
| VS Code | Development environment |
| Excel | Original operational data source |
| Markdown | Documentation |

---

## 5. Project Structure

```text
Airnology-Data-Governance/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── database/
│   └── airnology.db
│
├── analysis/
│   ├── setup_database.py
│   ├── create_tables.py
│   ├── insert_master_data.py
│   ├── load_registration.py
│   ├── insert_participants.py
│   ├── insert_submissions.py
│   ├── insert_criteria.py
│   ├── insert_assessment_ecc.py
│   ├── insert_ranking_ecc.py
│   ├── data_quality_report.py
│   ├── visualize_data.py
│   └── sql_analysis.py
│
├── documentation/
│   ├── data_quality_report.md
│   ├── data_dictionary.md
│   ├── data_lineage.md
│   ├── data_classification_access_control.md
│   └── project_results.md
│
└── README.md