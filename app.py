import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def crear_tabla():
    conn = sqlite3.connect('data/mensajes.db')
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL,
            mensaje TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

# Ruta principal: formulario
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        mensaje = request.form["mensaje"]

        conn = sqlite3.connect("data/mensajes.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO mensajes (nombre, email, mensaje) VALUES (?, ?, ?)",
            (nombre, email, mensaje)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("mensajes")) # Redireccion a la pagina de  mensajes

    return render_template("index.html")

# Nueva ruta: mostrar mensajes guardados
@app.route("/mensajes")
def mensajes():
    conn = sqlite3.connect("data/mensajes.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, email, mensaje FROM mensajes")
    datos = cursor.fetchall()
    conn.close()

    return render_template("mensajes.html", mensajes=datos)

@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    conn = sqlite3.connect("data/mensajes.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM mensajes WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("mensajes"))

@app.route("/editar/<int:id>")
def editar(id):
    conn = sqlite3.connect("data/mensajes.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mensajes WHERE id = ?", (id,))
    mensaje = cursor.fetchone()
    conn.close()

    return render_template("editar.html", mensaje=mensaje)

@app.route("/actualizar/<int:id>", methods=["POST"])
def actualizar(id):
    nombre = request.form["nombre"]
    email = request.form["email"]
    mensaje = request.form["mensaje"]

    conn = sqlite3.connect("data/mensajes.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE mensajes
        SET nombre = ?, email = ?, mensaje = ?
        WHERE id = ?
    """, (nombre, email, mensaje, id))
    conn.commit()
    conn.close()

    return redirect(url_for("mensajes"))


if __name__ == "__main__":
    crear_tabla()
    app.run(debug=True)

## Autor: Brando  