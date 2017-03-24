import time
from datetime import datetime

import config

import server
import bot


#
# @bot.message_handler(commands=['start'])
# def handle_start(message):
# 	# if len(bot.message_handlers) > 1:
# 	#     bot.message_handlers.pop()
# 	if len(bot.pre_message_subscribers_next_step) > 0:
# 		bot.pre_message_subscribers_next_step.clear()
# 		# bot.message_handlers.clear()
# 	r = Menu("Root", "", bot).get_root()
# 	r.add_row("11Б", handler.choose_class, back_button=False) \
# 		.append_column("11А", handler.choose_class, back_button=False)
# 	r.add_row("10Б", handler.choose_class, back_button=False) \
# 		.append_column("10А", handler.choose_class, back_button=False)
# 	handler.start_menu(r)
# 	msg = bot.send_message(message.chat.id, "Choose your class", reply_markup=r.make_keyboard())
# 	bot.register_next_step_handler(msg, r.handler)
# 	return True
#
# test_dict = {}
#
#
# @bot.message_handler(content_types=['text'])
# def handle_any(message):
# 	if test_dict.get(message.chat.id) is None:
# 		test_dict[message.chat.id] = True
# 	else:
# 		return
# 	if db.get_class(message.chat.id):
# 		root.handler(message)
# 	else:
# 		handle_start(message)
#
#
# def testt(msg):
# 	bot.send_message(msg.chat.id, "LIST CALLBACK!")
#

def questions_test():
	tg_id = config.anton_tg_id
	assert (server.get_users() == [])
	assert (server.get_users(tg_id) is None)

	assert (server.add_user(tg_id, 'Anton', 'Prokopev'))
	assert (server.get_users(tg_id) == (tg_id, 'Anton', 'Prokopev', None))
	assert (server.get_users() == [(tg_id, 'Anton', 'Prokopev', None)])
	# assert (server.set_room(tg_id, '1-306'))
	# assert (server.get_users(tg_id) == (tg_id, 'Anton', 'Prokopev', '1-306'))

	assert (server.add_user(10931724, 'Anton', 'Prokopev'))
	# assert (server.get_users() == [(tg_id, 'Anton', 'Prokopev', '1-306'), (10931724, 'Anton', 'Prokopev', None)])

	assert (server.remove_group(1))
	id_group = server.add_group('Holiday party')
	assert id_group
	assert server.add_team(id_group, '1234')
	assert server.add_users_to_group(id_group, [tg_id, 10931724])
	print(server.get_groups(tg_id))

	assert (server.remove_event(1))
	id_events = [server.add_event('Holiday', datetime.now().timestamp(), datetime.now().timestamp(), '123'),
				 server.add_event('Holiday2', datetime.now().timestamp(), datetime.now().timestamp() + 3600, '113'),
				 server.add_event('H3', datetime.now().timestamp() + 84600, datetime.now().timestamp() + 84600, '115')]
	assert (id_events != [])
	assert server.add_events_to_group(id_group, id_events)
	print(server.get_events(id_group))

	assert (server.remove_question(1))
	id_questions = [server.add_question(0, 'asd', 'asqwe'), server.add_question(1, 'asd', 'asqwe')]
	assert id_questions != []
	server.add_questions_to_team(id_group, id_questions)
	print(server.get_questions(id_group))

	id_achievement = server.add_achievement('Top 5', 'the best man')
	assert id_achievement
	assert (server.set_achievement_to_user(id_achievement, tg_id))
	print(server.get_achievements(tg_id))

	print(server.get_schedule(tg_id, datetime.now()))

	server.send_messages_by_ids([config.anton_tg_id], '/start')


if __name__ == '__main__':
	server.wipe_data()
	questions_test()

	bot.make_bot()
	bot.start_polling()
# print(server.get_start_end_date(datetime.now()))

# menu = Menu("Root", "ROOT", bot)
# handler = Handler(bot, menu)
# menu.set_back("Back")
# menu.set_wrong("Try again")
# root = menu.get_root()
# root.add_row("Get schedule", handler.get_schedule).add_row("Schedule changes", handler.get_schedule_changes)
# root.add_row("Get class", handler.get_class)
# root.add_row("Change class", handle_start)
#
# db = Database()
# # controller = Controller(config.spreadsheet_id)
# # print(controller.get_classes())
# # print(parser.get_schedule('10Б'))
# while True:
# 	try:
# 		bot.polling(none_stop=True)
# 	except Exception as e:
# 		print(e)
# 		time.sleep(10)
