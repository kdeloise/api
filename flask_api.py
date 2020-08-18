#!/usr/bin/env python3
# coding=utf-8
from flask import Flask, jsonify, request, Response, json, abort, make_response
from datetime import datetime, date
import json
import dbase

app = Flask(__name__)
client = app.test_client()


# -------------------------------------------------------------
#                           AUTH BLOCK
# -------------------------------------------------------------
# @app.route('/login', methods='POST')
# def login():
# 	pass
#
#
# @app.route('/logout', methods='GET')
# def logout():
# 	pass


# -------------------------------------------------------------
#                           PMS BLOCK
# -------------------------------------------------------------
@app.route('/api/pms/list', methods=['GET'])
def get_list_pms():
	schema_of_pms = {
		"error": "success",
		"timestamp": datetime.timestamp(datetime.now()),
		"total": 0,
		"offset": 0,
		"perPage": 0,
		"data": list()
	}
	list_of_id_pms = dbase.get_list_of_id_pms()
	for id_pm in list_of_id_pms:
		pm_projects = dbase.get_prjs_for_idpm(id_pm)
		projects_list = list()
		for prj in pm_projects:
			projects_list.append({
				"id": prj[0],
				"name": dbase.get_name_project(prj[0])
			})
		dict_for_pm = {
			"name": dbase.get_name_pm(id_pm),
			"telegram": dbase.get_username_of_tg(dbase.get_pm_tgid(id_pm))[0],
			"projects": projects_list
		}
		schema_of_pms["data"].append(dict_for_pm)
	return Response(json.dumps(schema_of_pms, ensure_ascii=False), mimetype='application/json')


def get_schema_of_pm(id_pm):
	try:
		schema_of_pm = {
			"error": "success",
			"timestamp": datetime.timestamp(datetime.now()),
			"data": dict()
		}
		pm_projects = dbase.get_prjs_for_idpm(id_pm)
		projects_list = list()
		for prj in pm_projects:
			projects_list.append({
				"id": prj[0],
				"name": dbase.get_name_project(prj[0])
			})
		data = {
			"name": dbase.get_name_pm(id_pm),
			"telegram": dbase.get_username_of_tg(dbase.get_pm_tgid(id_pm))[0],
			"projects": projects_list
		}
		schema_of_pm["data"] = data
	except:
		return False
	return schema_of_pm


@app.route('/api/pms/<int:id_pm>', methods=['GET', 'PUT', 'DELETE'])
def get_pm(id_pm):
	if request.method == 'GET':
		if get_schema_of_pm(id_pm):
			schema_of_pm = get_schema_of_pm(id_pm)
		else:
			abort(make_response(jsonify({
				"error": "invalid_request",
				"error_description": "Unauthorized"
			}), 401))
		return Response(json.dumps(schema_of_pm, ensure_ascii=False), mimetype='application/json')

	elif request.method == 'PUT':
		try:
			dbase.update_name_of_pm(id_pm, request.json["name"])
		except:
			abort(make_response(jsonify({
				"error": "invalid_request",
				"error_description": "Unauthorized"
			}), 401))
		schema_of_pm = get_schema_of_pm(id_pm)
		print('------>', request.json["name"], sep='')
		return Response(json.dumps(schema_of_pm, ensure_ascii=False), mimetype='application/json')

	elif request.method == 'DELETE':
		try:
			dbase.delete_pm(id_pm)
			response_json = {
				"error": "success",
				"timestamp": datetime.timestamp(datetime.now()),
				"data": {
					"message": "ok"
				}
			}
			return Response(json.dumps(response_json, ensure_ascii=False), mimetype='application/json')
		except:
			abort(make_response(jsonify({
				"error": "invalid_request",
				"error_description": "Unauthorized"
			}), 400))


@app.route('/api/pms/add', methods=['POST'])
def add_pm():
	try:
		if request.method == 'POST':
			pm_name = request.json["name"]
			tg_username = request.json["telegram"]
			dbase.add_pm(pm_name, tg_username)
			response_json = {
				"error": "success",
				"timestamp": datetime.timestamp(datetime.now()),
				"data": {
					"message": "ok"
				}
			}
			return Response(json.dumps(response_json, ensure_ascii=False), mimetype='application/json')
	except:
		abort(make_response(jsonify({
			"error": "invalid_request",
			"error_description": "Unauthorized"
		}), 400))


@app.route('/api/prj_pm/<id_pm>', methods=['GET', 'PUT', 'DELETE'])
def get_prj_pm(id_pm):
	if request.method == 'GET':
		pass
	elif request.method == 'PUT':
		pass
	elif request.method == 'DELETE':
		pass


@app.route('/api/prj_pm/add', methods=['POST'])
def add_prj_for_pm():
	pass


# -------------------------------------------------------------
#                           DEVS BLOCK
# -------------------------------------------------------------
def get_schema_of_dev(id_dev):
	try:
		schema_of_dev = {
			"error": "success",
			"timestamp": datetime.timestamp(datetime.now()),
			"data": dict()
		}
		dev_projects = dbase.get_prjs_for_dev(id_dev)
		projects_list = list()
		for prj in dev_projects:
			projects_list.append({
				"id": prj[0],
				"name": dbase.get_name_project(prj[0])
			})
		data = {
			"name": dbase.get_name_resource(id_dev),
			"telegram": dbase.get_username_of_tg(dbase.get_dev_tgid(id_dev))[0],
			"projects": projects_list
		}
		schema_of_dev["data"] = data
	except:
		return False
	return schema_of_dev


@app.route('/api/devs/list', methods=['GET'])
def get_list_devs():
	schema_of_devs = {
		"error": "success",
		"timestamp": datetime.timestamp(datetime.now()),
		"total": 0,
		"offset": 0,
		"perPage": 0,
		"data": list()
	}
	list_of_id_devs = dbase.get_list_of_id_devs()
	for id_dev in list_of_id_devs:
		dev_projects = dbase.get_prjs_for_dev(id_dev)
		projects_list = list()
		for prj in dev_projects:
			projects_list.append({
				"id": prj[0],
				"name": dbase.get_name_project(prj[0])
			})
		dict_for_dev = {
			"name": dbase.get_name_resource(id_dev),
			"telegram": dbase.get_username_of_tg(dbase.get_dev_tgid(id_dev))[0],
			"projects": projects_list
		}
		schema_of_devs["data"].append(dict_for_dev)
	return Response(json.dumps(schema_of_devs, ensure_ascii=False), mimetype='application/json')


@app.route('/api/devs/<id_dev>', methods=['GET', 'PUT', 'DELETE'])
def get_dev(id_dev):
	if request.method == 'GET':
		if get_schema_of_dev(id_dev):
			schema_of_dev = get_schema_of_dev(id_dev)
		else:
			abort(make_response(jsonify({
				"error": "invalid_request",
				"error_description": "Unauthorized"
			}), 401))
		return Response(json.dumps(schema_of_dev, ensure_ascii=False), mimetype='application/json')

	elif request.method == 'PUT':
		try:
			dbase.update_name_of_dev(id_dev, request.json["name"])
		except:
			abort(make_response(jsonify({
				"error": "invalid_request",
				"error_description": "Unauthorized"
			}), 401))
		schema_of_dev = get_schema_of_dev(id_dev)
		print('------>', request.json["name"], sep='')
		return Response(json.dumps(schema_of_dev, ensure_ascii=False), mimetype='application/json')

	elif request.method == 'DELETE':
		try:
			dbase.delete_dev(id_dev)
			response_json = {
				"error": "success",
				"timestamp": datetime.timestamp(datetime.now()),
				"data": {
					"message": "ok"
				}
			}
			return Response(json.dumps(response_json, ensure_ascii=False), mimetype='application/json')
		except:
			abort(make_response(jsonify({
				"error": "invalid_request",
				"error_description": "Unauthorized"
			}), 400))


@app.route('/api/devs/add', methods=['POST'])
def add_dev():
	try:
		if request.method == 'POST':
			dev_name = request.json["name"]
			tg_username = request.json["telegram"]
			dbase.add_dev(dev_name, tg_username)
			response_json = {
				"error": "success",
				"timestamp": datetime.timestamp(datetime.now()),
				"data": {
					"message": "ok"
				}
			}
			return Response(json.dumps(response_json, ensure_ascii=False), mimetype='application/json')
	except:
		abort(make_response(jsonify({
			"error": "invalid_request",
			"error_description": "Unauthorized"
		}), 400))


@app.route('/api/devs/<id_dev>/timelog', methods=['GET', 'PUT'])
def get_timelog_dev(id_dev):
	if request.method == 'GET':
		if dbase.get_schedule_dev(id_dev):
			schema_of_timelog_dev = {
				"error": "string",
				"timestamp": 1559751301818,
				"total": 0,
				"offset": 0,
				"perPage": 0,
				"data": list()
			}
			list_of_schedule = dbase.get_schedule_dev(id_dev)
			for schedule in list_of_schedule:
				split_schedule = schedule[0].split('/')
				date_ts = datetime(int(split_schedule[2]), int(split_schedule[1]), int(split_schedule[0]))
				dict_of_schedule = {
					"date": int(datetime.timestamp(date_ts)),
					"project": dbase.get_name_project(schedule[1]),
					"hours": schedule[2]
				}
				schema_of_timelog_dev["data"].append(dict_of_schedule)
		else:
			abort(make_response(jsonify({
				"error": "invalid_request",
				"error_description": "Unauthorized"
			}), 401))
		return Response(json.dumps(schema_of_timelog_dev, ensure_ascii=False), mimetype='application/json')

	elif request.method == 'PUT':
		try:
			date_ts = datetime.fromtimestamp(request.json["date"])
			date_str = f'{int(date_ts.day)}/{int(date_ts.month)}/{int(date_ts.year)}'
			print(request.json["date"], date_str, request.json["project"], request.json["hours"])
			dbase.update_schedule_for_dev(id_dev, date_str, request.json["project"], request.json["hours"])
			response_json = {
				"error": "success",
				"timestamp": datetime.timestamp(datetime.now()),
				"data": {
					"message": "ok"
				}
			}
		except:
			abort(make_response(jsonify({
				"error": "invalid_request",
				"error_description": "Unauthorized"
			}), 401))

		return Response(json.dumps(response_json, ensure_ascii=False), mimetype='application/json')


@app.route('/api/prj_devs/<id_dev>', methods=['GET', 'PUT', 'DELETE'])
def get_prj_dev(id_dev):
	if request.method == 'GET':
		pass
	elif request.method == 'PUT':
		pass
	elif request.method == 'DELETE':
		pass


@app.route('/api/prj_dev/add', methods=['POST'])
def add_prj_for_dev():
	pass


# -------------------------------------------------------------
#                           PRJS BLOCK
# -------------------------------------------------------------
@app.route('/api/prjs/list', methods=['GET'])
def get_list_prjs():
	schema_of_prjs = {
		"error": "success",
		"timestamp": datetime.timestamp(datetime.now()),
		"total": 0,
		"offset": 0,
		"perPage": 0,
		"data": list()
	}
	list_of_id_prjs = dbase.get_list_of_id_prjs()
	for id_prj in list_of_id_prjs:
		project_pms = dbase.get_pms_for_prj(id_prj)
		project_devs = dbase.get_devs_for_prj(id_prj)
		projects_dict = {
			"id": id_prj,
			"name": dbase.get_name_project(id_prj),
			"pms": list(),
			"developers": list()
		}
		for pm in project_pms:
			projects_dict["pms"].append({
				"id": pm[0],
				"name": dbase.get_name_pm(pm[0]),
				"telegram": dbase.get_username_of_tg(dbase.get_pm_tgid(pm[0]))[0],
			})
		for dev in project_devs:
			projects_dict["developers"].append({
				"id": dev[0],
				"name": dbase.get_name_resource(dev[0]),
				"telegram": dbase.get_username_of_tg(dbase.get_dev_tgid(dev[0]))[0]
			})
		schema_of_prjs["data"].append(projects_dict)
	return Response(json.dumps(schema_of_prjs, ensure_ascii=False), mimetype='application/json')


def get_schema_of_prj(id_prj):
	try:
		schema_of_prj = {
			"error": "success",
			"timestamp": datetime.timestamp(datetime.now()),
			"data": dict()
		}
		project_pms = dbase.get_pms_for_prj(id_prj)
		project_devs = dbase.get_devs_for_prj(id_prj)
		projects_dict = {
			"id": id_prj,
			"name": dbase.get_name_project(id_prj),
			"pms": list(),
			"developers": list()
		}
		for pm in project_pms:
			projects_dict["pms"].append({
				"id": pm[0],
				"name": dbase.get_name_pm(pm[0]),
				"telegram": dbase.get_username_of_tg(dbase.get_pm_tgid(pm[0]))[0],
			})
		for dev in project_devs:
			projects_dict["developers"].append({
				"id": dev[0],
				"name": dbase.get_name_resource(dev[0]),
				"telegram": dbase.get_username_of_tg(dbase.get_dev_tgid(dev[0]))[0]
			})
		schema_of_prj["data"] = projects_dict
		return schema_of_prj
	except:
		return False


@app.route('/api/prjs/<id_prj>', methods=['GET', 'PUT', 'DELETE'])
def get_prj(id_prj):
	if request.method == 'GET':
		if get_schema_of_prj(id_prj):
			schema_of_prj = get_schema_of_prj(id_prj)
		else:
			abort(make_response(jsonify({
				"error": "invalid_request",
				"error_description": "Unauthorized"
			}), 401))
		return Response(json.dumps(schema_of_prj, ensure_ascii=False), mimetype='application/json')

	elif request.method == 'PUT':
		try:
			dbase.update_name_of_prj(id_prj, request.json["name"])
		except:
			abort(make_response(jsonify({
				"error": "invalid_request",
				"error_description": "Unauthorized"
			}), 401))
		schema_of_prj = get_schema_of_prj(id_prj)
		print('------>', request.json["name"], sep='')
		return Response(json.dumps(schema_of_prj, ensure_ascii=False), mimetype='application/json')

	elif request.method == 'DELETE':
		try:
			dbase.delete_prj(id_prj)
			response_json = {
				"error": "success",
				"timestamp": datetime.timestamp(datetime.now()),
				"data": {
					"message": "ok"
				}
			}
			return Response(json.dumps(response_json, ensure_ascii=False), mimetype='application/json')
		except:
			abort(make_response(jsonify({
				"error": "invalid_request",
				"error_description": "Unauthorized"
			}), 400))


@app.route('/api/prjs/add', methods=['POST'])
def add_prj():
	try:
		if request.method == 'POST':
			prj_name = request.json["name"]
			print("prj_name------>", prj_name)
			dbase.add_prj(prj_name)
			response_json = {
				"error": "success",
				"timestamp": datetime.timestamp(datetime.now()),
				"data": {
					"message": "ok"
				}
			}
			return Response(json.dumps(response_json, ensure_ascii=False), mimetype='application/json')
	except:
		abort(make_response(jsonify({
			"error": "invalid_request",
			"error_description": "Unauthorized"
		}), 400))


if __name__ == '__main__':
	app.run()
