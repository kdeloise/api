from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import datetime
import calendar
import dbase


def reg_button():
	markup = InlineKeyboardMarkup()
	markup.row_width = 1
	markup.add(InlineKeyboardButton(text="Авторизация 🔑",
									callback_data="click_reg"))
	return markup


def back_to_main_menu():
	markup = InlineKeyboardMarkup()
	markup.row_width = 1
	markup.add(InlineKeyboardButton(text="↩Возврат в главное меню",
									callback_data="back_to_main"))
	return markup


def main_menu():
	markup = InlineKeyboardMarkup()
	markup.row_width = 1
	markup.add(InlineKeyboardButton(text="Передать ресурс",
									callback_data="send-resource"),
			   InlineKeyboardButton(text="Распределить ресурсы на проект",
									callback_data="choice_date_for_distribute"),
			   # callback_data="get-task"),
			   InlineKeyboardButton(text="Свободные ресурсы на сегодня",
									callback_data="free_dev"),
			   InlineKeyboardButton(text="Расписание",
									callback_data="сheck_schedule"))

	return markup


def main_menu_dev():
	markup = InlineKeyboardMarkup()
	markup.row_width = 1
	markup.add(InlineKeyboardButton(text="Мой график на сегодня",
									callback_data="check_schedule_today_dev"),
			   InlineKeyboardButton(text="Мой календарь",
									callback_data="check_schedule_calendar_dev"))
	return markup


def myrolle():
	markup = InlineKeyboardMarkup()
	markup.row_width = 2
	markup.add(InlineKeyboardButton(text="PM",
									callback_data="impm"),
			   InlineKeyboardButton(text="DEV",
									callback_data="imdev"))
	return markup


current_shown_dates = {}


def create_calendar(year, month, now_day, flag, flag_role, message):
	now = datetime.datetime.now()  # Текущая дата
	date = (now.year, now.month)
	markup = types.InlineKeyboardMarkup()
	# Первая дорожка - месяц и год
	row = []
	month_data = [" ", "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь",
				  "Ноябрь", "Декабрь"]
	row.append(types.InlineKeyboardButton(month_data[month] + " " + str(year),
										  callback_data="ignore"))
	markup.row(*row)
	# Вторая дорожка - дни недели
	week_days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
	row = []
	for day in week_days:
		row.append(types.InlineKeyboardButton(day,
											  callback_data="ignore"))
	markup.row(*row)
	# Остальные дорожки - дни
	my_calendar = calendar.monthcalendar(year, month)

	print(my_calendar)

	for week in my_calendar:
		row = []
		for day in week:
			if day == 0:
				row.append(types.InlineKeyboardButton(" ",
													  callback_data="ignore"))
			else:
				if flag_role:
					if (day >= int(now_day) and month == now.month) or (
							month > now.month and year == now.year) or year > now.year:
						check_date = str(day) + '/' + str(month) + '/' + str(year)
						if dbase.have_work(message, flag_role, check_date):
							row.append(types.InlineKeyboardButton(str(day) + '👨‍🎨',
																  callback_data="calendar-day-" + str(day) + '/' +
																				str(month) + '/' + str(year)))
						else:
							row.append(types.InlineKeyboardButton(str(day),
																  callback_data="calendar-day-" + str(day) + '/' +
																				str(month) + '/' + str(year)))
					else:
						row.append(types.InlineKeyboardButton(" ",
															  callback_data="ignore"))
				else:
					check_date = str(day) + '/' + str(month) + '/' + str(year)
					if dbase.have_work(message, flag_role, check_date):
						row.append(types.InlineKeyboardButton(str(day) + '👨‍💻',
															  callback_data="calendar-day-" + str(day) + '/' +
																			str(month) + '/' + str(year)))
					else:
						row.append(types.InlineKeyboardButton(str(day),
															  callback_data="calendar-day-" + str(day) + '/' +
																			str(month) + '/' + str(year)))
		markup.row(*row)
	# Последняя дорожка - кнопки
	row = []
	if flag_role:
		if year > date[0] or (year <= date[0] and month > date[1]):
			row.append(types.InlineKeyboardButton("⬅️",
												  callback_data="previous-month"))
		else:
			row.append(types.InlineKeyboardButton(" ",
												  callback_data="ignore"))
	else:
		row.append(types.InlineKeyboardButton("⬅️",
											  callback_data="previous-month"))
	if flag:
		row.append(types.InlineKeyboardButton("↩️",
											  callback_data="back_to_main"))
	else:
		row.append(types.InlineKeyboardButton("↩️",
											  callback_data="back_to_main"))
	row.append(types.InlineKeyboardButton("➡️",
										  callback_data="next-month"))
	markup.row(*row)
	return markup


def prj_button(user_id, soldate):
	prj = dbase.check_prj(user_id, soldate)
	print(prj)
	markup = InlineKeyboardMarkup()
	row = []
	for have in prj:
		row.append(types.InlineKeyboardButton(dbase.get_name_project(have[0]),
											  callback_data="tap-project" + str(have[0])))
	markup.row(*row)
	row = []
	row.append(types.InlineKeyboardButton("↩️",
										  callback_data="back_to_calendar"))
	markup.row(*row)
	return markup


def rsr_button(user_id, soldate, id_prj):
	rsr = dbase.check_rsr(user_id, soldate, id_prj)
	print(rsr)
	markup = InlineKeyboardMarkup()
	row = []
	i = 0
	for have in rsr:
		row.append(types.InlineKeyboardButton(dbase.get_name_resource(have),
											  callback_data="tap_resource" + str(have)))
	markup.row(*row)
	row = []
	row.append(types.InlineKeyboardButton("↩️",
										  callback_data="back_to_tap_project"))
	markup.row(*row)
	return markup


def hrs_button(user_id, hours, flag, id_dev):
	markup = InlineKeyboardMarkup()
	markup.row_width = 4
	i = 1
	row = []
	while i <= hours:
		if flag:
			row.append(types.InlineKeyboardButton(text=str(i) + "ч.",
												  callback_data="use_hours" + str(i)))
		else:
			row.append(types.InlineKeyboardButton(text=str(i) + "ч.",
												  callback_data="tap_hours" + str(i)))
		i += 1
		if i % 4 == 0:
			markup.row(*row)
			row = []
	if i % 4 != 0:
		markup.row(*row)
	row = []
	if flag:
		row.append(types.InlineKeyboardButton("↩️",
											  callback_data="back_to_project_for_distribute"))
	else:
		row.append(types.InlineKeyboardButton("↩️",
											  callback_data="back_to_tap_resource"))
	markup.row(*row)
	return markup


def get_list_pms(user_id, hours):
	print('glp')
	pms = dbase.check_pms(user_id)
	markup = InlineKeyboardMarkup()
	i = 0
	row = []
	for pm in pms:
		row.append(types.InlineKeyboardButton(pm,
											  callback_data="what-prj" + pm))
		i += 1
		if i % 2 == 0:
			markup.row(*row)
			row = []
	if i % 2 != 0:
		markup.row(*row)
	row = []
	row.append(types.InlineKeyboardButton("↩️",
										  callback_data="back_to_tap_hours"))
	markup.row(*row)
	return markup


def get_list_prj(user_id, pm_prjs):
	print(pm_prjs)
	markup = InlineKeyboardMarkup()
	i = 0
	row = []
	for pm in pm_prjs:
		prj = dbase.get_name_project(pm[0])
		row.append(types.InlineKeyboardButton(prj,
											  callback_data="update_schedule" + str(pm[0])))
		i += 1
		if i % 2 == 0:
			markup.row(*row)
			row = []
	if i % 2 != 0:
		markup.row(*row)
	row = []
	row.append(types.InlineKeyboardButton("↩️",
										  callback_data="back_to_what_prj"))
	markup.row(*row)
	return markup


def get_list_free_devs(user_id, list_devs):
	markup = InlineKeyboardMarkup()
	i = 0
	row = []
	for dev in list_devs:
		row.append(types.InlineKeyboardButton(dbase.get_name_resource(dev[0]) + ' ⏳ ' + str(dev[1]) + 'ч.',
											  callback_data="ignore"))
		i += 1
		if i % 2 == 0:
			markup.row(*row)
			row = []
	if i % 2 != 0:
		markup.row(*row)
	row = []
	row.append(types.InlineKeyboardButton("↩️",
										  callback_data="back_to_main"))
	markup.row(*row)
	return markup


def get_list_markups_of_projects_for_pm(user_id, list_of_prj_id):
	markup = InlineKeyboardMarkup()
	i = 0
	row = []
	for id_prj in list_of_prj_id:
		row.append(types.InlineKeyboardButton(dbase.get_name_project(id_prj),
											  callback_data="solution_amount_of_hours" + str(id_prj)))
		i += 1
		if i % 2 == 0:
			markup.row(*row)
			row = []
	if i % 2 != 0:
		markup.row(*row)
	row = []
	row.append(types.InlineKeyboardButton("↩️",
										  callback_data="back_to_resource_for_distribute"))
	markup.row(*row)
	return(markup)


def get_list_markups_of_resorces_for_pm(user_id, list_of_dev_name):
	markup = InlineKeyboardMarkup()
	i = 0
	row = []
	for dev in list_of_dev_name:
		row.append(types.InlineKeyboardButton(dbase.get_name_resource(dev),
											  callback_data="distribute-resource" + str(dev)))
		i += 1
		if i % 2 == 0:
			markup.row(*row)
			row = []
	if i % 2 != 0:
		markup.row(*row)
	row = []
	row.append(types.InlineKeyboardButton("↩️",
										  callback_data="back_to_calendar"))
	markup.row(*row)
	return(markup)
