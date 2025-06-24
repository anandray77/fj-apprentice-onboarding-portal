# Fujitsu Apprentice Onboarding Portal

A lightweight Flask web application designed to support apprentices during their onboarding experience at Fujitsu. The portal offers tailored features for both apprentices and administrators, delivering a role-specific, intuitive onboarding experience.

---

## Features

### For Apprentices
- Register, log in, and manage personal notes
- Access a personalised onboarding checklist
- Track document uploads, application progress, and key dates

### For Admins
- View and manage all registered users
- View notes submitted by all apprentices
- Register new admin accounts
- Access system-wide metrics (e.g. total users, notes)

---

## Tech Stack

- **Backend:** Python 3 + Flask
- **Frontend:** HTML, Jinja2, Bootstrap 5
- **Database:** SQLite (SQLAlchemy ORM)
- **Forms:** WTForms
- **Testing:** `unittest`, `coverage`
- **Containerisation:** Docker
- **Version Control:** Git + GitHub

---

## Project Structure

```
fj-apprentice-onboarding-portal/
├── simple_app/
│   ├── __init__.py
│   ├── auth.py
│   ├── forms.py
│   ├── models.py
│   ├── routes.py
│   ├── templates/
│   └── static/
├── tests/
├── requirements.txt
├── Dockerfile
├── README.md
├── app.py
├── .flaskenv
├── .gitignore
└── database.db
```

---

## Setup Instructions

### Local Setup (Python)

```bash
# 1. Clone the repo
git clone https://github.com/anandray77/fj-apprentice-onboarding-portal
cd fj-apprentice-onboarding-portal

# 2. Create Virtual Environment
python -m venv venv
venv\Scripts\activate     # Windows

# 3. Install Dependencies
pip install -r requirements.txt

# 4. Run the App
flask run
# Visit: http://localhost:5000
```

### Docker Setup

# Build Docker Image
docker build -t fj-portal .

# Run Container
docker run -p 5000:5000 fj-portal
# App will be live at: http://localhost:5000
```

---

## Testing & Coverage

# Run all unit tests
python -m unittest discover tests

# Check test coverage
coverage run -m unittest discover tests
coverage report
```

**Coverage Summary:**

```
simple_app/__init__.py      100%
simple_app/forms.py         100%
simple_app/models.py         90%
simple_app/routes.py         42%
tests/test_basic.py          97%
tests/test_routes.py        100%
TOTAL                        64%
```

---

## Secure Coding Practices

- Password hashing with `werkzeug.security` (`pbkdf2:sha256`)
- Form validation using WTForms
- Role-based access control (Admin vs User)
- CSRF protection
- Flash messages and user feedback

---

## 🔍 Example Accounts

**Admin:**
- Email: `MacRzepa@fujitsu.com`
- Password: `Abigail123!`

**User:**
- Email: `JennyDoeAspiringApprentice@hotmail.com`
- Password: `Abigail123!`

---

## License & Acknowledgements

**License:** Academic use only

**Acknowledgements:**  
Thanks to Fujitsu UK for providing the context and brief for this final-year university project. Built with ❤️ using Flask, Bootstrap, and lots of coffee.
