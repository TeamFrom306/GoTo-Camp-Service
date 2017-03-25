import sqlite3

from Server import config


# noinspection PyBroadException
class Database:
	def __init__(self):
		super().__init__()
		self.db = sqlite3.connect(config.database + '.db', check_same_thread=False)
		self.db.execute('PRAGMA FOREIGN_KEYS = ON')

	def remove_data(self, id_field, table):
		try:
			self.db.execute('DELETE FROM {1}s WHERE id_{1} = {0}'.format(id_field, table))
			self.db.commit()
			return True
		except Exception as e:
			print(e)
			return False

	def get_data(self, id_field, table):
		try:
			s = 'SELECT * FROM {}s'.format(table)
			if id_field is not None:
				s += ' WHERE id_{1} = {0}'.format(id_field, table)
				return self.db.execute(s).fetchone()
			return self.db.execute(s).fetchall()
		except Exception as e:
			print(e)
			return False

	def add_data_by_sql(self, string):
		try:
			c = self.db.cursor()
			c.execute(string)
			returned_id = c.lastrowid
			self.db.commit()
			return returned_id
		except Exception as e:
			print(e)
			return False

	def add_to_cross_table(self, id_field, id_list, name1, name2, table):
		try:
			c = self.db.cursor()
			s = "INSERT INTO {2} (id_{0}, id_{1}) VALUES ".format(name1, name2, table)
			for id_2 in id_list:
				s += " ({0}, {1}),".format(id_field, id_2)
			s = s[:-1]
			c.execute(s)
			self.db.commit()
			return True
		except Exception as e:
			print(e)
			return False

	def add_user(self, id_tg, name, surname):
		try:
			c = self.db.cursor()
			res = c.execute("SELECT * FROM users WHERE id_user = {0}".format(id_tg)).fetchone()
			if res is not None:
				return
			c.execute(
				"INSERT INTO users (id_user, name, surname, room) "
				"VALUES ({0}, '{1}', '{2}', NULL)".format(id_tg, name, surname))
			self.db.commit()
			return True
		except:
			return False

	def set_room(self, tg_id, room):
		try:
			s = "UPDATE users SET room = '{0}' WHERE id_user == {1}".format(room, tg_id)
			self.db.execute(s)
			self.db.commit()
			return True
		except:
			return False

	def add_event(self, name, date_start, date_end, description):
		s = "INSERT INTO events (time_start, time_end, description, name) VALUES ('{1}', '{2}', '{3}', '{0}')" \
			.format(name, date_start, date_end, description)
		return self.add_data_by_sql(s)

	def add_team(self, id_group, codeword):
		s = "INSERT INTO teams (id_group, codeword) VALUES ({0}, '{1}')".format(id_group, codeword)
		return self.add_data_by_sql(s)

	def add_group(self, name):
		s = "INSERT INTO groups (name) VALUES ('{0}')".format(name)
		return self.add_data_by_sql(s)

	def add_question(self, num, description, answer):
		s = "INSERT INTO questions (q_num, description, answer) VALUES ({0}, '{1}', '{2}')".format(num, description,
																								   answer)
		return self.add_data_by_sql(s)

	def add_achievement(self, name, description):
		s = "INSERT INTO achievements (name, description) VALUES ('{0}', '{1}')".format(name, description)
		return self.add_data_by_sql(s)

	def get_groups(self, id_tg):
		if id_tg is None:
			return self.get_data(None, 'group')
		else:
			try:
				c = self.db.cursor()
				s = "SELECT groups.id_group, groups.name " \
					"FROM users JOIN users_groups ON users.id_user = users_groups.id_user " \
					"JOIN groups ON users_groups.id_group = groups.id_group " \
					"WHERE users.id_user == {0}".format(id_tg)
				return c.execute(s).fetchall()
			except Exception as e:
				print(e)
				return False

	def get_questions(self, id_team):
		if id_team is None:
			return self.get_data(None, 'question')
		else:
			try:
				c = self.db.cursor()
				s = "SELECT questions.id_question, description, answer, questions.q_num " \
					"FROM teams JOIN groups_questions ON teams.id_group = groups_questions.id_group " \
					"JOIN questions ON groups_questions.id_question = questions.id_question " \
					"WHERE teams.id_group == {0}".format(id_team)
				return c.execute(s).fetchall()
			except Exception as e:
				print(e)
				return False

	def get_events(self, id_group):
		if id_group is None:
			return self.get_data(None, 'event')
		else:
			try:
				c = self.db.cursor()
				s = "SELECT events.id_event, events.name, description, time_start, time_end " \
					"FROM groups JOIN events_groups ON groups.id_group = events_groups.id_group " \
					"JOIN events ON events_groups.id_event = events.id_event " \
					"WHERE groups.id_group == {0}".format(id_group)
				return c.execute(s).fetchall()
			except Exception as e:
				print(e)
				return False

	def get_achievements(self, id_tg):

		if id_tg is None:
			return self.get_data(None, 'achievement')
		else:
			try:
				c = self.db.cursor()
				s = "SELECT achievements.id_achievement, achievements.name, description " \
					"FROM users JOIN users_achievements ON users.id_user = users_achievements.id_user " \
					"JOIN achievements ON users_achievements.id_achievement = achievements.id_achievement " \
					"WHERE users.id_user == {0}".format(id_tg)
				return c.execute(s).fetchall()
			except Exception as e:
				print(e)
				return False

	def get_schedule(self, id_tg, start, end):
		try:
			c = self.db.cursor()
			s = "SELECT events.id_event, events.name, description, time_start, time_end " \
				"FROM users JOIN users_groups ON users.id_user = users_groups.id_user " \
				"JOIN groups ON users_groups.id_group = groups.id_group " \
				"JOIN events_groups ON groups.id_group = events_groups.id_group " \
				"JOIN events ON events_groups.id_event = events.id_event " \
				"WHERE users.id_user == {0} AND events.time_start < {1} AND events.time_start > {2} " \
				"ORDER BY time_start ASC" \
				.format(id_tg, end, start)
			return c.execute(s).fetchall()
		except Exception as e:
			print(e)
			return False

	def get_groups_by_id(self, id_group):
		return self.get_data(id_group, 'group')

	def get_users_by_group(self, id_group):
		if id_group is None:
			return self.get_data(None, 'group')
		else:
			try:
				c = self.db.cursor()
				s = "SELECT groups.id_group, groups.name " \
					"FROM users JOIN users_groups ON users.id_user = users_groups.id_user " \
					"JOIN groups ON users_groups.id_group = groups.id_group " \
					"WHERE groups.id_group == {0}".format(id_group)
				return c.execute(s).fetchall()
			except Exception as e:
				print(e)
				return False

	def wipe_data(self):
		self.db.executescript(
			"DELETE FROM users_achievements;  "
			"DELETE FROM achievements;  "
			"DELETE FROM events_groups;  "
			"DELETE FROM events;  "
			"DELETE FROM users_groups;  "
			"DELETE FROM groups_questions;  "
			"DELETE FROM teams;  "
			"DELETE FROM groups;  "
			"DELETE FROM questions;  "
			"DELETE FROM reference_informations;  "
			"DELETE FROM users;")

	def get_events_by_tg_id(self, id_tg, date):
		try:
			c = self.db.cursor()
			s = "SELECT events.id_event, events.name, description, time_start, time_end " \
				"FROM users JOIN users_groups ON users.id_user = users_groups.id_user " \
				"JOIN groups ON users_groups.id_group = groups.id_group " \
				"JOIN events_groups ON groups.id_group = events_groups.id_group " \
				"JOIN events ON events_groups.id_event = events.id_event " \
				"WHERE users.id_user == {0} AND events.time_start < {1} AND events.time_end > {1} " \
				"ORDER BY time_start ASC" \
				.format(id_tg, date)
			return c.execute(s).fetchall()
		except Exception as e:
			print(e)
			return False

	def get_achievements_by_name(self, text):
		try:
			s = "SELECT * FROM achievements WHERE name == '{0}'".format(text)
			return self.db.execute(s).fetchone()
		except Exception as e:
			print(e)
			return False

	def get_event_by_name(self, text):
		try:
			s = "SELECT * FROM events WHERE name == '{0}'".format(text)
			return self.db.execute(s).fetchone()
		except Exception as e:
			print(e)
			return False

	def get_reference_info_by_name(self, text):
		try:
			s = "SELECT * FROM reference_informations WHERE name == '{0}'".format(text)
			return self.db.execute(s).fetchone()
		except Exception as e:
			print(e)
			return False

	def check_login(self, id_tg, codeword):
		try:
			s = "SELECT teams.id_group FROM " \
				"users JOIN users_groups ON users.id_user = users_groups.id_user " \
				"JOIN teams ON teams.id_group == users_groups.id_group " \
				"WHERE users.id_user == {0} AND codeword == '{1}'".format(id_tg, codeword)
			return self.db.execute(s).fetchone()
		except Exception as e:
			print(e)
			return False

	def get_next_question(self, id_group):
		try:
			s = "SELECT questions.description " \
				"FROM teams JOIN groups_questions ON teams.id_group = groups_questions.id_group " \
				"JOIN questions ON groups_questions.id_question = questions.id_question " \
				"WHERE teams.id_group == {0} AND teams.q_num == questions.q_num".format(id_group)
			return self.db.execute(s).fetchone()
		except Exception as e:
			print(e)
			return False

	def get_answer(self, id_group):
		try:
			s = "SELECT questions.answer " \
				"FROM teams JOIN groups_questions ON teams.id_group = groups_questions.id_group " \
				"JOIN questions ON groups_questions.id_question = questions.id_question " \
				"WHERE teams.id_group == {0} AND teams.q_num == questions.q_num".format(id_group)
			return self.db.execute(s).fetchone()
		except Exception as e:
			print(e)
			return False

	def inc(self, id_group):
		try:
			s = "UPDATE teams SET q_num = q_num + 1 WHERE id_group == {0}".format(id_group)
			self.db.execute(s)
			self.db.commit()
			return True
		except Exception as e:
			print(e)
			return False

	def add_reference_info(self, name, description):
		try:
			s = "INSERT INTO reference_informations (name, description) VALUES ('{0}', '{1}')".format(name, description)
			return self.add_data_by_sql(s)
		except Exception as e:
			print(e)
			return False

	def get_users_by_event(self, id_event):
		try:
			s = "SELECT DISTINCT users.id_user " \
				"FROM users JOIN users_groups ON users.id_user = users_groups.id_user " \
				"JOIN groups ON users_groups.id_group = groups.id_group " \
				"JOIN events_groups ON groups.id_group = events_groups.id_group " \
				"JOIN events ON events_groups.id_event = events.id_event " \
				"WHERE events.id_event == {0}".format(id_event)
			return self.db.execute(s).fetchall()
		except Exception as e:
			print(e)
			return False

	def check_password(self, password):
		try:
			s = "SELECT * FROM passwords WHERE password == '{0}'".format(password)
			return self.db.execute(s).fetchall()
		except Exception as e:
			print(e)
			return False

	def get_teams(self, id_group):
		try:
			s = 'SELECT * FROM teams'
			if id_group is not None:
				s += ' WHERE id_group = {0}'.format(id_group)
				return self.db.execute(s).fetchone()
			return self.db.execute(s).fetchall()
		except Exception as e:
			print(e)
			return False

	def remove_team(self, id_group):
		try:
			self.db.execute('DELETE FROM teams WHERE id_group = {0}'.format(id_group))
			self.db.commit()
			return True
		except Exception as e:
			print(e)
			return False
