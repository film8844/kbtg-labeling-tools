from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import JSON
from app import db


class project_user(db.Model,UserMixin):
    __tablename__ = 'project_user'
    id = db.Column(db.Integer, primary_key=True)
    user_id= db.Column('project_id', db.Integer, db.ForeignKey('users.id'))
    project_id = db.Column('user_id', db.Integer, db.ForeignKey('projects.id'))
    role = db.Column('role', db.String(60))


    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    type = db.Column(db.String(120), unique=False, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    labels_info = db.Column(JSON, nullable=False)

    def list(self):
        return (self.id, self.name, self.username, self.type)
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(120), unique=False, nullable=False)
    label = db.Column(JSON)
    label_by = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=True)
    finished = db.Column(db.Boolean, default=False)
    approved = db.Column(db.Boolean, default=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    def list(self):
        return (self.id, self.name, self.username, self.type)
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

def serialize(tables):
    models = [model.to_dict() for model in tables]
    return models


if __name__ == '__main__':
    data = project_user.query.filter().all()
    print(data)