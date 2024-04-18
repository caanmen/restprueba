from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'tu_jwt_secreto_muy_seguro'  # Cambia esta clave por una segura y única
jwt = JWTManager(app)

def get_db_connection():
    conn = psycopg2.connect(
        dbname="Restaurante",
        user="postgres",
        password="admin",
        host="localhost"
    )
    return conn

@app.route('/login', methods=['POST'])
def login():
    user_deils = request.json
    correo = user_details['correo']
    contrasena = user_details['contrasena']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, tipo_usuario, contrasena FROM public.usuarios WHERE correo = %s', (correo,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and check_password_hash(user[2], contrasena):
        access_token = create_access_token(identity={'user_id': user[0], 'role': user[1]})
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Correo electrónico o contraseña incorrectos'}), 401

@app.route('/mesas', methods=['POST'])
@jwt_required()
def crear_mesa():
    claims = get_jwt_identity()
    if claims['role'] in ['super_   administrador', 'administrador']:
        data = request.json
        capacidad = data['capacidad']
        localizacion = data['localizacion']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO mesas (capacidad, localizacion, disponible) VALUES (%s, %s, True) RETURNING numero_mesa;',
            (capacidad, localizacion)
        )
        numero_mesa = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"numero_mesa": numero_mesa}), 201
    else:
        return jsonify({"error": "Acceso denegado"}), 403

if __name__ == '__main__':
    app.run(debug=True)
