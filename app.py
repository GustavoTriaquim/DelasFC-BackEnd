from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
import bcrypt
from bson import ObjectId

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = "mongodb+srv://gustavotriaquim6:Salu0411G@delasfc-sitemobileclust.gedlw.mongodb.net/"
mongo = PyMongo(app)

@app.route('/register', methods=['POST'])
def register():
  data = request.get_json()

  required_fields = ["cpf", "nome", "email", "data_nasc", "senha"]
  for field in required_fields:
    if field not in data:
      return jsonify({"error": f"Campo {field} é obrigatório"}), 400
    
  existing_user = mongo.db.users.find_one({"email": data['email']})
  if existing_user:
    return jsonify({"error": "E-mail já cadastrado"}), 400
  
  hashed_password = bcrypt.hashpw(data['senha'].encode('utf-8'), bcrypt.gensalt())

  user = {
    "cpf": data["cpf"],
    "nome": data["nome"],
    "email": data["email"],
    "data_nasc": data["data_nasc"],
    "senha": hashed_password
  }

  mongo.db.users.insert_one(user)

  return jsonify({"message": "Usuário cadastrado com sucesso!"}), 201

@app.route('/login', methods=['POST'])
def login():
  data = request.get_json()

  if 'email' not in data or 'senha' not in data:
    return jsonify({"error": "Email e senha são obrigatórios"}), 400
  
  user = mongo.db.users.find_one({"email": data['email']})
  if not user:
    return jsonify({"error": "E-mail não encontrado"})
  
  if not bcrypt.checkpw(data['senha'].encode('utf-8'), user['senha']):
    return jsonify({"error": "Senha incorreta"}), 400
  
  return jsonify({"message": "Login bem-sucedido!"}), 200

if __name__ == '__main__':
  app.run(debug=True)