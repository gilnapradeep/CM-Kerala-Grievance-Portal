# 06 – Setup and Testing

## 1. Prerequisites
- Python 3.12 (or a version compatible with the pinned project dependencies)
- Node.js version supported by the installed Vite release
- PostgreSQL
- Git

## 2. Backend setup
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create `backend/.env` using `.env.example` as a template. Create the PostgreSQL database and set its credentials. Then:
```powershell
python manage.py migrate
python manage.py check
python manage.py runserver
```

## 3. Frontend setup
In another terminal:
```powershell
cd frontend
npm install
npm run dev
```
Set `VITE_API_BASE_URL=http://127.0.0.1:8000/api` in `frontend/.env` if required.

## 4. Functional test checklist
Use fictional data and separate accounts for each role.

### Public visitor
- [ ] Home page loads.
- [ ] About, How It Works, Departments, FAQ and Contact pages load.
- [ ] Contact enquiry is accepted and persisted.
- [ ] Tracking page handles an invalid reference safely.

### Citizen
- [ ] Citizen registration succeeds.
- [ ] Login returns tokens and profile role.
- [ ] Citizen can submit a grievance without an attachment.
- [ ] Citizen can submit a grievance with an allowed attachment.
- [ ] Unique reference number is returned.
- [ ] Citizen can only list/view their own grievances.
- [ ] Public tracking returns public history but not internal remarks.
- [ ] Feedback is accepted only after resolution and only once.

### CMO administrator
- [ ] CMO login and role protection work.
- [ ] Grievance list and dashboard statistics load.
- [ ] Filters work if implemented in the backend/frontend.
- [ ] AI analysis handles external API success and failure.
- [ ] AI provider/fallback is identifiable.
- [ ] AI recommendations require human approval.
- [ ] Assignment validates department and officer.
- [ ] CMO can view action reports.
- [ ] Approving/rejecting an action report records an auditable history entry.

### Department officer
- [ ] Officer login and role protection work.
- [ ] Officer sees only assigned grievances.
- [ ] Status updates record actor, timestamp and remarks.
- [ ] Officer can submit an action report.
- [ ] Officer cannot access CMO-only operations.

## 5. API smoke tests
Use Postman, Thunder Client or the Django browsable API. Verify status codes and response bodies. Do not paste access tokens, passwords, database passwords or API keys into screenshots or documentation.

## 6. Security checks
- [ ] `.env` is ignored by Git.
- [ ] `DEBUG=False` in production.
- [ ] `SECRET_KEY` is unique and private.
- [ ] `ALLOWED_HOSTS` and CORS origins are restricted.
- [ ] HTTPS is enabled in production.
- [ ] Upload size/type validation is active.
- [ ] Internal remarks and private files are protected.
- [ ] Role authorization is enforced server-side.

## 7. Final verification commands
```powershell
# Backend
python manage.py check
python manage.py showmigrations

# Frontend
npm run build
```
A successful build does not replace end-to-end API and role testing.
