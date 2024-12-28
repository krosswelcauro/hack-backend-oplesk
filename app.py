from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@hack-crud-oplesk.cvwayqmi2npj.us-east-2.rds.amazonaws.com:5432/crud_oplesk'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/crud_oplesk'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definicion de Modelo Usuarios
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "age": self.age,
        }

# Creando las tablas de la BD
with app.app_context():
    db.create_all()
    
    try:
        db.session.execute(text('SELECT 1'))
    except Exception as e:
        print(f'Error al conectar con la base de datos {e}')


@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    # usuarios_list = [{"id": user.id, "email": user.email, "name": user.name, "age": user.age} for user in users]
    users_list = [ user.to_dict() for user in users ] 
    # total_users = User.query.count()
    return jsonify({"data": users_list})

@app.route("/user/<int:userId>", methods=["GET"])
def get_user_by_id(userId):
    user = User.query.get(userId)
    if user:
        return jsonify(user.to_dict())
    return jsonify({"message": "Usuario no registrado"})

@app.route("/create-user", methods=["POST"])
def store_user():
    request_data = request.get_json()
    name = request_data["name"]
    email = request_data["email"]
    age = request_data["age"]

    new_user = User(name = name, email = email, age = age)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Usuario creado correctamente", "data": new_user.to_dict()})

@app.route("/delete-user/<int:userId>", methods=["DELETE"])
def delete_user_by_id(userId):
    user = User.query.get(userId)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Usuario eliminado"})
    return jsonify({"message": "El usuario no ha sido encontrado"})

@app.route("/update-user/<int:userId>", methods=["PATCH"])
def update_one_user(userId):
    data = request.get_json()
    user = User.query.get(userId)
    if user:
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return jsonify({"message": "Usuario modificado", "data": user.to_dict()})
    return jsonify({"message": "El usuario no ha sido encontrado"})