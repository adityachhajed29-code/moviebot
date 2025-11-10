import os
import re
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ.get("HF_TOKEN"),
)

def clean_user_message(message):
    """Remove prefixes like '[USER]', '[GEN]', 'user:', 'patient:' etc."""
    message = re.sub(r"^\s*(user|patient|gen)\s*:\s*", "", message, flags=re.IGNORECASE)
    message = re.sub(r"^\s*\[.*?\]\s*", "", message)
    return message.strip()

def clean_model_output(output):
    """Remove numbering, prefixes, and leftover brackets"""
    output = re.sub(r"\[/?[A-Z]+\]", "", output)  # remove [USER], [/USER], [GEN]
    output = re.sub(r"(recommendation:|Recommendation:)", "", output, flags=re.IGNORECASE)
    output = re.sub(r"\d+\.\s*", "", output)  # remove numbered lists
    return output.strip()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.json.get("message")
    user_message = clean_user_message(user_message)

    try:
        completion = client.chat.completions.create(
            model="HuggingFaceH4/zephyr-7b-beta:featherless-ai",
            messages=[
                {"role": "system", "content": (
                    "You are a helpful movie recommender. "
                    "Answer ONLY with the movie titles and years. "
                    "Do NOT repeat, summarize, or reference the user's input. "
                    "Do NOT number the movies. Do NOT add 'recommendation:' or any extra text. "
                    "Separate multiple movies with commas only."
                )},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150
        )

        bot_reply = completion.choices[0].message.content
        bot_reply = clean_model_output(bot_reply)

        return jsonify({"reply": bot_reply})

    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": "Sorry, something went wrong."}), 500

if __name__ == "__main__":
    app.run(debug=True)
