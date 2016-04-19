from app import app
from flask_nav import Nav, register_renderer
from flask_bootstrap.nav import BootstrapRenderer
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator
from markupsafe import escape

import flask.ext.login as flask_login
from app import login_manager

# Custom navbar renderer
class DefaultNavRenderer(BootstrapRenderer):
    def visit_Navbar(self, node):
        nav_tag = super(DefaultNavRenderer, self).visit_Navbar(node)
        nav_tag['class'] = 'navbar navbar-default navbar-fixed-top scripture-engagement-navbar'

        return nav_tag
#register renderer to app
register_renderer(app, 'defaultNav', DefaultNavRenderer)


# Initialize navbar class and create two navigation areas (top and footer)
nav = Nav()

def loginButton():
    """Dynamic login/logout button"""
    if flask_login.current_user and flask_login.current_user.is_authenticated:
        label = "Logout"
        route = "users.logout"
    else:
        label = "Login"
        route = "users.login"
    return View(label, route)

nav.register_element('frontend_top', Navbar(
    View('Scripture Engagement', 'index'),
    View('Home', 'index'),
    Subgroup(
        'Readings',
        View('View Readings', 'readings.all_readings'),
        View('Add Reading', 'readings.add_reading'),
    ),
    Subgroup(
        'Content',
        View('Add Content', 'content.add_content'),
    ),
    View('Read Scripture','scripture.list_translations'),
    Subgroup(
        'Plans',
        View('View Plans', 'plans.plan')
    ),
    loginButton()
))

nav.register_element('frontend_foot', Navbar(
    Text("Scripture Engagement ISD Team Orange 2016"),
))



