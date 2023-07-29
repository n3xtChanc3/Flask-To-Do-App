import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')

def create_table():
    conn = sqlite3.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS tasks
                   (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT, time TEXT)''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        create_table()
        if request.method == "POST":
            task = request.form['task']
            time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            conn = sqlite3.connect(DATABASE_URL)
            cur = conn.cursor()
            cur.execute('INSERT INTO TASKS (task, time) VALUES (?, ?)', (task, time))
            conn.commit()
            conn.close()
            print(f"Task added: {task}")

        conn = sqlite3.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute('SELECT * FROM tasks')
        tasks = cur.fetchall()
        conn.close()

        print(tasks)

        return render_template('index.html', tasks=tasks)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return "An error occurred. Please check the logs."

if __name__ == '__main__':
    app.run(debug=True)
