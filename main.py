from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

# Use env var in Render dashboard: OPENAI_API_KEY
client = OpenAI(api_key=os.environ["api_key"])

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/combine")
def combine():
    data = request.get_json(force=True) or {}

    # Accept both shapes
    a = data.get("a") or data.get("element1")
    b = data.get("b") or data.get("element2")
    if not a or not b:
        return jsonify(error="Missing 'a'/'b' (or 'element1'/'element2')."), 400

    try:
        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": "You are a crafting game engine like Infinite Craft. "
                            "User gives two elements. Respond with ONLY the result."},
                {"role": "user", "content": f"{a} and {b}"}
            ],
            temperature=0.7,
            max_tokens=32,
        )
        result = (r.choices[0].message.content or "").strip().title()
        if not result:
            return jsonify(error="Model returned empty result."), 502
        return jsonify(result=result)
    except Exception as e:
        return jsonify(error=f"{type(e).__name__}: {e}"), 500

if __name__ == "__main__":
    # Local run; on Render you’ll use gunicorn
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
