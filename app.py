from flask import Flask, request, render_template, send_file, redirect, url_for, jsonify
import yt_dlp
import os
import re
import uuid
import threading

app = Flask(__name__)

# Carpeta donde se guardarán los videos descargados
DOWNLOAD_FOLDER = "videos"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Para guardar progreso
progreso_dict = {}
descargados = {}

def limpiar_nombre(nombre):
    """Eliminar caracteres inválidos en Windows para nombres de archivo"""
    nombre = re.sub(r'[\\/*?:"<>|]', "_", nombre)
    return nombre

def descargar_video(url, nombre_personalizado=None, progreso_id=None):
    """Descarga el video y actualiza el progreso"""
    opciones = {
        "outtmpl": f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",
        "format": "best",
        "restrictfilenames": True,
        "progress_hooks": []
    }

    def hook(d):
        if d.get('status') == 'downloading' and progreso_id:
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded = d.get('downloaded_bytes', 0)
            if total:
                progreso = int(downloaded / total * 100)
                progreso_dict[progreso_id] = progreso

    opciones['progress_hooks'].append(hook)

    with yt_dlp.YoutubeDL(opciones) as ydl:
        info = ydl.extract_info(url, download=True)
        nombre_archivo = ydl.prepare_filename(info)
        nombre_final = limpiar_nombre(nombre_personalizado) if nombre_personalizado else limpiar_nombre(nombre_archivo)
        contador = 1
        base, ext = os.path.splitext(nombre_final)
        while os.path.exists(nombre_final):
            nombre_final = f"{base}_{contador}{ext}"
            contador += 1
        if nombre_archivo != nombre_final:
            os.rename(nombre_archivo, nombre_final)
        if progreso_id:
            descargados[progreso_id] = nombre_final
        return nombre_final

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        opciones = {"outtmpl": f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s", "format": "best", "restrictfilenames": True}
        with yt_dlp.YoutubeDL(opciones) as ydl:
            info = ydl.extract_info(url, download=False)
            nombre_sugerido = limpiar_nombre(ydl.prepare_filename(info))

        if os.path.exists(nombre_sugerido):
            return render_template("confirm.html", archivo=nombre_sugerido, url=url, nombre_sugerido=nombre_sugerido)

        # Crear un ID único para la descarga
        progreso_id = str(uuid.uuid4())
        progreso_dict[progreso_id] = 0

        # Descargar en un hilo separado
        thread = threading.Thread(target=descargar_video, args=(url, None, progreso_id))
        thread.start()

        return render_template("progress.html", progreso_id=progreso_id, url=url)

    return render_template("index.html")

@app.route("/confirm", methods=["POST"])
def confirm():
    url = request.form["url"]
    if request.form.get("cancelar") == "sí":
        return redirect(url_for("index"))

    nuevo_nombre = request.form.get("nuevo_nombre")
    progreso_id = str(uuid.uuid4())
    progreso_dict[progreso_id] = 0

    thread = threading.Thread(target=descargar_video, args=(url, nuevo_nombre, progreso_id))
    thread.start()

    return render_template("progress.html", progreso_id=progreso_id, url=url)

@app.route("/progreso/<progreso_id>")
def progreso(progreso_id):
    porcentaje = progreso_dict.get(progreso_id, 0)
    return f"{porcentaje}%"

@app.route("/descargar_final/<progreso_id>")
def descargar_final(progreso_id):
    archivo = descargados.get(progreso_id)
    if archivo and os.path.exists(archivo):
        return send_file(archivo, as_attachment=True)
    return "Archivo no encontrado", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
