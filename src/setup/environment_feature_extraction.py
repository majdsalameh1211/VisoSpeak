import os

# === Input/Output Directories ===
BASE_DATA_DIR = "data"
VIDEO_NAME = "sample_video"  # Change per run
MOUTH_CROP_DIR = os.path.join(BASE_DATA_DIR, VIDEO_NAME, "mouth_crops")
FEATURES_OUTPUT_DIR = os.path.join(BASE_DATA_DIR, VIDEO_NAME, "features")

# === Model Configuration ===
USE_3D_CNN = False   # Set True to use 3D CNN instead of ResNet18
BATCH_SIZE = 16
NUM_WORKERS = 2
DEVICE = "cpu" 

# === Frame/Clip Parameters ===
IMG_SIZE = 112  # Resize dimension for mouth crop images
CLIP_LEN = 16   # Number of frames per 3D clip (if using 3D CNN)

# === File Types ===
FRAME_EXTENSIONS = [".png", ".jpg"]
FEATURE_EXTENSION = ".npy"