from flask import Flask, jsonify, request

app = Flask(__name__)

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

# Endpoint: obtener laptop por ID
@app.route("/laptops/<int:laptop_id>", methods=["GET"])
def get_laptop(laptop_id):
    ans = list(filter(lambda x: x["id"] == int(laptop_id), laptops))
    if not ans:
        return {"error": "El laptop no existe"}, 404
    return ans[0], 200


# Endpoint: obtener las laptops con filtros
@app.route("/laptops", methods=["GET"])
def get_all_laptops():

    # Obtener query parameters
    marca_param = request.args.get("marca")
    procesador_param = request.args.get("procesador")
    ram_param = request.args.get("ram")

    print(f"Datos recibidos - marca: {marca_param}, procesador: {procesador_param}, ram: {ram_param}")

    ans = laptops

    #fultro por marca
    if marca_param:
        ans = list(filter(lambda x: x["marca"].lower() == marca_param.lower(), ans))
        print(f"Filtrado por marca: {ans}")
    
    #filtro por procesador
    if procesador_param:
        ans = list(filter(lambda x: x["procesador"].lower() == procesador_param.lower(), ans))
        print(f"Filtrado por procesador: {ans}")
    
    #filtro por ram
    if ram_param:
        ans = list(filter(lambda x: x["ram"].lower() == ram_param.lower(), ans))
        print(f"Filtrado por ram: {ans}")
    
    # Chequear si hay resultados
    if not ans:
        return {"error": "No se encontraron laptops con los filtros proporcionados"}, 404
    
    return ans, 200


# Endpoint: agregar una laptop
@app.route("/laptops", methods=["POST"])
def add_laptop():
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

    return {"mensaje": "Laptop agregado", "Laptop": new_laptop}, 201


# Endpoint: eliminar una laptop por ID
@app.route("/laptops/<int:laptop_id>", methods=["DELETE"])
def delete_laptop(laptop_id):
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
