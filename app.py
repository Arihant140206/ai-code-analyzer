from flask import Flask, render_template, request, jsonify
import joblib
from utils.analyzer import analyze_code

app = Flask(__name__)

# Load models
quality_model = joblib.load("models/quality_model.pkl")
risk_model = joblib.load("models/risk_model.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    code = data.get("code")

    # Extract features
    features = analyze_code(code)

    input_data = [[
        features["lines"],
        features["loops"],
        features["depth"]
    ]]

    risk_input = [[
        features["loops"],
        features["depth"],
        features["lines"]
    ]]

    # Predictions
    print("Predicting...")
    quality_score = quality_model.predict(input_data)[0]
    risk = risk_model.predict(input_data)[0]
    print("Done prediction")

    # AI Suggestions
    suggestions = []

    if features["depth"] > 2:
        suggestions.append("Reduce nested loops")

    if features["loops"] > 2:
        suggestions.append("Too many loops, try optimizing")

    if features["lines"] > 50:
        suggestions.append("Code is too long, consider modularization")

    if features["conditions"] > 3:
        suggestions.append("Too many conditions, simplify logic")

    return jsonify({
        "features": features,
        "quality_score": round(float(quality_score), 2),
        "risk": risk,
        "suggestions": suggestions
    })



if __name__ == "__main__":
    import os

    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))