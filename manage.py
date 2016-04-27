from flask.ext.script import Manager
import flask
import urllib

from app import app

manager = Manager(app)

@manager.command
def list_routes():
    """List all routes in flask application"""
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = flask.url_for(rule.endpoint, **options)
        line = urllib.parse.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)
    
    for line in sorted(output):
        print(line)

if __name__ == "__main__":
    manager.run()