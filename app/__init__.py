from flask import Flask, render_template, g
from flask_bootstrap import Bootstrap

app = Flask(__name__)

app.config.from_object('config')

#Load bootstrap helpers on app
Bootstrap(app)

#Load blueprints
from app.readings.controllers import readings as readings_module

app.register_blueprint(readings_module)


#Set up navigation
from app.nav import nav
nav.init_app(app)


