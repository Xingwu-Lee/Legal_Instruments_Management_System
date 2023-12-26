from flask import Flask, request, jsonify, redirect, url_for, session, render_template
from flask_uploads import UploadSet, configure_uploads, DOCUMENTS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db, Case, Client, Document
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
app.config['UPLOADED_FILES_DEST'] = '/database/file'
files = UploadSet('files', DOCUMENTS)
configure_uploads(app, files)
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
    user = User.query.get(user_id)  # 从数据库获取用户信息
    print("User:", user)
    if user:
        return render_template('main.html', user_name=user.name, user_phone=user.phone, user_id=user.id)
        # return render_template('main.html', user_name=user.name, user_phone=user.phone, token=token)
    else:
        return redirect(url_for('login'))  # 如果无法获取用户信息，则重定向到登录页面

@app.route('/newClient', methods=['POST'])
def newClient():
    data = request.get_json()
    existing_client = Client.query.filter_by(citizen_id=data['citizen_id']).first()
    #调试用
    print("Received data:", data)
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
    existing_case = Case.query.filter_by(case_number=data['case_number']).first()
    # 调试用
    print("Received data:", data)
    if existing_case:
        return jsonify({'message': '案件已存在'}), 409
    lawyer_id = session['user_id']  # 假设律师ID从会话中获取
    lawyer_name = User.query.get(session['user_id']).name  # 假设从数据库中获取律师姓名
    new_case = Case(client_name=data['client_name'], client_id=data['client_id'],
                    lawyer_name=lawyer_name, lawyer_id=lawyer_id, case_number=data['case_number'],
                    opposite_party_name=data['opposite_party_name'], case_type=data['case_type'], court=data['court'],
                    trial_level=data['trial_level'], dispute_subject=data['dispute_subject'],
                    agency_fee=data['agency_fee'], c_permission=data['c_permission'])
    print("New case info:", new_case)
    db.session.add(new_case)
    db.session.commit()
    return jsonify({'message': '案件添加成功！'}), 201

@app.route('/searchClients', methods=['GET'])
def searchClients():
    query = request.args.get('query')
    # 使用SQLAlchemy查询数据库以模糊搜索用户
    clients = Client.query.filter(Client.name.ilike(f'%{query}%')).all()
    # 将结果转换为JSON并发送回前端
    result = [{'citizen_id': client.citizen_id, 'name': client.name} for client in clients]
    return jsonify(result)

#加载客户列表
@app.route('/get_clients')
def get_clients():
    clients = Client.query.all()
    client_list = [{'id': c.id, 'name': c.name, 'phone': c.phone, 'citizen_id': c.citizen_id} for c in clients]
    return jsonify(client_list)

@app.route('/delete_client/<client_id>', methods=['DELETE'])
def delete_client(client_id):
    client = Client.query.get(client_id)
    if client:
        db.session.delete(client)
        db.session.commit()
        return jsonify({'message': '客户删除成功'})
    return jsonify({'message': '客户不存在'}), 404


#获取单个客户信息
@app.route('/get_client/<client_id>')
def get_client(client_id):
    client = Client.query.get(client_id)
    if client:
        client_data = {'id': client.id, 'name': client.name, 'phone': client.phone, 'citizen_id': client.citizen_id, 'address': client.address, 'email': client.email, 'postal_code': client.postal_code}
        return jsonify(client_data)
    return jsonify({'message': '客户不存在'}), 404
#update the client
@app.route('/update_client/<client_id>', methods=['PUT'])
def update_client(client_id):
    data = request.get_json()
    client = Client.query.get(client_id)
    if client:
        client.name = data['name']
        client.phone = data['phone']
        client.email = data['email']
        client.citizen_id = data['citizen_id']
        client.postal_code = data['postal_code']
        client.address = data['address']
        db.session.commit()
        return jsonify({'message': '客户信息已更新'})
    return jsonify({'message': '客户不存在'}), 404

# Load the list of cases
@app.route('/get_cases')
def get_cases():
    cases = Case.query.all()
    case_list = [{'case_number': case.case_number, 'client_name': case.client_name, 'case_type': case.case_type, 'lawyer_name': case.lawyer_name} for case in cases]
    return jsonify(case_list)

# Delete the case
@app.route('/delete_case/<case_number>', methods=['DELETE'])
def delete_case(case_number):
    case = Case.query.get(case_number)
    if case:
        db.session.delete(case)
        db.session.commit()
        return jsonify({'message': '案件删除成功'})
    return jsonify({'message': '案件不存在'}), 404

# Get single case info
@app.route('/get_case/<case_number>')
def get_case(case_number):
    case = Case.query.get(case_number)
    if case:
        case_data = {
            'opposite_party_name': case.opposite_party_name,
            'case_number': case.case_number,
            'case_type': case.case_type,
            'court': case.court,
            'agency_fee': case.agency_fee,
            'dispute_subject': case.dispute_subject,
            'trial_level': case.trial_level,
            'c_permission': case.c_permission
        }
        return jsonify(case_data)
    return jsonify({'message': '案件不存在'}), 404

# Update the case info
@app.route('/update_case/<case_number>', methods=['PUT'])
def update_case(case_number):
    data = request.get_json()
    case = Case.query.get(case_number)
    if case:
        case.opposite_party_name = data['opposite_party_name']
        case.case_number = data['case_number']
        case.case_type = data['case_type']
        case.court = data['court']
        case.agency_fee = data['agency_fee']
        case.dispute_subject = data['dispute_subject']
        case.trial_level = data['trial_level']
        case.c_permission = data['c_permission']
        db.session.commit()
        return jsonify({'message': '案件信息已更新'})
    return jsonify({'message': '案件不存在'}), 404



# 路由处理文件上传
@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' in request.files:
        file = request.files['file']
        description = request.form.get('description', '')
        filename = files.save(file)
        file_url = files.url(filename)

        # 创建一个新的文档对象并保存到数据库
        new_document = Document(
            name=filename,
            url=file_url,
            description=description
        )
        db.session.add(new_document)
        db.session.commit()

        return jsonify({'message': '文件上传成功', 'url': file_url})
    return jsonify({'message': '没有文件上传'}), 400


@app.route('/get_file_list')
def get_file_list():
    # 这里的逻辑取决于您是如何存储文件信息的
    # 假设有一个函数get_all_files()返回所有文件信息
    files = get_all_files() # 例如: [{'id': 1, 'name': 'file1.pdf', ...}, ...]
    return jsonify(files)
def get_all_files():
    # 查询所有文件信息
    documents = Document.query.all()
    return [{'id': doc.id, 'name': doc.name, 'url': doc.url, 'description': doc.description} for doc in documents]

@app.route('/delete_file/<int:file_id>', methods=['DELETE'])
def delete_file(file_id):
    document = Document.query.get(file_id)
    if document:
        db.session.delete(document)
        db.session.commit()
        file_path = os.path.join(app.config['UPLOADED_FILES_DEST'], document.name)
        if os.path.exists(file_path):
            os.remove(file_path)
        return jsonify({'message': '文件删除成功'})
    return jsonify({'message': '文件不存在'}), 404


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

    return jsonify({'message': 'New case created', 'case_number': new_case.id}), 201


'''
def generate_salt():
    # 在此函数中生成随机盐
    return os.urandom(16).hex()
    pass

if __name__ == '__main__':
    app.run(port=8080, debug=True)