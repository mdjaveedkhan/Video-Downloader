from flask import Flask, render_template, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")
    format_type = request.form.get("format")
    quality = request.form.get("quality")

    if not url:
        return jsonify({"error": "URL is required"})

    ydl_opts = {
        "outtmpl": f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",
        "noplaylist": True,
        "progress_hooks": [progress_hook],
    }

    if format_type == "mp3":
        ydl_opts.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]
        })
    else:
        if quality == "best":
            ydl_opts["format"] = "best"
        else:
            ydl_opts["format"] = f"bestvideo[height<={quality}]+bestaudio/best"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return jsonify({"success": "Download completed!"})
    except Exception as e:
        return jsonify({"error": str(e)})

def progress_hook(d):
    if d["status"] == "downloading":
        percent = d.get("_percent_str", "0%")
        print(f"Downloading: {percent}")

if __name__ == "__main__":
    app.run(debug=True)
