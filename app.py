"""Blogly application."""

from flask import Flask, render_template, request, redirect, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

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
    """Home route, redirects to users page **UPDATE IN PART TWO**"""
    return redirect('users')

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