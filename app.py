from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

YOUTUBE_API_KEY = "AIzaSyCkvi0DP_tygwrDMGY4RgF6o86qZs_S0X4"  # Replace with your actual key

MOOD_KEYWORDS = {
    "happy": "happy",
    "sad": "uplifting",  # positive instead of sad
    "relaxed": "relaxing chill",
    "energetic": "workout dance"
}

LANGUAGE_QUERIES = {
    "hindi": "bollywood",
    "english": "english",
    "marathi": "marathi"
}

@app.route("/")
def home():
    return "🎵 Welcome to the Mood-Based YouTube Music API!"

@app.route("/get-songs", methods=["POST"])
def get_songs():
    data = request.get_json()
    mood = data.get("mood", "happy").lower()
    language = data.get("language", "hindi").lower()

    mood_part = MOOD_KEYWORDS.get(mood, "popular")
    lang_part = LANGUAGE_QUERIES.get(language, "bollywood")
    query = f"{lang_part} {mood_part} songs"

    youtube_api_url = (
        f"https://www.googleapis.com/youtube/v3/search"
        f"?part=snippet&type=video&maxResults=10&q={query}&key={YOUTUBE_API_KEY}"
    )

    try:
        res = requests.get(youtube_api_url)
        data = res.json()

        songs = []
        for item in data.get("items", []):
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            channel = item["snippet"]["channelTitle"]
            url = f"https://www.youtube.com/watch?v={video_id}"

            songs.append({
                "name": title,
                "artist": channel,
                "url": url
            })

        return jsonify({"songs": songs})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Render-friendly host + port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
