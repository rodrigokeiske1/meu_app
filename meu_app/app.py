from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

def init_db():
    with sqlite3.connect('users.db') as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)')
        conn.commit()

def get_db_connection():
    conn = sqlite3.connect('users.db')
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return handle_registration()
    return render_template('index.html')

def handle_registration():
    name = request.form['name']
    age = request.form['age']
    conn = get_db_connection()
    conn.execute('PRAGMA journal_mode=WAL;')
    try:
        conn.execute('INSERT INTO users (name, age) VALUES (?, ?)', (name, age))
        conn.commit()
        session['user'] = {'name': name, 'age': age}
    except sqlite3.OperationalError as e:
        print(f"Erro ao inserir dados: {e}")
    finally:
        conn.close()
    return redirect(url_for('main'))

@app.route('/main')
def main():
    user = session.get('user')
    if user is None:
        return redirect(url_for('index'))
    return render_template('main.html', user=user)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
