from datetime import datetime
from multiprocessing import Process

import bot
import config
import listener

import server

test_dict = {}


def fill_data():
	tg_id = config.anton_tg_id
	assert (server.get_users() == [])
	assert (server.get_users(tg_id) is None)

	assert (server.add_user(tg_id, 'Anton', 'Prokopev'))
	assert (server.get_users(tg_id) == (tg_id, 'Anton', 'Prokopev', None))
	assert (server.get_users() == [(tg_id, 'Anton', 'Prokopev', None)])

	assert (server.add_user(10931724, 'Anton', 'Prokopev'))

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
	# Wipe all data from DB
	# Comment in realise
	server.wipe_data()

	bot.make_bot()

	# Comment in realise
	fill_data()

	# Scheduler for recent notifications
	p = Process(target=server.start_scheduler, args=())
	p.start()

	# Scheduler for sending a schedule every day
	# param#1 = hour, param#2 = minute
	p1 = Process(target=server.yet_another_scheduler, args=(14, 15,))
	p1.start()

	# Web listener for web-morda
	p2 = Process(target=listener.run, args=(True,))
	p2.start()

	# Start bot
	bot.start_polling()
