from flask import Blueprint, render_template, flash, redirect, url_for

# Import forms
from app.readings.forms import *

# Import models
from app.readings.models import *

# Create blueprint for readings routes
readings = Blueprint('readings', __name__)

# Display index page
@readings.route('/')
def index():
    return render_template('readings/index.html')
