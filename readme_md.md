# VisoSpeak - AI-Powered Lip Reading System

VisoSpeak is an advanced AI-powered lip reading application that converts visual speech from video into text using two complementary deep learning models. The system provides an intuitive web interface for real-time lip reading demonstrations and research.

## 📖 Research Background

This project is based on original research that builds upon the Transformer-based visual speech recognition system by Fenghour et al. (2020). Our research introduces **significant improvements to word boundary detection** and overall prediction accuracy through:

### Abstract
VisoSpeak is a visual-only speech recognition system that reconstructs spoken sentences from lip movements without the use of audio signals. The primary contribution of this work is the development of a **Transformer-based architecture designed to improve sentence prediction by explicitly modeling word boundaries and inter-word spacing**, a critical factor for enhancing segmentation and overall accuracy. In parallel, the LipNet architecture was reproduced as part of this study to explore alternative visual speech recognition methodologies and gain a broader perspective on potential system improvements, rather than for direct comparison. Additionally, this research discusses the potential integration of modern natural language processing techniques for word filtering and sentence construction, highlighting future directions for achieving more efficient and coherent post-prediction processing.

### Key Research Innovations

#### 🔬 **Enhanced Word Boundary Detection**
- **Original Approach**: Fixed time-gap heuristics for word segmentation
- **Our Approach**: Explicit `<sow>` (start-of-word) and `<eow>` (end-of-word) tokens learned directly within the decoder
- **Impact**: Variable-length word segmentation enables flexible alignment to different speaking speeds

#### 🎯 **Expanded Viseme Recognition**
- **Original**: 13 visemes + 5 special tokens
- **Our Enhancement**: Full CMU Pronouncing Dictionary-based viseme set (40+ visemes) + 7 structural tokens
- **Advantage**: Richer phonetic distinction and improved word boundary recognition

#### 🧠 **Modern NLP Integration**
- **Traditional**: Beam search with perplexity scoring
- **Our Innovation**: Fuzzy phoneme matching + ChatGPT-4 API for contextual word selection and sentence construction
- **Result**: Enhanced grammatical fluency and contextual accuracy

#### 📹 **Advanced Preprocessing**
- **Upgraded**: MediaPipe FaceMesh (468-point landmarks) vs. original dlib (68-point)
- **Extended**: Support for up to 250 frames (vs. 180) for longer utterances
- **Benefit**: More precise lip contour detection with reduced jitter

### Research Pipeline
This GUI application represents the **complete research implementation pipeline**:
1. **Data Preprocessing**: Advanced video processing and lip region extraction
2. **Model Training**: Both Transformer and LipNet architectures with our enhancements
3. **Prediction & Evaluation**: Real-time inference with accuracy metrics
4. **Research Analysis**: Tools for comparing model performance and boundary detection accuracy

The system serves as both a **practical demonstration** of our research contributions and a **research platform** for further analysis and improvements in visual speech recognition.

## 🎯 Project Overview

VisoSpeak bridges communication gaps in noisy environments and provides accessibility solutions for deaf and hard-of-hearing individuals through cutting-edge AI technology. The system employs two distinct approaches:

- **LipNet Model**: End-to-end character-based prediction for known vocabulary (research baseline)
- **Enhanced Transformer Model**: Our improved viseme-based approach with superior word boundary detection

## 🏗️ System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React Frontend │────│  Flask Backend   │────│  AI Models      │
│   (Port 3000)    │    │  (Port 5000)     │    │  - LipNet       │
└─────────────────┘    └──────────────────┘    │  - Transformer  │
                                                └─────────────────┘
```

## 🚀 Features

- **Dual Model Architecture**: Choose between LipNet and Transformer models based on your needs
- **Real-time Processing**: Live progress tracking with detailed status updates
- **Interactive Web Interface**: Modern React-based GUI with video preview and results visualization
- **Dataset Support**: Compatible with GRID Corpus and LRS2 datasets
- **Accuracy Metrics**: Detailed performance metrics including viseme and boundary matching
- **Cross-platform**: Runs on Windows, macOS, and Linux

## 📋 Prerequisites

### System Requirements
- Python 3.8 or higher
- Node.js 14.0 or higher
- npm or yarn package manager
- CUDA-compatible GPU (recommended for faster inference)
- Minimum 8GB RAM, 16GB recommended

### Datasets
- **GRID Corpus**: For LipNet model (1,000 videos)
- **LRS2 Dataset**: For Transformer model (80,000+ videos)

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/visospeak.git
cd visospeak
```

### 2. Backend Setup (Python)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup (React)
```bash
cd frontend
npm install
# or
yarn install
```

### 4. Model Setup
```bash
# Create models directory
mkdir -p backend/models

# Download pre-trained models (replace with actual download links)
# LipNet model weights
wget -O backend/models/lipnet.weights.h5 [MODEL_DOWNLOAD_URL]

# Transformer model weights  
wget -O backend/models/transformer.pt [MODEL_DOWNLOAD_URL]
```

### 5. Dataset Setup
```bash
# Create dataset directories
mkdir -p frontend/public/GRID
mkdir -p frontend/public/LRS2

# Place your video files in respective directories:
# - GRID videos (.mp4) and alignment files (.align) in frontend/public/GRID/
# - LRS2 videos (.mp4) and viseme tensors (.pt) in frontend/public/LRS2/
```

## 🚀 Running the Application

### Start Backend Server
```bash
cd backend
python server.py
```
Backend will start on `http://localhost:5000`

### Start Frontend Server
```bash
cd frontend
npm start
# or
yarn start
```
Frontend will start on `http://localhost:3000`

### Access the Application
Open your web browser and navigate to `http://localhost:3000`

## 📁 Project Structure

```
visospeak/
├── backend/
│   ├── models/
│   │   ├── lipnet_model.py          # LipNet architecture
│   │   └── lip_reading_model.py     # Transformer architecture
│   ├── config.py                    # Configuration settings
│   ├── server.py                    # Flask API server
│   ├── lipnet_prediction.py         # LipNet inference
│   ├── transformer_prediction.py    # Transformer inference
│   └── transformer_preprocess.py    # Video preprocessing
├── frontend/
│   ├── public/
│   │   ├── GRID/                    # GRID dataset videos
│   │   └── LRS2/                    # LRS2 dataset videos
│   ├── src/
│   │   ├── components/
│   │   │   ├── HomePage.js          # Landing page
│   │   │   ├── LipNetEndToEnd.js    # LipNet interface
│   │   │   └── TransformerEndToEnd.js # Transformer interface
│   │   └── design/                  # CSS stylesheets
│   └── package.json
├── requirements.txt                 # Python dependencies
└── README.md                       # This file
```

## 🔬 Research Applications

This GUI serves multiple research purposes:

### 1. **Model Performance Analysis**
- Real-time comparison between baseline LipNet and our enhanced Transformer
- Quantitative metrics: viseme accuracy, boundary detection precision
- Qualitative assessment of word segmentation improvements

### 2. **Boundary Detection Validation**
- Visual demonstration of `<sow>`/`<eow>` token effectiveness
- Comparison of fixed vs. learned word segmentation approaches
- Analysis of speaking speed adaptation capabilities

### 3. **Future Research Platform**
The system is designed to support ongoing research in:
- **Adaptive fuzzy thresholds** for phoneme matching optimization
- **Advanced NLP integration** (GPT-4, LLaMA) for semantic validation
- **Multilingual support** through expanded viseme-phoneme mappings
- **Edge deployment** optimization for real-time applications

### 4. **Accessibility Research**
- User validation with deaf and hard-of-hearing communities
- Performance analysis in various environmental conditions
- Evaluation of practical deployment scenarios

## 🎮 Usage & Research Interface

### 1. Home Page
- **Research overview** and model comparison
- **Architecture visualization** of both approaches
- **Navigation** to prediction interfaces for analysis

### 2. LipNet Interface (Research Baseline)
- Select from GRID dataset videos for baseline evaluation
- Real-time processing with progress tracking
- Character-level prediction results for comparison analysis

### 3. Enhanced Transformer Interface (Our Research Contribution)
- Select from LRS2 dataset videos for enhanced model testing
- **Advanced metrics**: Viseme accuracy and boundary detection precision
- **Token-level visualization** showing `<sow>`/`<eow>` boundary predictions
- **Research validation**: Direct comparison with ground truth boundaries

### Research Workflow
```
Video Input → Preprocessing → Model Prediction → Boundary Analysis → Research Metrics
     ↓              ↓              ↓                ↓                    ↓
  Dataset      MediaPipe/     LipNet vs.      Word Segmentation    Performance
 Selection     OpenCV        Transformer      Accuracy Analysis    Evaluation
```

## 📊 Model Details & Research Contributions

### LipNet Model (Research Baseline)
- **Architecture**: 3D CNN + Bidirectional LSTM + CTC Loss
- **Input**: 75 frames, 46×140 pixels (lip region)
- **Output**: Character sequences
- **Dataset**: GRID Corpus (1,000 videos)
- **Vocabulary**: 26 letters + special characters + digits
- **Purpose**: Baseline comparison and alternative methodology exploration

### Enhanced Transformer Model (Our Research Contribution)
- **Architecture**: 3D CNN + 2D ResNet + Enhanced Transformer Encoder-Decoder
- **Input**: 250 frames, 112×112 pixels (lip region)  
- **Output**: Viseme sequences with explicit word boundaries
- **Dataset**: LRS2 (80,000+ videos)
- **Enhanced Vocabulary**: 
  - **40+ visemes** from CMU Pronouncing Dictionary (vs. 13 in original)
  - **7 structural tokens** including `<sow>`, `<eow>` for word boundary detection
- **Key Innovations**:
  - MediaPipe-based preprocessing (468-point vs. 68-point landmarks)
  - Autoregressive decoder with explicit boundary modeling
  - Fuzzy phoneme matching + ChatGPT-4 integration
  - Support for longer sequences (250 vs. 180 frames)

### Research Pipeline Comparison

| Component | Original Approach | Our Enhancement | Research Impact |
|-----------|------------------|-----------------|-----------------|
| **Preprocessing** | dlib (68 landmarks) | MediaPipe (468 landmarks) | ↑ Precision & stability |
| **Boundary Detection** | Time-gap heuristics | Learned `<sow>`/`<eow>` tokens | ↑ Word segmentation accuracy |
| **Viseme Set** | 13 basic visemes | 40+ CMU-based visemes | ↑ Phonetic distinction |
| **Post-processing** | Beam search + perplexity | Fuzzy matching + ChatGPT-4 | ↑ Contextual accuracy |
| **Sequence Length** | 180 frames max | 250 frames max | ↑ Long utterance handling |

## 🔧 Configuration

Edit `backend/config.py` to customize:

- Model paths and weights
- Video processing parameters
- Dataset paths
- Frame dimensions and processing settings

## 🧪 API Endpoints

### Backend API Routes

#### `GET /prediction-progress`
Returns current prediction progress and status.

#### `POST /run-lipnet`
```json
{
  "video_name": "video_filename.mp4"
}
```
Runs LipNet prediction on specified video.

#### `POST /run-transformer`
```json
{
  "video_name": "video_filename.mp4"
}
```
Runs Transformer prediction on specified video.

## 🔍 Troubleshooting

### Common Issues

1. **Video Loading Issues**
   - Ensure videos are in supported format (MP4)
   - Check browser codec support
   - Verify file paths in config.py

2. **Model Loading Errors**
   - Verify model files exist in `backend/models/`
   - Check CUDA availability for GPU acceleration
   - Ensure sufficient RAM/VRAM

3. **CORS Errors**
   - Backend server must be running on port 5000
   - Frontend on port 3000
   - flask-cors properly configured

4. **Performance Issues**
   - Enable GPU acceleration if available
   - Reduce batch size for lower memory usage
   - Close other memory-intensive applications

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors & Research Team

**Research Authors:** Majd Salameh & Morad Asakli  
**Project Advisor:** Mr. Ilya Zeldner

### Research Contributions
This work builds upon the foundational Transformer-based visual speech recognition research by **Fenghour et al. (2020)**, with significant enhancements to word boundary detection and overall system accuracy. Our research demonstrates measurable improvements in visual speech recognition through innovative architectural modifications and modern NLP integration.

### Acknowledgments
- **Fenghour et al. (2020)** for the original Transformer-based approach
- GRID Corpus and LRS2 dataset providers for research datasets
- MediaPipe team for advanced facial landmark detection
- OpenAI for ChatGPT-4 API integration in post-processing
- TensorFlow and PyTorch communities for deep learning frameworks

### Academic Impact
This research contributes to the field of visual speech recognition by:
- Demonstrating the importance of explicit boundary modeling in lip reading systems
- Providing a practical framework for integrating modern NLP techniques in visual speech processing
- Establishing benchmarks for future research in word boundary detection accuracy

## 📞 Support

For support, please open an issue on GitHub or contact the development team.

## 🔗 Links

- [Demo Video](link-to-demo)
- [Research Paper](link-to-paper)
- [Dataset Information](link-to-datasets)

---

**VisoSpeak** - Bridging the gap between visual speech and text through AI innovation.