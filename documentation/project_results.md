# Airnology 2026 — Project Results

## 1. Project Summary

This project developed a prototype Data Management & Governance Framework for Airnology 2026.

The project addresses the challenge of managing event data that is distributed across multiple spreadsheets, forms, trackers, and documents.

The prototype focuses on organizing selected operational data into a structured relational database while establishing supporting data governance practices.

---

## 2. Problem Statement

Airnology 2026 generates data across multiple operational activities, including:

- Participant registration
- Competition submissions
- Assessment
- Team management
- Event operations
- Finance
- Sponsorship
- Marketing

The data originates from different operational sources and may use different structures, naming conventions, and formats.

This creates several data management challenges:

- Inconsistent data structures
- Repeated registration records
- Naming inconsistencies
- Limited traceability between data sources
- Unclear data ownership
- Different levels of data sensitivity
- Difficulty integrating operational data

---

## 3. Project Approach

The project follows the following workflow:

```text
Raw Operational Data
        ↓
Data Profiling
        ↓
Data Cleaning & Normalization
        ↓
Relational Data Modeling
        ↓
SQLite Database
        ↓
Data Quality Assessment
        ↓
Data Lineage
        ↓
Data Classification
        ↓
Access Control
        ↓
SQL Analysis & Visualization