# HexaSurvey Backend API

A RESTful backend for the **HexaSurvey Online Survey System**, developed as part of the **COS 121 (Information Systems)** group project.

The backend provides secure authentication, survey management, response collection, and analytics through a REST API built with **Flask**.

---

## Project Overview

HexaSurvey allows users to:

- Register as a Survey Creator or Respondent
- Create and publish surveys
- Share surveys using unique links
- Submit responses
- Prevent duplicate submissions
- View survey analytics

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3 |
| Framework | Flask |
| Database | SQLite |
| ORM | SQLAlchemy |
| Authentication | JWT (Flask-JWT-Extended) |
| Database Migration | Flask-Migrate |
| Password Hashing | Flask-Bcrypt |
| CORS | Flask-CORS |

---

# Project Structure

```
backend/
│
├── app/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── utils/
│   ├── extensions.py
│   ├── config.py
│   └── __init__.py
│
├── migrations/
├── instance/
├── run.py
├── requirements.txt
└── README.md
```

---

# Features

## Authentication

- User Registration
- User Login
- User Logout
- JWT Authentication
- Role-based Authorization

Supported roles

- Creator
- Respondent

---

## Survey Management

Creators can

- Create surveys
- View their surveys
- Update surveys
- Delete surveys
- Publish surveys

---

## Survey Builder

Supported question types

- Short Answer
- Paragraph
- Multiple Choice

Questions and options are submitted together when publishing the survey.

---

## Survey Sharing

Published surveys receive a unique share token.

Example

```
/api/surveys/share/ABCD1234
```

Only published surveys are accessible.

---

## Response Submission

Respondents can

- Open shared surveys
- Submit responses
- Submit only once per survey

---

## Analytics

Creators can view

- Total responses
- Response counts
- Percentages
- Chart-ready analytics

---

# API Base URL

Development

```
http://127.0.0.1:5000/api
```

Production

```
https://your-domain.com/api
```

---

# Authentication

Most endpoints require authentication.

Authentication uses **JWT stored in HTTP-only cookies**.

Frontend requests should include

```javascript
credentials: "include"
```

---

# API Endpoints

## Authentication

| Method | Endpoint |
|---------|----------|
| POST | /auth/register |
| POST | /auth/login |
| POST | /auth/logout |

---

## Surveys

| Method | Endpoint |
|---------|----------|
| GET | /surveys |
| POST | /surveys |
| GET | /surveys/{id} |
| PUT | /surveys/{id} |
| DELETE | /surveys/{id} |
| POST | /surveys/{id}/publish |

---

## Public Survey

| Method | Endpoint |
|---------|----------|
| GET | /surveys/share/{share_token} |

---

## Responses

| Method | Endpoint |
|---------|----------|
| POST | /surveys/share/{share_token}/submit |

---

## Analytics

| Method | Endpoint |
|---------|----------|
| GET | /surveys/{id}/analytics |

---

# Standard Success Response

```json
{
    "success": true,
    "message": "Operation completed successfully.",
    "data": {}
}
```

---

# Standard Error Response

```json
{
    "success": false,
    "message": "Validation failed."
}
```

---

# HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | OK |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict |
| 500 | Internal Server Error |

---

# Installation

Clone the repository

```bash
git clone <repository-url>
```

Move into the project

```bash
cd backend
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the virtual environment

Windows

```bash
.venv\\Scripts\\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file.

Example

```env
SECRET_KEY=your-secret-key

JWT_SECRET_KEY=your-jwt-secret

DATABASE_URL=sqlite:///instance/survey.db
```

---

# Database Migration

Initialize migrations

```bash
flask db init
```

Generate migration

```bash
flask db migrate -m "Initial migration"
```

Apply migration

```bash
flask db upgrade
```

---

# Running the Application

```bash
python run.py
```

The server starts at

```
http://127.0.0.1:5000
```

---

# Frontend Integration

Every authenticated request should include

```javascript
fetch(url, {
    credentials: "include"
});
```

The frontend communicates with the backend using JSON.

---

# Business Rules

- Only Creators can create or manage surveys.
- Only Respondents can submit survey responses.
- Only published surveys are accessible.
- A respondent can submit only one response per survey.
- Creators can only access surveys they own.
- Analytics are only available to the survey owner.

---

# Current Implementation Status

| Feature | Status |
|----------|--------|
| Authentication | ✅ |
| Survey CRUD | ✅ |
| Publish Survey | ✅ |
| Public Survey | ✅ |
| Submit Responses | ✅ |
| Duplicate Submission Prevention | ✅ |
| Analytics | ✅ |
| Email Distribution | 🚧 Planned |

---

# Future Improvements

- Email invitations
- Social media sharing
- CSV export
- PDF reports
- Dashboard statistics
- Advanced analytics
- Password reset

---

# Team

**Project:** COS 121 Online Survey System

**Department:** Information Systems

**Backend Lead:** Isuho Friday

---

# License

This project was developed for academic purposes as part of the COS 121 course.
