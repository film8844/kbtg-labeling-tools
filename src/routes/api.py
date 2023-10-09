from flask import Blueprint, jsonify,request,send_from_directory
from models import User, Project ,Task,serialize
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from random import randint
from app import db
import shutil
import glob
import os
from utils.export import write_to_yolo_format,create_classes_txt
import zipfile
router = Blueprint('api', __name__)

@router.route('/api/projects', methods=['GET'])
def projects():
    query = serialize(Project.query.filter_by(creator_id=current_user.id).all())
    projects = []
    
    for i in query:
        all_task = Task.query.filter(Task.project_id == i['id']).all()
        if len(all_task) != 0:
            task = Task.query.filter(Task.project_id == i['id'],Task.finished ==True).all()
            i['progress'] = (len(task)/len(all_task))*100
            i['tasks_all'] = len(all_task)
            i['tasks_finished'] = len(task)
            print(i['tasks_all'],i['tasks_finished'])
        projects.append(i)
    return jsonify(projects[::-1])

@router.route('/api/projects/<id>', methods=['GET'])
def project(int: id):
    query = Project.query.filter_by(id=id).first()
    if query is None:
        return "error", 404
    Task = Task.query.filter_by(project_id = id).all()
    projects = []
    for i in query:
        i['progress'] = randint(0,100)
        projects.append(i)
    return jsonify(projects[::-1])

@router.route('/api/projects/<id>/del', methods=['DELETE'])
def delete(id):
    query = Project.query.filter_by(id=int(id)).first()
    images = Task.query.filter_by(project_id = id).all()
    projects = []
    for i in images:
        db.session.delete(i)
    db.session.commit()
    shutil.rmtree(f"static/images/{id}")
    db.session.delete(query)
    db.session.commit()
    return jsonify(projects)

@router.route('/api/projects/<id>/export', methods=['POST'])
def export(id):
    data = request.form
    format = data['format']
    query = Project.query.filter_by(id=int(id)).first()
    if query is None:
        return "error", 404
    images = Task.query.filter_by(project_id = id).all()
    images = [image.to_dict() for image in images]

    os.makedirs('tmp',exist_ok=True)
    os.makedirs('tmp/images',exist_ok=True)
    os.makedirs('tmp/annotation',exist_ok=True)

    if format == "yolo":
        for image in images:
            shutil.copy(os.path.join(image['path']), 'tmp/images')
            name = os.path.basename(os.path.join(image['path'])).split('.')[0]
            write_to_yolo_format(image['label'],f'tmp/annotation/{name}.txt')
        create_classes_txt(query.labels_info['classname'],'tmp/classes.txt')
    else:
        return {"status": "error"}
    
    os.makedirs('export_file',exist_ok=True)
    zipname = f"{format}-{query.name.replace(' ','_')}.zip"
    with zipfile.ZipFile(os.path.join('export_file',zipname), 'w') as zipf:
        for foldername, subfolders, filenames in os.walk('tmp'):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                zipf.write(file_path, os.path.relpath(file_path, 'tmp'))

    shutil.rmtree('tmp')

    return send_from_directory(directory='export_file',path=zipname, as_attachment=True)

@router.route('/api/task/<id>', methods=['POST'])
def update_task(id):
    task = Task.query.get(id)
    if not task:
        return {"message": "Task not found"}, 404
    
    data = request.get_json()
    
    if "label" not in data:
        return {"message": "Label field is required"}, 400
    
    task.label = data["label"]
    task.label_by = data.get("label_by")  # Optional, remove this line if you don't want to update the label_by field
    try:
        task.finished = data["finished"]
    except:
        pass
    db.session.commit()
    
    return task.to_dict(), 200

@router.route('/api/task/<id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    if not task:
        return {"message": "Task not found"}, 404
    
    print(task.label)
    
    return jsonify(task.label), 200
