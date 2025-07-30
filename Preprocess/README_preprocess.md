# VisoSpeak Preprocessing

This module performs preprocessing for the VisoSpeak lip-reading project, converting raw video and alignment data into fixed-size tensors for deep learning models.

---

## Overview

The preprocessing step includes:
1. **Frame Extraction**: Convert videos into fixed-length sequences of frames.
2. **Lip Region Detection**: Use MediaPipe FaceMesh to crop and normalize mouth regions.
3. **Viseme Mapping**: Convert alignment text into viseme token sequences using CMUdict + G2P mapping.
4. **Tensor Preparation**: Pad/normalize data and save as `.pt` or `.npz` files for training and validation.

---

## Features

- **Video Preprocessing**: Extract frames at fixed FPS and crop lips accurately.
- **Alignment Parsing**: Map phonemes to visemes with special tokens (`<sos>`, `<sow>`, `<eow>`, `<eos>`).
- **Batch Conversion**: Process thousands of video-alignment pairs into compressed `.npz` batches.
- **GPU Ready**: Outputs tensors compatible with PyTorch GPU training.

---

## Requirements

Install required libraries:

```bash
pip install opencv-python dlib mediapipe g2p-en inflect nltk matplotlib
```

Ensure you download the `shape_predictor_68_face_landmarks.dat` model for dlib and place it in `dlib_models/`.

---

## Configuration

- **MAX_FRAMES**: Maximum frame length (default `250`)
- **Frame Size**: Cropped lip ROIs resized to `112x112`
- **Special Tokens**: `<sos>`, `<eos>`, `<sow>`, `<eow>`, `<space>`, `<sil>`, `<pad>`
- **Directories**:
  - Pretrain data: `PROJECT_ROOT/pretrain`
  - Main data: `PROJECT_ROOT/main`
  - Output tensors: `PROJECT_ROOT/processed/`

---

## Usage

### 1. Preprocess a Single Video

```python
video_tensor = video_to_preprocced_tensor("path/to/video.mp4")
viseme_tensor = alignment_to_viseme_tensor("path/to/alignment.txt")
```

### 2. Save as NPZ Batch

```python
pairs = [(video_path, alignment_path), ...]
save_npz_batch_from_pairs_in_memory_unit8(pairs, batch_index=1, save_root="/content/pretrain_data_batches_ready_to_load")
```

### 3. Validate Preprocessed Data

```python
video_tensor, viseme_tensor = process_pair_without_saving((video_path, alignment_path))
print(video_tensor.shape, viseme_tensor.shape)
```

---

## Output

- `.npz` files contain:
  - `videos`: `(B, 250, 112, 112, 1)` uint8 tensors
  - `visemes`: `(B, 250)` int64 viseme token IDs

- Compressed batches are saved in `pretrain_data_batches_ready_to_load/`.

---

## Notes

- Designed for Google Colab workflows (cell-based to script-friendly).
- Modular functions allow easy scaling to large datasets (80k+ videos).
- Part of the VisoSpeak pipeline: this is **Step 1 – Preprocessing**.
