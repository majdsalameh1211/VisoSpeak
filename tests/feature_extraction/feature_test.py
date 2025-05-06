import os
import numpy as np

def verify_feature_shapes(data_dir="data"):
    for video_name in os.listdir(data_dir):
        video_path = os.path.join(data_dir, video_name)
        features_dir = os.path.join(video_path, "features")

        if not os.path.isdir(features_dir):
            print(f"❌ {video_name}: No 'features/' folder found.")
            continue

        try:
            f3d = np.load(os.path.join(features_dir, "3d_features.npy"))
            f2d = np.load(os.path.join(features_dir, "2d_features.npy"))
        except FileNotFoundError as e:
            print(f"❌ {video_name}: Missing file - {e.filename}")
            continue

        print(f"📁 {video_name}")
        print(f"   ✓ 3D features shape: {f3d.shape} (expected (1, 128))")
        print(f"   ✓ 2D features shape: {f2d.shape} (expected (N, 512))")
        print(f"   ▶ Sample 3D vector (first 5 vals): {f3d[0][:5]}")
        print(f"   ▶ Sample 2D frame feature (first 5 vals): {f2d[0][:5]}")
        print()

if __name__ == "__main__":
    verify_feature_shapes()
