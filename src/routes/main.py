from flask import Blueprint, render_template, request, redirect, flash, url_for, jsonify
from werkzeug.utils import secure_filename
from models import User, Project
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from utils.forms import ProjectForm
from app import db, UPLOAD_FOLDER
import os

router = Blueprint('main', __name__)

@router.route('/')
@login_required
def home():
    all_projects = Project.query.filter_by(creator_id=current_user.id).all()
    return render_template('projects.html', projects=all_projects)

@router.route('/project/<id>')
@login_required
def project(id):
    project = Project.query.filter_by(id=id).first()
    return render_template('annotation.html', project=project)

@router.route('/create_project', methods=['GET', 'POST'])
@login_required
def create_project():
    form = ProjectForm()
    user_id = current_user.id
    print(user_id,form.name.data,form.type.data)
    if form.validate_on_submit():
        # return form.username.data+" "+form.password.data
        # Perform a query to find the user
        try:  
            new_project = Project(name=form.name.data, type=form.type.data, creator_id=user_id)
            db.session.add(new_project)
            db.session.commit()
            flash('New project has been created.', 'success')
            return redirect(url_for('main.home'))
        except Exception as e:
            flash(f'Create Error. {str(e)}', 'danger')
            print(f'Create Error. {str(e)}')
            return redirect(url_for('main.home'))
    return render_template('create_project.html', form=form)

@router.route('/upload_file/<project_id>', methods=['POST'])
def upload_file(project_id):
    project_path = os.path.join(UPLOAD_FOLDER, project_id)

    # Create project folder if it doesn't exist
    if not os.path.exists(project_path):
        os.makedirs(project_path)

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(project_path, filename)
        file.save(filepath)
        return jsonify({'success': 'File uploaded', 'filename': filename})

@router.route('/label')
@login_required
def labeling():
    return render_template('index.html')
