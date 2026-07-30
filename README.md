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

Authentication returns a JWT access token. Frontend authenticated requests
should send it as a Bearer token:

```javascript
fetch(url, {
    headers: {
        Authorization: `Bearer ${accessToken}`
    }
});
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
| POST | /surveys/share/{share_token}/responses |

---

## Email invitations

Creators can email a survey link to up to 20 recipients at once. Each
recipient receives a separate email, and replies go to the creator who sent it.

| Method | Endpoint |
|---------|----------|
| POST | /surveys/{id}/share/email |

```json
{
  "emails": ["person@example.com"]
}
```

### Frontend integration

The creator must be logged in. Use the `access_token` returned by
`POST /api/auth/login` as a Bearer token. Send one to 20 email addresses in
the `emails` array.

```javascript
const response = await fetch(
  `${API_BASE_URL}/api/surveys/${surveyId}/share/email`,
  {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`,
    },
    body: JSON.stringify({ emails: recipientEmails }),
  },
);

const result = await response.json();
```

On success, display `result.message` and use `result.data.sent_count` to tell
the creator how many invitations were sent. Show `result.message` as an error
when the request fails.

| Status | Frontend behavior |
|---------|-------------------|
| 200 | Show the sent count. |
| 400 | Ask the creator to correct the email addresses. |
| 403 | Hide this action for respondents; only survey owners may send invitations. |
| 404 | The survey does not exist or does not belong to the creator. |
| 502 | Show a temporary email-delivery error and allow retrying. |
| 503 | Email service configuration is unavailable. |

Do not put Brevo credentials in frontend code. The email is sent by the
backend, and the `SURVEY_SHARE_URL_TEMPLATE` determines the link included in
each invitation.

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


# SMTP provider settings (configure these in Render)
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-smtp-username
MAIL_PASSWORD=your-smtp-password
MAIL_DEFAULT_SENDER=noreply@yourdomain.com

# The public frontend route where a recipient completes a survey
SURVEY_SHARE_URL_TEMPLATE=https://your-frontend-domain.com/survey/{share_token}
```

Copy `.env.example` to `.env`, then replace the placeholder values. The `.env`
file is ignored by Git and is loaded automatically when the application starts.

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

Every authenticated request should include the login access token:

```javascript
fetch(url, {
    headers: {
        Authorization: `Bearer ${accessToken}`
    }
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
