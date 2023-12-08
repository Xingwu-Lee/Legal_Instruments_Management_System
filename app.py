from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db, Case
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

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



@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    existing_user = User.query.filter_by(name=data['name']).first()
    print("Received data:", data)
    print("Existing user:", existing_user)
    if existing_user:
        return jsonify({'message': '用户名已存在，来自：flask'}), 409
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(name=data['name'], password=hashed_password, role=data['role'], phone=data['phone'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Registered successfully!'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(name=data['name']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': '用户名或密码错误，来自：flask'}), 401
    else:
        token = create_access_token(identity=user.id)
        return jsonify({'token': token}), 200


'''
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

if __name__ == '__main__':
    app.run()
