# 03 – Database Design

## 1. Overview
The database is relational and uses PostgreSQL. The Django models are the source of truth; confirm exact field names and constraints against the current migrations before treating this document as a schema dump.

## 2. Main entities

### User
Custom Django user extending `AbstractUser`.
- Standard username/password/name/email fields.
- `role`: `CITIZEN`, `CMO_ADMIN` or `OFFICER`.
- `mobile`: optional mobile number.

### Department
- `name`
- `code`
- `description`
- `is_active`
- `created_at`

### Grievance
- `reference_number` (unique public identifier)
- `citizen` (User relationship)
- `district`, `category`, `subject`, `description`
- `status`, `priority`
- `assigned_department`, `assigned_officer`
- AI suggestion fields: department, category, priority, summary, analysis JSON and review flag
- `internal_remarks`
- `created_at`, `updated_at`, `due_at`

### GrievanceHistory
- `grievance`
- `old_status`, `new_status`
- `changed_by`
- `remarks`
- `is_internal`
- `created_at`

### DepartmentAssignment
- `grievance`
- `department`
- `assigned_by`
- `assigned_officer`
- `remarks`
- `assigned_at`
- `is_active`

### Attachment
- `grievance`
- `file`
- `original_name`
- `uploaded_at`

### ActionTakenReport
- `grievance`
- `officer`
- `investigation_details`
- `action_taken`
- `resolution_details`
- `submitted_to_cmo`
- `submitted_at`

### CitizenFeedback
- `grievance` (one-to-one relationship)
- `rating`
- `comments`
- `created_at`

### ContactEnquiry
- `name`
- `email`
- `subject`
- `message`
- `created_at`

## 3. Entity relationship diagram
```mermaid
erDiagram
    USER ||--o{ GRIEVANCE : submits
    USER ||--o{ GRIEVANCE_HISTORY : changes
    USER ||--o{ DEPARTMENT_ASSIGNMENT : assigns
    USER ||--o{ ACTION_TAKEN_REPORT : submits
    DEPARTMENT ||--o{ GRIEVANCE : receives
    DEPARTMENT ||--o{ DEPARTMENT_ASSIGNMENT : handles
    GRIEVANCE ||--o{ GRIEVANCE_HISTORY : records
    GRIEVANCE ||--o{ DEPARTMENT_ASSIGNMENT : has
    GRIEVANCE ||--o{ ATTACHMENT : includes
    GRIEVANCE ||--o{ ACTION_TAKEN_REPORT : receives
    GRIEVANCE ||--o| CITIZEN_FEEDBACK : receives
    USER {
        int id PK
        string username
        string email
        string role
        string mobile
    }
    DEPARTMENT {
        int id PK
        string name
        string code
        boolean is_active
    }
    GRIEVANCE {
        int id PK
        string reference_number UK
        int citizen_id FK
        int assigned_department_id FK
        int assigned_officer_id FK
        string district
        string category
        string status
        string priority
        datetime created_at
    }
    GRIEVANCE_HISTORY {
        int id PK
        int grievance_id FK
        int changed_by_id FK
        string old_status
        string new_status
        boolean is_internal
        datetime created_at
    }
    DEPARTMENT_ASSIGNMENT {
        int id PK
        int grievance_id FK
        int department_id FK
        int assigned_by_id FK
        int assigned_officer_id FK
        datetime assigned_at
    }
    ATTACHMENT {
        int id PK
        int grievance_id FK
        string file
        string original_name
    }
    ACTION_TAKEN_REPORT {
        int id PK
        int grievance_id FK
        int officer_id FK
        boolean submitted_to_cmo
        datetime submitted_at
    }
    CITIZEN_FEEDBACK {
        int id PK
        int grievance_id FK
        int rating
        string comments
    }
    CONTACT_ENQUIRY {
        int id PK
        string name
        string email
        string subject
        datetime created_at
    }
```

## 4. Integrity and privacy
- Reference numbers must be unique.
- A citizen feedback record should be limited to one per grievance if the model uses a one-to-one relation.
- Feedback should only be accepted from the grievance's citizen after resolution.
- Citizen-facing history must exclude internal entries.
- Foreign-key deletion behaviour should be reviewed before production.
- Confirm exact nullability, indexes, ordering and `on_delete` behaviour from Django model definitions and migrations.
