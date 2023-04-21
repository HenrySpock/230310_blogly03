"""Blogly application."""
 
from flask import Flask, render_template, jsonify, request, session, url_for, redirect, abort, flash 
from dotenv import load_dotenv
from models import db, connect_db, User   
from routes_posts import posts_bp
from routes_users import users_bp 
from routes_tags import tags_bp 

load_dotenv('.flaskenv')

app = Flask(__name__, template_folder='../templates', static_folder='../static') 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bloglydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = "sesh_secr"

with app.app_context():
    connect_db(app)
    db.create_all()

app.register_blueprint(users_bp)
app.register_blueprint(posts_bp)
app.register_blueprint(tags_bp)

if __name__ == '__main__':
    app.run(debug=True)
 