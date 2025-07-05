from flask import Flask, request, jsonify
from emoji_generator import generate_emoji
import tempfile
import os
import uuid

app = Flask(__name__)

@app.route('/generate-emoji', methods=['GET'])
def generate_emoji_endpoint():
    try:
        # Create a temporary output path
        temp_dir = tempfile.mkdtemp()
        output_path = os.path.join(temp_dir, f"{uuid.uuid4()}.png")

        # Use the user's prompt
        prompt = request.args.get('prompt', 'happy face')

        # Generate the emoji
        generate_emoji(prompt=prompt, output_path=output_path)

        return jsonify({
            "prompt": prompt,
            "emoji_path": output_path
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

