from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import List, ListItem, Base

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

# lists = session.query(List).all()
# print 'lists: \n'
# for list in lists:
#     print list.title
#     session.delete(list)
#
#
# list1 = List(title="Easter to-do list")
#
# session.add(list1)
# session.commit()
#
# listitem1 = ListItem(title="Cinema", list=list1, check=True)
# session.add(listitem1)
# session.commit()
#
# listitem1 = ListItem(title="Newstead Abbey", list=list1, check=False)
# session.add(listitem1)
# session.commit()
#
# listitem1 = ListItem(title="The Arboretum", list=list1, check=False)
# session.add(listitem1)
# session.commit()
#
# listitem1 = ListItem(title="Wollaton Hall", list=list1, check=False)
# session.add(listitem1)
# session.commit()
#
# listitem1 = ListItem(title="Nottingham Castle", list=list1, check=False)
# session.add(listitem1)
# session.commit()
#
# listitem1 = ListItem(title="Nottingham Caves", list=list1, check=False)
# session.add(listitem1)
# session.commit()
#
# listitem1 = ListItem(title="Nottingham Galleries", list=list1, check=False)
# session.add(listitem1)
# session.commit()
#
# listitem1 = ListItem(title="Old Market Square", list=list1, check=False)
# session.add(listitem1)
# session.commit()
#
# list2 = List(title="Alex's check list")
#
# session.add(list2)
# session.commit()
#
# listitem1 = ListItem(title="Possible wall charger", list=list2, check=False)
# session.add(listitem1)
# session.commit()
#
#
# listitem1 = ListItem(title="Phone + charger", list=list2, check=False)
# session.add(listitem1)
# session.commit()
#
# listitem1 = ListItem(title="Headphones", list=list2, check=False)
# session.add(listitem1)
# session.commit()
#
# listitem1 = ListItem(title="Shirts", list=list2, check=False)
# session.add(listitem1)
# session.commit()
#
# listitem1 = ListItem(title="Jeans", list=list2, check=False)
# session.add(listitem1)
# session.commit()

lists = session.query(List).all()
print 'lists: ---###---'
for list in lists:
    print list.title
    # session.delete(list)
    # session.commit()

print 'items: ---###---'
items = session.query(ListItem).all()
for item in items:
    print item.title, item.list_id
