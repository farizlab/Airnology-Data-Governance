# Airnology 2026 Data Classification & Access Control

## 1. Purpose

This document defines the proposed data classification and access control framework for Airnology 2026.

The framework is designed to reduce unauthorized access and ensure that sensitive data is only accessible to authorized roles.

---

## 2. Data Classification

The prototype uses four classification levels:

| Classification | Description |
|---|---|
| Public | Data that can be openly published |
| Internal | Data intended for internal committee use |
| Confidential | Data containing personal or participant information |
| Restricted | Highly sensitive data requiring limited access |

---

## 3. Data Classification by Domain

| Data Asset | Classification | Responsible Role |
|---|---|---|
| Competition Guidebook | Public | Lomba |
| Competition Information | Public | Lomba / Humas |
| Finalist Information | Internal → Public | Lomba / Sekretaris |
| Winner Information | Internal → Public | Lomba / Sekretaris |
| Participant Registration | Confidential | Lomba |
| Participant Contact Information | Confidential | Lomba |
| Participant Identity Documents | Confidential | Lomba |
| Committee Database | Confidential | Sekretaris |
| Committee Attendance | Confidential | Sekretaris |
| Timeline & Task Tracker | Internal | BPH / Sekretaris |
| Rundown | Internal | Acara |
| Sponsorship Tracker | Internal / Restricted | Sponsorship |
| Financial Records | Restricted | Bendahara |
| Fundraising Records | Restricted | Fundraising / Bendahara |
| Instagram Insights | Internal | Humas / Kreatif |
| Linktree Analytics | Internal | Humas |
| Assessment Scores | Internal | Lomba |
| Judge Information | Confidential | Lomba / Sekretaris |
| Database Prototype | Internal | BPH / Sekretaris |

---

## 4. Access Control Principles

Access should follow the principle of **least privilege**.

Users should only receive access to the data required for their responsibilities.

Example:

```text
BPH
 │
 ├── Governance / Oversight
 │
 ├── Sekretaris
 │     ├── Committee Data
 │     ├── Certificates
 │     └── Administrative Records
 │
 ├── Lomba
 │     ├── Registration
 │     ├── Submission
 │     └── Assessment
 │
 ├── Bendahara
 │     └── Financial Data
 │
 ├── Sponsorship
 │     └── Sponsor Data
 │
 ├── Humas / Kreatif
 │     └── Marketing & Analytics
 │
 └── Acara
       └── Event Operations