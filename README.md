# Scripture Engagement Platform - Team Orange ISD

> Encouraging Biblical study and engagement through a dynamic online platform

[![Build Status](https://travis-ci.org/BoringCode/scripture-engagement-platform.svg?branch=master)](https://travis-ci.org/BoringCode/scripture-engagement-platform)

This is our implementation of the system design presented during the Fall 2015 Information Systems Analysis class. The application is built on top of [Flask](http://flask.pocoo.org/).

## Requirements

- Python 3.3+
- sqlite3
- PIP
- virtualenv
- [Node Package Manager](https://www.npmjs.com/)

## Setup

Our main development IDE is PyCharm, which handles Python dependancy installation automatically. However if you want to install the dependancies manually, we are using virtualenv and PIP.

```bash
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Front-end dependancies and builds are handled with NPM and [Grunt](http://gruntjs.com/). Make sure you have both installed.

```bash
$ npm install
$ grunt
```

The database can be created within PyCharm using `app/db/create-db.sql`, or you can create it manually from the command line. You should create a file called `database.db` (or manually configure the path in `config.py`)

```bash
$ sqlite3 app/database.db
sqlite> .read app/db/create-db.sql;
```

The app allows you to create all the necessary data from within the site (users, readings, posts, etc...) but you can also optionally create some test data by reading in `app/db/init-db.sql`.

Now that you've installed all the dependancies, start the application.

```bash
$ python run.py
```

## API Setup
In our application we are using the Bible Gateway API to get access to our scripture. For any of this functionality to work you must first create a file with an unexpired access token from Bible Gateway. Read the [Bible Gateway API documentation](https://api.biblegateway.com/3/docs) for more information on the API.

This file should be titled "bg-keys.json" and stored in the application root. Inside this file should be the following:

```json
{
  "access_token": "INSERT UNEXPIRED ACCESS TOKEN HERE"
}
```

The access token must be updated every two weeks or else it will expire.

## Development

Front-end development should be performed in the `src/` folder. We are using SASS for our front-end styles. Each piece of the stylesheet should be written in a modular system to encourage the DRY principle.

Development on the Flask application occurs in `app/`. We are following a module system. Individual features of the application (such as plans, accounts, readings, groups, etc..) should be split out into their own module. Each module should contain `controllers.py`, `models.py`, and `forms.py` with each piece of functionality split up accordingly. Controllers should be implemented as [blueprints](http://flask.pocoo.org/docs/0.10/blueprints/) which are then instantiated on the main app controller in `app/__init__.py`.


## Tests

Tests are an important part of maintaining application quality. During development tests should be used to ensure that functionality is working as intended.

Run tests while within the virtualenv (or while using Flask)

```bash
$ python tests.py
``` 

Tests **must** be written and passing before pushing changes to the master branch.

## Manager

Certain actions can be performed from your CLI using `manage.py`. 

Call these actions from inside your virtualenv: `python manage.py action`

- **list_routes**
  
  List all available URL routes in the Flask application. Displays allowed methods and required parameters. 

## Team Members
- Bradley Rosenfeld
- Lindsay Robinson
- Austin Mackay
- Michael Free
- Jonathan Welde
