# COS Group 6 Online Survey System

A web-based online survey system that allows users to create, distribute, complete, and analyze surveys.

## Project Overview

The system is designed to provide a simple and user-friendly platform where survey creators can:

* Create and manage surveys
* Add different types of questions
* Publish surveys
* Share surveys through public links and email
* Collect responses
* Analyze survey results using totals, percentages, averages where applicable, and charts

## Technology Stack

* Python
* Flask
* Jinja
* SQLite
* HTML
* CSS
* JavaScript

## Architecture

The project uses a modular hybrid Flask architecture.

* Flask handles application routes, backend logic, authentication, database operations, analytics, and email services.
* Jinja handles server-side rendering of HTML pages.
* HTML, CSS, and JavaScript handle the user interface and browser interactions.
* Selective JSON endpoints may be used where dynamic interactions are useful.
* SQLite stores application data.

The frontend and backend teams work within the same codebase.

## Core MVP Features

### Authentication

* Register
* Login
* Logout

### Survey Management

* Create survey
* Edit survey
* Delete survey
* Publish survey

### Question Types

* Short Answer
* Paragraph
* Multiple Choice
* Checkbox

### Response Collection

* Open public survey
* Submit answers
* Store responses
* Display thank-you page

### Survey Distribution

* Public shareable link
* Email invitation
* WhatsApp sharing link

### Analytics

* Total responses
* Multiple-choice percentages
* Averages where applicable
* Simple charts

## Project Structure

```text
cos-group-6-online-survey-system/
│
├── app/
│   ├── __init__.py
│   ├── templates/
│   └── static/
│       ├── css/
│       ├── js/
│       └── images/
│
├── tests/
├── .gitignore
├── requirements.txt
├── run.py
└── README.md
```

The structure will grow gradually as real modules are implemented.

## Local Development Setup

### 1. Clone the repository

```bash
git clone https://github.com/reelforged-inf/cos-group-6-online-survey-system.git
```

### 2. Enter the project directory

```bash
cd cos-group-6-online-survey-system
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

#### Git Bash

```bash
source .venv/Scripts/activate
```

#### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

After activation, the terminal should normally display:

```text
(.venv)
```

### 5. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Run the application

```bash
python run.py
```

### 7. Open the application

Open the local Flask address shown in the terminal, normally:

```text
http://127.0.0.1:5000
```

## Git Workflow

Do not develop new features directly on `main`.

Before starting a new task:

```bash
git switch main
git pull origin main
git switch -c feature/task-name
```

After completing work:

```bash
git status
git add .
git commit -m "feat: describe completed work"
git push -u origin feature/task-name
```

Then open a Pull Request for review before merging into `main`.

## Branch Naming Convention

Examples:

```text
feature/login-ui
feature/authentication
feature/survey-crud
feature/question-builder
feature/analytics

fix/login-error
fix/response-validation

docs/setup-guide

test/survey-submission
```

## Commit Message Convention

Use clear commit messages:

```text
feat: add creator login
fix: correct analytics percentage
docs: update local setup guide
test: add survey submission tests
chore: configure Flask application
refactor: reorganize survey routes
```

## Team Structure

* Frontend Team
* Backend Team
* Testing Team
* Documentation Team

## Project Information

**Project:** Online Survey System

**Group:** COS Group 6

**Department:** Information Systems

**Backend Lead:** Isuho Friday
