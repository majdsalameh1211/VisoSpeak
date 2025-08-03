# VisoSpeak: Visual-Only Speech Recognition System

[![DOI](https://img.shields.io/badge/DOI-10.1109%2FACCESS.2020.3040906-blue)](https://doi.org/10.1109/ACCESS.2020.3040906)
[![License](https://img.shields.io/badge/License-Research-green)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![Framework](https://img.shields.io/badge/Framework-PyTorch%20%7C%20TensorFlow-orange)](https://pytorch.org)

A state-of-the-art **visual speech recognition system** that reconstructs spoken sentences purely from lip movements, without audio input. This project builds upon and enhances the seminal work by Fenghour et al. (2020), introducing key innovations in **word boundary detection**, **viseme vocabulary expansion**, and **real-time preprocessing**.

---

## 🚀 Quick Start

### 1. Download Pre-trained Models
Due to GitHub size limits, models are hosted on Google Drive:

**[Download Models Here](https://drive.google.com/drive/folders/1KgVinW_bmLaf8nShHXJ2E4vuokAZumko?usp=sharing)**

Place downloaded models into:
```
Viso_Speak_GUI/backend/models/
```
Files included:
- `lipnet.weights.h5` – LipNet model weights
- `transformer.pt` – Transformer checkpoint

---

### 2. Installation & Setup

#### Clone the Repository
```bash
git clone https://github.com/majdsalameh1211/VisoSpeak.git
cd VisoSpeak
```

#### Backend Setup
```bash
cd Viso_Speak_GUI/backend
pip install -r requirements.txt
python app.py
```

#### Frontend Setup
```bash
cd Viso_Speak_GUI/frontend
npm install
npm start
```

Access the app via `http://localhost:3000`.

---

## 📖 Project Overview

### Original Approach (Fenghour et al., 2020)
The original system introduced a **Transformer-based viseme classifier** with perplexity-based viseme-to-word mapping:

- **Visual Frontend**: 3D-CNN + 2D ResNet for spatiotemporal features  
- **Viseme Classification**: 13 visemes + special tokens (`<sos>`, `<eos>`, `<space>`)  
- **Word Construction**: CMU Dictionary mapping + beam search (perplexity analysis)  
- **Limitation**: Word boundaries inferred heuristically, limited vocabulary

### Our Enhancements

#### 1. Explicit Word Boundary Modeling
- Introduced `<sow>` and `<eow>` tokens for learned word segmentation
- Improves boundary detection and flexibility across speaking speeds

#### 2. Expanded Viseme Vocabulary
- Mapped full CMU dictionary (40+ visemes) vs original 13 visemes
- Enhances phonetic coverage and linguistic precision

#### 3. MediaPipe-based Preprocessing
- Enhancement includes replacing the traditional Dlib model with **MediaPipe FaceMesh** for lip landmark extraction, resulting in higher accuracy and robustness.
- Replaced Dlib (68 landmarks) with MediaPipe FaceMesh (468 landmarks)
- Improves lip tracking accuracy, speed (20 FPS vs 6 FPS), and robustness to pose/lighting

#### 4. Extended Sequence Length
- Increased max sequence length from 180 → 250 frames
- Supports longer utterances and natural speech patterns

#### 5. End-to-End Optimization
- Joint training of visual frontend and Transformer
- Reduces error propagation and aligns features with decoder

---

## 🔬 Technical Architecture

### Dual Model Design

#### **LipNet (Baseline)**
- 3D-CNN → Bi-GRU → CTC Loss
- Direct character-level prediction
- Effective for constrained vocabularies

#### **Transformer (Enhanced)**
- 3D-CNN Visual Frontend → Transformer Encoder → Transformer Decoder
- Autoregressive viseme prediction with explicit boundary tokens
- Suitable for complex, unconstrained datasets (e.g., LRS2)

### System Workflow

```
Video Input → Preprocessing → Feature Extraction → Viseme Prediction → NLP Filtering → Sentence Reconstruction
```

---

## 🚀 Future Work

1. **Modern NLP Integration**
   - Replace beam search with GPT-4/Claude for context-aware candidate filtering  
2. **Fuzzy Viseme-Phoneme Mapping**
   - Levenshtein-based similarity scoring for robust word recovery  
3. **Multimodal Extensions**
   - Optional audio-visual fusion for improved accuracy in noisy environments  
4. **Real-Time Optimization**
   - ONNX/TensorRT deployment for low-latency inference  
5. **Domain Adaptation**
   - Fine-tune for specialized domains (medical, legal, assistive communication)

---

## 📊 Performance Highlights

| Feature                  | Original (2020) | Our Enhancement |
|--------------------------|-----------------|-----------------|
| Viseme Vocabulary        | 13 visemes      | 40+ visemes     |
| Sequence Length          | 180 frames      | 250 frames      |
| Boundary Detection       | Heuristic       | Learned tokens  |
| Processing Speed         | ~6 FPS          | ~20 FPS         |
| Word Segmentation        | Fixed timing    | Adaptive        |

---

## 🔧 Requirements

### Hardware
- **GPU**: 15 GB VRAM minimum (e.g., NVIDIA L4/A100)
- **RAM**: 32 GB minimum
- **Storage**: 500 GB (datasets + checkpoints)

### Software
- **Python 3.10+**
- **Core Libraries**: PyTorch, TensorFlow, Keras, OpenCV, MediaPipe
- **Web**: Flask (backend), React + TailwindCSS (frontend)

---


> **Note**: The LRS2 dataset is provided by the University of Oxford and was accessed with official approval for research purposes only.
## 📚 References

1. Fenghour, S., et al. (2020). *Lip Reading Sentences Using Deep Learning With Only Visual Cues*. IEEE Access.  
2. Assael, Y., et al. (2016). *LipNet: Sentence-Level Lipreading*.  
3. Chung, J. S., et al. (2017). *Lip Reading Sentences in the Wild*. CVPR.

---

## 👥 Team & Acknowledgements

- **Students**: Majd Salameh, Morad Asakli  
- **Supervisor**: Mr. Ilya Zeldner, ORT Braude College of Engineering  
- **Datasets**: BBC LRS2, GRID Corpus  
- **Infrastructure**: Google Colab GPU   

---

## 📧 Contact

- Majd Salameh – [Majd.Salameh@e.braude.ac.il](mailto:Majd.Salameh@e.braude.ac.il)  
- Morad Asakli – [Morad.Asakli@e.braude.ac.il](mailto:Morad.Asakli@e.braude.ac.il)

**GitHub Repository**: [https://github.com/majdsalameh1211/VisoSpeak](https://github.com/majdsalameh1211/VisoSpeak)
