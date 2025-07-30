import os
import cv2
import numpy as np
import torch
import mediapipe as mp
from pathlib import Path
from config import (
    MAX_FRAMES, FRAME_WIDTH, FRAME_HEIGHT, TARGET_FPS,
    LIP_OUTPUT_SIZE, MOUTH_LANDMARKS, PADDING
)

# Device (if needed later)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Mediapipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.75
)

# === Frame Extraction ===
def extract_frames_fixed_length(video_path: str, target_fps: int = TARGET_FPS,
                                target_size: tuple = (FRAME_WIDTH, FRAME_HEIGHT),
                                max_frames: int = MAX_FRAMES):
    video_path = Path(video_path)
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print(f"Error: Cannot open video file: {video_path}")
        return None

    original_fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / original_fps

    timestamps = np.arange(0, duration, 1 / target_fps)[:max_frames]
    frames = []
    for t in timestamps:
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
        ret, frame = cap.read()
        if not ret:
            break
        if target_size:
            frame = cv2.resize(frame, target_size)
        frames.append(frame)

    cap.release()

    frames_np = np.array(frames)
    if len(frames_np) < max_frames:
        pad_len = max_frames - len(frames_np)
        pad_shape = (pad_len, *frames_np.shape[1:])
        pad_array = np.zeros(pad_shape, dtype=np.uint8)
        frames_np = np.concatenate([frames_np, pad_array], axis=0)

    return frames_np

# === Lip ROI Extraction ===
def extract_lip_rois_from_frames_mediapipe(frames_np: np.ndarray) -> torch.Tensor:
    mouth_crops = []
    for idx in range(MAX_FRAMES):
        try:
            frame = frames_np[idx]
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = mp_face_mesh.process(rgb)

            if not results.multi_face_landmarks:
                raise ValueError("No landmarks found")

            landmarks = results.multi_face_landmarks[0].landmark
            h, w, _ = frame.shape
            mouth_coords = [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in MOUTH_LANDMARKS]

            xs, ys = zip(*mouth_coords)
            x_min = max(min(xs) - PADDING, 0)
            x_max = min(max(xs) + PADDING, w)
            y_min = max(min(ys) - PADDING, 0)
            y_max = min(max(ys) + PADDING, h)

            mouth_crop = frame[y_min:y_max, x_min:x_max]
            if mouth_crop.size == 0:
                raise ValueError("Empty crop")

            gray_crop = cv2.cvtColor(mouth_crop, cv2.COLOR_BGR2GRAY)
            resized = cv2.resize(gray_crop, LIP_OUTPUT_SIZE)
            normalized = resized.astype(np.float32) / 255.0
            normalized = np.expand_dims(normalized, axis=-1)

            mouth_crops.append(normalized)

        except Exception:
            mouth_crops.append(np.zeros((*LIP_OUTPUT_SIZE, 1), dtype=np.float32))

    lips_np = np.stack(mouth_crops)
    return torch.tensor(lips_np, dtype=torch.float32)

# === Convert Video to Preprocessed Tensor ===
def video_to_preprocessed_tensor(video_path: str) -> torch.Tensor:
    frames = extract_frames_fixed_length(video_path)
    if frames is None:
        print(f"Frame extraction failed for: {video_path}")
        return None
    lips_tensor = extract_lip_rois_from_frames_mediapipe(frames)
    return lips_tensor
