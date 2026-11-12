# 01 – Project Overview

## 1. Project title
**CM Kerala – Chief Minister's Public Grievance Redressal Portal** (recruitment prototype).

## 2. Problem statement
Citizens need a straightforward way to submit public-service grievances and follow their progress. Administrators need a consolidated view of submissions, while department officers need a way to review assigned cases and report action taken.

## 3. Objectives
1. Provide citizen registration and JWT-based login.
2. Capture grievance district, category, subject, description and optional supporting files.
3. Generate a unique grievance reference number.
4. Allow public reference-number tracking.
5. Provide citizen, CMO administrator and department officer workflows.
6. Maintain status history with timestamps and responsible users.
7. Support department assignment and officer action reports.
8. Provide dashboard statistics and filters where implemented.
9. Provide AI-assisted classification/priority/summary suggestions with human review.
10. Collect citizen feedback after resolution.

## 4. Scope and user roles

| Role | Main capabilities |
|---|---|
| Citizen | Register/login, submit grievance, upload permitted attachments, view own grievances, track by reference, view public history, submit post-resolution feedback |
| CMO administrator | View grievances and statistics, review AI suggestions, assign grievances, monitor action reports, approve/reject action reports |
| Department officer | View assigned grievances, update status with remarks, submit action report to CMO |
| Public visitor | View public information, use reference tracking, submit a contact enquiry |

## 5. Grievance lifecycle
The intended lifecycle uses these states:
- `SUBMITTED`
- `UNDER_REVIEW`
- `IN_PROGRESS`
- `RESOLVED`
- `REOPENED`

Every transition should be recorded with old status, new status, actor, remarks, visibility and timestamp. Public tracking must not expose internal remarks.

## 6. AI-assisted processing
The AI assistant analyses the grievance description and can suggest a department, category, priority and concise summary. Suggestions are preliminary and must be reviewed by an authorized CMO administrator. The system must not make autonomous official decisions. A local keyword fallback may be used when the external model service is unavailable and must be identified as a fallback.

## 7. Limitations and assumptions
- This is a recruitment prototype, not an official government service.
- Department and officer master data may be demo data.
- Production-grade identity verification, digital signatures, SLA policies, notification gateways, audit/compliance review and high-availability infrastructure are outside the demonstrated prototype unless separately implemented.
- Do not use real citizen personal data in the demo.
