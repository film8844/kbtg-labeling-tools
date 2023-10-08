from flask import Blueprint, jsonify,request
from models import User, Project ,Task,serialize
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from random import randint
from app import db
import shutil
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
