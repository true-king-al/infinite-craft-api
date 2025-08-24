from flask import Flask, request, jsonify
from openai import OpenAI
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow requests from mobile app

part1 = "sk-jh6bLNn0602sJwt-AiRwPmuxqFI9oeIpFYQ990ybtOT"
part2 = "3BlbkFJFHfTLd4qNUJueCW3YevT7fGsIhyorV8vHs34mUuFYA"
full_key = part1 + part2
client = OpenAI(api_key=full_key)  # insert your key here

@app.route("/combine", methods=["POST"])
def combine():
    data = request.get_json()
    a, b = data.get("a"), data.get("b")
    try:
        result = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a crafting game engine like Infinite Craft. The user gives two elements. You return the result. No commentary."},
                {"role": "user", "content": f"{a} and {b}"}
            ],
            temperature=0.7,
            max_tokens=50
        ).choices[0].message.content.strip()
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

app.run(host='0.0.0.0', port=8080)
