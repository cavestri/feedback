"""
MIT License

Copyright (c) 2017 Franco Cavestri

https://github.com/cavestri/feedback

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


import time
import sqlite3
import logging
from jsonschema import validate, ValidationError
from flask import Flask, render_template, g, request, jsonify

APP = Flask(__name__)

FEEDBACK_SCHEMA = {
    'type': 'object',
    'properties': {
        'name': {
            'type': 'string',
            'minLength': 1
        },
        'type': {
            'type': 'string',
            'enum': ['like', 'dislike', 'issue']
        },
        'comment': {
            'type': 'string',
            'minLength': 1
        }
    },
    'additionalProperties': False,
    'required': ['name', 'type', 'comment']
}

QUERY_SCHEMA = {
    'type': 'object',
    'properties': {
        'type': {
            'type': 'string',
            'enum': ['like', 'dislike', 'issue']
        },
        'range': {
            'type': 'string',
            'enum': ['today', 'week', 'month']
        }
    },
    'additionalProperties': False
}


DATABASE = 'db\database.db'


@APP.route('/')
def home():
    return render_template('home.html')


@APP.route('/get')
def get():
    if is_input_valid(request.args, QUERY_SCHEMA):

        where_range = {
            'today': 'date = date("now")',
            'week': 'date >= date("now", "weekday 0", "-7 days")',
            'month': 'date >= date("now","start of month")'
        }

        if request.args.get('range'):
            where_range = where_range[request.args.get('range')]

        where_type = 'type="' + request.args.get('type', '') + '"'

        if request.args.get('range') and request.args.get('type'):
            where = 'where {} AND {}'.format(where_type, where_range)
        elif request.args.get('range'):
            where = 'where ' + where_range
        elif request.args.get('type'):
            where = 'where ' + where_type
        else:
            where = ''

        result = query_db("select * from feedback {} limit 1000".format(where))
        return jsonify(document_to_object(result)), 200
    else:
        return jsonify(QUERY_SCHEMA), 400


def document_to_object(result):
    response = []
    for row in result:
        element = {
            'user': row[0],
            'type': row[1],
            'date': row[2],
            'comment': row[3],
        }
        response.append(element)
    return response


@APP.route('/add', methods=['POST'])
def add():
    if is_input_valid(request.json, FEEDBACK_SCHEMA):
        cur = get_db().cursor()
        cur.execute('insert into feedback values ("' + request.json.get('name') + '", "' + request.json.get('type') + '", "' + time.strftime('%Y-%m-%d') + '", "' + request.json.get('comment') + '")')
        get_db().commit()
        return '', 201
    else:
        return jsonify(FEEDBACK_SCHEMA), 400


@APP.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def is_input_valid(data, schema):
    try:
        validate(data, schema)
        return True
    except ValidationError as error:
        logging.error('Error of user data: {}'.format(error.message))
        return False


APP.run(host='0.0.0.0', port=80, debug=True)
