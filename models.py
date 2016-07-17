from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class List(db.Model):
    __tablename__ = 'list'

    title = db.Column(db.String(80), nullable=False, unique=False)
    id = db.Column(db.Integer, primary_key=True)

    listitems = db.relationship("ListItem", backref = 'list', cascade = 'all, delete-orphan', order_by="ListItem.title")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return "<List(title=%s)>" % self.title

class ListItem(db.Model):
    __tablename__ = 'list_item'

    title = db.Column(db.String(80), nullable=False)
    check = db.Column(db.Boolean, default = False)
    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'))


    def __repr__(self):
        return "<ListItem(title=%s)>" % self.title


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    pw_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=False)

    lists = db.relationship("List", backref='user', cascade = 'all, delete-orphan', order_by="List.title")

    # from http://flask.pocoo.org/snippets/54/
    def __init__(self, username, password, email):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def __repr__(self):
        return "<User(username=%s)>" % self.username

