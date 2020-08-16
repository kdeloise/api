#!/usr/bin/env python3
# coding=utf-8
import dbase
import time
import random
import datetime
import telebot
from telebot import apihelper
import markups as markup
import re
import config
import cherrypy


TK = config.TOKEN1
bot = telebot.TeleBot(TK)
# apihelper.proxy = {
# 	"https": "socks5://voltmobi:9tr4vm49@socks.vmb.co:1080"
# # }
# apihelper.proxy = {
# 	"https": "https://34.90.113.143:3128"
# }


WEBHOOK_HOST = '46.17.105.214'
WEBHOOK_PORT= 88  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN= '46.17.105.214'  # На некоторых серверах придется указывать такой же IP, что и выше​
WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Путь к сертификату
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Путь к приватному ключу
WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (TK)


class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)



def salutation(name):
	now_time = datetime.datetime.now().strftime("%H:%M")
	if '00:00' <= now_time <= '05:59':
		msg = "Доброй ночи, {}".format(name)
	elif '06:00' <= now_time <= '11:59':
		msg = "Доброе утро, {}".format(name)
	elif '12:00' <= now_time <= '17:59':
		msg = "Добрый день, {}".format(name)
	elif '18:00' <= now_time <= '23:59':
		msg = "Добрый вечер, {}".format(name)
	return msg

@bot.message_handler(commands=["start"])
def start(message):
	# dbase.delete_duplicate_from_schedule()
	dbase.del_unuse_rows()
	result = dbase.check_user_exist_pir(message.chat.id)
	if result is True:
		name = dbase.get_user_name(message.chat.id)
		msg = salutation(name)
		if dbase.check_user_pmtable(message.chat.id):
			dict_flag_role_pm[message.chat.id] = True
			bot.send_message(message.chat.id, text=msg,
							 reply_markup=markup.main_menu())
		elif dbase.check_user_devtable(message.chat.id):
			dict_flag_role_pm[message.chat.id] = False
			bot.send_message(message.chat.id, text=msg,
							 reply_markup=markup.main_menu_dev())
		else:
			bot.send_message(message.chat.id, name + ", ваша роль в компании пока не определена!",
							 reply_markup=markup.myrolle())

	else:
		txt = "Здраствуйте!\nПрежде, чем мы начнем, авторизуйтесь.\n"
		bot.send_message(message.chat.id, text=txt,
						 reply_markup=markup.reg_button())




@bot.callback_query_handler(func=lambda call: call.data[:10] == 'next-month')
def next_month(call):
	now = datetime.datetime.now()
	user_id = call.message.chat.id
	saved_date = current_shown_dates.get(user_id)
	if saved_date is not None:
		year, month = saved_date
		month += 1
		if month > 12:
			month = 1
			year += 1
		date = (year, month)
		current_shown_dates[user_id] = date
		bot.edit_message_text("Выберите, дату:", call.from_user.id, call.message.message_id,
							  reply_markup=markup.create_calendar(year, month, now.day, dict_flag_dist[call.message.chat.id],
																  dict_flag_role_pm[call.message.chat.id], call.message))
		bot.answer_callback_query(call.id, text="Следующий месяц")
	else:
		# Do something to inform of the error
		pass

@bot.callback_query_handler(func=lambda call: call.data[:12] == 'back_to_main')
def back_to_main(call):
	user_id = call.message.chat.id
	name = dbase.get_user_name(user_id)
	msg = salutation(name)
	if dbase.check_user_pmtable(user_id):
		bot.delete_message(call.message.chat.id, call.message.message_id)
		bot.send_message(user_id, text=msg,
						 reply_markup=markup.main_menu())
	elif dbase.check_user_devtable(user_id):
		bot.delete_message(call.message.chat.id, call.message.message_id)
		bot.send_message(user_id, text=msg,
						 reply_markup=markup.main_menu_dev())

def get_calendar(message):
	user_id = message.chat.id
	now = datetime.datetime.now()  # Текущая дата
	date = (now.year, now.month)
	current_shown_dates[user_id] = date  # сохраняю данные в словарь
	bot.send_message(message.chat.id, "Выберите, дату:\n",
					 reply_markup=markup.create_calendar(now.year, now.month, now.day, dict_flag_dist[message.chat.id],
														 dict_flag_role_pm[message.chat.id], message))

@bot.callback_query_handler(func=lambda call: call.data[:14] == 'previous-month')
def previous_month(call):
	now = datetime.datetime.now()
	user_id = call.message.chat.id
	saved_date = current_shown_dates.get(user_id)
	if saved_date is not None:
		year, month = saved_date
		month -= 1
		if month < 1:
			month = 12
			year -= 1
		date = (year, month)
		current_shown_dates[user_id] = date
		bot.edit_message_text("Выберите, дату:", call.from_user.id, call.message.message_id,
							  reply_markup=markup.create_calendar(year, month, now.day, dict_flag_dist[call.message.chat.id],
																  dict_flag_role_pm[call.message.chat.id], call.message))
		bot.answer_callback_query(call.id, text="Предыдущий месяц")
	else:
		# Do something to inform of the error
		pass




def add_in_devtable(message):
	bot.delete_message(message.chat.id, message.message_id)
	dbase.reg_dev(message.chat.id)
	start(message)

@bot.callback_query_handler(func=lambda call: call.data[:5] == 'imdev')
def registrationdev(call):
	add_in_devtable(call.message)




def add_in_pmtable(message):
	bot.delete_message(message.chat.id, message.message_id)
	dbase.reg_pm(message.chat.id)
	start(message)

@bot.callback_query_handler(func=lambda call: call.data[:4] == 'impm')
def registrationpm(call):
	add_in_pmtable(call.message)




def pls_true_data(message, id):
	if id == 1:
		msg = bot.send_message(message.chat.id, text='Необходимо корректно ввести имя!'
													 '\nДопускается латиница и кириллица.'
													 '\nЦифры и спец-символы запрещенны.'
													 '\n\nВаше имя:')
		bot.register_next_step_handler(msg, get_user_name)
	elif id == 0:
		txt = 'Пожалуйста введите данные в текстовом формате!\n\nВаше имя:'
		msg = bot.send_message(message.chat.id, txt)
		bot.register_next_step_handler(msg, get_user_name)

def get_user_name(message):
	if message.content_type == 'text':
		name = message.text
		regex = re.compile(r"^[a-zA-Zа-яА-Я]{2,}([- ][a-zA-Zа-яА-Я]{2,})?$")
		if regex.findall(name):
			bot.delete_message(message.chat.id, message.message_id)
			dbase.reg_user(message.chat.id, name, message.chat.username)
			bot.send_message(message.chat.id, "Ваша роль в компании:\n",
							 reply_markup=markup.myrolle())
		else:
			pls_true_data(message, 1)
	else:
		bot.delete_message(message.chat.id, message.message_id)
		pls_true_data(message, 0)

def get_user_data(message):
	bot.delete_message(message.chat.id, message.message_id)
	msg = bot.send_message(message.chat.id, "Ваше имя:")
	bot.register_next_step_handler(msg, get_user_name)

@bot.callback_query_handler(func=lambda call: call.data[:9] == 'click_reg')
def registration(call):
	get_user_data(call.message)




def start_send_resource(message):
	# bot.delete_message(message.chat.id, message.message_id)
	get_calendar(message)

@bot.callback_query_handler(func=lambda call: call.data[:14] == 'send-resource')
def send_resource(call):
	dict_flag_check_schedule_for_pm[call.message.chat.id] = False
	dict_flag_dist[call.message.chat.id] = False
	dict_flag_check_schedule_for_dev[call.message.chat.id] = False
	bot.delete_message(call.message.chat.id, call.message.message_id)
	start_send_resource(call.message)




def str_for_schedule_dev_message(id_dev, nowdate):
	stroka = '📆' + nowdate
	stroka += '\n👨‍💻' + dbase.get_name_resource(id_dev) + '\n' + '📌️' * 8
	list_of_pph = dbase.get_list_of_prj_hours(id_dev, nowdate)
	for ls in list_of_pph:
		stroka += dbase.get_str_for_info_for_dev(ls[0], ls[1], ls[2])
	return stroka




def str_for_schedule_pm_message(message, nowdate):
	id_pm = dbase.get_pm_sqlid(message.chat.id)
	stroka = '📆' + nowdate
	stroka += '\n👨‍🎨: ' + dbase.get_name_pm(id_pm) + '\n' + '📌️' * 8
	list_of_pdh = dbase.get_list_of_prj_dev_hours(id_pm, nowdate)
	for ls in list_of_pdh:
		stroka += dbase.get_str_for_info(ls[0], ls[1], ls[2])
	return stroka




@bot.callback_query_handler(func=lambda call: call.data[:16] == 'back_to_calendar')
def back_to_calendar(call):
	bot.delete_message(call.message.chat.id, call.message.message_id)
	get_calendar(call.message)

def check_date_for_schedule_pm(message, date_for_schedule_pm):
	id_pm = dbase.get_pm_sqlid(message.chat.id)
	prj_dev_hours = dbase.get_list_of_prj_dev_hours(id_pm, date_for_schedule_pm)
	print('_________prj_dev_hours______Ты меня видишь?______prj_dev_hours___')
	stroka = str_for_schedule_pm_message(message, date_for_schedule_pm)
	if not prj_dev_hours:
		bot.delete_message(message.chat.id, message.message_id)
		bot.send_message(message.chat.id, "📆" + date_for_schedule_pm + "\nСвободный день!😳",
						 reply_markup=markup.back_to_main_menu())
	else:
		print(prj_dev_hours)
		bot.delete_message(message.chat.id, message.message_id)
		bot.send_message(message.chat.id, stroka,
						 reply_markup=markup.back_to_main_menu())

def next_check_dev_for_distribute(message):
	array_of_devs_id = dbase.list_id_of_dev()
	array_of_devs_name = []
	for id in array_of_devs_id:
		array_of_devs_name.append(id)
	bot.send_message(message.chat.id, 'Выберите ресурс!',
					 reply_markup=markup.get_list_markups_of_resorces_for_pm(message.chat.id, array_of_devs_name))

def check_dev_for_distribute(message, check_date):
	dict_distribute_date[message.chat.id] = check_date
	next_check_dev_for_distribute(message)

@bot.callback_query_handler(func=lambda call: call.data[:31] == 'back_to_resource_for_distribute')
def back_to_project_for_distribute(call):
	bot.delete_message(call.message.chat.id, call.message.message_id)
	next_check_dev_for_distribute(call.message)

def get_projects(message, check):
	dict_for_schedule[message.chat.id] = check
	print('DICTIONAARY')
	print(dict_for_schedule)
	now = datetime.datetime.now()
	bot.delete_message(message.chat.id, message.message_id)
	if not dbase.checkdate(message, check):
		bot.send_message(message.chat.id, 'Выберите другую дату!'
										  '\nНа эту дату у вас нет ресурсов')
		bot.send_message(message.chat.id, "Выберите, дату:\n",
						 reply_markup=markup.create_calendar(now.year, now.month, now.day, dict_flag_dist[message.chat.id],
															 dict_flag_role_pm[message.chat.id], message))
	else:
		bot.send_message(message.chat.id, "Выберите, проект:\n",
						 reply_markup=markup.prj_button(message.chat.id, check))

@bot.callback_query_handler(func=lambda call: call.data[:13] == 'calendar-day-')
def check_day(call):
	print(call.data[13:])
	if dict_flag_dist[call.message.chat.id]:
			check_dev_for_distribute(call.message, call.data[13:])
	else:
		if dict_flag_check_schedule_for_pm[call.message.chat.id]:
			print('___________________________Ты меня видишь?_______________________')
			check_date_for_schedule_pm(call.message, call.data[13:])
		elif dict_flag_check_schedule_for_dev[call.message.chat.id]:
			print('_____________________________дай расписание я же разраб')
			check_schedule_dev(call.message, call.data[13:])
		else:
			print('___________________________НЕ ВИЖУ?_______________________')
			get_projects(call.message, call.data[13:])




@bot.callback_query_handler(func=lambda call: call.data[:19] == 'back_to_tap_project')
def back_to_tap_project(call):
	get_projects(call.message, dict_for_schedule[call.message.chat.id])

def get_resource(message, id_prj):
	dict_from_prj[message.chat.id] = int(id_prj)
	bot.send_message(message.chat.id, "Выберите, ресурс:\n",
					 reply_markup=markup.rsr_button(message.chat.id, dict_for_schedule[message.chat.id], id_prj))

@bot.callback_query_handler(func=lambda call: call.data[:11] == 'tap-project')
def check_projects(call):
	bot.delete_message(call.message.chat.id, call.message.message_id)
	get_resource(call.message, call.data[11:])




@bot.callback_query_handler(func=lambda call: call.data[:20] == 'back_to_tap_resource')
def back_to_tap_resource(call):
	bot.delete_message(call.message.chat.id, call.message.message_id)
	get_resource(call.message, dict_from_prj[call.message.chat.id])

def get_hours(message, resource):
	bot.delete_message(message.chat.id, message.message_id)
	dict_dev[message.chat.id] = int(resource)
	# con = dbase.open_base()
	# cur = con.cursor()
	# command = "SELECT projects, clock from day_plan where \
	#             (dev_name = '{}' and projects = '{}')".format(resource, dbase.check_prj(message.chat.id)[0][0])
	# cur.execute(command)
	# rows = cur.fetchall()
	# stroka = '👨‍💻' + resource + '\n'
	# for row in rows:
	#     stroka += '📁:' + row[0] + '\n'
	#     stroka += '⌛️️: ' + str(row[1]) + 'ч.\n'
	if dbase.amount_of_resource(message, resource, dict_for_schedule[message.chat.id]):
		stroka = dbase.amount_of_resource(message, resource, dict_for_schedule[message.chat.id])
		print("Доступное время:")
		print(int(re.findall('(\d+)', stroka)[0]))
		bot.send_message(message.chat.id, stroka + "\nСКОЛЬКО ЧАСОВ ГОТОВЫ ПЕРЕДАТЬ?",
						 reply_markup=markup.hrs_button(message.chat.id, int(re.findall('(\d+)', stroka)[0]), dict_flag_dist[message.chat.id],
														dict_dev[message.chat.id]))
	else:
		bot.send_message(message.chat.id, 'Данный ресурс не задействован!'
										  '\nВыберите другой ресурс',
						 reply_markup=markup.rsr_button(message.chat.id, dict_for_schedule[message.chat.id]))

@bot.callback_query_handler(func=lambda call: call.data[:12] == 'tap_resource')
def check_projects(call):
	get_hours(call.message, call.data[12:])




@bot.callback_query_handler(func=lambda call: call.data[:17] == 'back_to_tap_hours')
def back_to_tap_hours(call):
	get_hours(call.message, dict_dev[call.message.chat.id])

def send_hours(message, hours):
	totalhours[message.chat.id] = int(hours)
	bot.delete_message(message.chat.id, message.message_id)
	msg = "Кому передать ресурс?"
	bot.send_message(message.chat.id, msg,
					 reply_markup=markup.get_list_pms(message.chat.id, hours))
	print(current_shown_dates)

@bot.callback_query_handler(func=lambda call: call.data[:9] == 'tap_hours')
def tap_hours(call):
	print('===============')
	send_hours(call.message, call.data[9:])




@bot.callback_query_handler(func=lambda call: call.data[:16] == 'back_to_what_prj')
def back_to_what_prj(call):
	send_hours(call.message, totalhours[call.message.chat.id])

def what_prj(message, pm):
	bot.delete_message(message.chat.id, message.message_id)
	dict_to_pm[message.chat.id] = dbase.get_pmid(pm)
	pm_prjs = dbase.pm_prj(pm)
	msg = "Выберите проект:"
	bot.send_message(message.chat.id, msg,
					 reply_markup=markup.get_list_prj(message.chat.id, pm_prjs))
	print(totalhours)
	print('vvvvvvv')
	print(dict_dev)
	print('vvvvvvv')
	print(dict_from_prj)

@bot.callback_query_handler(func=lambda call: call.data[:8] == 'what-prj')
def get_task(call):
	print('++++++++++++')
	print(call.data)
	print('++++++++++++')
	what_prj(call.message, call.data[8:])




def update_schedule(message, id_prj):
	bot.delete_message(message.chat.id, message.message_id)
	id_dev = dict_dev[message.chat.id]
	tg_id_dev = dbase.get_dev_tgid(id_dev)
	id_prj_from = dict_from_prj[message.chat.id]
	sendhours = totalhours[message.chat.id]
	id_to_pm = dict_to_pm[message.chat.id]
	tg_id_to_pm = dbase.get_pm_tgid(id_to_pm)
	id_from_pm = dbase.get_pm_sqlid(message.chat.id)
	mydate = dict_for_schedule[message.chat.id]
	dbase.update_base(message, mydate, int(id_prj), id_dev, id_prj_from, sendhours, id_to_pm)
	bot.send_message(message.chat.id, 'Ресурс передан!!',
					 reply_markup=markup.back_to_main_menu())
	bot.send_message(tg_id_dev, 'Ваше расписание на 📆' + mydate + ' сменилось\n'
								'ПМ:👨‍🎨{} сместил ⏳{}ч. Вас с проекта #{} на проект #{}\n'
								'Проверьте свое расписание!!!'.format(dbase.get_name_pm(id_from_pm), sendhours, dbase.get_name_project(id_prj_from), dbase.get_name_project(int(id_prj))))
	bot.send_message(tg_id_to_pm,	"Ваше расписание на {} сменилось\n"
									"ПМ:👨‍🎨{} передал Вам на ⏳{}ч. 👨‍💻:{} на проект #{}\n"
									"Проверьте свое расписание!!!".format(mydate, dbase.get_name_pm(id_from_pm), dbase.get_name_resource(id_dev),
																		  sendhours, dbase.get_name_project(id_prj)))


@bot.callback_query_handler(func=lambda call: call.data[:15] == 'update_schedule')
def update(call):
	update_schedule(call.message, call.data[15:])



@bot.callback_query_handler(func=lambda call: call.data[:8] == 'free_dev')
def free_dev(call):
	bot.delete_message(call.message.chat.id, call.message.message_id)
	now = datetime.datetime.now()
	nowdate = str(now.day)
	nowdate += '/' + str(now.month)
	nowdate += '/' + str(now.year)
	free_devs = dbase.not_busy_dev(nowdate)
	bot.send_message(call.message.chat.id, 'Свободные ресурсы на сегодня!!!\n'
										   'Оставшееся кол-во часов',
					 reply_markup=markup.get_list_free_devs(call.message.chat.id, free_devs))


def next_list_of_prj_for_distribute(message):
	prjs = dbase.pm_prj_for_dist(message.chat.id)
	list_of_prj_id = []
	print("PRJSSSSSSSSSSSSSSSSSSSSSS")
	print(prjs)
	for prj in prjs:
		list_of_prj_id.append(prj[0])
	bot.send_message(message.chat.id, 'Выберите проект:',
					 reply_markup=markup.get_list_markups_of_projects_for_pm(message.chat.id, list_of_prj_id))

@bot.callback_query_handler(func=lambda call: call.data[:19] == 'distribute-resource')
def  list_of_prj_for_distribute(call):
	dict_distribute_dev[call.message.chat.id] = call.data[19:]
	bot.delete_message(call.message.chat.id, call.message.message_id)
	next_list_of_prj_for_distribute(call.message)

@bot.callback_query_handler(func=lambda call: call.data[:30] == 'back_to_project_for_distribute')
def back_to_project_for_distribute(call):
	bot.delete_message(call.message.chat.id, call.message.message_id)
	next_list_of_prj_for_distribute(call.message)




@bot.callback_query_handler(func=lambda call: call.data[:22] == 'project_for_distribute')
def project_for_distribute(call):
	bot.delete_message(call.message.chat.id, call.message.message_id)
	dict_distribute_dev[call.message.chat.id] = call.data[22:]
	check_dev_for_distribute(call.message, call.data[22:])




@bot.callback_query_handler(func=lambda call: call.data[:26] == 'choice_date_for_distribute')
def choice_date_for_distribute(call):
	dict_flag_check_schedule_for_pm[call.message.chat.id] = False
	dict_flag_check_schedule_for_dev[call.message.chat.id] = False
	dict_flag_dist[call.message.chat.id] = True
	message = call.message
	bot.delete_message(message.chat.id, message.message_id)
	# dict_distribute_dev[message.chat.id] = call.data[26:]
	get_calendar(call.message)




def update_schedule_for_distribute(message):
	# bot.delete_message(message.chat.id, message.message_id)
	id_from_pm = dbase.get_pm_sqlid(message.chat.id)
	id_dev = dict_distribute_dev[message.chat.id]
	tg_id_dev = dbase.get_dev_tgid(id_dev)
	id_prj = dict_distribute_prj[message.chat.id]
	usehours = dict_distribute_hours[message.chat.id]
	usedate = dict_distribute_date[message.chat.id]
	dbase.update_base_distribute(message, usedate, id_prj, id_dev, usehours)
	bot.send_message(tg_id_dev, "У вас новая задача на 📆{}\n"
								"ПМ:👨‍🎨{} добавил Вам ⏳{}ч. на проект #{}\n"
								"Проверьте свое расписание!!!".format(usedate, dbase.get_name_pm(id_from_pm), usehours, dbase.get_name_project(id_prj)))
	bot.send_message(message.chat.id, 'Задача поставлена!!!',
					 reply_markup=markup.back_to_main_menu())

@bot.callback_query_handler(func=lambda call: call.data[:9] == 'use_hours')
def use_hours(call):
	message = call.message
	bot.delete_message(message.chat.id, message.message_id)
	dict_distribute_hours[message.chat.id] = int(call.data[9])
	update_schedule_for_distribute(message)



@bot.callback_query_handler(func=lambda call: call.data[:24] == 'solution_amount_of_hours')
def check_date_for_distribute(call):
	message = call.message
	id_rpj = call.data[24:]
	id_dev = dict_distribute_dev [message.chat.id]
	dict_distribute_prj[message.chat.id] = int(id_rpj)
	pdhs = dbase.check_amount_of_housr_dev(dict_distribute_date[message.chat.id], int(id_dev))
	bot.delete_message(message.chat.id, message.message_id)
	if 8 - pdhs == 0:
		bot.send_message(message.chat.id, "Данный ресурс полностью загружен сегодня!!!",
						 reply_markup=markup.hrs_button(message.chat.id, int(8 - pdhs), dict_flag_dist[message.chat.id],
														id_dev))
	else:
		bot.send_message(message.chat.id, "У данного ресурса осталось " + str(8 - pdhs) + 'ч. на данную дату\n'
																						  'На сколько часов вы хотите занять данный ресурс?\n',
						 reply_markup=markup.hrs_button(message.chat.id, int(8 - pdhs), dict_flag_dist[message.chat.id],
														id_dev))




@bot.callback_query_handler(func=lambda call: call.data[:14] == 'сheck_schedule')
def check_schedule(call):
	dict_flag_dist[call.message.chat.id] = False
	dict_flag_check_schedule_for_dev[call.message.chat.id] = False
	message = call.message
	dict_flag_check_schedule_for_pm[message.chat.id] = True
	bot.delete_message(message.chat.id, message.message_id)
	get_calendar(message)




def check_schedule_dev(message, date):
	id_dev = dbase.get_dev_sqlid_by_tgid(message.chat.id)
	stroka = str_for_schedule_dev_message(id_dev, date)
	prj_hours = dbase.get_list_of_prj_hours(id_dev, date)
	if not prj_hours:
		bot.delete_message(message.chat.id, message.message_id)
		bot.send_message(message.chat.id, "📆" + date + "\nСвободный день!😳",
						 reply_markup=markup.back_to_main_menu())
	else:
		print(prj_hours)
		bot.delete_message(message.chat.id, message.message_id)
		bot.send_message(message.chat.id, stroka,
						 reply_markup=markup.back_to_main_menu())

@bot.callback_query_handler(func=lambda call: call.data[:24] == 'check_schedule_today_dev')
def check_schedule_today_dev(call):
	dict_flag_check_schedule_for_pm[call.message.chat.id] = False
	dict_flag_dist[call.message.chat.id] = False
	dict_flag_check_schedule_for_dev[call.message.chat.id] = True
	message = call.message
	now = datetime.datetime.now()
	nowdate = str(now.day)
	nowdate += '/' + str(now.month)
	nowdate += '/' + str(now.year)
	print('NOWDATE___________________{}___________________NOWDATE'.format(nowdate))
	check_schedule_dev(message, nowdate)




@bot.callback_query_handler(func=lambda call: call.data[:27] == 'check_schedule_calendar_dev')
def check_schedule_calendar_dev(call):
	message = call.message
	dict_flag_check_schedule_for_pm[message.chat.id] = False
	dict_flag_dist[call.message.chat.id] = False
	dict_flag_check_schedule_for_dev[message.chat.id] = True
	bot.delete_message(message.chat.id, message.message_id)
	get_calendar(message)



current_shown_dates = {}
dict_for_schedule = {}
totalhours = {}
dict_dev = {}
dict_from_prj = {}
dict_to_pm = {}

dict_distribute_prj = {}
dict_distribute_dev = {}
dict_distribute_hours = {}
dict_distribute_date = {}
dict_flag_dist = {}
dict_flag_check_schedule_for_pm = {}
dict_flag_check_schedule_for_dev = {}
dict_flag_role_pm = {}


bot.remove_webhook()

bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})

# Собственно, запуск!
cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})

# while True:
# 	try:
# 		bot.polling(none_stop=True)
# 	except Exception as e:
# 		print(e)
# 		# повторяем через 15 секунд в случае недоступности сервера Telegram
# 		time.sleep(15)
