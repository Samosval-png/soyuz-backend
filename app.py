import os
import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False

DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'новый'
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS support (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'новый'
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ====== ЗАЯВКИ (leads) ======
@app.route('/api/leads', methods=['GET'])
def get_leads():
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM leads ORDER BY created_at DESC')
    rows = cur.fetchall()
    conn.close()
    return jsonify(rows)

@app.route('/api/leads', methods=['POST'])
def add_lead():
    data = request.json
    name = data.get('name', '')
    phone = data.get('phone', '')
    email = data.get('email', '')
    message = data.get('message', '')
    if not name or not phone:
        return jsonify({'error': 'Имя и телефон обязательны'}), 400
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO leads (name, phone, email, message) VALUES (%s, %s, %s, %s) RETURNING id',
        (name, phone, email, message)
    )
    lead_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return jsonify({'id': lead_id, 'message': 'Заявка принята'})

# ====== ТЕХПОДДЕРЖКА (support) ======
@app.route('/api/support', methods=['GET'])
def get_support():
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM support ORDER BY created_at DESC')
    rows = cur.fetchall()
    conn.close()
    return jsonify(rows)

@app.route('/api/support', methods=['POST'])
def add_support():
    data = request.json
    name = data.get('name', '')
    email = data.get('email', '')
    message = data.get('message', '')
    if not name or not email or not message:
        return jsonify({'error': 'Имя, email и сообщение обязательны'}), 400
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO support (name, email, message) VALUES (%s, %s, %s) RETURNING id',
        (name, email, message)
    )
    support_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return jsonify({'id': support_id, 'message': 'Сообщение отправлено'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))
