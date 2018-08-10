from typing import List, Dict
from flask import Flask, redirect
import mysql.connector
import json

app = Flask(__name__)


def favorite_colors() -> List[Dict]:
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        # 'host': 'mysql-service',
        'port': '3306',
        'database': 'knights'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM favorite_colors')
    results = [{name: color} for (name, color) in cursor]
    cursor.close()
    connection.close()

    return results

def add_favorite_color(name, color):
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        # 'host': 'mysql-service',
        'port': '3306',
        'database': 'knights'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    add_record = ('INSERT INTO favorite_colors '
                '(name, color) '
                'VALUES (%(name)s, %(color)s)')
    name_color = {
        'name': name,
        'color': color,
    }
    cursor.execute(add_record, name_color)
    connection.commit()
    cursor.close()
    connection.close()

    return True

@app.route('/')
def index() -> str:
    text = 'Hello Docker!\n ' + json.dumps({'favorite_colors': favorite_colors()})
    return text

@app.route('/add/<name>/<color>')
def add(name, color):
    add_favorite_color(name, color)
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
