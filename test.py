from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import List, ListItem, Base

engine = create_engine('sqlite:///lists.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

lists = session.query(List).all()
print 'lists: \n'
for list in lists:
    print list
    for item in list.listitems:
        print item.check
#   session.delete(list)
#   session.commit()
print "-----####-----"
items = session.query(ListItem).all()
for item in items:
    print item.title, item.list_id