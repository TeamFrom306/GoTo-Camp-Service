from datetime import datetime, timedelta
from db_connection import Database
import bot

db = Database()
last_team_id = {}


# region Urgent Messages
def send_messages_by_ids(id_list, text):
	bot.send_message(id_list, text)


def send_message_to_group(id_group, text):
	users = db.get_users_by_group(id_group)
	id_list = []
	for user in users:
		id_list.append(user[0])
	bot.send_message(id_list, text)


# endregion


# <editor-fold desc="Users">
def add_user(id_tg, name, surname):
	return db.add_user(id_tg, name, surname)


def remove_user(id_tg):
	return db.remove_data(id_tg, 'user')


def get_users(id_tg=None):
	return db.get_data(id_tg, 'user')


def set_room(tg_id, room):
	return db.set_room(tg_id, room)


def add_users_to_group(id_group, id_users):
	return db.add_to_cross_table(id_group, id_users, 'group', 'user', 'users_groups')


# </editor-fold>

# <editor-fold desc="Events">
def add_event(name, date_start, date_end, description):
	return db.add_event(name, date_start, date_end, description)


def remove_event(id_event):
	return db.remove_data(id_event, 'event')


def get_events(id_group=None):
	return db.get_events(id_group)


def add_events_to_group(id_group, id_events):
	return db.add_to_cross_table(id_group, id_events, 'group', 'event', 'events_groups')


# </editor-fold>

# <editor-fold desc="Info">
def get_reference_info(id_tg):
	ref_info = db.get_data(None, 'reference_information')
	room = get_users(id_tg)
	return ref_info, room


def add_reference_information(name, description):
	return db.add_reference_info(name, description)


# </editor-fold>

# <editor-fold desc="Teams">
def add_team(id_group, codeword):
	return db.add_team(id_group, codeword)


def remove_team(id_group):
	return db.remove_data(id_group, 'team')


def get_teams(id_group=None):
	return db.get_data(id_group, 'team')


# </editor-fold>

# <editor-fold desc="Groups">
def add_group(name):
	return db.add_group(name)


def remove_group(id_group):
	return db.remove_data(id_group, 'group')


def get_groups(id_tg=None):
	return db.get_groups(id_tg)


def get_group_by_id(id_group):
	return db.get_groups_by_id(id_group)


# </editor-fold>

# <editor-fold desc="Questions">
def add_question(num, description, answer):
	return db.add_question(num, description, answer)


def remove_question(id_question):
	return db.remove_data(id_question, 'question')


def get_questions(id_team=None):
	return db.get_questions(id_team)


def add_questions_to_team(id_team, id_questions):
	return db.add_to_cross_table(id_team, id_questions, 'group', 'question', 'groups_questions')


# </editor-fold>

# <editor-fold desc="Achievements">
def add_achievement(name, description):
	return db.add_achievement(name, description)


def remove_achievement(id_achievement):
	return db.remove_data(id_achievement, 'achievement')


def get_achievements(id_tg=None):
	return db.get_achievements(id_tg)


def set_achievement_to_user(id_achievement, id_tg):
	return db.add_to_cross_table(id_tg, [id_achievement], 'user', 'achievement', 'users_achievements')


# </editor-fold>


# <editor-fold desc="Schedule">
def get_schedule(id_tg, date):
	start, end = get_start_end_date(date)
	return db.get_schedule(id_tg, start, end)


def get_start_end_date(date):
	start = datetime.combine(date.date(), datetime.min.time()).timestamp()
	end = datetime.combine(date.date() + timedelta(days=1), datetime.min.time()).timestamp()
	return start, end


# </editor-fold>
def wipe_data():
	db.wipe_data()


def get_achievements_by_name(text):
	return db.get_achievements_by_name(text)


def get_events_by_tg_id(tg_id, date):
	return db.get_events_by_tg_id(tg_id, date)


def get_event_by_name(text):
	return db.get_event_by_name(text)


def get_info_by_name(text):
	return db.get_reference_info_by_name(text)


def check_login(id_tg, codeword):
	res = db.check_login(id_tg, codeword)
	if res:
		last_team_id[id_tg] = res[0]
	return res


def get_next_question(id_tg):
	return db.get_next_question(last_team_id[id_tg])


def get_answer(id_tg):
	return db.get_answer(last_team_id[id_tg])


def inc(id_tg):
	db.inc(last_team_id[id_tg])
