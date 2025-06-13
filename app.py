from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# Replace with your OpenAI API key
openai.api_key = "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"
openai.api_base = "https://openrouter.ai/api/v1"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json["question"]
    try:
       response = openai.ChatCompletion.create(
    model="mistralai/mistral-7b-instruct",  # or "openchat/openchat-3.5"
    messages=[
        {"role": "system", "content": "You are Agnix, a helpful assistant."},
        {"role": "user", "content": "Hello, Agnix!"}
    ]
)     (response['choices'][0]['message']['content'])
       return jsonify({"answer": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
 
if __name__ == "__main__":
    app.run(debug=True)
