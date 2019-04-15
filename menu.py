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

@app.route('/api/menusection', methods=["GET", "POST"])
def handle_data():
    if request.method == "GET":
        q = 'select * from menu'
        result = run_query(q)

        ans = {}
        ans["MenuSection"] = []
        for elem in result:
            ans["MenuSection"].append({"id": elem[0], "name": elem[1]})
        resp = Response(json.dumps(ans, indent=2), status=200, mimetype='application/json')
        return resp

    else:
        new_r = request.get_json()
        w_clause, args = template_to_where_clause(new_r)
        args = map(lambda k: "'" + k + "'", args)
        q = 'select * from menu ' + w_clause + " "
        result = run_query(q % tuple(args))

        ans = {}
        ans["success"] = True
        ans["MenuSection"] = []
        for elem in result:
            ans["MenuSection"].append({"id": elem[0], "name": elem[1]})
        resp = Response(json.dumps(ans, indent=2), status=200, mimetype='application/json')
        return resp

@app.route('/api/menusection/<id>', methods=["GET", "POST", "DELETE"])
def handle_specific_data(id):
    if request.method == "GET":
        q = 'select * from menu where id= ' + id
        result = run_query(q)

        ans = {}
        ans["MenuSection"] = []
        for elem in result:
            ans["MenuSection"].append({"id": elem[0], "name": elem[1]})
        resp = Response(json.dumps(ans, indent=2), status=200, mimetype='application/json')
        return resp

    elif request.method == "POST":
        new_r = request.get_json()
        new_r["id"] = id
        w_clause, args = template_to_where_clause(new_r)
        args = map(lambda k: "'" + k + "'", args)
        q = 'select * from menu ' + w_clause + " "
        result = run_query(q % tuple(args))

        ans = {}
        ans["success"] = True
        ans["MenuSection"] = []
        for elem in result:
            ans["MenuSection"].append({"id":elem[0], "name":elem[1]})
        resp = Response(json.dumps(ans, indent=2), status=200, mimetype='application/json')
        return resp

    else:
        q = 'delete from menu where id = ' + id
        run_query(q)

        ans = {}
        ans["success"] = True
        resp = Response(json.dumps(ans, indent=2), status=200, mimetype='text/plain')
        return resp

if __name__ == '__main__':
    app.run()