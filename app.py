from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import tempfile

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")
    file_type = request.form.get("type")

    if not url:
        return "URL is required", 400

    temp_dir = tempfile.mkdtemp()

    if file_type == "mp3":
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": f"{temp_dir}/%(title)s.%(ext)s",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }
    else:
        ydl_opts = {
            "format": "best",
            "outtmpl": f"{temp_dir}/%(title)s.%(ext)s",
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

            if file_type == "mp3":
                filename = filename.rsplit(".", 1)[0] + ".mp3"

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)
