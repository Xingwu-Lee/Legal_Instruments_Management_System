from flask import Flask, request, jsonify, redirect, url_for, session, render_template
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db, Case, Client
from flask_cors import CORS
from middlewares import check_empty_json
import os
import uuid


app = Flask(__name__, template_folder='web', static_folder='web/src')
#CORS(app, supports_credentials=True, expose_headers=['Content-Type', 'Authorization', 'X-Requested-With'])
CORS(app, supports_credentials=True)
#app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = 'your_secret_key'  # 设置一个安全的密钥

# Database Configuration
#app.config.from_object('config_test.TestConfig')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this!

#db = SQLAlchemy(app)
jwt = JWTManager(app)

@app.route('/')
def index():
    # 使用 redirect 函数将 '/' 重定向到 '/login'
    return redirect(url_for('login'))
# Register the check_empty_json middleware
@app.before_request
def before_request():
    error_response = check_empty_json(request)
    if error_response:
        return error_response

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        user = User.query.filter_by(name=data['name']).first()
        if user is None:
            return jsonify({'message': '用户名不存在'}), 401
        stored_hashed_password = user.password
        stored_salt = user.salt
        if check_password_hash(stored_hashed_password, data['password'] + stored_salt):
            #token = create_access_token(identity=user.id)
            session['user_id'] = user.id  # 存储用户ID到会话
            return jsonify({'redirect': url_for('profile')}), 200
        else:
            return jsonify({'message': '密码错误'}), 401
    else:
        # Logic for GET request, like rendering a login form
        return render_template('login.html')
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    existing_user = User.query.filter_by(name=data['name']).first()
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

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    #user = session.get(User, user_id)
    user = User.query.get(user_id)  # 从数据库获取用户信息
    print("User:", user)
    if user:
        return render_template('main.html', user_name=user.name, user_phone=user.phone, user_id=user.id)
        #return render_template('main.html', user_name=user.name, user_phone=user.phone, token=token)
    else:
        return redirect(url_for('login'))  # 如果无法获取用户信息，则重定向到登录页面

@app.route('/newClient', methods=['POST'])
def newClient():
    data = request.get_json()
    existing_client = Client.query.filter_by(citizen_id=data['citizen_id']).first()
    #调试用
    print("Received data:", data)
    print("Existing client:", existing_client)
    if existing_client:
        return jsonify({'message': '客户已存在'}), 409
    client_id = str(uuid.uuid4())
    new_client = Client(id=client_id, name=data['name'], phone=data['phone'], email=data['email'],
                        citizen_id=data['citizen_id'], postal_code=data['postal_code'], address=data['address'])
    print("New user info:", new_client)
    db.session.add(new_client)
    db.session.commit()
    return jsonify({'message': '客户档案添加成功！'}), 201
@app.route('/newCase', methods=['POST'])
def newCase():
    data = request.get_json()
    case_id = str(uuid.uuid4())
    new_case = Case(id=case_id, name=data['name'], phone=data['phone'], email=data['email'],
                        citizen_id=data['citizen_id'], postal_code=data['postal_code'], address=data['address'])
    print("New case info:", new_case)
    db.session.add(new_case)
    db.session.commit()
    return jsonify({'message': '案件添加成功！'}), 201

@app.route('/search_clients', methods=['GET'])
def search_clients():
    query = request.args.get('query')
    # 使用SQLAlchemy查询数据库以模糊搜索用户
    clients = Client.query.filter(Client.name.ilike(f'%{query}%')).all()
    # 将结果转换为JSON并发送回前端
    #result = [{'citizen_id': client.citizen_id, 'name': client.name} for client in clients]
    result = [{'name': client.name} for client in clients]
    return jsonify(result)



'''
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    # 可以使用current_user来获取当前登录的用户ID
    # ...
    return jsonify(logged_in_as=current_user)

@app.route('/user/<user_id>/documents', methods=['GET', 'POST'])
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


@app.route('/user/<user_id>/files', methods=['GET', 'POST', 'PUT', 'DELETE'])
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


@app.route('/user/<user_id>/cases', methods=['POST'])
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


'''
def generate_salt():
    # 在此函数中生成随机盐
    return os.urandom(16).hex()
    pass

if __name__ == '__main__':
    app.run(port=8080, debug=True)

