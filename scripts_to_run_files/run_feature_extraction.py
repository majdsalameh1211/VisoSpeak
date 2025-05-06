import sys
import os
import torch
import numpy as np
from PIL import Image
from torchvision import transforms
from tqdm import tqdm

# === Add project root to path ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.feature_extraction.resnet2d_extractor import get_resnet18_model
from src.feature_extraction.cnn3d_extractor import get_3dcnn_model
from src.setup import environment_feature_extraction as config

video_name = "vid_001"

def load_images(mouth_crop_dir, use_3d=False):
    files = sorted([
        os.path.join(mouth_crop_dir, f)
        for f in os.listdir(mouth_crop_dir)
        if any(f.endswith(ext) for ext in config.FRAME_EXTENSIONS)
    ])

    if use_3d:
        # For 3D CNN: force 3-channel grayscale to match pretrained r3d_18
        transform = transforms.Compose([
            transforms.Grayscale(num_output_channels=3),
            transforms.Resize((config.IMG_SIZE, config.IMG_SIZE)),
            transforms.ToTensor(),
        ])
    else:
        # For ResNet: use 1-channel grayscale to match modified input layer
        transform = transforms.Compose([
            transforms.Grayscale(num_output_channels=1),
            transforms.Resize((config.IMG_SIZE, config.IMG_SIZE)),
            transforms.ToTensor(),
        ])

    if use_3d:
        clips = []
        for i in range(0, len(files) - config.CLIP_LEN + 1):
            clip = [transform(Image.open(files[j])) for j in range(i, i + config.CLIP_LEN)]
            clip_tensor = torch.stack(clip)  # (T, C, H, W)
            clips.append(clip_tensor.permute(1, 0, 2, 3))  # (C, T, H, W)
        return clips
    else:
        return [transform(Image.open(f)) for f in files]

def extract_features(video_name, use_3d):
    # Prepare paths
    mouth_crop_dir = os.path.join(config.BASE_DATA_DIR, video_name, "mouth_crops")
    base_feature_dir = os.path.join(config.BASE_DATA_DIR, video_name, "features")
    subdir = "3d_cnn" if use_3d else "resnets"
    feature_output_dir = os.path.join(base_feature_dir, subdir)
    os.makedirs(feature_output_dir, exist_ok=True)

    # Load model
    model = get_3dcnn_model() if use_3d else get_resnet18_model()
    model = model.to(config.DEVICE).eval()

    # Load data
    print(f"🔄 Loading {'clips' if use_3d else 'images'} for {'3D CNN' if use_3d else 'ResNet18'}...")
    images_or_clips = load_images(mouth_crop_dir, use_3d)

    print(f"🚀 Extracting features with {'3D CNN' if use_3d else 'ResNet18'}...")
    with torch.no_grad():
        for i, item in enumerate(tqdm(images_or_clips, desc=f"Saving to {subdir}")):
            input_tensor = item.unsqueeze(0).to(config.DEVICE)  # (1, C, H, W) or (1, C, T, H, W)
            features = model(input_tensor)
            feature_vector = features.cpu().numpy().squeeze()
            np.save(os.path.join(feature_output_dir, f"{i:05d}{config.FEATURE_EXTENSION}"), feature_vector)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        video_name = sys.argv[1]
    elif len(sys.argv) > 2:
        print("Usage: python run_feature_extraction.py [video_name]")
        sys.exit(1)

    print(f"🔍 Starting dual feature extraction for: {video_name}")
    extract_features(video_name, use_3d=False)  # ResNet18 (2D)
    extract_features(video_name, use_3d=True)   # 3D CNN
    print("✅ Both feature extractions completed.")
