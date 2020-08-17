#!/usr/bin/env python3
# coding=utf-8
import psycopg2
import config


# ПОДКЛЮЧАЕМСЯ К БАЗЕ ДАННЫХ
def open_base():
	con = psycopg2.connect(
		database=config.DATABASE["database"],
		user=config.DATABASE["user"],
		password=config.DATABASE["password"],
		host=config.DATABASE["host"],
		port=config.DATABASE["port"]
	)
	print("Database opened successfully")
	return con


def get_username_of_tg(tg_id):
	command = "SELECT username from lstusers where tgid={}".format(tg_id)
	con = open_base()
	cur = con.cursor()
	cur.execute(command)
	tg_username = cur.fetchall()[0]
	con.close()
	return tg_username


def not_busy_dev(checkdate):
	row_of_dev = get_list_of_id_devs()
	array_len = len(row_of_dev)
	command = "SELECT id_dev, hours from schedule where lstdate = '{}'".format(checkdate)
	con = open_base()
	cur = con.cursor()
	cur.execute(command)
	dev_date = cur.fetchall()
	row = []
	tuple = []
	i = 0
	j = 0
	while i < array_len:
		# j += i
		hours = 8
		while j < len(dev_date):
			if row_of_dev[i] == dev_date[j][0]:
				hours -= dev_date[j][1]
			j += 1
		j = 0;
		row = [row_of_dev[i], hours]
		if row:
			tuple.append(row)
		row = []
		i += 1
	con.close()
	return tuple


def get_list_of_id_devs():
	command = "SELECT id from dev_table"
	con = open_base()
	cur = con.cursor()
	cur.execute(command)
	all_dev = cur.fetchall()
	row = []
	for dev in all_dev:
		row.append(dev[0])
	con.close()
	return row


def get_list_of_id_prjs():
	command = "SELECT id from prj_table"
	con = open_base()
	cur = con.cursor()
	cur.execute(command)
	all_prj = cur.fetchall()
	row = []
	for id_prj in all_prj:
		row.append(id_prj[0])
	con.close()
	return row


def get_list_of_id_pms():
	command = "SELECT id from pm_table"
	con = open_base()
	cur = con.cursor()
	cur.execute(command)
	all_pms = cur.fetchall()
	row = []
	for id_pm in all_pms:
		row.append(id_pm[0])
	con.close()
	return row


# def get_pm_sqlid_by_user_id(user_id):
# 	command = "SELECT id from pm_table where tg_id = '{}'".format(user_id)
# 	con = open_base()
# 	cur = con.cursor()
# 	cur.execute(command)
# 	pm_id = cur.fetchall()
# 	con.close()
# 	return pm_id[0][0]


def get_pm_sqlid(user_id):
	get_pm_id_command = "SELECT id from pm_table where tg_id={}".format(user_id)
	con = open_base()
	cur = con.cursor()
	cur.execute(get_pm_id_command)
	pm_id = cur.fetchall()
	con.close()
	return pm_id[0][0]


def get_dev_sqlid_by_tgid(user_id):
	get_dev_id_command = "SELECT id from dev_table where tg_id={}".format(user_id)
	con = open_base()
	cur = con.cursor()
	cur.execute(get_dev_id_command)
	dev_id = cur.fetchall()
	con.close()
	return dev_id[0][0]


def get_pmid(name_pm):
	print(name_pm)
	get_pmid_command = "SELECT id from pm_table where pm = '{}'".format(name_pm)
	con = open_base()
	cur = con.cursor()
	cur.execute(get_pmid_command)
	pm_name = cur.fetchall()
	con.close()
	print(pm_name[0][0])
	return pm_name[0][0]


def get_name_pm(id_pm):
	get_name_command = "SELECT pm from pm_table where id={}".format(id_pm)
	con = open_base()
	cur = con.cursor()
	cur.execute(get_name_command)
	pm_name = cur.fetchall()
	con.close()
	return pm_name[0][0]


def get_name_resource(id_dev):
	print('id_dev:' + str(id_dev))
	get_name_command = "SELECT dev from dev_table where id={}".format(id_dev)
	con = open_base()
	cur = con.cursor()
	cur.execute(get_name_command)
	dev_name = cur.fetchall()
	con.close()
	return dev_name[0][0]


def get_name_project(id_prj):
	get_name_command = "SELECT prj from prj_table where id={}".format(id_prj)
	con = open_base()
	cur = con.cursor()
	cur.execute(get_name_command)
	prj_name = cur.fetchall()
	con.close()
	return prj_name[0][0]


def get_dev_tgid(id_dev):
	get_dev_tgid_command = "SELECT tg_id from dev_table where id = {}".format(id_dev)
	con = open_base()
	cur = con.cursor()
	cur.execute(get_dev_tgid_command)
	dev_id = cur.fetchall()
	con.close()
	return dev_id[0][0]


def get_pm_tgid(id_pm):
	pm_dev_tgid_command = "SELECT tg_id from pm_table where id = {}".format(id_pm)
	con = open_base()
	cur = con.cursor()
	cur.execute(pm_dev_tgid_command)
	pm_id = cur.fetchall()
	con.close()
	return pm_id[0][0]


def get_dev_sqlid(name_dev):
	get_dev_id_command = "SELECT id from dev_table where dev = '{}'".format(name_dev)
	con = open_base()
	cur = con.cursor()
	cur.execute(get_dev_id_command)
	dev_id = cur.fetchall()
	con.close()
	print('+++++++++++++++++++++++++++++++++')
	print(dev_id[0][0])
	return dev_id[0][0]


def get_user_sqlid(user_id):
	get_user_id_command = "SELECT id FROM lstusers WHERE tgid={}".format(user_id)
	con = open_base()
	cur = con.cursor()
	cur.execute(get_user_id_command)
	user_id_from_db = cur.fetchall()
	con.close()
	return user_id_from_db[0][0]


def get_user_name(user_id):
	get_user_name_command = "SELECT usname FROM lstusers WHERE tgid={}".format(user_id)
	con = open_base()
	cur = con.cursor()
	cur.execute(get_user_name_command)
	user_name_from_db = cur.fetchall()
	con.close()
	return user_name_from_db[0][0]


def reg_dev(user_id):
	name = get_user_name(user_id)
	con = open_base()
	cur = con.cursor()
	checkid = "SELECT tg_id from pm_table"
	cur.execute(checkid)
	list_of_id = cur.fetchall()
	for sqlid in list_of_id:
		print(sqlid[0])
		if sqlid[0] == user_id:
			print(user_id, '❗❗Вы ПМ❗❗')
			return
	else:
		cur = con.cursor()
		cur.execute("SELECT tg_id from dev_table where tg_id = {}".format(user_id))
		list_of_tgid = cur.fetchall()
		if list_of_tgid:
			print('Вы уже зарегистрированы, как DEV 👨‍💻')
			return
		else:
			cur = con.cursor()
			command = "INSERT INTO dev_table (dev, tg_id) values ('{}', {})".format(name, user_id)
			print(name + 'DEV добавлен в dev_table')
			cur.execute(command)
			con.commit()
	con.close()


def reg_pm(user_id):
	name = get_user_name(user_id)
	con = open_base()
	cur = con.cursor()
	checkid = "SELECT tg_id from dev_table"
	cur.execute(checkid)
	list_of_id = cur.fetchall()
	for sqlid in list_of_id:
		print(sqlid[0])
		if sqlid[0] == user_id:
			print(user_id, '❗❗Вы разработчик❗❗')
			return
	else:
		cur = con.cursor()
		cur.execute("SELECT tg_id from pm_table where tg_id = {}".format(user_id))
		list_of_tgid = cur.fetchall()
		if list_of_tgid:
			print('Вы уже зарегистрированы, как PM 👨‍🎨')
			return
		else:
			cur = con.cursor()
			command = "INSERT INTO pm_table (pm, tg_id) values ('{}', {})".format(name, user_id)
			print(name + 'PM добавлен в pm_table')
			cur.execute(command)
			con.commit()
	con.close()


def reg_user(user_id, name, tg):
	tgusername = '@' + str(tg)
	con = open_base()
	cur = con.cursor()
	command = '''INSERT INTO lstusers (usname, username, tgid) VALUES ('{}','{}',{})'''.format(name, tgusername,
	                                                                                           user_id)
	cur.execute(command)
	con.commit()
	con.close()


def check_prj(user_id, soldate):
	pmid = get_pm_sqlid(user_id)
	pm_list_command = "SELECT id_prj from schedule where id_pm = {} and lstdate = '{}'".format(pmid, soldate)
	con = open_base()
	cur = con.cursor()
	cur.execute(pm_list_command)
	prj = cur.fetchall()
	print('=========================================soldate===================================')
	print(soldate)
	print(prj)
	print('=========================================prj===================================')
	return set(prj)


def check_rsr(user_id, soldate, id_prj):
	pmid = get_pm_sqlid(user_id)
	con = open_base()
	cur = con.cursor()
	row = []
	cur.execute(
		"SELECT id_dev from schedule where id_prj = {} and lstdate = '{}' and id_pm = {}".format(id_prj, soldate, pmid))
	rsr = cur.fetchall()
	for r in rsr:
		row.append(r[0])
	print('Это ресурсы')
	print(row)
	return (set(row))


def check_user_exist_pir(user_id):
	user_list_command = "SELECT tgid from lstusers"
	con = open_base()
	cur = con.cursor()
	cur.execute(user_list_command)
	users = cur.fetchall()
	user_list = []
	for user in users:
		user_list.append(user[0])
	if user_id in user_list:
		return True
	else:
		return False
	con.close()


def check_user_pmtable(user_id):
	user_list_command = "SELECT tg_id from pm_table"
	con = open_base()
	cur = con.cursor()
	cur.execute(user_list_command)
	users = cur.fetchall()
	user_list = []
	for user in users:
		user_list.append(user[0])
	if user_id in user_list:
		print('True pmtable')
		return True
	else:
		print('False pmtable')
		return False
	con.close()


def check_user_devtable(user_id):
	user_list_command = "SELECT tg_id from dev_table"
	con = open_base()
	cur = con.cursor()
	cur.execute(user_list_command)
	users = cur.fetchall()
	user_list = []
	for user in users:
		user_list.append(user[0])
	if user_id in user_list:
		print('True devtable')
		return True
	else:
		print('False devtable')
		return False
	con.close()


def amount_of_resource(message, resource, lstdate):
	con = open_base()
	cur = con.cursor()
	print('=====' + str(get_pm_sqlid(message.chat.id)))
	print('=====id_dev' + str(resource))
	print('=====date' + lstdate)
	command = "SELECT hours from schedule where (id_pm = {} " \
	          "and id_dev = {} and lstdate = '{}')".format(get_pm_sqlid(message.chat.id), resource, lstdate)
	cur.execute(command)
	aors = cur.fetchall()
	print(aors)
	stroka = '👨‍💻' + get_name_resource(resource) + '\n'
	have = 0
	for aor in aors:
		if aor[0] > 0:
			have += aor[0]
		else:
			return False
	stroka += '⌛️️: ' + str(have) + 'ч.\n'
	return stroka


def check_pms(user_id):
	command = "SELECT pm from pm_table"
	con = open_base()
	cur = con.cursor()
	cur.execute(command)
	pms = cur.fetchall()
	pmsqlid = get_pm_sqlid(user_id)
	row = []
	for pm in pms:
		pmid = get_pmid(pm[0])
		print('pm')
		print(pm[0])
		print('pmsqlid')
		print(pmsqlid)
		if pmid == pmsqlid:
			continue
		row.append(pm[0])
	print(pms)
	return row


def checkdate(message, check):
	chkdate_comand = "SELECT id_pm from schedule where (id_pm = {} and lstdate = '{}')".format(
		get_pm_sqlid(message.chat.id), check)
	con = open_base()
	cur = con.cursor()
	cur.execute(chkdate_comand)
	pms = cur.fetchall()
	if not pms:
		print(False)
		return False
	else:
		print(True)
		return True


def pm_prj_for_dist(tg_id_pm):
	pmid = get_pm_sqlid(tg_id_pm)
	get_project_command = "SELECT id_prj from prj_pm where id_pm = {}".format(pmid)
	con = open_base()
	cur = con.cursor()
	cur.execute(get_project_command)
	prjs = cur.fetchall()
	print(prjs)
	return (prjs)


def pm_prj(pm_name):
	print('------>' + pm_name)
	pmid = get_pmid(pm_name)
	print('pmid')
	print(pmid)
	get_project_command = "SELECT id_prj from prj_pm where id_pm = {}".format(pmid)
	con = open_base()
	cur = con.cursor()
	cur.execute(get_project_command)
	prjs = cur.fetchall()
	print(prjs)
	return prjs


def get_prjs_for_idpm(pmid):
	print(pmid)
	get_project_command = "SELECT id_prj from prj_pm where id_pm = {}".format(pmid)
	con = open_base()
	cur = con.cursor()
	cur.execute(get_project_command)
	prjs = cur.fetchall()
	print(prjs)
	return prjs


def get_prjs_for_dev(devid):
	print(devid)
	get_project_command = "SELECT id_prj from prj_dev where id_dev = {}".format(devid)
	con = open_base()
	cur = con.cursor()
	cur.execute(get_project_command)
	prjs = cur.fetchall()
	print(prjs)
	return prjs


def get_pms_for_prj(id_prj):
	print(id_prj)
	get_pm_command = "SELECT id_pm from prj_pm where id_prj = {}".format(id_prj)
	con = open_base()
	cur = con.cursor()
	cur.execute(get_pm_command)
	pms = cur.fetchall()
	print(pms)
	return pms


def get_devs_for_prj(id_prj):
	print(id_prj)
	get_dev_command = "SELECT id_dev from prj_dev where id_prj = {}".format(id_prj)
	con = open_base()
	cur = con.cursor()
	cur.execute(get_dev_command)
	devs = cur.fetchall()
	print("prj_devs-------->", devs, sep="")
	return devs


def get_prj_id(prj_name):
	print("FAQ________")
	print(prj_name)
	print('-------------')
	get_id_command = "SELECT id from prj_table where prj = '{}'".format(prj_name)
	con = open_base()
	cur = con.cursor()
	cur.execute(get_id_command)
	prj_id = cur.fetchall()[0][0]
	con.close()
	print('А вот и я')
	print(prj_id)
	return prj_id


# get list of devs by the prj_name
def prj_devs(prj_name):
	print('А что тут у нас?______________________________________')
	print(prj_name)
	prjid = get_prj_id(prj_name)
	get_list_of_devs_command = "SELECT id_dev from prj_dev where id_prj = {}".format(prjid)
	con = open_base()
	cur = con.cursor()
	cur.execute(get_list_of_devs_command)
	id_devs = cur.fetchall()
	print('это ид этой у нас___________________')
	print(id_devs)
	array_of_iddevs = []
	for id in id_devs:
		array_of_iddevs.append(id[0])
	con.close()
	return array_of_iddevs


def already_exist(mydate, id_prj, id_dev, id_to_pm):
	command = "SELECT id from schedule where lstdate = '{}'" \
	          "and id_prj = {} and id_dev = {} and id_pm  = {}".format(mydate, id_prj, id_dev, id_to_pm)
	con = open_base()
	cur = con.cursor()
	cur.execute(command)
	ids = cur.fetchall()
	if not ids:
		print(False)
		return False
	else:
		print(True)
		return True


def del_unuse_rows():
	command = "DELETE from schedule where hours <= 0"
	con = open_base()
	cur = con.cursor()
	cur.execute(command)
	con.commit()
	con.close()


def update_base(message, mydate, id_prj, id_dev, id_prj_from, sendhours, id_to_pm):
	id_from_pm = get_pm_sqlid(message.chat.id)
	update_command_from = "UPDATE schedule SET hours = hours - {} where lstdate = '{}'" \
	                      "and id_pm = {} and id_prj = {} and id_dev = {}".format(sendhours,
	                                                                              mydate, id_from_pm, id_prj_from,
	                                                                              id_dev)
	con = open_base()
	cur = con.cursor()
	cur.execute(update_command_from)
	con.commit()
	if not already_exist(mydate, id_prj, id_dev, id_to_pm):
		update_command_to = "INSERT into schedule (lstdate, id_prj, id_dev, hours, id_pm)" \
		                    "values ('{}', {}, {}, {}, {})".format(mydate, id_prj, id_dev, sendhours, id_to_pm)
	else:
		update_command_to = "UPDATE schedule SET hours = hours + {} where lstdate = '{}'" \
		                    "and id_pm = {} and id_prj = {} and id_dev = {}".format(sendhours,
		                                                                            mydate, id_to_pm, id_prj, id_dev)
	cur.execute(update_command_to)
	con.commit()
	con.close()
	del_unuse_rows()


def check_idpm_schedule(checkdate):
	command = "SELECT id_pm from schedule where lstdate = '{}'".format(checkdate)
	con = open_base()
	cur = con.cursor()
	cur.execute(command)
	id_pms = cur.fetchall()
	row = []
	for id_pm in id_pms:
		row.append(id_pm[0])
	con.close()
	return list(set(row))


def check_id_dev_schedule(checkdate):
	command = "SELECT id_dev from schedule where lstdate = '{}'".format(checkdate)
	con = open_base()
	cur = con.cursor()
	cur.execute(command)
	id_pms = cur.fetchall()
	row = []
	for id_dev in id_pms:
		row.append(id_dev[0])
	con.close()
	return list(set(row))


def get_str_for_info(id_prj, id_dev, hours):
	name_prj = get_name_project(id_prj)
	name_dev = get_name_resource(id_dev)
	str_hours = str(hours)
	stroka = '\n📁: ' + '#' + name_prj + '\n'
	stroka += '👨‍💻: ' + name_dev + ' ' + '⌛️️: ' + str_hours + 'ч.\n'
	return stroka


def get_list_of_prj_dev_hours(id_pm, checkdate):
	command = "SELECT id_prj, id_dev, hours from schedule where id_pm = {} and lstdate = '{}'".format(id_pm, checkdate)
	con = open_base()
	cur = con.cursor()
	cur.execute(command)
	list_of_pdh = cur.fetchall()
	row = []
	for pdh in list_of_pdh:
		row.append(pdh)
	con.close()
	return row


def get_str_for_info_for_dev(id_prj, id_pm, hours):
	name_prj = get_name_project(id_prj)
	name_pm = get_name_pm(id_pm)
	str_hours = str(hours)
	stroka = '\n📁: ' + '#' + name_prj + '\n'
	stroka += '👨‍🎨: ' + name_pm + ' ' + '⌛️️: ' + str_hours + 'ч.\n'
	return stroka


def get_list_of_prj_hours(id_dev, checkdate):
	command = "SELECT id_prj, id_pm, hours from schedule where id_dev = {} and lstdate = '{}'".format(id_dev, checkdate)
	con = open_base()
	cur = con.cursor()
	cur.execute(command)
	list_of_pph = cur.fetchall()
	row = []
	for pph in list_of_pph:
		row.append(pph)
	con.close()
	return row


def check_amount_of_housr_dev(check_date, id_dev):
	command = "SELECT hours from schedule where id_dev = {} and lstdate = '{}'".format(id_dev, check_date)
	con = open_base()
	cur = con.cursor()
	cur.execute(command)
	pdhs = cur.fetchall()
	sum_of_pdhs = 0
	for pdh in pdhs:
		sum_of_pdhs += pdh[0]
	return sum_of_pdhs


def update_base_distribute(message, usedate, id_prj, id_dev, hours):
	id_pm = get_pm_sqlid(message.chat.id)
	con = open_base()
	cur = con.cursor()
	if not already_exist(usedate, id_prj, id_dev, id_pm):
		update_command_to = "INSERT into schedule (lstdate , id_prj, id_dev, hours, id_pm)" \
		                    "values ('{}', {}, {}, {}, {})".format(usedate, id_prj, id_dev, hours, id_pm)
	else:
		update_command_to = "UPDATE schedule SET hours = hours + {} where lstdate = '{}'" \
		                    "and id_pm = {} and id_prj = {} and id_dev = {}".format(hours,
		                                                                            usedate, id_pm, id_prj, id_dev)
	cur.execute(update_command_to)
	con.commit()
	print('Задача поставлена!!!')
	con.close()


def have_work(message, flag_role, date):
	if flag_role:
		id_pm = get_pm_sqlid(message.chat.id)
		command = "SELECT id from schedule where id_pm = {} and lstdate = '{}'".format(id_pm, date)
	else:
		id_dev = get_dev_sqlid_by_tgid(message.chat.id)
		command = "SELECT id from schedule where id_dev = {} and lstdate = '{}'".format(id_dev, date)
	con = open_base()
	cur = con.cursor()
	cur.execute(command)
	have_task = cur.fetchall()
	row = []
	for ids in have_task:
		row.append(ids[0])
	return row


def update_name_of_pm(id_pm, update_name):
	print(id_pm, update_name)
	update_name = "UPDATE pm_table set pm = '{}' WHERE id = {}".format(update_name, id_pm)
	print(update_name)
	con = open_base()
	cur = con.cursor()
	cur.execute(update_name)
	con.commit()
	con.close()


def delete_pm(id_pm):
	del_pm_prj = "DELETE from prj_pm WHERE id_pm = {}".format(id_pm)
	del_pm_table = "DELETE from pm_table WHERE id = {}".format(id_pm)
	del_lstusers = "DELETE from lstusers WHERE tgid = {}".format(get_pm_tgid(id_pm))
	print(del_pm_table)
	print(del_pm_prj)
	print(del_lstusers)
	con = open_base()
	cur = con.cursor()
	if get_prjs_for_idpm(id_pm):
		cur.execute(del_pm_prj)
		con.commit()
		print("delete_prj_pm")
	cur.execute(del_pm_table)
	con.commit()
	cur.execute(del_lstusers)
	con.commit()
	con.close()


def add_pm(pm_name, tg_username):
	add_lstusers = "INSERT into lstusers (usname, username, tgid) VALUES ('{}', '{}', {})" \
											" RETURNING id".format(pm_name, tg_username, 0)
	set_unique_tg_id_lst = "UPDATE lstusers set tgid=id where tgid = {}".format(0)
	add_pm_table = "INSERT into pm_table (pm, tg_id) VALUES ('{}', '{}')".format(pm_name, 0)
	con = open_base()
	cur = con.cursor()
	cur.execute(add_lstusers)
	last_id = cur.fetchone()[0]
	con.commit()
	cur.fetchall()
	cur.execute(set_unique_tg_id_lst)
	con.commit()
	cur.execute(add_pm_table)
	con.commit()
	cur.execute("UPDATE pm_table set tg_id={} where tg_id = {}".format(last_id, 0))
	con.commit()
	con.close()


def update_name_of_dev(id_dev, update_name):
	print(id_dev, update_name)
	update_name = "UPDATE dev_table set dev = '{}' WHERE id = {}".format(update_name, id_dev)
	print(update_name)
	con = open_base()
	cur = con.cursor()
	cur.execute(update_name)
	con.commit()
	con.close()


def delete_dev(id_dev):
	del_dev_prj = "DELETE from prj_dev WHERE id_dev = {}".format(id_dev)
	del_dev_table = "DELETE from dev_table WHERE id = {}".format(id_dev)
	del_lstusers = "DELETE from lstusers WHERE tgid = {}".format(get_dev_tgid(id_dev))
	print(del_dev_table)
	print(del_dev_prj)
	print(del_lstusers)
	con = open_base()
	cur = con.cursor()
	if get_prjs_for_dev(id_dev):
		cur.execute(del_dev_prj)
		con.commit()
		print("delete_prj_dev")
	cur.execute(del_dev_table)
	con.commit()
	cur.execute(del_lstusers)
	con.commit()
	con.close()


def add_dev(dev_name, tg_username):
	add_lstusers = "INSERT into lstusers (usname, username, tgid) VALUES ('{}', '{}', {})" \
											" RETURNING id".format(dev_name, tg_username, 0)
	set_unique_tg_id_lst = "UPDATE lstusers set tgid=id where tgid = {}".format(0)
	add_dev_table = "INSERT into dev_table (dev, tg_id) VALUES ('{}', '{}')".format(dev_name, 0)
	con = open_base()
	cur = con.cursor()
	cur.execute(add_lstusers)
	last_id = cur.fetchone()[0]
	con.commit()
	cur.fetchall()
	cur.execute(set_unique_tg_id_lst)
	con.commit()
	cur.execute(add_dev_table)
	con.commit()
	cur.execute("UPDATE dev_table set tg_id={} where tg_id = {}".format(last_id, 0))
	con.commit()
	con.close()


def update_name_of_prj(id_prj, update_name):
	print(id_prj, update_name)
	update_name = "UPDATE prj_table set prj = '{}' WHERE id = {}".format(update_name, id_prj)
	print(update_name)
	con = open_base()
	cur = con.cursor()
	cur.execute(update_name)
	con.commit()
	con.close()


def delete_prj(id_prj):
	del_dev_prj = "DELETE from prj_dev WHERE id_prj = {}".format(id_prj)
	del_pm_prj = "DELETE from prj_pm WHERE id_prj = {}".format(id_prj)
	del_prj_table = "DELETE from prj_table WHERE id = {}".format(id_prj)
	print(del_dev_prj)
	print(del_pm_prj)
	print(del_prj_table)
	con = open_base()
	cur = con.cursor()
	if get_devs_for_prj(id_prj):
		cur.execute(del_dev_prj)
		con.commit()
		print("delete_prj_from_devs")
	if get_pms_for_prj(id_prj):
		cur.execute(del_pm_prj)
		con.commit()
		print("delete_prj_from_pms")
	cur.execute(del_prj_table)
	con.commit()
	con.close()


def add_prj(prj_name):
	add_prj_table = "INSERT into prj_table (prj) VALUES ('{}')".format(prj_name)
	con = open_base()
	cur = con.cursor()
	cur.execute(add_prj_table)
	con.commit()
	con.close()
