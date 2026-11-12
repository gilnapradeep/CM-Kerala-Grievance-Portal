# CM Kerala – Public Grievance Redressal Portal

A recruitment-prototype web application demonstrating citizen grievance submission, status tracking, role-based review, department assignment, officer action reports, citizen feedback and AI-assisted grievance analysis.

> **Prototype notice:** This is an independent recruitment/demo prototype. It is not an official Government of Kerala website or service. Use fictional demo data only.

## Technology
- Frontend: React, Vite, React Router, Axios
- Backend: Python, Django, Django REST Framework
- Database: PostgreSQL
- Authentication: JWT (Simple JWT)
- AI integration: Google GenAI API, with a clearly identified local fallback when the external service is unavailable
- File uploads: Django media storage

## Repository layout
```text
CM-Kerala-Grievance-Portal/
├── backend/
│   ├── config/
│   ├── accounts/
│   ├── grievances/
│   ├── departments/
│   ├── ai_assistant/
│   ├── contact/
│   ├── media/                 # local uploads; do not commit private uploads
│   ├── manage.py
│   └── .env                   # local secrets; never commit
├── frontend/
│   ├── src/
│   ├── package.json
│   └── .env                   # optional local frontend configuration
├── DOCUMENTATION/
└── README.md
```

## Local setup

### 1. PostgreSQL
Create a database and database user, then configure the backend environment variables in `backend/.env`.

### 2. Backend
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

If your project does not yet have a complete `requirements.txt`, install the packages already used by this project (Django, djangorestframework, django-cors-headers, psycopg[binary], Pillow, python-dotenv, djangorestframework-simplejwt and google-genai) and then generate the file:
```powershell
pip freeze > requirements.txt
```

### 3. Frontend
Open a second terminal:
```powershell
cd frontend
npm install
npm run dev
```
The frontend defaults to `http://127.0.0.1:8000/api`. To change it, set `VITE_API_BASE_URL` in `frontend/.env`.

## Roles
- `CITIZEN`: register, submit grievances, track grievances, view own grievance history and submit feedback after resolution.
- `CMO_ADMIN`: review grievances, view dashboard statistics, review AI recommendations, assign grievances and review officer action reports.
- `OFFICER`: view assigned grievances, update permitted statuses and submit action reports.

Role checks must be enforced by backend permissions; hiding frontend routes alone is not security.

## AI behaviour
AI-generated department/category/priority/summary values are suggestions, not official decisions. A CMO administrator must review recommendations. If the external AI service is unavailable, the application may use a local keyword-based fallback; the API response should identify the provider/fallback and explain that the result is preliminary.

## Important deployment checks
- Set `DEBUG=False` and a strong unique `SECRET_KEY`.
- Restrict `ALLOWED_HOSTS` and CORS origins to the deployed domains.
- Use HTTPS.
- Keep `.env`, database credentials, API keys, uploaded private files and real citizen information out of Git.
- Configure production static/media storage and database backups.
- Use only synthetic demo data for recruitment demonstrations.
- Test every API route and role with separate demo accounts before sharing the URL.

## Documentation
See `DOCUMENTATION/` for the project overview, architecture, database design, API notes, AI integration, setup/testing and user guide.
