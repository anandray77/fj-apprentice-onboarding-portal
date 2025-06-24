Fujitsu Apprentice Onboarding Portal

A lightweight Flask web application designed to support apprentices during their onboarding experience at Fujitsu. This portal includes tailored features for both regular users and administrators, ensuring a clear, accessible, and role-specific experience.

Features:

For Apprentices -

Register, log in, and manage personal notes
Access your personal onboarding checklist
Track document uploads, important dates, and application progress


For Admins -

View and manage all registered users
View all apprentice notes
Register new admins
Access system-wide dashboard metrics (user count, note totals, etc.)

Tech Stack:

Backend: Python 3, Flask
Frontend: HTML, Jinja2 templating, Bootstrap 5
Database: SQLite3 (via SQLAlchemy)

Forms: WTForms

📁 Project Structure

├── app.py                 # Main app launcher
├── models.py              # SQLAlchemy models
├── forms.py               # WTForm classes
├── routes.py              # Main route logic
├── auth.py                # Authentication routes
├── templates/             # All Jinja2 HTML templates
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   └── ...
├── static/
│   └── style.css
├── requirements.txt
├── Procfile
├── .flaskenv
├── database.db            # SQLite DB

⚙️ Setup Instructions

1. Clone the Repo

git clone https://github.com/anandray77/fj-apprentice-onboarding-portal

cd fj-apprentice-onboarding-portal


2. Create Virtual Environment

python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

3. Install Requirements

pip install -r requirements.txt

4. Run the App

flask run

The app will be live at http://localhost:5000.


Example Accounts:

Admin -

Email: MacRzepa@fujitsu.com
Password: Abigail123!

User -

Email: JennyDoeAspiringApprentice@hotmail.com
Password: Abigail123!

Highlights:

Mobile-responsive layout
Role-based navigation and content
Flash messages for feedback
Commented and annotated template files

License:

This project is for academic demonstration purposes only.

Acknowledgements:
Thanks to Fujitsu UK for providing the context and challenge brief for this apprenticeship-ready portal. Built with ❤️ using Flask and Bootstrap.

