from flask import Flask, render_template, g

app = Flask(__name__)


if __name__ == "__main__":
	app.run(debug=True, port=8080)
