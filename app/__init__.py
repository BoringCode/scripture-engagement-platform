from flask import Flask, render_template, g
from flask_bootstrap import Bootstrap
import flask.ext.login as flask_login
from app.db import DB
from datetime import datetime
from flask_nav import register_renderer
from app.nav import nav, DefaultNavRenderer, initNav

app = Flask(__name__)

app.config.from_object('config')

# Init login manager
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# Init nav on app object
nav.init_app(app)
register_renderer(app, 'defaultNav', DefaultNavRenderer)

# Setup database
@app.before_request
def before():
	g.db = DB()

	g.user = flask_login.current_user

	initNav()


@app.teardown_request
def after(exception):
	if hasattr(g, 'db'):
		g.db.close(exception)

#Load bootstrap helpers on app
Bootstrap(app)

#Load blueprints
from app.readings.controllers import readings as readings_module
from app.content.controllers import content as content_module
from app.scripture.controllers import scripture as scripture_module
from app.posts.controllers import posts as posts_module
from app.plans.controllers import plans as plans_module
from app.users.controllers import users as users_module

app.register_blueprint(readings_module, url_prefix="/readings")
app.register_blueprint(posts_module, url_prefix="/posts")
app.register_blueprint(content_module, url_prefix="/content")
app.register_blueprint(scripture_module, url_prefix="/scripture")
app.register_blueprint(plans_module, url_prefix="/plans")
#Users module is located on root prefix
app.register_blueprint(users_module)


@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    if fmt is None:
    	fmt='%b %d, %Y'
    return format(datetime.fromtimestamp(date), fmt)


# Home page
@app.route("/")
def index():
	return render_template("index.html")