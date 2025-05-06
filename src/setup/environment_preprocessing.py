from pathlib import Path
import os
import cv2
from PIL import Image

def verify_environment(project_root="."):
    print("🔧 Verifying preprocessing environment...")

    project_root = Path(project_root).resolve()

    required_folders = [
        "data",
        "models",
        "src",
        "notebooks",
        "tests"
    ]

    for folder in required_folders:
        full_path = project_root / folder
        if not full_path.exists():
            print(f"⚠️  Warning: Required folder missing → {full_path}")
        else:
            print(f"✅ Folder exists: {folder}")

    # Check and create data/raw if missing
    raw_path = project_root / "data" / "raw_videos"
    if not raw_path.exists():
        raw_path.mkdir(parents=True, exist_ok=True)
        print("📁 Created missing folder: data/raw_videos")
    else:
        print("✅ Folder exists: data/raw_videos")

    # Haar cascade checks
    haar_path = Path(cv2.data.haarcascades)
    face = haar_path / "haarcascade_frontalface_default.xml"
    mouth = haar_path / "haarcascade_mcs_mouth.xml"

    if not face.exists() or not mouth.exists():
        raise FileNotFoundError("❌ Haar cascade files not found in OpenCV.")
    print("✅ Haar cascade files are available.")

    # PIL check
    try:
        _ = Image.new("RGB", (1, 1))
        print("✅ PIL installed and working.")
    except Exception as e:
        print(f"❌ PIL test failed: {e}")

    print("🟢 Environment setup verified.")
