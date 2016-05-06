from flask import g
from flask_nav import Nav, register_renderer
from flask_bootstrap.nav import BootstrapRenderer
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator
from markupsafe import escape

nav = Nav()

# Custom navbar renderer
class DefaultNavRenderer(BootstrapRenderer):
    def visit_Navbar(self, node):
        nav_tag = super(DefaultNavRenderer, self).visit_Navbar(node)
        nav_tag['class'] = 'navbar navbar-default navbar-fixed-top scripture-engagement-navbar'

        return nav_tag

def is_logged_in():
    return g.user is not None and g.user.is_authenticated

def initNav():
    """Create navigation elements after application context has been created"""
    nav.register_element('frontend_top', constructNavbar())

    nav.register_element('frontend_foot', Navbar(
        Text("Scripture Engagement ISD Team Orange 2016"),
    ))

def constructNavbar():
    elements = [
        View("Scripture Engagement", "index"),
        View("Home", "index"),
        readings()
    ]

    if is_logged_in():
        elements.append(Subgroup(
            'Content',
            View('Add Content', 'content.add_content'),
        ))

    elements.append(View("Read Scripture", "scripture.list_translations"))

    elements.append(Subgroup(
        'Plans',
        View('View Plans', 'plans.plan'),
        View('Edit Plans', 'plans.edit_plans'),
        View('Add Plan', 'plans.add_plan')
    ))
    elements.append(Subgroup(
        'Groups',
        View('View Groups', 'groups.group'),
        View('Edit Groups', 'groups.edit_group'),
        View('Add Group', 'groups.add_group')
    ))


    elements.append(loginButton())

    return Navbar(*elements)

def readings():
    elements = ["Readings"]

    elements.append(View("View Readings", "readings.all_readings"))

    if is_logged_in():
        elements.append(View("Add Reading", "readings.add_reading"))

    return Subgroup(*elements)

def loginButton():
    """Dynamic login/logout button"""
    if is_logged_in():
        return Subgroup(
            g.user.first_name,
            View("Profile", "users.profile", user_id=g.user.user_id),
            View("Logout", "users.logout")
        )
    else:
        label = "Login"
        route = "users.login"
        return View(label, route)
