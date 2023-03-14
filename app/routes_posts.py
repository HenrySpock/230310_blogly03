from flask import Blueprint 
from flask import Flask, render_template, jsonify, request, session, url_for, redirect, abort, flash
from dotenv import load_dotenv

from models import Post, User, PostTag, Tag
from models import db

posts_bp = Blueprint('posts', __name__, url_prefix='/posts')

@posts_bp.route('/<int:user_id>/new')
def new_post_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('2posts/new_post.html', user=user)

# @posts_bp.route('/<int:user_id>/new', methods=['POST'])
# def new_post(user_id):
#     title = request.form.get('title')
#     content = request.form.get('content')
#     user = User.query.get_or_404(user_id)

#     if title:
#         post = Post(title=title, content=content, user=user)
#         db.session.add(post)
#         db.session.commit()
#         return redirect(url_for('users.show_user', user_id=user.id))
#     else:
#         return render_template('2posts/new_post.html', user=user, error="Title is required.")

@posts_bp.route('/<int:user_id>/new', methods=['POST'])
def new_post(user_id):
    title = request.form.get('title')
    content = request.form.get('content')
    tag_ids = request.form.getlist('tags')
    user = User.query.get_or_404(user_id)

    if title:
        post = Post(title=title, content=content, user=user)

        # Associate the post with tags
        for tag_id in tag_ids:
            tag = Tag.query.get(tag_id)
            if tag:
                post_tag = PostTag(post=post, tag=tag)
                db.session.add(post_tag)

        db.session.add(post)
        db.session.commit()
        return redirect(url_for('users.show_user', user_id=user.id))
    else:
        return render_template('2posts/new_post.html', user=user, error="Title is required.")


# @posts_bp.route('/<int:post_id>')
# def show_post(post_id):
#     post = Post.query.get_or_404(post_id)
#     return render_template('2posts/post.html', post=post)

@posts_bp.route('/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    tags = [post_tag.tag for post_tag in post.post_tags]
    return render_template('2posts/post.html', post=post, tags=tags)



# @posts_bp.route('/<int:post_id>/edit')
# def edit_post_form(post_id):
#     post = Post.query.get_or_404(post_id)
#     return render_template('2posts/edit_post.html', post=post)

# @posts_bp.route('/<int:post_id>/edit')
# def edit_post_form(post_id):
#     """Show the edit form for a post"""
#     post = Post.query.get_or_404(post_id)
#     tags = Tag.query.all()
#     return render_template('2posts/edit_post.html', post=post, tags=tags)

# @posts_bp.route('/<int:post_id>/edit', methods=['GET', 'POST'])
# def edit_post_form(post_id):
#     """Show the edit form for a post"""
#     post = Post.query.get_or_404(post_id)
#     tags = Tag.query.all()

#     # Get the selected tags for the post
#     post_tag_ids = set([post_tag.tag_id for post_tag in post.post_tags])

#     if request.method == 'POST':
#         # Handle form submission
#         title = request.form['title']
#         content = request.form['content']
#         tag_ids = request.form.getlist('tags')
#         errors = {}

#         if not title:
#             errors['title'] = 'Title is required.'

#         if not content:
#             errors['content'] = 'Content is required.'

#         if errors:
#             # Render the edit form with error messages
#             return render_template('2posts/edit_post.html', post=post, tags=tags, post_tag_ids=post_tag_ids, errors=errors)

#         # Update the post
#         post.title = title
#         post.content = content
#         post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

#         db.session.commit()

#         # Redirect to the post page
#         return redirect(url_for('posts.show_post', post_id=post.id))

#     # Return the edit form
#     return render_template('2posts/edit_post.html', post=post, tags=tags, post_tag_ids=post_tag_ids)

# @posts_bp.route('/<int:post_id>/edit', methods=['GET', 'POST'])
# def edit_post_form(post_id):
#     """Show the edit form for a post"""
#     post = Post.query.get_or_404(post_id)
#     tags = Tag.query.all()

#     # Get the selected tags for the post
#     post_tag_ids = set([post_tag.tag_id for post_tag in post.post_tags])

#     if request.method == 'POST':
#         # Handle form submission
#         title = request.form['title']
#         content = request.form['content']
#         tag_ids = request.form.getlist('tags')
#         errors = {}

#         if not title:
#             errors['title'] = 'Title is required.'

#         if not content:
#             errors['content'] = 'Content is required.'

#         if errors:
#             # Render the edit form with error messages
#             return render_template('2posts/edit_post.html', post=post, tags=tags, post_tag_ids=post_tag_ids, errors=errors)

#         # Update the post
#         post.title = title
#         post.content = content
#         post.post_tags = []

#         for tag_id in tag_ids:
#             post_tag = PostTag(post_id=post.id, tag_id=tag_id)
#             db.session.add(post_tag)

#         db.session.commit()

#         # Redirect to the post page
#         return redirect(url_for('posts.show_post', post_id=post.id))

#     # Return the edit form
#     return render_template('2posts/edit_post.html', post=post, tags=tags, post_tag_ids=post_tag_ids)

@posts_bp.route('/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post_form(post_id):
    """Show the edit form for a post"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    # Get the selected tags for the post
    post_tag_ids = set([post_tag.tag_id for post_tag in post.post_tags])

    if request.method == 'POST':
        # Handle form submission
        title = request.form['title']
        content = request.form['content']
        tag_ids = request.form.getlist('tags')
        errors = {}

        if not title:
            errors['title'] = 'Title is required.'

        if not content:
            errors['content'] = 'Content is required.'

        if errors:
            # Render the edit form with error messages
            return render_template('2posts/edit_post.html', post=post, tags=tags, post_tag_ids=post_tag_ids, errors=errors)

        # Update the post
        post.title = title
        post.content = content

        # Update the post tags
        post.post_tags = []
        for tag_id in tag_ids:
            tag = Tag.query.get(tag_id)
            if tag:
                post_tag = PostTag(post=post, tag=tag)
                db.session.add(post_tag)

        db.session.commit()

        # Redirect to the post page
        return redirect(url_for('posts.show_post', post_id=post.id))

    # Return the edit form
    return render_template('2posts/edit_post.html', post=post, tags=tags, post_tag_ids=post_tag_ids)


@posts_bp.route('/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)

    title = request.form.get('title')
    content = request.form.get('content')

    if title:
        post.title = title
        post.content = content
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts.show_post', post_id=post.id))
    else:
        return render_template('2posts/edit_post.html', post=post, error="Title is required.")

@posts_bp.route('/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('users.show_user', user_id=post.user_id))

