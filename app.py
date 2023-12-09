from flask import Flask, request, jsonify, redirect, url_for, session, render_template
#from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db, Case
from flask_cors import CORS
import os
import uuid

app = Flask(__name__, template_folder='web')
CORS(app, supports_credentials=True)
app.secret_key = 'your_secret_key'  # 设置一个安全的密钥

# Database Configuration
#app.config['SQLALCHEMY_DATABASE_URI'] = 'your-database-uri'
#app.config.from_object('config_test.TestConfig')
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this!

#db = SQLAlchemy(app)
jwt = JWTManager(app)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(name=data['name']).first()
    if user is None:
        return jsonify({'message': '用户名不存在'}), 401
    stored_hashed_password = user.password
    stored_salt = user.salt
    if check_password_hash(stored_hashed_password, data['password'] + stored_salt):
        token = create_access_token(identity=user.id)
        session['user_id'] = user.id  # 存储用户ID到会话
        return jsonify({'redirect': url_for('profile')}), 200
    else:
        return jsonify({'message': '密码错误'}), 401

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    existing_user = User.query.filter_by(name=data['name']).first()
    #调试用
    print("Received data:", data)
    print("Existing user:", existing_user)
    if existing_user:
        return jsonify({'message': '用户名已存在'}), 409
    #生成盐 加密密码 用户id
    salt = generate_salt()     # 生成随机盐
    password = generate_password_hash(data['password'] + salt, method='pbkdf2:sha256')
    user_id = str(uuid.uuid4())
    new_user = User(id=user_id, name=data['name'], password=password, salt=salt, phone=data['phone'])
    print("New user info:", new_user)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': '注册成功！'}), 201

@app.route('/api/profile')
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    user = User.query.get(user_id)  # 从数据库获取用户信息
    if user:
        return render_template('main.html', user_name=user.name, user_phone=user.phone, token=token)
    else:
        return redirect(url_for('login'))  # 如果无法获取用户信息，则重定向到登录页面
'''
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    # 可以使用current_user来获取当前登录的用户ID
    # ...
    return jsonify(logged_in_as=current_user)

@app.route('/api/user/<user_id>/documents', methods=['GET', 'POST'])
@jwt_required()
def manage_documents():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if request.method == 'POST':
        data = request.get_json()
        if user.role != 'admin':     # Admin-specific logic here
            return jsonify({'message': 'Access denied!'}), 403
        new_document = Document(...)
        db.session.add(new_document)
        db.session.commit()
        return jsonify({'message': 'Document created!'}), 201
    else:
        documents = Document.query.all()
        return jsonify([document.to_dict() for document in documents]), 200

#Need merge two function together
'''

'''


@app.route('/api/user/<user_id>/files', methods=['GET', 'POST', 'PUT', 'DELETE'])
@jwt_required()
def user_files(user_id):
    if request.method == 'POST':
        #Code to upload a new file
    elif request.method == 'GET':
        #Code to list all files for the user
    elif request.method == 'PUT':
        # Code to update a file
    elif request.method == 'DELETE':
        # Code to delete a file

@app.route('/api/user/<user_id>/clients', methods=['GET', 'POST'])
@jwt_required()
def manage_clients():


@app.route('/api/user/<user_id>/cases', methods=['POST'])
@jwt_required()
def create_case(user_id):
    if get_jwt_identity() != user_id:
        return jsonify({'message': 'Unauthorized access'}), 403

    data = request.get_json()
    new_case = Case(
        client_name=data['client_name'],
        lawyer_id=user_id,
            # ... set other fields from data
        )
    db.session.add(new_case)
    db.session.commit()

    return jsonify({'message': 'New case created', 'case_id': new_case.id}), 201


@app.route('/api/user/<user_id>/cases', methods=['GET', 'POST'])
def manage_cases():
# ... and for cases ...


'''
def generate_salt():
    # 在此函数中生成随机盐
    return os.urandom(16).hex()
    pass

if __name__ == '__main__':
    app.run(debug=True)
