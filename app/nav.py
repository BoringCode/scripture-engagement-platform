from app import app
from flask_nav import Nav, register_renderer
from flask_bootstrap.nav import BootstrapRenderer
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator
from markupsafe import escape

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
        View('View Plans', 'plans.plan'),
        View('Edit Plans', 'plans.edit_plans'),
        View('Add Plan', 'plans.add_plan')

    ),
    Subgroup(
        'Groups',
        View('View Groups', 'groups.group'),
        View('Edit Group', 'groups.edit_group'),
        View('Add Group', 'groups.add_group')

    )
))

nav.register_element('frontend_foot', Navbar(
    Text("Scripture Engagement ISD Team Orange 2016"),
))



