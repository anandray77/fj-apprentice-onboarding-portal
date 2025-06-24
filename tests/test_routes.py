import unittest
from flask import session
from simple_app import create_app, db
from simple_app.models import User, Asset
from werkzeug.security import generate_password_hash

class RouteTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            admin = User(
                email="admin@example.com",
                password=generate_password_hash("adminpass"),
                first_name="Admin",
                last_name="User",
                role="Admin"
            )
            user = User(
                email="user@example.com",
                password=generate_password_hash("userpass"),
                first_name="Regular",
                last_name="User",
                role="User"
            )
            db.session.add(admin)
            db.session.add(user)
            db.session.commit()
            self.admin_id = admin.id
            self.user_id = user.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def login(self, email, password):
        return self.client.post('/login', data=dict(email=email, password=password), follow_redirects=True)

    def test_login_valid_user(self):
        response = self.login('user@example.com', 'userpass')
        self.assertIn(b'Welcome, Regular', response.data)

    def test_login_invalid_user(self):
        response = self.login('invalid@example.com', 'wrongpass')
        self.assertIn(b'Invalid email or password!', response.data)

    def test_dashboard_requires_login(self):
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assertIn(b'You need to log in to access the dashboard.', response.data)

    def test_dashboard_user(self):
        self.login('user@example.com', 'userpass')
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assertIn(b'documents_uploaded', response.data.decode())

    def test_dashboard_admin(self):
        self.login('admin@example.com', 'adminpass')
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assertIn(b'total_users', response.data.decode())

    def test_add_note_user(self):
        self.login('user@example.com', 'userpass')
        response = self.client.post('/notes/add', data=dict(name='Note1', description='User note'), follow_redirects=True)
        self.assertIn(b'Note added successfully!', response.data)

    def test_view_notes_admin(self):
        self.login('admin@example.com', 'adminpass')
        response = self.client.get('/notes', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_view_notes_user(self):
        self.login('user@example.com', 'userpass')
        response = self.client.get('/notes', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.login('user@example.com', 'userpass')
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'Logged out successfully!', response.data)
