import os
import sys

# --- Step 1: Setup project path ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

# --- Step 2: Import setup and preprocessing modules ---
from src.setup.environment_preprocessing import verify_environment
from src.preprocessing.extract_frames import extract_frames_from_video

# --- Step 3: Run environment check ---
verify_environment(project_root)

# --- Step 4: Define path to raw video file ---
video_path = os.path.join(project_root, "data", "raw_videos", "vid_001.mpg")

# --- Step 5: Run preprocessing (frame extraction) ---
extract_frames_from_video(
    video_path=video_path,
    data_root=os.path.join(project_root, "data")
)
