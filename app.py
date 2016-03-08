from flask import Flask, render_template, request, redirect, url_for, session, flash, Response
from werkzeug.security import generate_password_hash, check_password_hash
from models import List, ListItem, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)


app.config.from_object(os.environ['APP_SETTINGS'])
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
dbsession = DBSession()

db = SQLAlchemy(app)


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
    # lists_dic = {}
    #for list in lists:
    #    print list.title
    #    lists_dic[list.title] = dbsession.query(ListItem).filter_by(list_id=list.id).order_by(ListItem.title)
    # return render_template('index.html', lists_dic = lists_dic, alert=alert)

    lists = dbsession.query(List).all()
    return render_template('index.html', lists=lists)


@app.route('/newlist', methods=['POST'])
@requires_auth
def newlist():
    if request.method == "POST":
        title = request.form['title']
        if title:
            newlist = List(title=title)
            dbsession.add(newlist)
            dbsession.commit()
            flash('Success!', 'success')
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
            list = dbsession.query(List).filter_by(id = list_id).first()
            if list:
                newitem = ListItem(title=title, list_id = list.id)
                dbsession.add(newitem)
                dbsession.commit()
                flash('Success!', 'success')
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
            list = dbsession.query(List).filter_by(id = list_id).first()
            checkitem = dbsession.query(ListItem).filter_by(list = list, id = item_id).first()
            if checkitem and list:
                if check == 'true':
                    checkitem.check = True
                else:
                    checkitem.check = False
                dbsession.add(checkitem)
                dbsession.commit()
                flash('Success!', 'success')
                return redirect(url_for('index'))

    flash('An error occurred', 'danger')
    return redirect(url_for('index'))

@app.route('/deletelist', methods=['POST'])
@requires_auth
def deletelist():
    if request.method == "POST":
        id = request.form['list-id']
        if id:
            deletelist = dbsession.query(List).filter_by(id=id).first()
            if deletelist:
                dbsession.delete(deletelist)
                dbsession.commit()
                flash('Success!', 'success')
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
            list = dbsession.query(List).filter_by(id = list_id).first()
            deleteitem = dbsession.query(ListItem).filter_by(list = list, id = item_id).first()
            if deleteitem and list:
                dbsession.delete(deleteitem)
                dbsession.commit()
                flash('Success!', 'success')
                return redirect(url_for('index'))

    flash('An error occurred', 'danger')
    return redirect(url_for('index'))

if __name__ == "__main__":
    port = int( app.config['PORT'] )
    app.run(host = '0.0.0.0', port=port)
