from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)
app.secret_key = 'tu_super_secreto'

def get_db_connection():
    conn = psycopg2.connect(
        dbname="Restaurante",
        user="postgres",
        password="admin",
        host="localhost"
    )
    return conn

@app.route('/create_user', methods=['POST'])
def create_user():
    user_details = request.json
    nombre = user_details['nombre']
    apellido = user_details['apellido']
    correo = user_details['correo']
    telefono = user_details['telefono']
    tipo_usuario = user_details['tipo_usuario']
    contrasena = user_details['contrasena']  # Ahora almacenamos la contraseña en texto plano

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO public.usuarios (nombre, apellido, correo, telefono, tipo_usuario, contrasena) VALUES (%s, %s, %s, %s, %s, %s)',
        (nombre, apellido, correo, telefono, tipo_usuario, contrasena)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Usuario creado exitosamente'}), 201

if __name__ == '__main__':
    app.run(debug=True)
