import os
import cv2
import numpy as np
from models.lipnet_model import load_lipnet, predict_video
from config import (
    GRID_PATH,
    LIPNET_MODEL_PATH,
    lipnet_target_frames,
    lipnet_frame_height,
    lipnet_frame_width,
)

# ===== Global cached model =====
_lipnet_model = None

def get_lipnet_model():
    """Load LipNet model once and cache it for reuse."""
    global _lipnet_model
    if _lipnet_model is None:
        _lipnet_model = load_lipnet(LIPNET_MODEL_PATH)
    return _lipnet_model


# ===== Preprocessing (shared) =====
def video_to_lipnet_tensor(video_path):
    """
    Convert video to (75,46,140,1) tensor normalized to [0,1]
    Matches Colab-trained LipNet model (46x140 input).
    """
    cap = cv2.VideoCapture(video_path)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Convert to grayscale
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Resize to 140×46
        frame = cv2.resize(frame, (lipnet_frame_width, lipnet_frame_height))
        frames.append(frame)
    cap.release()

    # Pad or truncate to target frames
    if len(frames) < lipnet_target_frames:
        pad_len = lipnet_target_frames - len(frames)
        frames.extend([np.zeros((lipnet_frame_height, lipnet_frame_width), dtype=np.uint8)] * pad_len)
    else:
        frames = frames[:lipnet_target_frames]

    # Normalize and add channel dim
    frames = np.array(frames, dtype=np.float32) / 255.0
    frames = np.expand_dims(frames, axis=-1)  # Shape: (75, 46, 140, 1)
    return frames


# ===== Prediction with progress =====
def run_lipnet_prediction(video_path, progress_callback=None):
    """Runs LipNet prediction with optional progress updates."""
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video not found: {video_path}")

    if progress_callback:
        progress_callback(20, "Preprocessing video...")
    video_tensor = video_to_lipnet_tensor(video_path)

    if progress_callback:
        progress_callback(60, "Loading LipNet model...")
    model = get_lipnet_model()

    if progress_callback:
        progress_callback(90, "Running LipNet prediction...")
    prediction = predict_video(model, video_tensor)

    if progress_callback:
        progress_callback(100, "LipNet prediction complete!")
    return prediction
