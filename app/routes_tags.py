from flask import Blueprint 
from flask import Flask, render_template, jsonify, request, session, url_for, redirect, abort, flash
from dotenv import load_dotenv

from models import User, Tag, PostTag
from models import db

tags_bp = Blueprint('tags', __name__, url_prefix='/tags')

@tags_bp.route('/')
def list_tags():
    tags = Tag.query.all()
    return render_template('3tags/list_tags.html', tags=tags)


@tags_bp.route('/new_tag')
def new_tag():
    return render_template('3tags/create_tag.html')

@tags_bp.route('/new_tag', methods=['POST'])
def create_tag():
    name = request.form['name']
    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()
    return redirect(url_for('tags.list_tags'))

@tags_bp.route('/<int:tag_id>')
def show_tag(tag_id):
    tag = Tag.query.get(tag_id)
    return render_template('3tags/show_tag.html', tag=tag)

@tags_bp.route('/<int:tag_id>/edit')
def edit_tag(tag_id):
    tag = Tag.query.get(tag_id)
    return render_template('3tags/edit_tag.html', tag=tag)

@tags_bp.route('/<int:tag_id>/edit', methods=['POST'])
def update_tag(tag_id):
    tag = Tag.query.get(tag_id)
    tag.name = request.form['name']
    db.session.commit()
    return redirect(url_for('tags.list_tags'))

@tags_bp.route('/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    tag = Tag.query.get(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect(url_for('tags.list_tags'))
