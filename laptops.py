from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from datetime import timedelta

app = Flask(__name__)


# Configuracion JWT
app.config["JWT_SECRET_KEY"] = "super-secret-key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)


# Usuarios predefinidos
users = [
    {"username": "cliente1", "password": generate_password_hash("1234"), "role": "client"},
    {"username": "manager1", "password": generate_password_hash("1234"), "role": "manager"},
    {"username": "admin1", "password": generate_password_hash("1234"), "role": "admin"},
]


# Login (POST)
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = next((u for u in users if u["username"] == username), None)
    if not user or not check_password_hash(user["password"], password):
        return jsonify({"msg": "Credenciales inválidas"}), 401

    access_token = create_access_token(
        identity=str(user["username"]),
        additional_claims={"role": user["role"]}
    )
    return jsonify({"msg": "Login exitoso", "token": access_token}), 200


# Endpoint para crear nuevos usuarios (solo admin)
@app.route("/add_user", methods=["POST"])
@jwt_required()
def add_user():
    current_user = get_jwt_identity()
    if current_user["role"] != "admin":
        return jsonify({"msg": "No autorizado. Solo un administrador puede crear usuarios."}), 403

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role")

    if not username or not password or not role:
        return jsonify({"msg": "Faltan campos requeridos"}), 400

    if any(u["username"] == username for u in users):
        return jsonify({"msg": "El usuario ya existe"}), 400

    new_user = {"username": username, "password": generate_password_hash(password), "role": role}
    users.append(new_user)

    return jsonify({"msg": "Usuario creado exitosamente", "usuario": new_user}), 201


# Diccionarios: 5 laptops predefinidas
laptops = [
    {
        "id": 1, 
        "marca": "Dell",
        "modelo": "XPS 13", 
        "procesador": "Intel i7", 
        "ram": "16GB", 
        "pricio": 10627000
    },
    {
        "id": 2, 
        "marca": "Apple", 
        "modelo": "MacBook Air M2", 
        "procesador": "Apple M2", 
        "ram": "8GB", 
        "pricio": 4949000
        },
    {
        "id": 3, 
        "marca": "HP", 
        "modelo": "Pavilion 15", 
        "procesador": "Intel i5", 
        "ram": "8GB", 
        "precio": 2000000
        },
    {
        "id": 4, 
        "marca": "Lenovo", 
        "modelp": "ThinkPad X1 Carbon", 
        "procesador": "Intel i7", 
        "ram": "16GB", 
        "precio": 2200000
        },
    {
        "id": 5,
        "marca": "Asus", 
        "modelo": "ROG Zephyrus G14", 
        "procesador": "AMD Ryzen 9", 
        "ram": "32GB", 
        "precio": 5500000
        }
]


# Endpoint: obtener laptop por ID (acceso solo con token)
@app.route("/laptops/<int:laptop_id>", methods=["GET"])
@jwt_required()
def get_laptop(laptop_id):
    ans = list(filter(lambda x: x["id"] == int(laptop_id), laptops))
    if not ans:
        return {"error": "El laptop no existe"}, 404
    return ans[0], 200


# Endpoint: obtener las laptops con filtros (solo clientes autenticados)
@app.route("/laptops", methods=["GET"])
@jwt_required()
def get_all_laptops():

    # Obtener query parameters
    marca_param = request.args.get("marca")
    procesador_param = request.args.get("procesador")
    ram_param = request.args.get("ram")

    print(f"Datos recibidos - marca: {marca_param}, procesador: {procesador_param}, ram: {ram_param}")

    ans = laptops

    # Filtro por marca
    if marca_param:
        ans = list(filter(lambda x: x["marca"].lower() == marca_param.lower(), ans))
        print(f"Filtrado por marca: {ans}")
    
    # Filtro por procesador
    if procesador_param:
        ans = list(filter(lambda x: x["procesador"].lower() == procesador_param.lower(), ans))
        print(f"Filtrado por procesador: {ans}")
    
    #filtro por ram
    if ram_param:
        ans = list(filter(lambda x: x["ram"].lower() == ram_param.lower(), ans))
        print(f"Filtrado por ram: {ans}")
    
    if not ans:
        return {"error": "No se encontraron laptops con los filtros proporcionados"}, 404
    
    return ans, 200


# Endpoint: agregar una laptop (solo manager o admin)
@app.route("/laptops", methods=["POST"])
@jwt_required()
def add_laptop():

    current_user = get_jwt_identity()
    if current_user["role"] not in ["manager", "admin"]:
        return jsonify({"msg": "No autorizado. Solo manager o admin pueden agregar laptops."}), 403

    new_laptop = request.get_json()
    
    # validar datos
    campos_requeridos = ["marca", "modelo", "procesador", "ram", "precio"]
    for campo in campos_requeridos:
        if campo not in new_laptop:
            return {"error": f"Falta el campo requerido: {campo}"}, 400
        
    new_id = len(laptops) + 1
    # Agregar nueva laptop al diccionario
    new_laptop = {
        "id": new_id,
        "marca": new_laptop["marca"],
        "modelo": new_laptop["modelo"],
        "procesador": new_laptop["procesador"],
        "ram": new_laptop["ram"],
        "precio": new_laptop["precio"]
    }
    
    laptops.append(new_laptop)
    print(f"Laptop agregada: {new_laptop}")

    return {"mensaje": "Laptop agregada", "Laptop": new_laptop}, 201


# Endpoint: eliminar una laptop (solo admin)
@app.route("/laptops/<int:laptop_id>", methods=["DELETE"])
@jwt_required()
def delete_laptop(laptop_id):
    current_user = get_jwt_identity()
    if current_user["role"] != "admin":
        return jsonify({"msg": "No autorizado. Solo admin puede eliminar laptops."}), 403

    ans = list(filter(lambda x: x["id"] == int(laptop_id), laptops))
    if not ans:
        return {"error": "El laptop no existe"}, 404    
    laptops.remove(ans[0])
    print(f"Laptop eliminada: {ans[0]}") 

    return {"mensaje": "Laptop eliminada", "Laptop": ans[0]}, 200  


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8003,
        debug=True
    )
    