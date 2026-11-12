# 04 – API Documentation

## 1. Base URL
Local development: `http://127.0.0.1:8000/api`

All request and response bodies are JSON unless file upload is involved. Protected routes use:
`Authorization: Bearer <access_token>`

## 2. Authentication
| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/accounts/register/` | Register a citizen |
| POST | `/accounts/login/` | Obtain JWT access and refresh tokens |
| GET | `/accounts/profile/` | Get authenticated user's profile |

Registration fields used by the frontend: `username`, `password`, `first_name`, `last_name`, `email`, `mobile`.

## 3. Citizen grievance endpoints
| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/grievances/` | List authenticated citizen's grievances |
| POST | `/grievances/` | Submit grievance (multipart form when attaching files) |
| GET | `/grievances/<reference_number>/` | Retrieve grievance detail subject to backend permissions |
| GET | `/grievances/track/<reference_number>/` | Public reference-number tracking |
| POST | `/grievances/<reference_number>/feedback/` | Submit post-resolution feedback (requires implementation) |

Submission fields: `district`, `category`, `subject`, `description`, optional repeated `uploaded_files` parts.

## 4. CMO endpoints
| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/grievances/cmo/list/` | List grievances for CMO |
| GET | `/grievances/cmo/stats/` | Dashboard statistics |
| POST | `/grievances/cmo/<reference_number>/assign/` | Assign department/officer |
| PATCH/POST | `/grievances/cmo/<reference_number>/status/` | CMO status update; verify supported method |
| GET | `/grievances/cmo/action-reports/` | List officer action reports |
| POST | `/grievances/cmo/action-reports/<report_id>/review/` | Approve/reject report (requires implementation) |

Assignment payload expected by the supplied frontend:
```json
{
  "department_id": 1,
  "officer_id": 3,
  "remarks": "Please investigate and report the action taken."
}
```

Action-report review payload:
```json
{
  "approved": true,
  "remarks": "Reviewed."
}
```

## 5. Officer endpoints
| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/grievances/officer/list/` | List grievances assigned to authenticated officer |
| PATCH | `/grievances/officer/<reference_number>/status/` | Update grievance status with remarks |
| POST | `/grievances/officer/<reference_number>/action-report/` | Submit report to CMO |

Action report payload:
```json
{
  "investigation_details": "Inspection carried out.",
  "action_taken": "Necessary action initiated.",
  "resolution_details": "The reported issue has been addressed."
}
```

## 6. AI endpoints
| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/ai/analyze/<reference_number>/` | Generate preliminary AI suggestions |
| POST | `/ai/review/<reference_number>/` | CMO approves/rejects suggestions |

## 7. Contact endpoint
| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/contact/` | Public contact enquiry submission |

Contact payload:
```json
{
  "name": "Demo User",
  "email": "demo@example.com",
  "subject": "Portal enquiry",
  "message": "This is a fictional demonstration enquiry."
}
```

## 8. Important implementation note
This is a frontend-oriented endpoint inventory based on the project workflow. Before submission, compare every path, HTTP method, permission and payload with the current `urls.py`, views and serializers. Endpoints marked “requires implementation” must not be described as working until tested.
