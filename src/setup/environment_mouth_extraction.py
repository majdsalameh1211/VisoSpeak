from pathlib import Path
import cv2

def verify_environment(project_root="."):
    print("🔧 Verifying mouth extraction environment...")
    project_root = Path(project_root).resolve()

    required_folders = [
        "data",
        "src",
        "models",
        "notebooks",
        "tests"
    ]

    for folder in required_folders:
        full_path = project_root / folder
        if not full_path.exists():
            print(f"⚠️  Warning: Required folder missing → {full_path}")
        else:
            print(f"✅ Folder exists: {folder}")

    # Haar cascade file check
    haar_path = Path(cv2.data.haarcascades)
    mouth = haar_path / "haarcascade_mcs_mouth.xml"
    if not mouth.exists():
        raise FileNotFoundError("❌ haarcascade_mcs_mouth.xml not found in OpenCV haarcascade directory.")
    print("✅ Haar cascade for mouth is available.")

    print("🟢 Mouth extraction environment verified.")
