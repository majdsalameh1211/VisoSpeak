from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback
import os
from config import LRS2_PATH, GRID_PATH
from transformer_prediction import run_transformer_prediction
from lipnet_prediction import run_lipnet_prediction

app = Flask(__name__)
CORS(app)

# Progress tracking
prediction_progress = {'progress': 0, 'status': 'idle', 'message': ''}

def update_progress(progress, message):
    prediction_progress['progress'] = progress
    prediction_progress['message'] = message
    print(f"Progress: {progress}% - {message}")

@app.route('/prediction-progress', methods=['GET'])
def get_prediction_progress():
    return jsonify(prediction_progress)

@app.route('/run-transformer', methods=['POST'])
def run_transformer():
    try:
        data = request.json
        video_name = data.get('video_name')
        if not video_name:
            return jsonify({"status": "error", "error": "No video name provided"}), 400

        result = run_transformer_prediction(video_name, LRS2_PATH, update_progress)
        return jsonify(result)
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"status": "error", "error": str(e)}), 500

@app.route('/run-lipnet', methods=['POST'])
def run_lipnet():
    try:
        data = request.json
        video_name = data.get('video_name')
        if not video_name:
            return jsonify({"status": "error", "error": "No video name provided"}), 400

        if video_name.endswith(".mp4"):
            video_name = video_name[:-4]

        video_path = os.path.join(GRID_PATH, f"{video_name}.mp4")
        if not os.path.exists(video_path):
            return jsonify({"status": "error", "error": f"Video not found: {video_path}"}), 404

        prediction = run_lipnet_prediction(video_path, update_progress)
        align_path = os.path.join(GRID_PATH, "align", f"{video_name}.align")
        original_text = "No ground truth available"

        if os.path.exists(align_path):
            with open(align_path, 'r') as f:
                lines = [line.strip() for line in f if line.strip()]
            tokens = []
            for line in lines:
                parts = line.split()
                if len(parts) >= 3 and parts[2] != 'sil':
                    tokens.extend([' ', parts[2]])
            original_text = "".join(tokens).strip()

        return jsonify({"status": "success", "prediction": prediction, "original": original_text})
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"status": "error", "error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(port=5000, debug=False)
