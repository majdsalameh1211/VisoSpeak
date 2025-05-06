import os
import sys

# Set root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

# Import modules
from src.setup.environment_mouth_extraction import verify_environment
from src.mouth_detection.mouth_extraction import extract_mouth_from_frames

# Run environment check
verify_environment(project_root)

# Run extraction
video_name = "vid_001"
video_dir = os.path.join(project_root, "data", video_name)
extract_mouth_from_frames(video_dir)
