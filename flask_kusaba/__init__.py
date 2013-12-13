from flask import Flask
from flask_login import LoginManager
from models import *

# Setup the Flask webapp
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'C:\\tmp\\'
app.config['SECRET_KEY'] = 'KUSABA'

# Setup the login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.anonymous_user = AnonymousUser

# Setup all database access
setup_all()

# Setup login callback
@login_manager.user_loader
def load_user(userid):
	user = User.query.filter_by(username=userid)
	if user.count() == 0:
		return None
	else:
		return user.one()

import flask_kusaba.views