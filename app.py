from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False

DATA_FILE = 'data.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return {
            'projects': [],
            'team': [],
            'faq': [],
            'partners': [],
            'leads': [],
            'support': []  # ← новое поле
        }
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ====== ПРОЕКТЫ ======
@app.route('/api/projects', methods=['GET'])
def get_projects():
    return jsonify(load_data()['projects'])

@app.route('/api/projects', methods=['POST'])
def add_project():
    data = load_data()
    new = {
        'id': int(os.path.getmtime(DATA_FILE)) if os.path.exists(DATA_FILE) else 1,
        'title': request.json.get('title', ''),
        'description': request.json.get('description', ''),
        'image_url': request.json.get('image_url', ''),
        'link': request.json.get('link', ''),
        'category': request.json.get('category', '')
    }
    if not new['title']:
        return jsonify({'error': 'Название обязательно'}), 400
    data['projects'].append(new)
    save_data(data)
    return jsonify({'id': new['id'], 'message': 'Проект добавлен'})

# ====== КОМАНДА ======
@app.route('/api/team', methods=['GET'])
def get_team():
    return jsonify(load_data()['team'])

@app.route('/api/team', methods=['POST'])
def add_team():
    data = load_data()
    new = {
        'id': int(os.path.getmtime(DATA_FILE)) if os.path.exists(DATA_FILE) else 1,
        'name': request.json.get('name', ''),
        'role': request.json.get('role', ''),
        'photo_url': request.json.get('photo_url', ''),
        'description': request.json.get('description', '')
    }
    if not new['name']:
        return jsonify({'error': 'Имя обязательно'}), 400
    data['team'].append(new)
    save_data(data)
    return jsonify({'id': new['id'], 'message': 'Участник добавлен'})

# ====== FAQ ======
@app.route('/api/faq', methods=['GET'])
def get_faq():
    return jsonify(load_data()['faq'])

@app.route('/api/faq', methods=['POST'])
def add_faq():
    data = load_data()
    new = {
        'id': int(os.path.getmtime(DATA_FILE)) if os.path.exists(DATA_FILE) else 1,
        'question': request.json.get('question', ''),
        'answer': request.json.get('answer', '')
    }
    if not new['question'] or not new['answer']:
        return jsonify({'error': 'Вопрос и ответ обязательны'}), 400
    data['faq'].append(new)
    save_data(data)
    return jsonify({'id': new['id'], 'message': 'Вопрос добавлен'})

# ====== ПАРТНЁРЫ ======
@app.route('/api/partners', methods=['GET'])
def get_partners():
    return jsonify(load_data()['partners'])

@app.route('/api/partners', methods=['POST'])
def add_partner():
    data = load_data()
    new = {
        'id': int(os.path.getmtime(DATA_FILE)) if os.path.exists(DATA_FILE) else 1,
        'name': request.json.get('name', ''),
        'logo_url': request.json.get('logo_url', ''),
        'link': request.json.get('link', '')
    }
    if not new['name']:
        return jsonify({'error': 'Название обязательно'}), 400
    data['partners'].append(new)
    save_data(data)
    return jsonify({'id': new['id'], 'message': 'Партнёр добавлен'})

# ====== ЗАЯВКИ (LEADS) ======
@app.route('/api/leads', methods=['POST'])
def add_lead():
    data = load_data()
    name = request.json.get('name', '')
    phone = request.json.get('phone', '')
    email = request.json.get('email', '')
    message = request.json.get('message', '')
    if not name or not phone:
        return jsonify({'error': 'Имя и телефон обязательны'}), 400
    new = {
        'id': int(os.path.getmtime(DATA_FILE)) if os.path.exists(DATA_FILE) else 1,
        'name': name,
        'phone': phone,
        'email': email,
        'message': message,
        'created_at': '2025-01-01',
        'status': 'новый'
    }
    data['leads'].append(new)
    save_data(data)
    return jsonify({'id': new['id'], 'message': 'Заявка принята'})

@app.route('/api/leads', methods=['GET'])
def get_leads():
    return jsonify(load_data()['leads'])

# ====== ТЕХПОДДЕРЖКА (SUPPORT) – НОВЫЙ РАЗДЕЛ ======
@app.route('/api/support', methods=['POST'])
def add_support():
    data = load_data()
    name = request.json.get('name', '')
    email = request.json.get('email', '')
    message = request.json.get('message', '')
    if not name or not email or not message:
        return jsonify({'error': 'Имя, email и сообщение обязательны'}), 400
    new = {
        'id': int(os.path.getmtime(DATA_FILE)) if os.path.exists(DATA_FILE) else 1,
        'name': name,
        'email': email,
        'message': message,
        'created_at': '2025-01-01',
        'status': 'новый'
    }
    data['support'].append(new)
    save_data(data)
    return jsonify({'id': new['id'], 'message': 'Сообщение в техподдержку принято'})

@app.route('/api/support', methods=['GET'])
def get_support():
    return jsonify(load_data()['support'])

# ====== ЗАПУСК ======
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))
