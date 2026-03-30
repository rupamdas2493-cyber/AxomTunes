from flask import Flask, render_template, request, send_from_directory
import os
import requests

app = Flask(__name__)

SONG_FOLDER = os.path.join("static", "songs")

# ✅ FIXED: Proper API key handling
YOUTUBE_API_KEY = os.environ.get("AIzaSyBq_on5XnyoQWUDZgLu-kJSHwQfkXQ4Lss") or "AIzaSyBq_on5XnyoQWUDZgLu-kJSHwQfkXQ4Lss"


@app.route("/")
def index():
    try:
        songs = os.listdir(SONG_FOLDER)
        songs = [s for s in songs if s.endswith(".mp3")]
    except:
        songs = []

    return render_template("index.html", songs=songs, videos=None)


@app.route("/songs/<path:filename>")
def get_song(filename):
    return send_from_directory(SONG_FOLDER, filename)


# ✅ UPDATED SEARCH (GET + POST + SAFE)
@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = request.form.get("query", "")
    else:
        query = request.args.get("query", "")

    yt_query = query + " Jubin Garg Assamese song"

    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={yt_query}&key={YOUTUBE_API_KEY}&maxResults=5&type=video"

    videos = []
    filtered_songs = []

    # 🎬 YouTube search
    try:
        response = requests.get(url).json()

        if "items" in response:
            for item in response["items"]:
                videos.append({
                    "id": item["id"]["videoId"],
                    "title": item["snippet"]["title"],
                    "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"]
                })

    except Exception as e:
        print("YT ERROR:", e)

    # 🎵 Local song search
    try:
        songs = os.listdir(SONG_FOLDER)
        songs = [s for s in songs if s.endswith(".mp3")]

        if query:
            filtered_songs = [
                s for s in songs if query.lower() in s.lower()
            ]
        else:
            filtered_songs = songs

    except Exception as e:
        print("LOCAL ERROR:", e)
        filtered_songs = []

    return render_template(
        "index.html",
        songs=filtered_songs,
        videos=videos
    )


# ✅ DEPLOYMENT READY
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
