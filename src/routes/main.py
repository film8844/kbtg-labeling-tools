from flask import Blueprint, render_template, request, redirect, flash, url_for
from models import User, Project
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from utils.forms import ProjectForm
from app import db
router = Blueprint('main', __name__)

@router.route('/')
@login_required
def home():
    all_projects = Project.query.all()
    return render_template('index.html', projects=all_projects)

@router.route('/create_project', methods=['GET', 'POST'])
def create_project():
    if request.method == 'POST':
        name = request.form.get('name')
        type = request.form.get('type')

        # Validation (e.g., check if name or type already exists) can go here

        new_project = Project(name=name, type=type)
        db.session.add(new_project)
        db.session.commit()
        
        flash('New project has been created.', 'success')
        return redirect(url_for('main.index'))

    return render_template('create_project.html')

@router.route('/label')
@login_required
def labeling():
    return render_template('index.html')
