# VisoSpeak – Transformer Training (Colab)

## Overview
This notebook trains the **VisoSpeak lip-reading Transformer model**, combining a **3D CNN visual frontend** with **Transformer encoder–decoder** architecture to convert silent lip movements into viseme sequences.  
The training process is designed for **Google Colab** and optimized for large datasets through **RAM-buffer streaming** and **dynamic batch sizing**.

---

## Key Features
- **3D CNN + Transformer**: End-to-end viseme prediction model.
- **Streaming Data Loader**:
  - Prefetches `.npz` batches from Google Drive into a RAM buffer.
  - Keeps GPU fed continuously without I/O bottlenecks.
- **Dynamic Batch Sizing**:
  - Automatically adjusts based on detected GPU (L4 vs A100).
  - Prevents out-of-memory errors.
- **Mixed Precision Training (AMP)**:
  - Reduces memory usage and speeds up training.
- **Checkpointing + Resume**:
  - Saves model state every epoch (`epoch_X.pt`).
  - Auto-resumes training from last checkpoint.

---

## Dataset
- Preprocessed `.npz` batches generated from the **preprocessing pipeline**.
- Each batch file contains:
  - `videos`: `(32, 250, 112, 112, 1)` – normalized lip ROI frames.
  - `visemes`: `(32, 250)` – tokenized viseme sequences.

---

## Colab-Specific Optimizations

### 1. RAM Buffer Streaming
- Loads batches from Google Drive into RAM.
- Trains directly from RAM to avoid Drive latency.
- Monitors buffer usage, refilling asynchronously with threads.

### 2. Dynamic Batch Size
- Batch size chosen based on GPU memory:
  - **A100**: ~128
  - **L4**: ~64
- Configurable via `BATCH_SIZE` in notebook.

---

## Training Pipeline

1. **Setup**
   - Install dependencies: `torch`, `mediapipe`, `g2p-en`, `inflect`, `nltk`
   - Mount Google Drive
   - Set project paths

2. **Model Initialization**
   - Load token dictionaries (visemes + special tokens)
   - Build `LipReadingModel` (3D CNN + Transformer)

3. **Buffer Prefetch**
   - Threaded function to keep buffer filled with preprocessed `.npz` batches

4. **Training Loop**
   - Mixed precision with `torch.cuda.amp`
   - CrossEntropy loss (ignores `<pad>` tokens)
   - Validation every 10 epochs
   - Early stopping after 3 epochs with no improvement

5. **Checkpointing**
   - Saves `epoch_X.pt` in model folder
   - Auto-resumes from latest checkpoint

---

## Metrics

- **Boundary Accuracy**: Placement of `<sow>` and `<eow>` tokens.
- **Viseme Accuracy**: Token match ignoring special tokens.
- **Loss Tracking**: Training and validation loss logged.

---

## Visualization

- Accuracy and loss curves plotted per epoch.
- Histograms for boundary and viseme accuracy distribution.

---

## How to Run

### 1. Install Dependencies
```bash
pip install torch torchvision torchaudio
pip install mediapipe g2p-en inflect nltk
```

### 2. Mount Google Drive
```python
from google.colab import drive
drive.mount('/content/drive')
```

### 3. Configure Paths
Update `MODEL_SAVE_FOLDER` and `BATCH_FOLDER` variables to your Drive paths.

### 4. Start Training
```python
auto_resume_and_train()
```

---

## Output
- Model checkpoints saved as `epoch_X.pt`
- Accuracy plots saved to `MODEL_SAVE_FOLDER`
- Boundary/viseme metrics exported as `.npy`
