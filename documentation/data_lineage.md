# Airnology 2026 Data Lineage

## 1. Purpose

This document describes how Airnology 2026 data flows from its original sources into the operational database and how the data is transformed into assessment and ranking outputs.

The lineage helps establish traceability between source data, processed data, and derived results.

---

## 2. High-Level Data Flow

```text
RAW DATA SOURCES
      │
      ▼
Registration Data
      │
      ├── Data Cleaning
      ├── Competition Mapping
      ├── Team Identification
      └── Registration Versioning
      │
      ▼
TEAM + REGISTRATION
      │
      ▼
PARTICIPANT + TEAM MEMBER
      │
      ▼
SUBMISSION
      │
      ▼
ASSESSMENT
      │
      ├── Criterion
      └── Score
      │
      ▼
FINAL SCORE
      │
      ▼
RANKING