import hashlib
from datetime import datetime
from flask import Flask, request, jsonify, abort, render_template
import server
import config

import os
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../webmorda/dist')
app = Flask(__name__, template_folder=ASSETS_DIR, static_folder=ASSETS_DIR + "/static")

tokens = {}
debug = True


@app.route('/<path:dummy>')
def fallback(dummy):
	return render_template("index.html"), 302

@app.route('/')
def index():
	return render_template("index.html"), 302


def validate_token(token):
	if (not tokens.get(token)) & (not debug):
		return abort(403)


@app.route('/login/<pas>')
def authentication(pas):
	if server.check_password(pas):
		hash_object = hashlib.sha1(str(datetime.now().timestamp()).encode())
		hex_dig = hash_object.hexdigest()
		tokens[hex_dig] = True
		return jsonify({"result": {"token": hex_dig}})
	return abort(404)


@app.route('/<token>/users/', methods=['GET'])
def users_get(token):
	validate_token(token)
	res = server.get_users()
	if not res:
		return abort(404)
	users = []
	for r in res:
		users.append({
			'id': r[0],
			'name': r[1],
			'surname': r[2],
			'room': r[3],
		})
	obj = {"result": users}
	return jsonify(obj)


@app.route('/<token>/users/<id_user>/', methods=['DELETE'])
def users_delete(token, id_user):
	validate_token(token)
	res = server.remove_user(id_user)
	if not res:
		return abort(404)
	obj = {"result": res}
	return jsonify(obj)


@app.route('/<token>/achievements/', defaults={'id_user': None}, methods=['GET'])
@app.route('/<token>/achievements/<id_user>/', methods=['GET'])
def achievements_get(token, id_user):
	validate_token(token)
	res = server.get_achievements(id_user)
	if not res:
		return abort(404)
	achievements = []
	for r in res:
		achievements.append({
			'id': r[0],
			'name': r[1],
			'description': r[2],
		})
	obj = {"result": achievements}
	return jsonify(obj)


@app.route('/<token>/achievements/', methods=['POST'])
def achievements_post(token):
	validate_token(token)
	res = server.add_achievement(request.json["name"], request.json["description"])
	if not res:
		return abort(404)
	res = {'id': res}
	obj = {"result": res}
	return jsonify(obj)


@app.route('/<token>/achievements/<id_achievement>/', methods=['DELETE'])
def achievements_delete(token, id_achievement):
	validate_token(token)
	res = server.remove_achievement(id_achievement)
	if not res:
		return abort(404)
	obj = {"result": res}
	return jsonify(obj)


@app.route('/<token>/achievements/<id_user>/', methods=['POST'])
def achievement_to_user(token, id_user):
	validate_token(token)
	id_achievement = request.json['achievementId']
	res = server.set_achievement_to_user(id_achievement, id_user)
	if not res:
		return abort(404)
	obj = {"result": res}
	return jsonify(obj)


@app.route('/<token>/schedule/<id_user>/', defaults={'date': datetime.now().timestamp()}, methods=['GET'])
@app.route('/<token>/schedule/<id_user>/<date>/', methods=['GET'])
def schedule_get(token, id_user, date):
	validate_token(token)
	res = server.get_schedule(id_user, date)
	if not res:
		return abort(404)
	schedule = []
	for r in res:
		schedule.append({
			'id': r[0],
			'name': r[1],
			'description': r[2],
			'start': int(r[3]),
			'end': int(r[4]),
		})
	obj = {"result": schedule}
	return jsonify(obj)


@app.route('/<token>/groups/', defaults={'id_user': None}, methods=['GET'])
@app.route('/<token>/groups/<id_user>/', methods=['GET'])
def groups_get(token, id_user):
	validate_token(token)
	res = server.get_groups(id_user)
	if not res:
		return abort(404)
	groups = []
	for r in res:
		groups.append({
			'id': r[0],
			'name': r[1]
		})
	obj = {"result": groups}
	return jsonify(obj)


@app.route('/<token>/groups/', methods=['POST'])
def groups_post(token):
	validate_token(token)
	name = request.json['name']
	res = server.add_group(name)
	if not res:
		return abort(404)
	obj = {"result": res}
	return jsonify(obj)


@app.route('/<token>/groups/<id_group>/', methods=['DELETE'])
def group_delete(token, id_group):
	validate_token(token)
	res = server.remove_group(id_group)
	if not res:
		return abort(404)
	obj = {"result": res}
	return jsonify(obj)


@app.route('/<token>/groups/<id_group>/', methods=['POST'])
def add_users_to_group_post(token, id_group):
	validate_token(token)
	users = request.json['users']
	res = server.add_users_to_group(id_group, users)
	if not res:
		return abort(404)
	obj = {"result": res}
	return jsonify(obj)


@app.route('/<token>/teams/<id_group>/', methods=['POST'])
def teams_post(token, id_group):
	validate_token(token)
	codeword = request.json['codeword']
	res = server.add_team(id_group, codeword)
	if not res:
		return abort(404)
	obj = {"result": {'id': res}}
	return jsonify(obj)


@app.route('/<token>/teams/<id_team>/', methods=['DELETE'])
def teams_delete(token, id_team):
	validate_token(token)
	res = server.remove_team(id_team)
	if not res:
		return abort(404)
	obj = {"result": res}
	return jsonify(obj)


@app.route('/<token>/teams/', defaults={'id_user': None}, methods=['GET'])
@app.route('/<token>/teams/<id_user>/', methods=['GET'])
def teams_get(token, id_user):
	validate_token(token)
	res = server.get_teams(id_user)
	if not res:
		return abort(404)
	teams = []
	for r in res:
		teams.append({
			'id': r[0],
			'name': r[1],
			'num': r[2]
		})
	obj = {"result": teams}
	return jsonify(obj)


@app.route('/<token>/questions/', defaults={'id_team': None}, methods=['GET'])
@app.route('/<token>/questions/<id_team>/', methods=['GET'])
def questions_get(token, id_team):
	validate_token(token)
	res = server.get_questions(id_team)
	if not res:
		return abort(404)
	questions = []
	for r in res:
		questions.append({
			'id': r[0],
			'description': r[2],
			'answer': r[3],
			'num': r[1]
		})
	obj = {"result": questions}
	return jsonify(obj)


@app.route('/<token>/questions/', methods=['POST'])
def questions_post(token):
	validate_token(token)
	num = request.json['num']
	description = request.json['description']
	answer = request.json['answer']
	res = server.add_question(num, description, answer)
	if not res:
		return abort(404)
	obj = {"result": {'id': res}}
	return jsonify(obj)


@app.route('/<token>/questions/<id_group>/', methods=['POST'])
def questions_to_teams_post(token, id_group):
	validate_token(token)
	questions = request.json['questions']
	res = server.add_questions_to_team(id_group, questions)
	if not res:
		return abort(404)
	obj = {"result": res}
	return jsonify(obj)


@app.route('/<token>/questions/<id_question>/', methods=['DELETE'])
def questions_delete(token, id_question):
	validate_token(token)
	res = server.remove_question(id_question)
	if not res:
		return abort(404)
	obj = {"result": res}
	return jsonify(obj)


@app.route('/<token>/events/', defaults={'id_group': None}, methods=['GET'])
@app.route('/<token>/events/<id_group>/', methods=['GET'])
def events_get(token, id_group):
	validate_token(token)
	res = server.get_events(id_group)
	if not res:
		return abort(404)
	events = []
	for r in res:
		events.append({
			'id': r[0],
			'name': r[1],
			'description': r[2],
			'start': int(r[3]),
			'end': int(r[4])
		})
	obj = {"result": events}
	return jsonify(obj)


@app.route('/<token>/events/', methods=['POST'])
def events_post(token):
	validate_token(token)
	name = request.json['name']
	description = request.json['description']
	start = request.json['start']
	end = request.json['end']
	res = server.add_event(name, float(start), float(end), description)
	if not res:
		return abort(404)
	obj = {"result": {'id': res}}
	return jsonify(obj)


@app.route('/<token>/events/<id_group>', methods=['POST'])
def events_to_group_post(token, id_group):
	validate_token(token)
	events = request.json['events']
	res = server.add_events_to_group(id_group, events)
	if not res:
		return abort(404)
	obj = {"result": res}
	return jsonify(obj)


@app.route('/<token>/events/<id_event>/', methods=['DELETE'])
def events_delete(token, id_event):
	validate_token(token)
	res = server.remove_event(id_event)
	if not res:
		return abort(404)
	obj = {"result": res}
	return jsonify(obj)


@app.route('/<token>/messages/<id_group>', methods=['POST'])
def messages_to_group_post(token, id_group):
	validate_token(token)
	text = request.json['text']
	res = server.send_message_to_group(id_group, text)
	if not res:
		return abort(404)
	obj = {"result": res}
	return jsonify(obj)


def run(d=True):
	global debug
	debug = d

	app.run(
		host="127.0.0.1",
		port=int(config.server_port),
		debug=False
	)
