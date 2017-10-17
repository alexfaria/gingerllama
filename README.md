# gingerllama
Simple website with to-do lists.

___
Dependencies:
* Python 2.7
* Virtualenv
* Flask
* Flask-SQLAlchemy
* Bootstrap
* jQuery
* jQuery.countdown



___
Todo:
- [x] Add users
- [ ] Make 'index.html' use template inheritance
- [ ] Functioning account settings page




___
Deploying Locally:  
To deploy locally you'll need pip and virtualenv installed
* create a new virtualenv  
`virtualenv env`  
* activate the virtualenv  
`source bin/activate`  
* install the requirements to run gingerllama  
`pip install -r requirements.txt`  
* run gingerllama  
`python app.py`  
* optionally set the environment variables in `env/bin/activate`  
example:    
```
DATABASE_URL="sqlite:///lists.db"
APP_SETTINGS="config.ProdConfig"
PORT=5000
SECRET_KEY="very-secret-key-here"
```
 
