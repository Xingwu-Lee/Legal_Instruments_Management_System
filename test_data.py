from app import db
from models import User, Document, Client, Case
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_database.db'
    db.init_app(app)
    return app

def create_tables():
    # Create the database tables
    app = create_app()
    with app.app_context():
        db.create_all()
    print("Database tables created successfully.")

def delete_tables():
    # Drop all database tables
    app = create_app()
    with app.app_context():
        db.drop_all()
    print("Database tables deleted successfully.")

def view_data():
        app = create_app()
    # View data from database tables
        with app.app_context():
            users = User.query.all()
            clients = Client.query.all()
            cases = Case.query.all()

            print("Users:")
            for user in users:
                print(f"User ID: {user.id}, Name: {user.name}, Role: {user.role}  Password: {user.password} Salt: {user.salt}\n")

            print("\nClients:")
            for client in clients:
                print(f"Client ID: {client.id}, Name: {client.name}")

            print("\nCases:")
            for case in cases:
                print(f"Client Name: {case.client_name}, Lawyer Name:{case.lawyer_name}, Case Number: {case.case_number}")

if __name__ == "__main__":
    action = input("Enter action (create, delete, view): ").strip().lower()

    if action == "create":
        create_tables()
    elif action == "delete":
        confirm = input("This will delete all data in the database. Are you sure? (yes/no): ").strip().lower()
        if confirm == "yes":
            delete_tables()
    elif action == "view":
        view_data()
    else:
        print("Invalid action. Use 'create', 'delete', or 'view'.")
