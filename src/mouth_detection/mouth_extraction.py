import os
import cv2
import json
import numpy as np
import mediapipe as mp

def extract_mouth_from_frames(video_dir):
    """
    Extract mouth region using MediaPipe landmarks and save cropped mouth frames.
    """

    frames_dir = os.path.join(video_dir, "frames")
    mouth_crops_dir = os.path.join(video_dir, "mouth_crops")
    metadata_path = os.path.join(video_dir, "metadata.json")

    os.makedirs(mouth_crops_dir, exist_ok=True)

    if not os.path.exists(metadata_path):
        raise FileNotFoundError(f"Metadata file not found at: {metadata_path}")

    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    # Setup MediaPipe
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5
    )

    # Lip landmark indices
    MOUTH_LANDMARKS = list(range(78, 88)) + list(range(308, 318))
    PADDING = 2
    OUTPUT_SIZE = (96, 64)

    # Process frames
    for entry in metadata:
        frame_path = os.path.join(frames_dir, entry["frame"])
        image = cv2.imread(frame_path)
        if image is None:
            continue

        h, w = image.shape[:2]
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        if not results.multi_face_landmarks:
            continue

        landmarks = results.multi_face_landmarks[0]

        mouth_points = np.array([
            [landmark.x * w, landmark.y * h]
            for i, landmark in enumerate(landmarks.landmark)
            if i in MOUTH_LANDMARKS
        ], dtype=np.float32)

        if len(mouth_points) < 5:
            continue

        hull = cv2.convexHull(mouth_points)
        x, y, bw, bh = cv2.boundingRect(hull)

        x1 = max(int(x - PADDING), 0)
        y1 = max(int(y - PADDING), 0)
        x2 = min(int(x + bw + PADDING), w)
        y2 = min(int(y + bh + PADDING), h)

        crop = image[y1:y2, x1:x2]
        if crop.shape[0] < 10 or crop.shape[1] < 10:
            continue

        crop_resized = cv2.resize(crop, OUTPUT_SIZE)
        crop_path = os.path.join(mouth_crops_dir, entry["frame"])
        cv2.imwrite(crop_path, crop_resized)

    print(f"✅ Mouth crops saved for: {os.path.basename(video_dir)}")
