from flask import Flask, request, jsonify, redirect, url_for, session, render_template, send_from_directory
from flask_uploads import UploadSet, configure_uploads, DOCUMENTS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db, Case, Client, Document
from flask_cors import CORS
from middlewares import check_empty_json
import os
import uuid

import subprocess


app = Flask(__name__, template_folder='web', static_folder='web/src')
#CORS(app, supports_credentials=True, expose_headers=['Content-Type', 'Authorization', 'X-Requested-With'])
CORS(app, supports_credentials=True)
#app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = 'your_secret_key'  # 设置一个安全的密钥

# Database Configuration
#app.config.from_object('config_test.TestConfig')

UPLOAD_FOLDER = '/database/file'
#ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


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
    def generate_salt():
        # 在此函数中生成随机盐
        return os.urandom(16).hex()
        pass

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
    result = [{'citizen_id': client.citizen_id, 'name': client.name, } for client in clients]
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
    data = request.get_json()
    print("Received data:", data)
    file_id = str(uuid.uuid4())
    new_document = Document(id=file_id, title=data['file_title'], description=data['file_description'], type=data['file_type'], case_number=data['file_case_number'])
    print("New file info:", new_document)
    db.session.add(new_document)
    db.session.commit()
    return jsonify({'message': '文件上传成功！'}), 201

'''
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Save document details in database
        new_document = Document(
            document_number=request.form['document_number'],
            title=request.form['title'],
            type=request.form['type'],
            d_permission=request.form['d_permission'],
            owner_id=1,  # Assign an owner ID
            file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        )
        db.session.add(new_document)
        db.session.commit()

        return redirect(url_for('index'))
'''

@app.route('/get_file_list')
def get_file_list():
    files = Document.query.all()
    files_list = [{'title': d.title, 'description': d.description, 'type': d.type} for d in files]
    return jsonify(files_list)
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

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    pdfdata = request.json

    # 获取用户选择的模板
    template_choice = pdfdata.get('template_choice', 'default')

    # 根据不同模板选择获取相应数据
    if template_choice == 'default':
        # 获取基本信息
        party_a = pdfdata.get('party_a', 'Party A')
        party_b = pdfdata.get('party_b', 'Party B')
        agreement_content = pdfdata.get('agreement_content', 'This is the content of the agreement.')

        # 获取PDF格式设置
        margin = pdfdata.get('margin', '2cm')
        linespread = pdfdata.get('linespread', '1.5')
        font_size = pdfdata.get('font_size', '12pt')

        latex_code = f"""
        \\documentclass[{font_size}]{{article}}
        \\usepackage{{ctex}}
        \\usepackage[utf8]{{inputenc}}
        \\usepackage[margin={margin}]{{geometry}}
        \\usepackage{{setspace}}
        \\setstretch{{{linespread}}}
        \\begin{{document}}
        \\title{{Agreement}}
        \\maketitle

        This Agreement is made this day between {party_a} and {party_b}.

        \\section*{{Terms and Conditions}}
        {agreement_content}

        \\section*{{Signatures}}
        \\noindent
        {party_a}: \\underline{{\\hspace{{4cm}}}} \\hfill {party_b}: \\underline{{\\hspace{{4cm}}}}

        \\end{{document}}
        """
    elif template_choice == 'authorization_letter':
        # 获取受委托书的信息
        client_name = pdfdata.get('client_name', '')
        attorney_name = pdfdata.get('attorney_name', '')
        work_unit = pdfdata.get('work_unit', '')
        position = pdfdata.get('position', '')
        phone = pdfdata.get('phone', '')
        case_name = pdfdata.get('case_name', '')
        case_reason = pdfdata.get('case_reason', '')
        agent_power = pdfdata.get('agent_power', '')

        latex_code = f"""
        \\documentclass[12pt]{{article}}
        \\usepackage{{ctex}} % 支持中文字符
        \\usepackage{{ulem}} % 用于文本下划线
        \\usepackage{{geometry}} % 页面边距设置
        \\geometry{{a4paper, left=25mm, right=25mm, top=25mm, bottom=25mm}}

        \\begin{{document}}

        \\begin{{center}}
            \\zihao{{3}} \\textbf{{授 权 委 托 书}} % 标题加粗，字号较大
        \\end{{center}}

        \\zihao{{4}} % 正文字号
        \\textbf{{委托人：}} {client_name}\par

        \\textbf{{受委托人：}} \\quad 姓名：{attorney_name}\par
        \\hspace*{{27mm}} 工作单位：{work_unit} \\hspace{{2em}} 职务：{position}\par
        \\hspace*{{27mm}} 电话：{phone}\par

        现委托上列受委托人在我与{case_name}因{case_reason}纠纷一案中，作为我的诉讼代理人。\par

        代理人\\hspace{{2em}}的代理权限为：{agent_power}\par

        \\vspace{{5\\baselineskip}} % 留出五行空白

        \\begin{{flushright}}
            委托人：（签名或盖章）\\underline{{\\hspace{{4cm}}}} \\\\
            年 \\quad 月 \\quad 日
        \\end{{flushright}}

        \\end{{document}}
        """


    elif template_choice == 'legal_rep_identity':
        rep_name = pdfdata.get('rep_name', '')
        position = pdfdata.get('position', '')
        unit_name = pdfdata.get('unit_name', '')
        date = pdfdata.get('date', '')
        address = pdfdata.get('address', '')
        phone = pdfdata.get('phone', '')
        year, month, day = date.split('-')

        latex_code = f"""
        \\documentclass[12pt]{{article}}
        \\usepackage{{ctex}} % 支持中文字符
        \\usepackage{{geometry}} % 页面边距设置
        \\geometry{{a4paper, left=25mm, right=25mm, top=25mm, bottom=25mm}}

        \\begin{{document}}

        \\begin{{center}}
            \\zihao{{3}} \\textbf{{法定代表人身份证明书}} % 标题加粗，字号较大
        \\end{{center}}

        \\zihao{{4}} % 正文字号
        \\textbf{{{rep_name}同志，在我单位任{position}职务，特此证明。}} \\

        \\begin{{flushright}}
            \\textbf{{单位全称（盖章）：{unit_name}}} \\\\
            \\textbf{{{year}年 {month}月 {day}日}}
        \\end{{flushright}}

        \\vspace{{2\\baselineskip}} % 地址前的空白
        \\textbf{{附：该代表人住址：}}{address} \\

        \\vspace{{1\\baselineskip}} % 地址空白
        \\hspace*{{22mm}} \\textbf{{电 话：{phone}}} \\



        \\begin{{flushleft}}
            \\small \\textbf{{注：企业事业单位、机关、团体的主要负责人为本单位的法定代表人。}}
        \\end{{flushleft}}

        \\end{{document}}
        """
    elif template_choice == 'lawyer_agency_contract':
        client_address = pdfdata.get('client_address', '')
        client_postcode = pdfdata.get('client_postcode', '')
        client_phone = pdfdata.get('client_phone', '')
        opponent_name = pdfdata.get('opponent_name', '')
        case_reason = pdfdata.get('case_reason', '')
        trial_authority = pdfdata.get('trial_authority', '')
        trial_level = pdfdata.get('trial_level', '')
        dispute_object = pdfdata.get('dispute_object', '')

        latex_code = f"""
        \\documentclass[12pt]{{article}}
        \\usepackage{{ctex}} % 支持中文字符
        \\usepackage{{geometry}} % 页面边距设置
        \\geometry{{a4paper, left=25mm, right=25mm, top=25mm, bottom=25mm}}

        \\begin{{document}}

        \\section*{{委托律师代理合同（个人诉讼）}}

        \\subsection*{{甲方信息}}
        \\begin{{itemize}}
            \\item 地址：{client_address}
            \\item 邮政编码：{client_postcode}
            \\item 电话：{client_phone}
        \\end{{itemize}}

        \\subsection*{{乙方信息}}
        乙方：北京市中鸿律师事务所
        \\begin{{itemize}}
            \\item 地址：北京市东长安街 10 号长安大厦 704 室
            \\item 邮政编码：100006
            \\item 电话：010—65251878
            \\item 传真：010—65257668
        \\end{{itemize}}

        甲方因纠纷一案，根据中华人民共和国《合同法》、《民事诉讼法》、《仲裁法》和《律师法》等有关法律的规定，聘请乙方的律师作为委托代理人。

        甲乙双方按照诚实信用原则，经协商一致，立此合同，共同遵守。

        \\section*{{第一条 委托代理事项}}
        乙方接受甲方委托，委派律师在下列案件中担任甲方的委托代理人：
        \\begin{{enumerate}}
            \\item 对方当事人名称或者姓名：{opponent_name}
            \\item 案由：{case_reason}
            \\item 审理机关：{trial_authority}
            \\item 审级：{trial_level}
            \\item 诉讼（仲裁）争议标的：{dispute_object}
        \\end{{enumerate}}

        （此争议标的数额与诉讼/仲裁请求事项均由甲方确定，并对此负责。）

        \\section*{{第二条 委托代理权限}}
        一般代理。
        或者
        特别授权，包括（选择项）：
        \\begin{{enumerate}}
            \\item 变更或者放弃诉讼请求；
            \\item 承认诉讼请求；
            \\item 提起反诉；
            \\item 进行调解或者和解；
            \\item 提起上诉；
            \\item 申请执行；
            \\item 收取或者收转执行标的；
            \\item 签署、送达、接受法律文书。
        \\end{{enumerate}}

        \\section*{{第三条 乙方的义务}}
        \\begin{{enumerate}}
            \\item 乙方委派律师作为上述案件中甲方的委托代理人，甲方同意上述律师指派其他业务助理配合完成辅助工作，但乙方更换代理律师应取得甲方认可；
            \\item 乙方律师应当勤勉、尽责地完成第一条所列委托代理事项；
            \\item 乙方律师应当尽最大努力维护甲方利益；
            \\item 乙方律师应当根据审理机关的要求，及时提交证据，按时出庭，并应甲方要求通报案件进展情况；
            \\item 乙方律师不得违反《律师执业规范》，在涉及甲方的对抗性案件中，未经甲方同意，不得同时担任与甲方具有法律上利益冲突的另一方的委托代理人；
            \\item 乙方律师对其获知的甲方的商业机密／或者甲方的个人隐私负有保密责任，非由法律规定或者甲方同意，不得向任何第三方披露；
            \\item 乙方对涉及甲方的原始证据、法律文件和财物应当妥善保管。
        \\end{{enumerate}}

        \\section*{{第四条 甲方的义务}}
        \\begin{{enumerate}}
            \\item 甲方应当真实、详尽和及时地向乙方律师叙述案件，主动向乙方律师提供与委托代理事项有关的证据、文件及其它事实材料；
            \\item 甲方应当积极、主动地配合乙方律师的工作，甲方对乙方律师提出的要求应当明确、合理；
            \\item 甲方应当按时、足额向乙方支付律师代理费和工作费用；
            \\item 甲方指定为乙方律师的联系人，负责转达甲方的指示和要求，提供文件和资料等；
            \\item 甲方有责任对委托代理事项作出独立的判断、决策。甲方根据乙方律师提供的法律意见、建议、方案所作出的决定而导致的损失，由甲方自行承担；
            \\item 甲方对案件中自己一方的起诉状（仲裁申请）、答辩状、申请书等法律文件的内容、真实、是否有效、是否被有关机关采信负责。
        \\end{{enumerate}}

        \\end{{document}}
        """
    elif template_choice == 'power_of_attorney':
        client_unit = pdfdata.get('client_unit', '')
        case = pdfdata.get('case', '')
        case_reason = pdfdata.get('case_reason', '')
        date = pdfdata.get('date', '')
        year, month, day = date.split('-')

        latex_code = f"""
        \\documentclass[12pt]{{article}}
        \\usepackage{{ctex}} % 支持中文字符
        \\usepackage{{geometry}} % 页面边距设置
        \\geometry{{a4paper, left=25mm, right=25mm, top=25mm, bottom=25mm}}

        \\begin{{document}}

        \\section*{{授权委托书}}

        委托单位：{client_unit}

        法定代表人：职务：

        受委托人：姓名：周唯 职务：律师

        工作单位：北京市中闻律师事务所

        住址：北京市海淀区北太平庄路 18 号城建大厦 A 座 7 层

        电话：83355416 手机：13901129159

        现委托上列受委托人在我单位与{case}案，作为我方代理人。 

        因{case_reason}纠纷一

        代理人周唯律师的代理权限为：代理财产保全，代为提出/承认、放弃、变更诉讼请求，进行和解，提起反诉/上诉，参加一/二审诉讼全过程。

        委托单位：{client_unit}

        年 {year} 月 {month} 日 {day}

        \\end{{document}}
        """
    elif template_choice == 'contract':

        client_name = pdfdata.get('client_name', '')
        client_gender = pdfdata.get('client_gender', '')
        client_id = pdfdata.get('client_id', '')
        client_phone = pdfdata.get('client_phone', '')
        client_email = pdfdata.get('client_email', '')
        client_address = pdfdata.get('client_address', '')
        opposing_party_name = pdfdata.get('opposing_party_name', '')
        case_reason = pdfdata.get('case_reason', '')
        judicial_body = pdfdata.get('judicial_body', '')
        judicial_level = pdfdata.get('judicial_level', '')
        lawyer_fee = pdfdata.get('lawyer_fee', '')
        signing_date = pdfdata.get('signing_date', '')

        latex_code = f"""
        \\documentclass[12pt]{{article}}
        \\usepackage{{ctex}} % 支持中文字符
        \\usepackage{{geometry}} % 页面边距设置
        \\geometry{{a4paper, left=25mm, right=25mm, top=25mm, bottom=25mm}}

        \\begin{{document}}

        \\section*{{委托代理合同}}

        甲方：\\
        {client_name}\\
        {client_gender}\\
        {client_id}\\
        {client_phone}\\
        {client_email}\\
        {client_address}\\

        乙方：

        根据中华人民共和国相关适用法律，甲方聘请乙方律师作为参加诉讼的委托代理人。双方经协商一致，立此合同。

        \\section{{第一条：委托代理事项}}
        乙方接受甲方委托，委派律师在下列案件中担任甲方的诉讼代理人：\\
        （一）对方当事人名称或者姓名 {opposing_party_name}\\
        （二）案由 {case_reason}\\
        （三）审理机关 {judicial_body}\\
        （四）审级 {judicial_level}\\

        \\section{{第二条 委托代理权限}}
        一般代理。

        \\section{{第三条 乙方义务}}
        "乙方委派赵晶律师作为甲方的委托代理人，代理权限由双方另以《授权委托书》确认。甲方同意乙方委派律师指派其他律师或者业务助理完成除庭审外的委托代理工作。乙方律师应以其依据法律作出的判断，向甲方提示法律风险，尽最大努力维护甲方利益。乙方律师应当根据审理机关的要求，及时提交证据，按时出庭。乙方律师对其获知的甲方信息依法负有保密义务，非由法律规定或者甲方同意，不得向任何第三方披露。"

        \\section{{第四条 甲方义务}}
        "甲方应当真实、详尽和及时地向乙方律师陈述案情，提供与委托代理事项有关的证据、文件及其它事实材料。甲方应当积极、主动配合乙方律师的工作，甲方对乙方律师提出的要求应当明确、合理。甲方应当按时、足额向乙方支付律师费和工作费用。甲方有义务对委托代理事项作出独立的判断、决策。"

        \\section{{第五条 律师费}}
        ¥- {lawyer_fee}（大写：人民币 零 元整）。\\
        甲方于本合同生效之日支付至乙方如下账户：\\
        （一）户 名：\\
        （二）开户行：\\
        （三）账 号：

        \\section{{第六条 工作费用}}
        "乙方律师办理甲方委托代理事项发生的下列工作费用，由甲方承担：（一）相关行政、司法、鉴定、公证等部门收取的费用，包括但不限于乙方为甲方提供法律服务的过程中发生的诉讼费、仲裁费、鉴定费、检验费、评估费、公证费、查档费等；（二）北京市外发生的差旅费、食宿费；（三）征得甲方同意后支出的其它费用。"

        \\section{{第七条 争议解决}}
        因本合同引起的或与本合同有关的任何争议，均适用中华人民共和国法律，并提请北京仲裁委员会／北京国际仲裁中心按照其仲裁规则进行仲裁。仲裁裁决是终局的，对双方均有约束力。

        \\section{{第八条 附则}}
        本合同中文打印，无手书内容，一式三份，甲方一份、乙方二份，由甲方签字、乙方盖章，自签订之日起生效，至乙方完成本合同约定委托代理事项之日终止。

        \\section{{第九条 通知送达}}
        甲乙双方因履行本合同而相互发出或者提供的所有通知、文件、资料，纸质版以双方另行确认的地址送达，电子版以电子邮件送达。电子邮件地址：\\
        （一）甲方： {client_email}\\
        （二）乙方：

        任何一方变更送达地址，应当将变更后的地址送达另一方，否则不得以未送达为由抗辩。
        （下无正文！）

        甲方：\\
        乙方：\\

        “签约日期”于中国北京 {signing_date}

        \\end{{document}}
        """

    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    tex_filename = 'document.tex'
    pdf_filename = 'document.pdf'
    tex_filepath = os.path.join(output_dir, tex_filename)

    with open(tex_filepath, "w", encoding="utf-8") as file:
        file.write(latex_code)

    # pdflatex_path = "/server/MiKTeX/miktex/bin/x64/pdflatex"
    # subprocess.run([pdflatex_path, "-output-directory", output_dir, tex_filepath])

    # xelatex_path = "xelatex"
    # subprocess.run([xelatex_path, "-output-directory", output_dir, tex_filepath])

    #lualatex_path = r"/server/MiKTeX/miktex/bin/x64/lualatex.exe"
    #目前使用绝对路径（‘\’是Windows格式），需要改成项目内相对路径用‘/’Linux格式
    lualatex_path = r"E:\OneDrive\College\FYP\Legal_Instruments_Management_System\server\MiKTeX\miktex\bin\x64\lualatex"
    subprocess.run([lualatex_path, "-output-directory", output_dir, tex_filepath])

    return send_from_directory(output_dir, pdf_filename, as_attachment=True)


if __name__ == '__main__':
    app.run(port=8080, debug=True)