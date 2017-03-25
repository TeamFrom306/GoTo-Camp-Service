import datetime

import config
import telebot
from db_connection import Database

from Server import server


class Handler:
	def __init__(self, bot, menu):
		super().__init__()
		self.bot = bot
		self.menu = menu
		self.db = Database()
		self.start_root = None
		self.classes = dict()

	def get_achievements(self, msg):
		achievements = server.get_achievements(msg.chat.id)
		markup = telebot.types.ReplyKeyboardMarkup()
		for a in achievements:
			markup.row(a[1])
		markup.row("Back")
		self.bot.send_message(msg.chat.id, "Choose", reply_markup=markup)
		self.bot.register_next_step_handler(msg, self.get_description_achievement)
		return True

	def get_description_achievement(self, msg):
		if msg.text == 'Back':
			self.bot.send_message(msg.chat.id, config.main_menu_msg, reply_markup=self.menu.get_root().make_keyboard())
			self.bot.register_next_step_handler(msg, self.menu.get_root().handler)
		else:
			description = server.get_achievements_by_name(msg.text)
			if (description is not None) & (description != ""):
				self.bot.send_message(msg.chat.id, description[2])
			self.bot.register_next_step_handler(msg, self.get_description_achievement)
		return True

	def get_description_event(self, msg):
		if msg.text == 'Back':
			self.bot.send_message(msg.chat.id, config.main_menu_msg, reply_markup=self.menu.get_root().make_keyboard())
			self.bot.register_next_step_handler(msg, self.menu.get_root().handler)
		else:
			description = server.get_event_by_name(msg.text[:-19], msg.chat.id)
			if (description is not None) & (description != ""):
				self.bot.send_message(msg.chat.id, description)
			self.bot.register_next_step_handler(msg, self.get_description_event)
		return True

	def get_schedule(self, msg):
		events = server.get_schedule(msg.chat.id, datetime.datetime.now())
		markup = telebot.types.ReplyKeyboardMarkup()
		for event in events:
			start = datetime.datetime.fromtimestamp(event[3]).strftime("%H:%M:%S")
			end = datetime.datetime.fromtimestamp(event[4]).strftime("%H:%M:%S")
			markup.row(event[1] + "  " + start + "-" + end)
		markup.row("Back")
		self.bot.send_message(msg.chat.id, "Choose event to display description", reply_markup=markup)
		self.bot.register_next_step_handler(msg, self.get_description_event)
		return True

	def get_events(self, msg):
		events = server.get_events_by_tg_id(msg.chat.id, datetime.datetime.now().timestamp())
		markup = telebot.types.ReplyKeyboardMarkup()
		for event in events:
			start = datetime.datetime.fromtimestamp(event[3]).strftime("%H:%M:%S")
			end = datetime.datetime.fromtimestamp(event[4]).strftime("%H:%M:%S")
			markup.row(event[1] + "  " + start + "-" + end)
		markup.row("Back")
		self.bot.send_message(msg.chat.id, "Choose event to display description", reply_markup=markup)
		self.bot.register_next_step_handler(msg, self.get_description_event)
		return True

	def get_info(self, msg):
		ref_info, user = server.get_reference_info(msg.chat.id)
		markup = telebot.types.ReplyKeyboardMarkup()
		for event in ref_info:
			markup.row(event[1])
		if user[3] is None:
			markup.row("Room")
		else:
			markup.row("Room = " + user[3])
		markup.row("Back")
		self.bot.send_message(msg.chat.id, "Choose info to display description", reply_markup=markup)
		self.bot.register_next_step_handler(msg, self.get_info_description)
		return True

	def get_info_description(self, msg):
		if msg.text == 'Back':
			self.bot.send_message(msg.chat.id, config.main_menu_msg, reply_markup=self.menu.get_root().make_keyboard())
			self.bot.register_next_step_handler(msg, self.menu.get_root().handler)
		elif msg.text.startswith('Room'):
			return self.set_room(msg)
		else:
			description = server.get_info_by_name(msg.text)
			if (description is not None) & (description != ""):
				self.bot.send_message(msg.chat.id, description[2])
			self.bot.register_next_step_handler(msg, self.get_info_description)
		return True

	def set_room(self, msg):
		markup = telebot.types.ReplyKeyboardHide(selective=False)
		self.bot.send_message(msg.chat.id, "Send your room", reply_markup=markup)
		self.bot.register_next_step_handler(msg, self.set_room_callback)
		return True

	def set_room_callback(self, msg):
		server.set_room(msg.chat.id, msg.text)
		self.bot.send_message(msg.chat.id, config.successful_msg, reply_markup=self.menu.get_root().make_keyboard())
		self.bot.register_next_step_handler(msg, self.menu.get_root().handler)
		return True

	def main_menu(self, msg):
		self.bot.send_message(msg.chat.id, config.main_menu_msg, reply_markup=self.menu.get_root().make_keyboard())
		self.bot.register_next_step_handler(msg, self.menu.get_root().handler)
		return True

	def start_quest(self, msg):
		markup = telebot.types.ReplyKeyboardMarkup()
		markup.add("Back")
		self.bot.send_message(msg.chat.id, config.start_quest_msg, reply_markup=markup)
		self.bot.register_next_step_handler(msg, self.check_login)
		return True

	def check_login(self, msg):
		if msg.text == 'Back':
			self.bot.send_message(msg.chat.id, config.main_menu_msg, reply_markup=self.menu.get_root().make_keyboard())
			self.bot.register_next_step_handler(msg, self.menu.get_root().handler)
			return True
		id_team = server.check_login(msg.chat.id, msg.text)
		markup = telebot.types.ReplyKeyboardMarkup()
		markup.add('Back')
		if id_team:
			self.ask_question(msg)
		else:
			self.bot.send_message(msg.chat.id, config.wrong_codeword_msg, reply_markup=markup)
			self.bot.register_next_step_handler(msg, self.check_login)
		return True

	def ask_question(self, msg):
		if msg.text == 'Back':
			self.bot.send_message(msg.chat.id, config.main_menu_msg, reply_markup=self.menu.get_root().make_keyboard())
			self.bot.register_next_step_handler(msg, self.menu.get_root().handler)
			return True
		question = server.get_next_question(msg.chat.id)
		if not question:
			self.bot.send_message(msg.chat.id, config.congratulation_msg, reply_markup=self.menu.get_root().make_keyboard())
			self.bot.register_next_step_handler(msg, self.menu.get_root().handler)
		else:
			markup = telebot.types.ReplyKeyboardMarkup()
			markup.add('Question')
			markup.add('Back')
			self.bot.send_message(msg.chat.id, question[0], reply_markup=markup)
			self.bot.register_next_step_handler(msg, self.check_answer)
		return True

	def check_answer(self, msg):
		if msg.text == 'Back':
			self.bot.send_message(msg.chat.id, config.main_menu_msg, reply_markup=self.menu.get_root().make_keyboard())
			self.bot.register_next_step_handler(msg, self.menu.get_root().handler)
			return True
		if msg.text == 'Question':
			return self.ask_question(msg)
		answer = server.get_answer(msg.chat.id)
		if answer[0].lower() == msg.text.lower():
			server.inc(msg.chat.id)
			return self.ask_question(msg)
		else:
			markup = telebot.types.ReplyKeyboardMarkup()
			markup.add('Question')
			markup.add('Back')
			self.bot.send_message(msg.chat.id, config.wrong_answer_msg, reply_markup=markup)
			self.bot.register_next_step_handler(msg, self.check_answer)
			return True

	def start_menu(self, start_root):
		self.start_root = start_root
