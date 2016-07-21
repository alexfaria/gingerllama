from models import List, ListItem, User, db
from flask import Flask, render_template, request, redirect, url_for, session, flash, Response, jsonify
from werkzeug.contrib.fixers import ProxyFix
from functools import wraps
import os

app = Flask(__name__)
app.config.from_object(os.getenv('APP_SETTINGS', 'config.ProdConfig'))

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
    user = db.session.query(User).filter_by(username=session['username']).first()
    if user:
        lists = user.lists
        return render_template('index.html', lists=lists)
    # invalid session cookie
    session.clear()
    return redirect(url_for('login'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    username = None
    if request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        remember = request.form.get('remember-me', None)
        if not username:
           error = 'Invalid username'
        if not password:
           error = 'Invalid password'

        if not error:
            user = db.session.query(User).filter_by(username=username).first()
            if user and user.check_password(password):
                session['logged_in'] = True
                session['username'] = username
                if remember:
                    session.permanent = True
                flash('Success! You were logged in.', 'success')
                return redirect(url_for('index'))
            else:
                error = 'Wrong credentials.'
    if error:
        flash(error, 'danger')
    return render_template('login.html', username=username)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    error = None
    email = None
    username = None
    if request.method == 'POST':
        username = request.form.get('username', None)
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        password2 = request.form.get('password2', None)
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
                session['username'] = username
                flash('Success! You were logged in.', 'success')
                return redirect(url_for('index'))

    if error:
        flash(error, 'danger')
    return render_template('signup.html', username=username, email=email)


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
    title = request.form.get('title', None)
    user_id = db.session.query(User).filter_by(username=session['username']).first().id
    if title and user_id:
        newlist = List(title=title, user_id=user_id)
        db.session.add(newlist)
        db.session.commit()
        flash('Success! Added \'%s\'' % title, 'success')
        return redirect(url_for('index'))

    flash('An error occurred', 'danger')
    return redirect(url_for('index'))


@app.route('/api/new', methods=['POST'])
@login_required
def api_new():
    title = request.form.get('item', None)
    list_id = request.form.get('list-id', None)
    if title and list_id:
        list = db.session.query(List).filter_by(id = list_id).first()
        if list:
            newitem = ListItem(title=title, list_id = list.id)
            db.session.add(newitem)
            db.session.commit()
            return jsonify(list_id=list_id, title=title, id=newitem.id)


@app.route('/api/check', methods=['POST'])
@login_required
def api_check():
    check = request.form.get('check', None)
    item_id = request.form.get('item-id', None)
    list_id = request.form.get('list-id', None)
    if check and item_id and list_id:
        list = db.session.query(List).filter_by(id = list_id).first()
        checkitem = db.session.query(ListItem).filter_by(list = list, id = item_id).first()
        if checkitem and list:
            if check == 'true':
                checkitem.check = True
            else:
                checkitem.check = False
            db.session.add(checkitem)
            db.session.commit()
            return jsonify(check=checkitem.check)


@app.route('/api/deletelist', methods=['POST'])
@login_required
def api_deletelist():
    id = request.form.get('list-id', None)
    if id:
        deletelist = db.session.query(List).filter_by(id=id).first()
        if deletelist:
            title = deletelist.title
            db.session.delete(deletelist)
            db.session.commit()
            return jsonify(status='ok')


@app.route('/api/delete', methods=['POST'])
@login_required
def api_delete():
    item_id = request.form.get('item-id', None)
    list_id = request.form.get('list-id', None)
    if item_id and list_id:
        list = db.session.query(List).filter_by(id = list_id).first()
        deleteitem = db.session.query(ListItem).filter_by(list = list, id = item_id).first()
        if deleteitem and list:
            title = deleteitem.title
            db.session.delete(deleteitem)
            db.session.commit()
            return jsonify(result='true')


@app.route('/new', methods=['POST'])
@login_required
def new():
    title = request.form.get('item', None)
    list_id = request.form.get('list-id', None)
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
    check = request.form.get('check', None)
    item_id = request.form.get('item-id', None)
    list_id = request.form.get('list-id', None)
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
                return redirect(url_for('index'))
    flash('An error occurred', 'danger')
    return redirect(url_for('index'))


@app.route('/delete', methods=['POST'])
@login_required
def delete():
    item_id = request.form.get('item-id', None)
    list_id = request.form.get('list-id', None)
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


@app.route('/deletelist', methods=['POST'])
@login_required
def deletelist():
    id = request.form.get('list-id', None)
    if id:
        deletelist = db.session.query(List).filter_by(id=id).first()
        if deletelist:
            title = deletelist.title
            db.session.delete(deletelist)
            db.session.commit()
            flash('Success! Deleted \'%s\'' % title, 'success')
            return redirect(url_for('index'))
    flash('An error occurred', 'danger')
    return redirect(url_for('index'))

app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == "__main__":
    app.run(host = '0.0.0.0', port=int(app.config['PORT']))
