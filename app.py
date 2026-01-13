from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_link", methods=["POST"])
def get_link():
    url = request.form.get("url")
    format_type = request.form.get("format")

    if not url:
        return jsonify({"error": "URL is required"})

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            if format_type == "mp3":
                for f in info["formats"]:
                    if f.get("acodec") != "none":
                        return jsonify({"download_url": f["url"]})
            else:
                return jsonify({"download_url": info["url"]})

    except Exception as e:
        return jsonify({"error": "This video is restricted by platform"})

if __name__ == "__main__":
    app.run(debug=True)
