from app import app
from models import List

db.create_all()

db.session.add(List(title = 'Check List 1'))
db.session.add(List(title = 'Check List 2'))
db.session.add(List(title = 'Check List 3'))
db.session.add(List(title = 'Check List 4'))

db.session.commit()
