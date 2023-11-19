from flask import abort
from functools import wraps
from flask_login import current_user
from models import User, Project, Task,project_user,serialize

# This is a decorator that you can apply to your route functions
def require_project_permission():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            project_id = kwargs.get('id')  # Assuming the project ID is passed as a URL parameter
            
            # Replace 'Project' and 'project_user' with your actual models and relationship setup
            project = Project.query.get(project_id)
            if not project:
                abort(404, description='Project not found')

            # Check if the current user is the owner of the project
            if project.creator_id == current_user.id:
                return f(*args, **kwargs)

            # Check if the current user has the required permission on the project
            project_permission = project_user.query.filter_by(
                project_id=project_id,
                user_id=current_user.id
            ).first()

            if not project_permission:
                abort(403, description='You do not have permission to access this resource')
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def get_project_permission(id):
    project = Project.query.get(id)
    if project.creator_id == current_user.id:
        return 'labeler'

    project_permission = project_user.query.filter_by(
                project_id=id,
                user_id=current_user.id
            ).first()
    
    if not project_permission:
                abort(403, description='You do not have permission to access this resource')
    else:
        return project_permission.role

