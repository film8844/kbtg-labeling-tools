from flask import Blueprint, jsonify
from models import User, Project
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

router = Blueprint('api', __name__)

@router.route('/api/projects', methods=['GET'])
def api_projects():
    all_projects = Project.query.all()
    return jsonify([project.list() for project in all_projects])