# 💻 API Laptops - Flask + MongoDB + JWT

Esta API permite **gestionar laptops** con autenticación por roles (`client`, `manager`, `admin`) usando **Flask**, **MongoDB** y **JWT**.  
Incluye autenticación, autorización, renderizado del lado del servidor (SSR) y manejo de filtros.

---

## 📁 Estructura del proyecto

project/
│
├── laptops.py # Archivo principal (endpoints + app)
├── models.py # Conexión y operaciones con MongoDB
├── .env # Variables de entorno (no subir a GitHub)
├── requirements.txt # Dependencias
├── README.md # Documentación
│
└── templates/
└── laptops.html # Vista HTML (server-side rendering)


---

## ⚙️ Configuración del entorno

1️⃣ **Crea un entorno virtual**
```bash
python -m venv venv
venv\Scripts\activate        # En Windows
# o en Linux/Mac
source venv/bin/activate

2️⃣ Instala las dependencias
pip install -r requirements.txt

3️⃣ Crea el archivo .env
JWT_SECRET_KEY=super-secret-key
MONGO_URI=mongodb://localhost:27017/laptopdb

4️⃣ Ejecuta la aplicación
python laptops.py

La API correrá en:
👉 http://localhost:8003

-------------------------

🔑 Endpoints y ejemplos con CURL

1️⃣ Registrar un usuario
curl -X POST http://localhost:8003/register \
 -H "Content-Type: application/json" \
 -d '{
   "username": "admin",
   "password": "1234",
   "role": "admin"
 }'


Respuesta:
{"msg": "Usuario creado correctamente"}

2️⃣ Login (Obtener token)
curl -X POST http://localhost:8003/login \
 -H "Content-Type: application/json" \
 -d '{
   "username": "admin",
   "password": "1234"
 }'


Respuesta:
{
  "msg": "Login exitoso",
  "token": "<JWT_TOKEN>"
}

3️⃣ Agregar una laptop (solo manager o admin)
curl -X POST http://localhost:8003/laptops \
 -H "Authorization: Bearer <JWT_TOKEN>" \
 -H "Content-Type: application/json" \
 -d '{
   "marca": "Dell",
   "modelo": "XPS 15",
   "procesador": "Intel i7",
   "ram": "16GB",
   "precio": 5200
 }'


Respuesta:

{"msg": "Laptop agregada exitosamente"}

4️⃣ Obtener todas las laptops
curl -X GET http://localhost:8003/laptops


Respuesta:

[
  {
    "marca": "Dell",
    "modelo": "XPS 15",
    "procesador": "Intel i7",
    "ram": "16GB",
    "precio": 5200
  }
]

5️⃣ Obtener laptops con filtro
curl "http://localhost:5000/laptops?marca=Dell&ram=16GB"

6️⃣ Renderizado en HTML (SSR)

Visualiza en navegador:
👉 http://localhost:8003/laptops/html

O con cURL:

curl -H "Accept: text/html" http://localhost:8003/laptops/html

🧠 Roles y permisos
Rol	Puede ver laptops	Puede agregar laptops	Puede agregar usuarios
Client	✅ Sí	❌ No	❌ No
Manager	✅ Sí	✅ Sí	❌ No
Admin	✅ Sí	✅ Sí	✅ Sí


🧰 Requerimientos
Archivo requirements.txt:

Flask
Flask-JWT-Extended
pymongo
python-dotenv
Werkzeug

🧾 Notas
Si aparece “Signature verification failed”, borra el token y vuelve a hacer login.
Si aparece “Missing Bearer”, revisa que el header tenga el formato:
Authorization: Bearer <JWT_TOKEN>


La base de datos MongoDB debe estar corriendo localmente o en Atlas.
El archivo .env no se sube al repositorio.
