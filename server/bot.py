from time import sleep
import config
import telebot
from handler import Handler
from menu import Menu

import server

bot = telebot.TeleBot(config.token)
menu = Menu("Root", "ROOT", bot)
test_id = config.anton_tg_id
handler = Handler(menu=menu, bot=bot)


@bot.message_handler(commands=['start'])
def handle_start(message):
	if len(bot.message_handlers) > 1:
	    bot.message_handlers.pop()
	server.add_user(message.chat.id, message.chat.first_name, message.chat.last_name)
	if len(bot.pre_message_subscribers_next_step) > 0:
		bot.pre_message_subscribers_next_step.clear()
	r = Menu("Root", "", bot).get_root()
	r.add_row("Enter room", handler.set_room, back_button=False)
	r.add_row("Skip", handler.main_menu, back_button=False)
	handler.start_menu(r)
	bot.send_message(message.chat.id, config.welcome_msg, reply_markup=r.make_keyboard())
	bot.register_next_step_handler(message, r.handler)
	return True


@bot.message_handler(content_types=['text'])
def handle_any(message):
	if users_dict.get(message.chat.id) is None:
		users_dict[message.chat.id] = True
	else:
		return
	if server.get_users(message.chat.id):
		menu.get_root().handler(message)
	else:
		handle_start(message)


users_dict = {}


def send_message(id_list, text):
	for chat_id in id_list:
		try:
			bot.send_message(chat_id, text)
		except Exception as e:
			print(e)
		sleep(0.05)


def make_bot():
	menu.set_back(config.back_msg)
	menu.set_wrong(config.wrong_msg)
	root = menu.get_root()
	root.add_row("Achievements", handler.get_achievements)
	root.add_row("Schedule", handler.get_schedule)
	root.add_row("What now", handler.get_events)
	root.add_row("Help/info", handler.get_info)
	root.add_row("Start quest", handler.start_quest)


def start_polling():
	bot.polling(none_stop=True)
