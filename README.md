# gingerllama
Simple website with to-do lists.

[Self-hosted](http://gingerllama.noip.me) on a Raspberry PI 2 Model B using NGINX, Gunicorn, Supervisor and Virtualenv

For a demo simply login using
```
Username: demo
Password: demo
```
___
Uses:
* Flask
* Flask-SQLAlchemy
* Bootstrap
* jQuery.countdown



___
Todo:
- [x] Add users
- [ ] Make 'index.html' use template inheritance
- [ ] Functioning account settings page




___
Example Configuration:
```
DATABASE_URL="sqlite:///lists.db"
APP_SETTINGS="config.ProdConfig"
PORT=5000
SECRET_KEY="very-secret-key-here"
```
