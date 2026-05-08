from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # разрешаем запросы с любых доменов

DATA_FILE = 'data.json'

# Загрузка данных
def load_data():
    if not os.path.exists(DATA_FILE):
        return {
            'projects': [],
            'team': [],
            'faq': [],
            'partners': [],
            'leads': []
        }
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# Сохранение данных
def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ====== API ======

# Проекты
@app.route('/api/projects', methods=['GET'])
def get_projects():
    data = load_data()
    return jsonify(data['projects'])

@app.route('/api/projects', methods=['POST'])
def add_project():
    data = load_data()
    new_project = {
        'id': int(os.path.getmtime(DATA_FILE)) if os.path.exists(DATA_FILE) else 1,
        'title': request.json.get('title', ''),
        'description': request.json.get('description', ''),
        'image_url': request.json.get('image_url', ''),
        'link': request.json.get('link', ''),
        'category': request.json.get('category', '')
    }
    if not new_project['title']:
        return jsonify({'error': 'Название обязательно'}), 400
    data['projects'].append(new_project)
    save_data(data)
    return jsonify({'id': new_project['id'], 'message': 'Проект добавлен'})

# Команда
@app.route('/api/team', methods=['GET'])
def get_team():
    data = load_data()
    return jsonify(data['team'])

@app.route('/api/team', methods=['POST'])
def add_team_member():
    data = load_data()
    new_member = {
        'id': int(os.path.getmtime(DATA_FILE)) if os.path.exists(DATA_FILE) else 1,
        'name': request.json.get('name', ''),
        'role': request.json.get('role', ''),
        'photo_url': request.json.get('photo_url', ''),
        'description': request.json.get('description', '')
    }
    if not new_member['name']:
        return jsonify({'error': 'Имя обязательно'}), 400
    data['team'].append(new_member)
    save_data(data)
    return jsonify({'id': new_member['id'], 'message': 'Участник добавлен'})

# FAQ
@app.route('/api/faq', methods=['GET'])
def get_faq():
    data = load_data()
    return jsonify(data['faq'])

@app.route('/api/faq', methods=['POST'])
def add_faq():
    data = load_data()
    new_faq = {
        'id': int(os.path.getmtime(DATA_FILE)) if os.path.exists(DATA_FILE) else 1,
        'question': request.json.get('question', ''),
        'answer': request.json.get('answer', '')
    }
    if not new_faq['question'] or not new_faq['answer']:
        return jsonify({'error': 'Вопрос и ответ обязательны'}), 400
    data['faq'].append(new_faq)
    save_data(data)
    return jsonify({'id': new_faq['id'], 'message': 'Вопрос добавлен'})

# Партнёры
@app.route('/api/partners', methods=['GET'])
def get_partners():
    data = load_data()
    return jsonify(data['partners'])

@app.route('/api/partners', methods=['POST'])
def add_partner():
    data = load_data()
    new_partner = {
        'id': int(os.path.getmtime(DATA_FILE)) if os.path.exists(DATA_FILE) else 1,
        'name': request.json.get('name', ''),
        'logo_url': request.json.get('logo_url', ''),
        'link': request.json.get('link', '')
    }
    if not new_partner['name']:
        return jsonify({'error': 'Название обязательно'}), 400
    data['partners'].append(new_partner)
    save_data(data)
    return jsonify({'id': new_partner['id'], 'message': 'Партнёр добавлен'})

# Заявки (leads)
@app.route('/api/leads', methods=['POST'])
def add_lead():
    data = load_data()
    name = request.json.get('name', '')
    phone = request.json.get('phone', '')
    email = request.json.get('email', '')
    message = request.json.get('message', '')
    if not name or not phone:
        return jsonify({'error': 'Имя и телефон обязательны'}), 400
    new_lead = {
        'id': int(os.path.getmtime(DATA_FILE)) if os.path.exists(DATA_FILE) else 1,
        'name': name,
        'phone': phone,
        'email': email,
        'message': message,
        'created_at': '2025-01-01',
        'status': 'новый'
    }
    data['leads'].append(new_lead)
    save_data(data)
    return jsonify({'id': new_lead['id'], 'message': 'Заявка принята'})

@app.route('/api/leads', methods=['GET'])
def get_leads():
    data = load_data()
    return jsonify(data['leads'])

# ====== Запуск (для Render) ======
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))