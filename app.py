from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# अपनी Together AI API Key डालें
API_KEY = "778c6b05ab7cc4425700910e5ef24373deca63ce6ee0bb4cc6fa2601c6b29485"

@app.route('/generate_titles', methods=['POST'])
def generate_titles():
    try:
        data = request.json
        user_input = data.get("keyword", "").strip()

        if not user_input:
            return jsonify({"error": "Keyword is required"}), 400

        response = requests.post(
            "https://api.together.xyz/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
            json={
                "model": "meta-llama/Meta-Llama-3-70B-Instruct-Turbo",
                "messages": [{"role": "user", "content": f"Generate 5 best YouTube video titles for: {user_input}"}]
            }
        )

        result = response.json()

        # Check if response contains expected data
        if "choices" in result and len(result["choices"]) > 0:
            raw_content = result["choices"][0]["message"]["content"]
            titles = [title.strip("-. ") for title in raw_content.split("\n") if title.strip()]
            return jsonify({"titles": titles})
        else:
            return jsonify({"error": "Invalid response from API", "details": result}), 500

    except Exception as e:
        return jsonify({"error": "Something went wrong", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
