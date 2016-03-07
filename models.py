import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class List(Base):
    __tablename__ = 'list'

    title = Column(String(80), nullable=False, unique=True)
    id = Column(Integer, primary_key=True)

    listitems = relationship("ListItem", backref = 'list', cascade = 'all, delete-orphan', order_by="ListItem.title")

    def __repr__(self):
        return "<List(title=%s)>" % self.title

class ListItem(Base):
    __tablename__ = 'list_item'

    title = Column(String(80), nullable=False)
    check = Column(Boolean, default = False)
    id = Column(Integer, primary_key=True)
    list_id = Column(Integer, ForeignKey('list.id'))


    def __repr__(self):
        return "<ListItem(title=%s)>" % self.title


engine = create_engine('sqlite:///lists.db')


Base.metadata.create_all(engine)
