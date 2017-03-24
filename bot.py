import telebot
from time import sleep
import config
import server
from handler import Handler
from menu import Menu

bot = telebot.TeleBot(config.token)
menu = Menu("Root", "ROOT", bot)
test_id = config.anton_tg_id
handler = Handler(menu=menu, bot=bot)


@bot.message_handler(commands=['start'])
def handle_start(message):
	# if len(bot.message_handlers) > 1:
	#     bot.message_handlers.pop()
	server.add_user(message.chat.id, message.chat.first_name, message.chat.last_name)
	if len(bot.pre_message_subscribers_next_step) > 0:
		bot.pre_message_subscribers_next_step.clear()
	# bot.send_message(message.chat.id, message.text)
	# users = server.get_groups(message.chat.id)
	# bot.send_message(message.chat.id, str(users))
	r = Menu("Root", "", bot).get_root()
	r.add_row("Enter room", handler.set_room, back_button=False)
	r.add_row("Skip", handler.main_menu, back_button=False)
	handler.start_menu(r)
	bot.send_message(message.chat.id, config.welcome_msg, reply_markup=r.make_keyboard())
	bot.register_next_step_handler(message, r.handler)
	# bot.message_handlers.clear()
	# r = Menu("Root", "", bot).get_root()
	# r.add_row("11Б", handler.choose_class, back_button=False) \
	# 	.append_column("11А", handler.choose_class, back_button=False)
	# r.add_row("10Б", handler.choose_class, back_button=False) \
	# 	.append_column("10А", handler.choose_class, back_button=False)
	# handler.start_menu(r)
	# msg = bot.send_message(message.chat.id, "Choose your class", reply_markup=r.make_keyboard())
	# bot.register_next_step_handler(msg, r.handler)
	return True


test_dict = {}


@bot.message_handler(content_types=['text'])
def handle_any(message):
	pass


# if test_dict.get(message.chat.id) is None:
# 	test_dict[message.chat.id] = True
# else:
# 	return
# if db.get_class(message.chat.id):
# 	root.handler(message)
# else:
# 	handle_start(message)


def send_message(id_list, text):
	for chat_id in id_list:
		bot.send_message(chat_id, text)
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
	while True:
		try:
			bot.polling(none_stop=True)
		except Exception as e:
			print(e)
			sleep(1)
