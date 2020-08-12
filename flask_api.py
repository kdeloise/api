#!/usr/bin/env python3
# coding=utf-8
from flask import Flask, jsonify, request, Response, json
from datetime import datetime
import json
import dbase

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
client = app.test_client()


@app.route('/api/pms/list', methods=['GET'])
def get_list_pms():
    schema_of_pms = {
        "error": "string",
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


@app.route('/api/pms/<int:id>', methods=['GET', 'PUT'])
def get_pm(id):
    pm_projects = dbase.get_prjs_for_idpm(id)
    projects_list = list()
    for prj in pm_projects:
        projects_list.append({
            "id": prj[0],
            "name": dbase.get_name_project(prj[0])
        })
    schema_of_pm = {
        "error": "string",
        "timestamp": datetime.timestamp(datetime.now()),
        "data": {
            "name": dbase.get_name_pm(id),
            "telegram": dbase.get_username_of_tg(dbase.get_pm_tgid(id))[0],
            "projects": projects_list
        }
    }
    if request.method == 'GET':
        print(request.method)
        return Response(json.dumps(schema_of_pm, ensure_ascii=False), mimetype='application/json')
    elif request.method == 'PUT':
        print(request.method)
        params = request.json
        print('------>', params, sep='')
        return Response(json.dumps(schema_of_pm, ensure_ascii=False), mimetype='application/json')


@app.route('/echo', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_echo():
    if request.method == 'GET':
        return "ECHO: GET\n"

    elif request.method == 'POST':
        return "ECHO: POST\n"

    elif request.method == 'PATCH':
        return "ECHO: PACTH\n"

    elif request.method == 'PUT':
        return request.json

    elif request.method == 'DELETE':
        return "ECHO: DELETE"


@app.route('/api/pms/<int:id>', methods=['DELETE'])
def delete_pm(id):
    pass


@app.route('/api/pms/add', methods=['POST'])
def add_pm():
    pass


if __name__ == '__main__':
    app.run()
