import time
from datetime import datetime
import sched
from multiprocessing import Pool, Process
import config
import server
import bot
import hashlib
import listener


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

def do_something():
	print(123)


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

	assert (server.remove_event(1))
	id_events = [server.add_event('Holiday', datetime.now().timestamp(), datetime.now().timestamp(), '123'),
				 server.add_event('Holiday2', datetime.now().timestamp(), datetime.now().timestamp() + 3600, '113'),
				 server.add_event('H3', datetime.now().timestamp() + 960, datetime.now().timestamp() + 84600, '115')]
	assert (id_events != [])
	assert server.add_events_to_group(id_group, id_events)

	assert (server.remove_question(1))
	id_questions = [server.add_question(0, 'question1', '123'), server.add_question(1, 'question2', '234')]
	assert id_questions != []
	server.add_questions_to_team(id_group, id_questions)

	server.add_reference_information('Number1', '8999999999')
	server.add_reference_information('Number2', '9888888888')

	id_achievement = server.add_achievement('Top 5', 'the best man')
	assert id_achievement
	assert (server.set_achievement_to_user(id_achievement, tg_id))

	server.send_messages_by_ids([config.anton_tg_id], '/start')


if __name__ == '__main__':
	pass
	server.wipe_data()
	bot.make_bot()
	questions_test()
	p = Process(target=server.start_scheduler, args=())
	d = datetime(hour=1, minute=30, year=1970, month=1, day=1)
	p1 = Process(target=server.yet_another_scheduler, args=(d,))
	p2 = Process(target=listener.run, args=())
	p.start()
	p1.start()
	p2.start()
	bot.start_polling()
	# server.start_scheduler()
