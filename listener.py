from flask import Flask, render_template, request, jsonify

server = None


def set_server(s):
	global server
	server = s


app = Flask(__name__)


@app.route('/')
def add_numbers():
	a = request.args.get('a', 0, type=int)
	b = request.args.get('b', 0, type=int)
	return jsonify(result=a + b)


def run():
	app.run(
		host="127.0.0.1",
		port=int("80"),
		debug=True
	)
