from flask import Blueprint, render_template, request, redirect, flash, url_for, jsonify
from werkzeug.utils import secure_filename
from models import User, Project, Task
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from utils.forms import ProjectForm
from app import db, UPLOAD_FOLDER
import os
from PIL import Image

router = Blueprint('main', __name__)

@router.route('/')
@login_required
def home():
    form = ProjectForm()
    return render_template('projects.html', form=form)

@router.route('/project/<id>')
@login_required
def project(id):
    project = Project.query.filter_by(id=id).first()
    tasks = Task.query.filter_by(project_id = id).all()
    return render_template('annotation.html', project=project,tasks=tasks)

@router.route('/task/<id>')
@login_required
def project_task(id):
    task = Task.query.filter_by(id=id).first()
    project = Project.query.filter_by(id = task.project_id).first()
    return render_template('object_detection.html', project=project, task=task)

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

@router.route('/upload/<id>')
@login_required
def project_upload(id):
    project = Project.query.filter_by(id=id).first()
    return render_template('upload.html', project=project)


@router.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(UPLOAD_FOLDER, f.filename))
    return jsonify({'status': 'uploaded'})

@router.route('/upload_file/<project_id>', methods=['GET', 'POST'])
def upload_file(project_id):
    if request.method == 'POST':
        folder_path = os.path.join(UPLOAD_FOLDER,project_id)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        f = request.files.get('file')
        f.save(os.path.join(folder_path, f.filename))
        new_task = Task(path=os.path.join(folder_path, f.filename), project_id=project_id,label=[])
        db.session.add(new_task)
        db.session.commit()
    return jsonify({'status': 'uploaded'})

@router.route('/label')
@login_required
def labeling():
    return render_template('index.html')
