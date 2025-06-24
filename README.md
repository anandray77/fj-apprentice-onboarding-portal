# Fujitsu Apprentice Onboarding Portal

A lightweight Flask web application designed to support apprentices during their onboarding experience at Fujitsu. This portal includes tailored features for both regular users and administrators, ensuring a clear, accessible, and role-specific experience.

---

## Features

### For Apprentices
- Register, log in, and manage personal notes
- Access your personal onboarding checklist
- Track document uploads, important dates, and application progress

### For Admins
- View and manage all registered users
- View all apprentice notes
- Register new admins
- Access system-wide dashboard metrics (user count, note totals, etc.)

---

## Tech Stack

- **Backend**: Python 3, Flask
- **Frontend**: HTML, Jinja2 templating, Bootstrap 5
- **Database**: SQLite3 (via SQLAlchemy)
- **Forms**: WTForms
- **Testing**: `unittest`, `coverage`
- **Containerisation**: Docker
- **Source Control**: Git + GitHub

---

## Project Structure

├── simple_app/
│ ├── init.py # App factory and setup
│ ├── models.py # SQLAlchemy models
│ ├── forms.py # WTForm classes
│ ├── routes.py # Main route logic
│ ├── templates/ # Jinja2 HTML templates
│ ├── static/ # CSS files
│ └── database.db # SQLite DB
├── tests/ # Unit tests
├── requirements.txt
├── Dockerfile
├── .gitignore
├── README.md


---


## Setup Instructions


# 1. Clone the repo
git clone https://github.com/anandray77/fj-apprentice-onboarding-portal
cd fj-apprentice-onboarding-portal

# 2. Create Virtual Environment
python -m venv venv
venv\\Scripts\\activate   # (Windows)

# 3. Install Dependencies
pip install -r requirements.txt

# 4. Run the App
flask run
App will be live at http://localhost:5000

Docker Instructions

# Build the Docker image
docker build -t fj-portal .

# Run the app in a container
docker run -p 5000:5000 fj-portal
App accessible at http://localhost:5000 inside the container


Testing & Coverage

# Run all unit tests
python -m unittest discover tests

# Measure code coverage
coverage run -m unittest discover tests
coverage report
Test Coverage Report
matlab

simple_app/__init__.py      100%
simple_app/forms.py         100%
simple_app/models.py         90%
simple_app/routes.py         24%
TOTAL                        44%

Includes tests for:

Homepage accessibility
Login (valid and invalid credentials)
Note creation (by logged-in users)
Access denial (non-authenticated users)


Secure Coding & Academic Conventions

Passwords hashed with pbkdf2:sha256
Input validation with WTForms
Role-based access (User vs Admin)
Consistent naming, indentation, and modular design
Flash messages and user feedback with proper grammar

📸 Screenshots
Add screenshots of:

Homepage

Admin dashboard

User portal

Notes management

Docker CLI output


Example Accounts

Admin
Email: MacRzepa@fujitsu.com
Password: Abigail123!

User
Email: JennyDoeAspiringApprentice@hotmail.com
Password: Abigail123!

License
This project is for academic demonstration purposes only.

Acknowledgements
Thanks to Fujitsu UK for providing the context for this apprenticeship-ready portal. Built with ❤️ using Flask and Bootstrap.
