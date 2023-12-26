from pydoc import classname
from flask import (
    Blueprint,
    render_template,
    abort,
    request,
    redirect,
    flash,
    url_for,
    jsonify,
)
from werkzeug.utils import secure_filename
from models import User, Project, Task, project_user, serialize
from sqlalchemy import desc
from flask_login import (
    LoginManager,
    login_required,
    login_user,
    logout_user,
    current_user,
)
from utils.forms import ProjectForm
from app import db, UPLOAD_FOLDER
import os
from PIL import Image
from utils.colors import generate_colors
from utils.auth import require_project_permission, get_project_permission

router = Blueprint("main", __name__)


@router.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template("pages-error-404.html"), 404


@router.route("/")
@login_required
def home():
    form = ProjectForm()
    return render_template("projects.html", form=form)


@router.route("/project/<id>")
@login_required
@require_project_permission()
def project(id):
    project = Project.query.filter_by(id=id).first()
    # If no project is found for the given ID, abort with a 404 error.
    if project is None:
        abort(404)
    tasks = Task.query.filter_by(project_id=id).order_by(Task.id).all()
    owner = User.query.get(project.creator_id)
    users = (
        project_user.query.join(User, project_user.user_id == User.id)
        .add_columns(
            User.id,
            project_user.user_id,
            User.name,
            User.username,
            project_user.project_id,
            project_user.role,
        )
        .filter(project_user.project_id == id)
        .all()
    )
    all_user = User.query.all()
    return render_template(
        "annotation.html",
        project=project,
        tasks=tasks,
        users=users,
        owner=owner,
        all_user=all_user,
    )


@router.route("/task/<id>")
@login_required
def project_task(id):
    task = Task.query.filter_by(id=id).first()
    project = Project.query.filter_by(id=task.project_id).first()
    start = False
    end = False
    tasks = Task.query.filter_by(project_id=project.id).order_by(Task.id).all()
    all_tasks = sorted([i.to_dict()["id"] for i in tasks])
    print(all_tasks)
    print(id, all_tasks[0], all_tasks[-1])

    users = project_user.query.filter_by(project_id=project.id).all()
    users = serialize(users)

    permission = get_project_permission(project.id)
    print(permission)
    # return permission

    if int(id) == all_tasks[0]:
        start = True
    if int(id) == all_tasks[-1]:
        end = True
    print(start, end)
    if project.type == "det":
        if permission == "reviewer":
            return render_template(
                "object_detection_review.html",
                project=project,
                task=task,
                start=start,
                end=end,
            )
        return render_template(
            "object_detection.html",
            project=project,
            task=task,
            start=start,
            end=end,
            tasks=tasks,
        )
    elif project.type == "class":
        if permission == "reviewer":
            return render_template(
                "classification_review.html",
                project=project,
                task=task,
                start=start,
                end=end,
            )
        return render_template(
            "classification.html", project=project, task=task, start=start, end=end
        )


@router.route("/create_project", methods=["GET", "POST"])
@login_required
def create_project():
    form = ProjectForm()
    user_id = current_user.id
    print(user_id, form.name.data, form.type.data)
    if form.validate_on_submit():
        # return form.username.data+" "+form.password.data
        # Perform a query to find the user
        try:
            classes = form.labels.data
            classes = [
                number.strip() for number in classes.split("\n") if number.strip() != ""
            ]
            # return classes
            colors = generate_colors(len(classes))
            labels_info = {"classname": classes, "colors": colors}
            # print(labels_info)
            # return jsonify(labels_info)
            new_project = Project(
                name=form.name.data,
                type=form.type.data,
                creator_id=user_id,
                labels_info=labels_info,
            )
            db.session.add(new_project)
            db.session.commit()
            flash("New project has been created.", "success")
            return redirect(url_for("main.home"))
        except Exception as e:
            flash(f"Create Error. {str(e)}", "danger")
            print(f"Create Error. {str(e)}")
            return redirect(url_for("main.home"))
    return render_template("create_project.html", form=form)


@router.route("/upload/<id>")
@login_required
def project_upload(id):
    project = Project.query.filter_by(id=id).first()
    return render_template("upload.html", project=project)


@router.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        f = request.files.get("file")
        f.save(os.path.join(UPLOAD_FOLDER, f.filename))
    return jsonify({"status": "uploaded"})


@router.route("/upload_file/<project_id>", methods=["GET", "POST"])
def upload_file(project_id):
    if request.method == "POST":
        folder_path = os.path.join(UPLOAD_FOLDER, project_id)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        f = request.files.get("file")
        f.save(os.path.join(folder_path, f.filename))
        new_task = Task(
            path=os.path.join(folder_path, f.filename), project_id=project_id, label=[]
        )
        db.session.add(new_task)
        db.session.commit()
    return jsonify({"status": "uploaded"})


@router.route("/labeling/<id>")
@login_required
def labeling(id):
    print(id)
    project = Project.query.filter_by(id=id).first()
    start = False
    end = False
    all_tasks = Task.query.filter_by(project_id=project.id).all()
    all_tasks = sorted([i.to_dict()["id"] for i in all_tasks])

    permission = get_project_permission(project.id)
    print(permission)
    # return permission

    if int(id) == all_tasks[0]:
        start = True
    if int(id) == all_tasks[-1]:
        end = True
    print(start, end)
    if project.type == "det":
        if permission == "reviewer":
            return render_template(
                "object_detection_review.html",
                project=project,
                task=task,
                start=start,
                end=end,
            )
        return render_template(
            "object_detection_v2.html", project=project, tasks=all_tasks
        )
    elif project.type == "class":
        if permission == "reviewer":
            return render_template(
                "classification_review.html",
                project=project,
                task=task,
                start=start,
                end=end,
            )
        return render_template(
            "classification.html", project=project, task=task, start=start, end=end
        )
    return render_template("object_detection_v2.html")
