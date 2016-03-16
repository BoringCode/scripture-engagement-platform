from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator
from markupsafe import escape

nav = Nav()

nav.register_element('frontend_top', Navbar(
    View('Scripture Engagement', '.index'),
    View('Home', '.index'),
    Subgroup(
        'Readings',
        #View('View Readings', 'readings.all_readings'),
        View('Add Reading', 'readings.add_reading'),
        Separator(),
    ),
))


