from flask import Flask, render_template, request, jsonify
from gita_recommender import GitaEmotionRecommender

app = Flask(__name__)
recommender = GitaEmotionRecommender("gita_vedabase.json")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input received."}), 400

        user_text = data.get("text", "").strip()
        if not user_text:
            return jsonify({"error": "Please enter what you are feeling."}), 400

        results = recommender.recommend_verses(user_text, top_k=3)
        detected_emotion = results[0]["emotion"] if results else "guidance"

        return jsonify({
            "detected_emotion": detected_emotion,
            "results": results
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)