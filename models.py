from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    salt = db.Column(db.String(64), nullable=False)
    role = db.Column(db.Enum('lawyer', 'admin'), default='lawyer', nullable=False)
    phone = db.Column(db.String(20))
    register_time = db.Column(db.DateTime, default=datetime.utcnow)
    key = db.Column(db.String(255))

    # Relationships
    documents = db.relationship('Document', backref='owner', lazy=True)
    cases = db.relationship('Case', backref='lawyer', lazy=True)


class Document(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    #document_number = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    case_number = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Client(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(50))
    citizen_id = db.Column(db.String(20), unique=True, nullable=False)
    postal_code = db.Column(db.String(10))
    address = db.Column(db.String(255))


    # Relationship
    cases = db.relationship('Case', backref='client', lazy=True)


class Case(db.Model):
    client_name = db.Column(db.String(100), nullable=False)
    client_id = db.Column(db.String(20), db.ForeignKey('client.citizen_id'), nullable=False)
    lawyer_name = db.Column(db.String(100), nullable=False)
    #lawyer_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    lawyer_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False, primary_key=True, default=str(uuid.uuid4()))
    case_number = db.Column(db.String(20), unique=True, nullable=False)
    opposite_party_name = db.Column(db.String(100))
    case_type = db.Column(db.String(50), nullable=False)
    court = db.Column(db.String(50))
    trial_level = db.Column(db.Enum('1', '2', '3'), default='1', nullable=False)
    dispute_subject = db.Column(db.Numeric(10, 2))
    agency_fee = db.Column(db.Numeric(10, 2))
    c_permission = db.Column(db.Enum('1', '2', '3', '4', '5', '6', '7', '8'), default='1', nullable=False)

