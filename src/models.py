from datetime import datetime
from flask_login import UserMixin
from app import db


project_user = db.Table('project_user',
                    db.Column('project_id', db.Integer, db.ForeignKey('users.id')),
                    db.Column('user_id', db.Integer, db.ForeignKey('projects.id'))
                    )

class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def list(self):
        return (self.id, self.email, self.username, self.role)

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    type = db.Column(db.String(120), unique=True, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    member = db.relationship('User', secondary=project_user, backref='posts')

    def list(self):
        return (self.id, self.name, self.username, self.type)
    

