from flask import Flask, render_template, g
from flask_bootstrap import Bootstrap
from app.db import DB

from datetime import datetime

app = Flask(__name__)

app.config.from_object('config')

#Load bootstrap helpers on app
Bootstrap(app)

# Setup database
@app.before_request
def before():
	g.db = DB()

@app.teardown_request
def after(exception):
	g.db.close(exception)

#Load blueprints
from app.readings.controllers import readings as readings_module
from app.content.controllers import content as content_module
from app.scripture.controllers import scripture as scripture_module
from app.posts.controllers import posts as posts_module
from app.plans.controllers import plans as plans_module

app.register_blueprint(readings_module, url_prefix="/readings")
app.register_blueprint(posts_module, url_prefix="/posts")
app.register_blueprint(content_module)
app.register_blueprint(scripture_module)
app.register_blueprint(plans_module, url_prefix="/plans")


@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    if fmt is None:
    	fmt='%b %d, %Y'
    return format(datetime.fromtimestamp(date), fmt)


# Home page
@app.route("/")
def index():
	return render_template("index.html")

#Set up navigation
from app.nav import nav
nav.init_app(app)


