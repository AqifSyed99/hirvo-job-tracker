# JobTracker

A web application for tracking job applications throughout the hiring process.

## Tech Stack

- **Frontend**: Vue 3 + Vite, Pinia, Vue Router, Chart.js
- **Backend**: Flask (Python), SQLAlchemy, Flask-CORS, PyJWT, bcrypt
- **Database**: Neon (PostgreSQL)
- **File Storage**: Cloudinary
- **AI (reserved)**: Groq API

## Project Structure

```
.
├── backend/          # Flask REST API
│   ├── app/          # Application package
│   │   ├── models/   # SQLAlchemy models
│   │   └── services/ # Business logic services
│   ├── tests/        # pytest test suite
│   ├── config.py     # Environment-based configuration
│   ├── run.py        # Development server entry point
│   └── requirements.txt
└── frontend/         # Vue 3 SPA
    ├── src/
    │   ├── views/        # Page-level components
    │   ├── components/   # Reusable UI components
    │   ├── store/        # Pinia stores
    │   ├── router/       # Vue Router configuration
    │   └── layouts/      # Layout wrappers
    ├── index.html
    └── package.json
```

## Setup

### Backend

1. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and fill in your values:
   ```bash
   cp .env.example .env
   ```

4. Run the development server:
   ```bash
   python run.py
   ```

### Frontend

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Run tests:
   ```bash
   npm test
   ```

## Environment Variables

### Backend (`backend/.env`)

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string (Neon) |
| `JWT_SECRET` | Secret key for signing JWTs |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary cloud name |
| `CLOUDINARY_API_KEY` | Cloudinary API key |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret |
| `GROQ_API_KEY` | Groq API key (reserved for future AI features) |

### Frontend (`frontend/.env`)

| Variable | Description |
|----------|-------------|
| `VITE_API_BASE_URL` | Base URL of the Flask API (default: `http://localhost:5000`) |
