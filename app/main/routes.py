
from functools import wraps
from datetime import date
from flask import render_template, redirect, url_for, request, session, abort
from flask_login import current_user

from app import db
from app.main import bp
from app.main.email import send_email
from app.main.forms import CreatePostForm
from app.models import BlogPost

def _admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error.
        if current_user.id != 1:
            return abort(403)
        # Otherwise continue with the route function.
        return f(*args, **kwargs)
    
    return decorated_function

@bp.route('/')
def get_all_posts():
    # Query the database for all the posts. Convert the data to a Python list
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template('index.html', all_posts=posts, current_user=current_user)

@bp.route('/about')
def about():
    # Check if the user is authenticated.
    if not current_user.is_authenticated:
        # Store the requested URL in the session.
        session['next'] = request.path
        # Redirect to the login page.
        return redirect(url_for('auth.login'))
    # If the user is authenticated, render the about page.
    return render_template('about.html')

@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    # Check if the user is authenticated.
    if not current_user.is_authenticated:
        # Store the requested URL in the session.
        session['next'] = request.path
        # Redirect to the login page.
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        data = request.form
        send_email(data['name'], data['email'], data['message'])
        return render_template('contact.html', msg_sent=True)
    # If the user is authenticated, render the contact page.
    return render_template('contact.html')

@bp.route('/new-post', methods=['GET', 'POST'])
@_admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y"),
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('main.get_all_posts'))
    
    return render_template('make-post.html', form=form, current_user=current_user)

@bp.route('/delete/<int:post_id>')
@_admin_only
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('main.get_all_posts'))

@bp.route('/post/<int:post_id>')
def show_post(post_id):
    # Retrieve a BlogPost from the database based on the post_id.
    requested_post = db.get_or_404(BlogPost, post_id)
    return render_template('post.html', post=requested_post)

@bp.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
@_admin_only
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        body=post.body,
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for('main.show_post', post_id=post.id))
    
    return render_template('make-post.html', form=edit_form, is_edit=True)