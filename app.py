from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "🚀 Servidor corriendo en Render correctamente ✅"

# 👇 Importante: NO usar app.run() aquí,
# Gunicorn lo arranca automáticamente en Render.
