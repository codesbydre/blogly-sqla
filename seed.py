"""Seed file for sample data"""
from models import User, Post, Tag, PostTag, db
from app import app


with app.app_context():
    db.drop_all()
    db.create_all()
    User.query.delete()
    Post.query.delete()

    user1 = User(first_name='John', last_name='Smith', image_url='https://img.freepik.com/free-icon/user_318-563642.jpg')
    user2 = User(first_name='Jane', last_name='Doe', image_url='https://img.freepik.com/free-icon/user_318-563642.jpg')

    db.session.add_all([user1, user2])

    db.session.commit()

    post1 = Post(title='Hello World', content='This is the first post.', created_by=user1.id)
    post2 = Post(title='Another Post', content='This is another post.', created_by=user2.id)
    post3=  Post(title='Blah', content='Blahblahblah.', created_by=user1.id)

    db.session.add_all([post1, post2, post3])

    db.session.commit()

    tag1 = Tag(name='Random')
    tag2 = Tag(name='Fun')
    tag3 = Tag(name='Wow')
    tag4 = Tag(name='Cool')

    db.session.add_all([tag1, tag2, tag3, tag4])

    post_tag1 = PostTag(post_id=post1.id, tag_id=tag1.id)
    post_tag2 = PostTag(post_id=post2.id, tag_id=tag2.id)
    post_tag3 = PostTag(post_id=post3.id, tag_id=tag3.id)

    db.session.add_all([post_tag1, post_tag2, post_tag3])
    db.session.commit()