from datetime import datetime as dt
from app import db
from flask_login import UserMixin
from app import login_manager
from werkzeug.security import check_password_hash, generate_password_hash

class Submit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    regarding = db.Column(db.String)
    explain = db.Column(db.Text)
    created = db.Column(db.DateTime, default=dt.utcnow)

    def from_dict(self, data):
        for field in ['email', 'regarding', 'explain']:
            if field in data:
                if field == 'email':
                    setattr(self, field, data[field].lower())
                else:
                    setattr(self, field, data[field])

    def to_dict(self):
        return {
            '_id': self.id,
            'email': self.email,
            'regarding':self.regarding,
            'explain': self.explain,
            'created': dt.strftime(self.created, '%m/%d/%Y')
        }

    def __repr__(self):
        return f'<Submit: [{self.email}]: {self.explain[:20]}...>'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=dt.utcnow)

    def save(self):
        self.set_password(self.password)
        db.session.add(self)
        db.session.commit()

    def set_password(self, pword):
        self.password = generate_password_hash(pword)

    def check_password(self, pword):
        return check_password_hash(self.password, pword)
        
    def from_dict(self,data):
        for field in ['first_name', 'last_name', 'email', 'password']:
            if field in data:
                if field == 'email':
                    setattr(self, field, data[field].lower())
                else:
                    setattr(self, field, data[field])
    def to_dict(self):
        return {
            '_id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password,
            'created': dt.strftime(self.created_on, '%m/%d/%Y')
        }

    def __repr__(self):
        return f'<User: [{self.email}]>'

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)   

class Post(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String)
    body=db.Column(db.Text)
    created= db.Column(db.DateTime, default=dt.utcnow)

    # def from_dict(self):
    #     pass

    def to_dict(self):
        return {
            '_id':self.id,
            'email':self.email,
            'body':self.title,
            'created':dt.strftime(self.created, '%m/%d/%Y')
        }

    def __repr__(self):
        return f'<Post: [{self.email}]: {self.body[:20]}...>'

