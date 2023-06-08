from unittest import TestCase

from app import app, db
from models import User, Post, Tag, PostTag

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
        
        PostTag.query.delete()
        Post.query.delete()
        User.query.delete()
        Tag.query.delete()

        user = User(first_name="Test", last_name="User", image_url="https://img.freepik.com/free-icon/user_318-563642.jpg")
        db.session.add(user)
        db.session.commit()

        post = Post(title="Test Post", content="Test Content", created_by=user.id)
        db.session.add(post)
        db.session.commit()

        tag1 = Tag(name="Tag1")
        tag2 = Tag(name="Tag2")
        db.session.add(tag1)
        db.session.add(tag2)
        db.session.commit()

        post_tag = PostTag(post_id=post.id, tag_id=tag1.id)
        db.session.add(post_tag)
        db.session.commit()

        self.user_id = user.id
        self.post_id = post.id
        self.tag1_id = tag1.id
        self.tag2_id = tag2.id
        self.post_tag_post_id = post_tag.post_id
        self.post_tag_tag_id = post_tag.tag_id


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

    def test_posts_new(self):
        """Tests the posts new route"""
        with self.app.test_client() as client:
            d = {"title": "New Test Post", "content": "New Test Content"}
            resp = client.post(f"/users/{self.user_id}/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('New Test Post', html)

    def test_posts_show(self):
        """Tests the posts show route"""
        with self.app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Test Post</h1>', html)

    def test_posts_edit(self):
        """Tests the posts edit route"""
        with self.app.test_client() as client:
            d = {"title": "Updated Test Post", "content": "Updated Test Content"}
            resp = client.post(f"/posts/{self.post_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Updated Test Post', html)

    def test_posts_delete(self):
        """Tests the posts delete route"""
        with self.app.test_client() as client:
            resp = client.post(f"/posts/{self.post_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Test Post', html)

    def test_tags_index(self):
        """Tests the tags index route"""
        with self.app.test_client() as client:
            resp = client.get("/tags")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Tag1', html)
            self.assertIn('Tag2', html)

    def test_tags_new(self):
        """Tests the tags new route"""
        with self.app.test_client() as client:
            d = {"name": "Tag3"}
            resp = client.post("/tags/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Tag3', html)

    def test_tags_show(self):
        """Tests the tags show route"""
        with self.app.test_client() as client:
            resp = client.get(f"/tags/{self.tag1_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Tag1', html)

    def test_tags_edit(self):
        """Tests the tags edit route"""
        with self.app.test_client() as client:
            d = {"name": "Updated Tag1"}
            resp = client.post(f"/tags/{self.tag1_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Updated Tag1', html)

    def test_tags_delete(self):
        """Tests the tags delete route"""
        with self.app.test_client() as client:
            resp = client.post(f"/tags/{self.tag1_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Updated Tag1', html)

  






    
