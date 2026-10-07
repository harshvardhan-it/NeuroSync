# NeuroSync

NeuroSync is an AI-powered Decision Intelligence Platform that turns business datasets into insights, risk assessment, forecasts, recommendations, and executive decisions.

## Architecture

- Frontend: React + Vite + Tailwind
- Backend: FastAPI + SQLModel
- Database: SQLite locally / PostgreSQL (Neon) in production
- Analytics: Pandas, NumPy, scikit-learn
- Executive AI: Groq
- Reports: ReportLab

## Local development

### Backend

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt -r requirements-dev.txt
uvicorn backend.main:app --reload
```

Copy `backend/.env.example` to `backend/.env` and configure it.

### Frontend

```bash
cd frontend
npm ci
npm run dev
```

Copy `frontend/.env.example` to `frontend/.env`.

## Production configuration

### Backend (Render / Railway)

Required environment variables:

- `ENVIRONMENT=production`
- `SECRET_KEY` — long random secret, 32+ characters
- `DATABASE_URL` — PostgreSQL/Neon connection string
- `GROQ_API_KEY`
- `ALLOWED_ORIGINS` — comma-separated frontend origins
- `ACCESS_TOKEN_EXPIRE_MINUTES` — e.g. `60`
- `DEBUG=false`

### Frontend (Vercel)

- `VITE_API_URL=https://<your-backend-host>`

Do not put secrets in the frontend environment.

## Verification

Backend:

```bash
python -m compileall backend
pytest -q
```

Frontend:

```bash
cd frontend
npm ci
npm run lint
npm run build
```

CI runs the same verification through GitHub Actions.

## Data and storage notes

Uploaded datasets are stored locally for the current prototype. Local filesystem storage is not durable on ephemeral deployment platforms; object storage can be introduced later behind a storage abstraction without changing the analytics pipeline.

Never commit `.env`, databases, uploads, generated PDFs, virtual environments, or build artifacts.
