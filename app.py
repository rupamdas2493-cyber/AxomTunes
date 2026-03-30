import os
from flask import Flask, render_template, request
from googleapiclient.discovery import build

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'

# ✅ TEMP: Hardcoded API key (to make it work)

API_KEY = os.environ.get("AIzaSyBq_on5XnyoQWUDZgLu-kJSHwQfkXQ4Lss")
if not API_KEY:
    raise ValueError("YOUTUBE_API_KEY missing")

# ✅ Build YouTube client
youtube = build("youtube", "v3", developerKey=API_KEY)

videos_cache = []  # store results temporarily


@app.route("/")
def home():
    return render_template("index.html", videos=[], selected_video=None)


@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("query")

    global videos_cache
    videos_cache = []

    try:
        request_api = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=8
        )
        response = request_api.execute()

        for item in response.get("items", []):
            videos_cache.append({
                "id": item["id"]["videoId"],
                "title": item["snippet"]["title"],
                "thumbnail": item["snippet"]["thumbnails"]["high"]["url"]
            })

    except Exception as e:
        print("YouTube API Error:", e)

    return render_template("index.html", videos=videos_cache, selected_video=None)


@app.route("/play/<video_id>")
def play(video_id):
    return render_template("index.html", videos=videos_cache, selected_video=video_id)


if __name__ == "__main__":
    # ✅ Works locally + Render
    app.run(host="0.0.0.0", port=5000, debug=True)
