import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

# Ruta principal: formulario
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        nombre = request.form["nombre"]
        mensaje = request.form["mensaje"]

        conn = sqlite3.connect("data/mensajes.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO mensajes (nombre, mensaje) VALUES (?, ?)",
            (nombre, mensaje)
        )
        conn.commit()
        conn.close()

    return render_template("index.html")


# Nueva ruta: mostrar mensajes guardados
@app.route("/mensajes")
def mensajes():
    conn = sqlite3.connect("data/mensajes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, mensaje FROM mensajes")
    datos = cursor.fetchall()
    conn.close()

    return render_template("mensajes.html", mensajes=datos)


if __name__ == "__main__":
    app.run(debug=True)
