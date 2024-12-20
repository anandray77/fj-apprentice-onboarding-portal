Description:
The IT Asset Management System is a web application designed to manage and track IT assets efficiently. It allows Admin users to perform CRUD (Create, Read, Update, Delete) operations on assets and users, while Regular users can view and update assets assigned to them.

Features:
Role-Based Access Control - Admin: Full control over users and assets. User: Restricted to viewing and updating their assigned assets.
Authentication - User login and registration with role-based navigation.
CRUD Operations: Manage users and IT assets.
Dashboard - Admin: Overview of total users and assets. User: Personalised view of assigned assets.
Validation - Prevent invalid data submissions.
Confirmation Dialogs - User confirmation before logging out or deleting records.

Technologies Used
Framework: Flask (Python)
Database: MySQL
Frontend: HTML, CSS (Bootstrap for styling)
Tools: SQLAlchemy ORM for database management

Installation and Setup
Requirements
Python 3.8+
MySQL Server
Virtual Environment (optional)
I

Installation Steps

----------------------------------------------

Create a virtual environment:
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt
Configure the database:

Create a MySQL database:

CREATE DATABASE it_asset_management;

Update the SQLALCHEMY_DATABASE_URI in __init__.py:

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:<password>@localhost/it_asset_management'

Initialize the database:

flask shell
>>> from simple_app import db
>>> db.create_all()
>>> exit()

Run the application:

flask run

Open the application in your browser:

http://127.0.0.1:5000

----------------------------------------------------


Usage

Admin User:
Manage users and assets from the dashboard.
Add, edit, delete, and view all assets.
Assign assets to users.

Regular User:
View assigned assets.
Update details for their assets.


it-asset-management/
│
├── simple_app/
│   ├── __init__.py           # App initialization
│   ├── models.py             # Database models (Users, Assets)
│   ├── routes.py             # Application routes
│   ├── static/
│   │   └── style.css         # Custom CSS
│   ├── templates/
│   │   ├── base.html         # Base template
│   │   ├── index.html        # Homepage
│   │   ├── login.html        # Login page
│   │   ├── register.html     # Registration page
│   │   ├── assets.html       # View assets
│   │   └── add_asset.html    # Add new asset
│   └── ...
├── requirements.txt          # Dependencies
├── README.md                 # This file
└── ...

Database Testing:

Ensure assets and users are stored correctly.
Verify relationships between users and assets.

Functionality:

Test CRUD operations.
Test role-based navigation and permissions.

Error Handling:

Test invalid form submissions.
Confirm error messages display appropriately.

License
This project is licensed under the MIT License.