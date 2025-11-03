from flask import Flask, jsonify, request, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
)
from datetime import timedelta
from dotenv import load_dotenv
import os
from models import laptops_collection, users_collection

load_dotenv()

app = Flask(__name__)

# Config JWT
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
    hours=int(os.getenv("TOKEN_EXPIRES_HOURS", 1))
)
jwt = JWTManager(app)

# Crear usuario admin si no existe
if users_collection.count_documents({"username": "admin"}) == 0:
    users_collection.insert_one({
        "username": "admin",
        "password": generate_password_hash("1234"),
        "role": "admin"
    })

# ---- LOGIN ----
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = users_collection.find_one({"username": username})
    if not user or not check_password_hash(user["password"], password):
        return jsonify({"msg": "Credenciales inválidas"}), 401

    access_token = create_access_token(
        identity=username,
        additional_claims={"role": user["role"]}
    )
    return jsonify(access_token=access_token), 200


# ---- AGREGAR LAPTOP ----
@app.route("/laptops", methods=["POST"])
@jwt_required()
def add_laptop():
    claims = get_jwt()
    role = claims.get("role")

    if role not in ["manager", "admin"]:
        return jsonify({"msg": "No autorizado."}), 403

    new_laptop = request.get_json()
    campos = ["marca", "modelo", "procesador", "ram", "precio"]
    for campo in campos:
        if campo not in new_laptop:
            return {"error": f"Falta el campo requerido: {campo}"}, 400

    laptops_collection.insert_one(new_laptop)
    return {"mensaje": "Laptop agregada", "Laptop": new_laptop}, 201


# ---- OBTENER TODAS LAS LAPTOPS ----
@app.route("/laptops", methods=["GET"])
def get_laptops():
    laptops = list(laptops_collection.find({}, {"_id": 0}))
    return jsonify(laptops)


# ---- SSR: Renderizado del lado del servidor ----
@app.route("/laptops/view")
def view_laptops():
    laptops = list(laptops_collection.find({}, {"_id": 0}))
    return render_template("laptops.html", laptops=laptops)

if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8003,
        debug=True
    )
    