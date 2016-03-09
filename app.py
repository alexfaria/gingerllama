from flask import Flask, render_template, request, redirect, url_for, session, flash, Response
from models import List, ListItem, User, db
from functools import wraps
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

db.init_app(app)

with app.app_context():
    db.create_all()


def login_required(f):
    @wraps(f)
    def wrap(*args, **kargs):
        if 'logged_in' in session:
            return f(*args, **kargs)
        else:
            flash('You need to login first', 'info')
            return redirect(url_for('login'))
    return wrap


@app.route('/')
@login_required
def index():
    lists = db.session.query(List).all()
    return render_template('index.html', lists=lists)

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username:
           error = 'Invalid username'
        if not password:
           error = 'Invalid password'

        if not error:
            user = db.session.query(User).filter_by(username=username).first()
            if user and user.check_password(password):
                session['logged_in'] = True
                session['username'] = username
                flash('Success! You were logged in.', 'success')
                return redirect(url_for('index'))
            else:
                error = 'Wrong credentials.'
    if error:
        flash(error, 'danger')
    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']
        if not username:
            error = 'username is required'
        if not password:
            error = 'password is required'
        if not password2 or password != password2:
            error = 'passwords don\'t match'

        if not error:
            if db.session.query(User).filter_by(username=username).first():
                error = 'Account already exists'
            else:
                newuser = User(username = username, password=password, email = email)
                db.session.add(newuser)
                db.session.commit()
                session['logged_in'] = True
                flash('Success! You were logged in.', 'success')
                return redirect(url_for('index'))


    if error:
        flash(error, 'danger')
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('Success! You were logged out', 'success')
    return redirect(url_for('login'))

@app.route('/newlist', methods=['POST'])
@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
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
