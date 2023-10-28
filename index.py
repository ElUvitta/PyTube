from flask import Flask, render_template, request, send_file
import os
from pytube import YouTube

app = Flask(__name__)

path = os.getcwd() + "/output/"

# Configura la ruta para los archivos estáticos
app.static_folder = 'static'

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'), 404

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/envia", methods=['POST'])
def envia():
    if request.method == 'POST':
        url = request.form['url']
        action = request.form['action']
        print(f"URL: {url}, Action: {action}")

        if action == "mp4":
            yt = YouTube(url)
            video = yt.streams.get_highest_resolution()
            archivo_salida = video.download(output_path=path)
            print(f"El archivo de salida de python dice: {archivo_salida}")
            return send_file(archivo_salida, as_attachment=True)
        elif action == "mp3":
            yt = YouTube(url)
            audio = yt.streams.filter(only_audio=True).first()
            archivo_salida = audio.download(output_path=path)
            nombre_base, extension = os.path.splitext(archivo_salida)
            nuevo_archivo = nombre_base + '.mp3'
            os.rename(archivo_salida, nuevo_archivo)

            if os.path.exists(nuevo_archivo):
                return send_file(nuevo_archivo, as_attachment=True)
            else:
                return "El archivo MP3 no se encontró en la ubicación correcta."
            
        # Redirige al usuario a una página de confirmación o muestra un mensaje
        return "Descarga completada. Puedes volver <a href='/'>aquí</a>."

if __name__ == "__main__":
    app.run(debug=True, port=5000)
