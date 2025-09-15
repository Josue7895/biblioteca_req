from flask import Flask, render_template, request, send_from_directory, abort
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Carpeta donde estarán los PDFs (biblioteca/static/libros)
UPLOAD_FOLDER = os.path.join(app.root_path, "static", "libros")
ALLOWED_EXTENSIONS = {".pdf"}

# Asegura que exista localmente (en Render puede ser solo lectura)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename: str) -> bool:
    return os.path.splitext(filename.lower())[1] in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    # Lista todos los PDFs dentro de static/libros
    try:
        files = sorted(
            [f for f in os.listdir(app.config["UPLOAD_FOLDER"]) if f.lower().endswith(".pdf")]
        )
    except FileNotFoundError:
        files = []
    return render_template("index.html", files=files)


@app.route("/upload", methods=["POST"])
def upload_file():
    # Subida opcional (útil en local; en Render puede no persistir)
    if "file" not in request.files:
        abort(400, "No se envió ningún archivo")
    file = request.files["file"]
    if file.filename == "":
        abort(400, "Archivo vacío")
    if allowed_file(file.filename):
        safe_name = secure_filename(file.filename)
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], safe_name)
        file.save(save_path)
        return "Libro subido con éxito"
    abort(400, "Formato no permitido (solo PDF)")


@app.route("/download/<path:filename>")
def download_file(filename):
    # Descarga segura desde static/libros
    if not allowed_file(filename):
        abort(404)
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)


if __name__ == "__main__":
    # Modo local. En Render se usa gunicorn con el Procfile (web: gunicorn app:app)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
