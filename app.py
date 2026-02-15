from flask import Flask, render_template, request, redirect, url_for
from models import db, Mensaje

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mensajes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


# Ruta principal: formulario
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        mensaje_texto = request.form["mensaje"]

        nuevo_mensaje = Mensaje(
            nombre=nombre,
            email=email,
            mensaje=mensaje_texto
        )

        db.session.add(nuevo_mensaje)
        db.session.commit()

        return redirect(url_for("mensajes"))

    return render_template("index.html")


# Listar mensajes
@app.route("/mensajes")
def mensajes():
    mensajes = Mensaje.query.all()
    return render_template("mensajes.html", mensajes=mensajes)


# Eliminar mensaje
@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    mensaje = Mensaje.query.get_or_404(id)
    db.session.delete(mensaje)
    db.session.commit()
    return redirect(url_for("mensajes"))


# Editar mensaje
@app.route("/editar/<int:id>")
def editar(id):
    mensaje = Mensaje.query.get_or_404(id)
    return render_template("editar.html", mensaje=mensaje)


# Actualizar mensaje
@app.route("/actualizar/<int:id>", methods=["POST"])
def actualizar(id):
    mensaje = Mensaje.query.get_or_404(id)

    mensaje.nombre = request.form["nombre"]
    mensaje.email = request.form["email"]
    mensaje.mensaje = request.form["mensaje"]

    db.session.commit()
    return redirect(url_for("mensajes"))


if __name__ == "__main__":
    app.run(debug=True)

## Autor: Brando  