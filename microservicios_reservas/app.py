from flask import Flask, request, jsonify, session
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

@app.route('/reservas', methods=['POST'])
def crear_reserva():
    if 'role' in session and session['role'] == 'cliente':
        data = request.json
        id_usuario = data['id_usuario']
        numero_mesa = data['numero_mesa']
        hora = data['hora']
        detalle = data.get('detalle', '')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO reservas (id_usuario, numero_mesa, hora, detalle, estado) VALUES (%s, %s, %s, %s, \'confirmada\') RETURNING id;',
            (id_usuario, numero_mesa, hora, detalle)
        )
        reserva_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"id": reserva_id}), 201

if __name__ == '__main__':
    app.run(debug=True)
