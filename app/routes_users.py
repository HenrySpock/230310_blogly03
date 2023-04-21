from flask import Blueprint 
from flask import Flask, render_template, jsonify, request, session, url_for, redirect, abort, flash
from dotenv import load_dotenv

from models import User
from models import db

users_bp = Blueprint('users', __name__)

@users_bp.route('/')
def home():
    return redirect('/users')

@users_bp.route('/users')
def list_users():
    users = User.query.all()
    return render_template('1users/list.html', users=users)

@users_bp.route('/users/new')
def new_user():
    return render_template('1users/create.html') 

@users_bp.route('/users/new', methods=['POST'])
def add_user():
    first_name = request.form['first_name'].strip() or "No"
    middle_name = request.form['middle_name'] or ""
    last_name = request.form['last_name'].strip() or "Name"
    image_url = request.form['image_url']
    new_user = User(first_name=first_name, middle_name=middle_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')

@users_bp.route('/users/<int:user_id>')
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('1users/details.html', user=user) 

@users_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.first_name = request.form['first_name']
        user.middle_name = request.form['middle_name']
        user.last_name = request.form['last_name']
        user.image_url = request.form['image_url']
        db.session.commit()
        flash(f"{user.first_name} {user.middle_name} {user.last_name} updated!")
        return redirect(url_for('users.show_user', user_id=user.id))
        
    return render_template('1users/edit.html', user=user)

@users_bp.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

