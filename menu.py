from flask import Flask
from flask import request
from flask import Response
from flask import g
import sqlite3
import os
import json
import re
import json
from urllib.parse import urlencode


app = Flask(__name__)
DATABASE = "menu.db"


def template_to_where_clause(t):

    terms = []
    args = []

    for k, v in t.items():
        temp_s = k + "=%s "
        terms.append(temp_s)
        args.append(v)

    if len(terms) > 0:
        w_clause = "WHERE " + " AND ".join(terms)
    else:
        w_clause = ""
        args = None

    return w_clause, args

def run_query(q, commit=True, fetch=True):
    conn = sqlite3.connect("menu.db")
    cur = conn.cursor()
    r = cur.execute(q)

    if fetch:
        r = cur.fetchall()
    if commit:
        conn.commit()
    return r


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Menu</h1>
    <p>Welcome to our restaurant menu</p>'''

@app.route('/explain', methods = ['GET', 'PUT', 'POST', 'DELETE'])
def explain_what():

    result = "Hello world"
    response = Response(result, status=200, mimetype="text/plain")

    return response

@app.route('/api/menusection', methods=["GET", "POST","PUT"])
def handle_data():
    if request.method == "GET":
        q = 'select * from menu'
        result = run_query(q)

        ans = {}
        ans["MenuSection"] = []
        backup = {}
        for elem in result:
            backup[str(elem[0]) + "_" + elem[1]] = backup.get(str(elem[0]) + "_" + elem[1], []) + [elem[2]]
        for elem in backup:
            id, name = elem.split("_")[0], elem.split("_")[1]
            ans["MenuSection"].append({"id": id, "name": name, "item":backup[elem]})
        resp = Response(json.dumps(ans, indent=2), status=200, mimetype='application/json')
        return resp

    elif request.method == "POST":
        new_r = request.get_json()
        q = 'insert into menu values (' + str(new_r["id"]) + ',"' + new_r["name"] + '", "' + new_r["item"] + '")'
        run_query(q)

        w_clause, args = template_to_where_clause(new_r)
        args[1:] = map(lambda k: '"' + k + '"', args[1:])
        q = 'select * from menu ' + w_clause + " "
        result = run_query(q % tuple(args))

        ans = {}
        ans["success"] = True
        ans["MenuSection"] = []
        backup = {}
        for elem in result:
            backup[str(elem[0]) + "_" + elem[1]] = backup.get(str(elem[0]) + "_" + elem[1], []) + [elem[2]]
        for elem in backup:
            id, name = elem.split("_")[0], elem.split("_")[1]
            ans["MenuSection"].append({"id": id, "name": name, "item": backup[elem]})
        resp = Response(json.dumps(ans, indent=2), status=200, mimetype='application/json')
        return resp


@app.route('/api/menusection/<id>', methods=["GET", "POST", "DELETE", "PUT"])
def handle_specific_data(id):
    if request.method == "GET":
        q = 'select * from menu where id= ' + id
        result = run_query(q)

        ans = {}
        ans["success"] = True
        ans["MenuSection"] = []
        backup = {}
        for elem in result:
            backup[str(elem[0]) + "_" + elem[1]] = backup.get(str(elem[0]) + "_" + elem[1], []) + [elem[2]]
        for elem in backup:
            id, name = elem.split("_")[0], elem.split("_")[1]
            ans["MenuSection"].append({"id": id, "name": name, "item": backup[elem]})
        resp = Response(json.dumps(ans, indent=2), status=200, mimetype='application/json')
        return resp

    elif request.method == "POST":
        new_r = request.get_json()
        new_r["id"] = id
        q = 'insert into menu values (' + str(new_r["id"]) + ',"' + new_r["name"] + '", "' + new_r["item"] + '")'
        run_query(q)

        w_clause, args = template_to_where_clause(new_r)
        args[:-1] = map(lambda k: '"' + k + '"', args[:-1])
        q = 'select * from menu ' + w_clause + " "
        result = run_query(q % tuple(args))

        ans = {}
        ans["success"] = True
        ans["MenuSection"] = []
        backup = {}
        for elem in result:
            backup[str(elem[0]) + "_" + elem[1]] = backup.get(str(elem[0]) + "_" + elem[1], []) + [elem[2]]
        for elem in backup:
            id, name = elem.split("_")[0], elem.split("_")[1]
            ans["MenuSection"].append({"id": id, "name": name, "item": backup[elem]})
        resp = Response(json.dumps(ans, indent=2), status=200, mimetype='application/json')
        return resp

    elif request.method == "DELETE":
        q = 'delete from menu where id = ' + id
        run_query(q)

        ans = {}
        ans["success"] = True
        resp = Response(json.dumps(ans, indent=2), status=200, mimetype='text/plain')
        return resp


@app.route('/api/menusection/<id>/<temp>', methods=["PUT"])
def update_data(id, temp):
    new_r = request.get_json()
    terms = []
    set_args = []
    for k, v in new_r.items():
        terms.append(k + '=%s')
        set_args.append(v)
    set_args = list(map(lambda k: '"' + k + '"', set_args))

    temp = temp.split(",")
    template = {}
    for t in temp:
        t = t.split("=")
        template[t[0]] = t[1]
    template["id"] = id
    w_clause, args = template_to_where_clause(template)
    args[:-1] = map(lambda k: '"' + k + '"', args[:-1])
    set_args.extend(args)
    print(set_args)

    q = "update menu set " + ", ".join(terms) + " " + w_clause
    q = q % tuple(set_args)
    print(q)
    run_query(q)

    ans = {}
    ans["success"] = True
    resp = Response(json.dumps(ans, indent=2), status=200, mimetype='text/plain')
    return resp

if __name__ == '__main__':
    app.run()