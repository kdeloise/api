#!/usr/bin/env python3
# coding=utf-8
from flask import Flask, jsonify, request, Response, json, abort, make_response
from datetime import datetime
import json
import dbase

app = Flask(__name__)
client = app.test_client()


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
	return jsonify(schema_of_pms)


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
		print(request.method)
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
def get_prj_pm():
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
@app.route('/api/dev/list', methods=['GET'])
def get_list_devs():
	pass


@app.route('/api/dev/<id_dev>', methods=['GET', 'PUT', 'DELETE'])
def get_dev(id_dev):
	if request.method == 'GET':
		pass

	elif request.method == 'PUT':
		pass

	elif request.method == 'DELETE':
		pass


@app.route('/api/dev/add', methods=['POST'])
def add_dev():
	pass


@app.route('/api/prj_dev/<id_dev>', methods=['GET', 'PUT', 'DELETE'])
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
@app.route('/api/prj/list', methods=['GET'])
def get_list_prjs():
	pass


@app.route('/api/prj/<id_prj>', methods=['GET', 'PUT', 'DELETE'])
def get_prj(id_prj):
	if request.method == 'GET':
		pass

	elif request.method == 'PUT':
		pass

	elif request.method == 'DELETE':
		pass


@app.route('/api/prj/add', methods=['POST'])
def add_dev():
	pass


if __name__ == '__main__':
	app.run()
