# import os
# import sys
# from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import create_engine

# Base = declarative_base()
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class List(db.Model):
    __tablename__ = 'list'

    title = db.Column(db.String(80), nullable=False, unique=True)
    id = db.Column(db.Integer, primary_key=True)

    listitems = db.relationship("ListItem", backref = 'list', cascade = 'all, delete-orphan', order_by="ListItem.title")

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

# engine = create_engine('sqlite:///lists.db')
# Base.metadata.create_all(engine)
