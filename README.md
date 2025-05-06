
# VisoSpeak - Visual Speech Recognition Pipeline

VisoSpeak is a multi-step deep learning system that converts silent video of a speaking person into full reconstructed text using lip reading, viseme classification, and language modeling.

This README outlines the current project progress and how to run each completed step.

---

## ✅ Project Status

We have completed the following major phases:

1. **Preprocessing** – extract frames and detect faces
2. **Mouth Extraction** – crop and save lip regions per frame
3. **Feature Extraction** – extract frame-level (ResNet2D) and clip-level (3D CNN) features and save as `.npy`

Next steps include:
- Viseme sequence prediction using a Transformer
- Word matching and GPT-2 scoring
- Full sentence correction and evaluation

---

## 🔧 Setup Instructions

### 1. Clone the repo
```bash
cd VisoSpeak
```

### 2. Install required packages
In any Jupyter cell or terminal:
```python
import sys
!{sys.executable} -m pip install --upgrade pip
!{sys.executable} -m pip install torch torchvision torchaudio numpy pillow tqdm matplotlib seaborn scikit-learn opencv-python
```

---

## 🧱 Project Steps (Completed)

### 01 – Preprocessing
Extract video frames and detect face bounding boxes.
```bash
python scripts_to_run_files/run_preprocessing.py --video_path data/raw/vid_001.mp4
```
Generates: `data/vid_001/frames/`

### 02 – Mouth Extraction
Crop and save the mouth region using face detection metadata.
```bash
python scripts_to_run_files/run_mouth_extraction.py --video_name vid_001
```
Generates: `data/vid_001/mouth_crops/`

### 03 – Feature Extraction
Extract two sets of features:
- Static (ResNet2D)
- Spatio-temporal (3D CNN)

```bash
python scripts_to_run_files/run_feature_extraction.py --video_name vid_001
```
Generates:
```
data/vid_001/features/
  ├── resnets/      ← One .npy per frame
  └── 3d_cnn/       ← One .npy per clip
```

You can inspect and visualize the output using:
```bash
notebooks/03_feature_extraction.ipynb
```

---

## 📂 Folder Summary
- `notebooks/` – Test, visualize and inspect results at each step
- `scripts_to_run_files/` – CLI interface to execute each step
- `src/` – Core implementation for each module
- `data/` – Raw inputs, intermediate files, and final outputs
- `models/` – Pretrained weights used for each model

---

## 🚧 Next Steps
- `04_viseme_prediction.ipynb` → Map features to viseme sequence using a transformer
- `05_word_generation.ipynb` → Match visemes to words using CMU & GPT
- `06_sentence_correction.ipynb` → Refine final output with a sentence corrector

---

For help running or extending the pipeline, please check the relevant notebook for each phase.
