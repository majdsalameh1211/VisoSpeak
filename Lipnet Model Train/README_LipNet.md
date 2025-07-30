# LipNet Training Pipeline

This README documents the **LipNet model training pipeline**, implemented and tested entirely in **Google Colab** using GPU acceleration. LipNet is a deep learning model that predicts text sequences directly from silent video frames of lip movements.

---

## Overview

The pipeline follows these main stages:

1. **Data Preprocessing**  
   - Extracts frames from video files.  
   - Converts frames to grayscale and resizes to `(50x100)`.  
   - Aligns video frames with text annotations for training.

2. **Model Architecture (LipNet)**  
   - **3D Convolutional Layers** for spatiotemporal feature extraction.  
   - **Bidirectional LSTM** layers to capture temporal dependencies.  
   - **CTC (Connectionist Temporal Classification)** loss for sequence alignment between predicted characters and target text.

3. **Training**  
   - Trains the LipNet model on processed videos.  
   - Uses dynamic GPU memory handling with Colab’s environment.  
   - Includes checkpoint saving and accuracy tracking per epoch.

4. **Evaluation**  
   - Computes character-level and word-level accuracy.  
   - Visualizes predictions vs. ground truth for sample videos.

---

## Environment (Google Colab)

This pipeline is **optimized for Google Colab** with GPU runtime:

- **Dynamic Batch Size:** Automatically adjusts based on GPU memory availability.  
- **Buffer Loading:** Uses RAM buffer preloading to minimize I/O delays when streaming video batches.  
- **Mixed Precision (AMP):** Enables faster training with reduced memory usage.

---

## Dependencies

Install required libraries in Colab:

```bash
!pip install opencv-python dlib matplotlib mediapipe g2p-en
!pip install tensorflow keras
!pip install nltk inflect
```

Download NLTK data:

```python
import nltk
nltk.download('cmudict')
nltk.download('averaged_perceptron_tagger')
nltk.download('names')
```

---

## Data Preparation

- **Input:**  
  - Video files (`.mp4`) and corresponding alignment files (`.txt`).

- **Preprocessing Steps:**  
  1. Extract frames at **25 FPS** and resize to **50x100**.  
  2. Convert to grayscale and normalize pixel values.  
  3. Map alignment text to character sequences using a predefined vocabulary.  
  4. Pad sequences to fixed lengths for batch processing.

---

## Model Architecture

- **Input:** `(T, 50, 100, 3)` video frames (T = time steps).  
- **Layers:**
  1. Three 3D convolution + max-pooling layers.  
  2. Flattening and reshaping into sequences.  
  3. Two Bidirectional LSTM layers.  
  4. Dense softmax layer for character prediction.  

- **Loss Function:** `CTC Loss` (handles unaligned sequences).  
- **Optimizer:** `Adam` with learning rate scheduling.

---

## Training Workflow

1. **Initialize Model** – Build LipNet architecture and compile with CTC loss.  
2. **Load Data** – Preprocessed video-text pairs are streamed in batches.  
3. **Train** – Run for `N` epochs with validation after each epoch.  
4. **Checkpoints** – Save best model weights (`lipnet.weights.h5`).  
5. **Evaluation** – Compute accuracy and visualize predictions.

---

## Running the Training

**Steps in Colab:**
1. Upload videos and alignments to Google Drive.  
2. Mount Drive and set `PROJECT_ROOT` path.  
3. Run preprocessing cells to generate training-ready datasets.  
4. Execute the training cell to start model training:  

```python
model.fit(train_dataset,
          validation_data=val_dataset,
          epochs=100,
          callbacks=[checkpoint_callback])
```

5. Best weights are automatically saved during training.

---

## Output

- **Model Weights:** `lipnet.weights.h5` (best performing model).  
- **Logs:** Training/validation loss and accuracy per epoch.  
- **Visualizations:** Comparison of predicted vs. actual text sequences.

---

## Notes

- This pipeline is designed as a **baseline model** for lip reading.  
- It does **not include viseme or boundary token predictions** (handled in Transformer model).  
- It was primarily used to **analyze alternative approaches** for lip reading within the VisoSpeak research project.
