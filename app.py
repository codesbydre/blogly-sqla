"""Blogly application."""

from flask import Flask, render_template, request, redirect, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.config['SECRET_KEY'] = "secret123"
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def home():
    """Home route, redirects to users page"""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('home.html', posts=posts)

@app.route('/users')
def users_index():
    """Shows list of all users"""
    users = User.query.all()
    return render_template('user_list.html', users=users)

@app.route('/users/new', methods=['GET', 'POST'])
def users_new():
    """Add a new user"""
    if request.method == 'POST':
        user = User(
            first_name=request.form['first_name'], 
            last_name=request.form['last_name'], 
            image_url=request.form['image_url'] or None
        )
        db.session.add(user)
        db.session.commit()

        return redirect('/users')

    return render_template('new_user.html')

@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show details for a single user"""
    user = User.query.get_or_404(user_id)
    return render_template('user_detail.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def users_edit(user_id):
    """Show the edit page for a user and process the edit form"""
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.image_url = request.form['image_url'] or None
        db.session.commit()

        return redirect('/users')

    return render_template('user_edit.html', user=user)

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def users_delete(user_id):
    """Delete a user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new', methods=['GET', 'POST'])
def posts_new(user_id):
    """Create a new post for a user"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    if request.method == 'POST':
        post = Post(
            title=request.form['title'],
            content=request.form['content'],
            created_by=user_id
        )

        tag_ids = [int(num) for num in request.form.getlist("tags")]
        post.tags = [Tag.query.get(tag_id) for tag_id in tag_ids]

        db.session.add(post)
        db.session.commit()

        return redirect(f'/users/{user_id}')

    return render_template('post_form.html', user=user, tags=tags)

@app.route('/posts/<int:post_id>', methods=['GET'])
def posts_show(post_id):
    """Show a post"""
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
def posts_edit(post_id):
    """Edit a post"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']

        tag_ids = [int(num) for num in request.form.getlist("tags")]
        post.tags = [Tag.query.get(tag_id) for tag_id in tag_ids]

        db.session.commit()

        return redirect(f'/posts/{post_id}')

    return render_template('post_edit.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def posts_delete(post_id):
    """Delete a post"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.created_by}')

@app.route('/tags')
def tags_index():
    """Lists all tags, with links to the tag detail page."""
    tags = Tag.query.all()
    return render_template('tag_list.html', tags=tags)


@app.route('/tags/<int:tag_id>')
def tags_show(tag_id):
    """Show detail about a tag. Have links to edit form and to delete."""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_detail.html', tag=tag)


@app.route('/tags/new', methods=['GET', 'POST'])
def tags_new():
    """Shows a form to add a new tag and process add form."""
    if request.method == 'POST':
        name = request.form['name']
        new_tag = Tag(name=name)
        db.session.add(new_tag)
        db.session.commit()
        return redirect('/tags')

    return render_template('tag_form.html', edit_mode=False)


@app.route('/tags/<int:tag_id>/edit', methods=['GET', 'POST'])
def tags_edit(tag_id):
    """Show edit form for a tag and process edit form."""
    tag = Tag.query.get_or_404(tag_id)

    if request.method == 'POST':
        tag.name = request.form['name']
        db.session.commit()
        return redirect('/tags')

    return render_template('tag_form.html', tag=tag, edit_mode=True)


@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def tags_delete(tag_id):
    """Delete a tag."""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')