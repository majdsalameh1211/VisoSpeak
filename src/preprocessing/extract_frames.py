import os
import cv2
import json

def extract_frames_from_video(video_path, data_root="data"):
    """
    Extract frames from a single video and save them under:
      data/{video_name}/frames/
      data/{video_name}/mouth_crops/
      data/{video_name}/metadata.json
    """
    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"Video not found: {video_path}")

    video_name = os.path.splitext(os.path.basename(video_path))[0]
    video_dir = os.path.join(data_root, video_name)
    frames_dir = os.path.join(video_dir, "frames")
    crops_dir = os.path.join(video_dir, "mouth_crops")
    metadata_path = os.path.join(video_dir, "metadata.json")

    os.makedirs(frames_dir, exist_ok=True)
    os.makedirs(crops_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    metadata = []
    frame_idx = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_name = f"{frame_idx:04d}.jpg"
        frame_path = os.path.join(frames_dir, frame_name)
        cv2.imwrite(frame_path, frame)

        metadata.append({
            "frame": frame_name,
            "timestamp": cap.get(cv2.CAP_PROP_POS_MSEC)
        })

        frame_idx += 1

    cap.release()

    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"✅ Extracted {frame_idx} frames for video '{video_name}' and saved metadata.")
