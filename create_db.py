from app import app
from models import List

print "APP_SETTINGS = " + app.config['APP_SETTINGS']
db.create_all()

db.session.add(List(title = 'Check List 1'))
db.session.add(List(title = 'Check List 2'))
db.session.add(List(title = 'Check List 3'))
db.session.add(List(title = 'Check List 4'))

db.session.commit()
