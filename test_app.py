from unittest import TestCase

from app import app, db
from models import User

def setup_app():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['TESTING'] = True
    app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

    with app.app_context():
        db.drop_all()
        db.create_all()

    return app

app = setup_app()

class BloglyTestCase(TestCase):
    """Tests Blogly app and routes"""

    @classmethod
    def setUpClass(cls):
        """Sets up Test class.
        
        Called once for the entire class. Initializes application 
        and test client to be used by all test instances.
        """
        cls.app = app
        cls.client = app.test_client()

    def setUp(self):
        """Sets up Test instance.
        
        Called before each test function is executed. Prepares a 
        new app context and adds a sample user in the database.
        """
        self.ctx = self.app.app_context()
        self.ctx.push()
        
        User.query.delete()
        user = User(first_name="Test", last_name="User", image_url="https://img.freepik.com/free-icon/user_318-563642.jpg")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Cleans up after Test instance.
        
        Called after each test function is executed. Rolls back 
        any fouled transactions and removes the app context.
        """
        db.session.rollback()
        self.ctx.pop()

    def test_users_index(self):
        """Tests the users index route"""
        with self.app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test User', html)

    def test_users_new(self):
        """Tests the users new route"""
        with self.app.test_client() as client:
            d = {"first_name": "Test2", "last_name": "User2", "image_url": "https://img.freepik.com/free-icon/user_318-563642.jpg"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test2 User2', html)

    def test_users_show(self):
        """Tests the users show route"""
        with self.app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Test User</h1>', html)

    def test_users_edit(self):
        """Tests the users edit route"""
        with self.app.test_client() as client:
            d = {"first_name": "UpdatedTest", "last_name": "User", "image_url": "https://img.freepik.com/free-icon/user_318-563642.jpg"}
            resp = client.post(f"/users/{self.user_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('UpdatedTest User', html)

    def test_users_delete(self):
        """Tests the users delete route"""
        with self.app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Test User', html)





    
