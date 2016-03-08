from flask import Flask, render_template, request, redirect, url_for, session, flash, Response
from werkzeug.security import generate_password_hash, check_password_hash
from models import List, ListItem, db
from functools import wraps
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

db.init_app(app)

with app.app_context():
    db.create_all()

def check_auth(username, password):
    pw_hash = 'pbkdf2:sha1:1000$3fr9NOwx$cb6cbfded475f7b2a426f7d56eb199fc5d205418'

    return username == 'admin' and check_password_hash(pw_hash, password)
def authenticate():
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route('/')
@requires_auth
def index():
    lists = db.session.query(List).all()
    return render_template('index.html', lists=lists)


@app.route('/newlist', methods=['POST'])
@requires_auth
def newlist():
    if request.method == "POST":
        title = request.form['title']
        if title:
            newlist = List(title=title)
            db.session.add(newlist)
            db.session.commit()
            flash('Success! Added \'%s\'' % title, 'success')
            return redirect(url_for('index'))

    flash('An error occurred', 'danger')
    return redirect(url_for('index'))

@app.route('/new', methods=['POST'])
@requires_auth
def new():
    if request.method == 'POST':
        title = request.form['item']
        list_id = request.form['list-id']
        if title and list_id:
            list = db.session.query(List).filter_by(id = list_id).first()
            if list:
                newitem = ListItem(title=title, list_id = list.id)
                db.session.add(newitem)
                db.session.commit()
                flash('Success! Added \'%s\' to \'%s\'' % (title, list.title), 'success')
                return redirect(url_for('index'))


    flash('An error occurred', 'danger')
    return redirect(url_for('index'))


@app.route('/check', methods=['POST'])
@requires_auth
def check():
    if request.method == "POST":
        check = request.form['check']
        item_id = request.form['item-id']
        list_id = request.form['list-id']
        if id and list_id:
            list = db.session.query(List).filter_by(id = list_id).first()
            checkitem = db.session.query(ListItem).filter_by(list = list, id = item_id).first()
            if checkitem and list:
                if check == 'true':
                    checkitem.check = True
                else:
                    checkitem.check = False
                db.session.add(checkitem)
                db.session.commit()
                # flash('Success!', 'success')
                return redirect(url_for('index'))

    flash('An error occurred', 'danger')
    return redirect(url_for('index'))

@app.route('/deletelist', methods=['POST'])
@requires_auth
def deletelist():
    if request.method == "POST":
        id = request.form['list-id']
        if id:
            deletelist = db.session.query(List).filter_by(id=id).first()
            if deletelist:
                title = deletelist.title
                db.session.delete(deletelist)
                db.session.commit()
                flash('Success! Deleted \'%s\'' % title, 'success')
                return redirect(url_for('index'))
    flash('An error occurred', 'danger')
    return redirect(url_for('index'), alert=True)

@app.route('/delete', methods=['POST'])
@requires_auth
def delete():
    if request.method == "POST":
        item_id = request.form['item-id']
        list_id = request.form['list-id']
        if item_id and list_id:
            list = db.session.query(List).filter_by(id = list_id).first()
            deleteitem = db.session.query(ListItem).filter_by(list = list, id = item_id).first()
            if deleteitem and list:
                title = deleteitem.title
                db.session.delete(deleteitem)
                db.session.commit()
                flash('Success! Deleted \'%s\' from \'%s\'' % (title, list.title), 'success')
                return redirect(url_for('index'))

    flash('An error occurred', 'danger')
    return redirect(url_for('index'))

if __name__ == "__main__":
    port = int( app.config['PORT'] )
    app.run(host = '0.0.0.0', port=port)
