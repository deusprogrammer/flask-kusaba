from elixir import *
from flask import Flask

app = Flask(__name__)

if !os.path.exists():
	create_all()

setup_all()

import flask_kusaba.views
