# VisoSpeak: Lip Reading with Transformer & LipNet

This project is a full-stack application that predicts speech from silent videos using two deep learning models:
- **Transformer-based Viseme Prediction**
- **LipNet-based Word-Level Prediction**

The application includes:
- **Backend (Flask + PyTorch/TensorFlow)** for video preprocessing and prediction
- **Frontend (React + TailwindCSS)** for user interface

---

## Project Structure

```
Viso_Speak_GUI/
├── backend/
│   ├── config.py
│   ├── server.py
│   ├── transformer_prediction.py
│   ├── transformer_preprocess.py
│   ├── lipnet_prediction.py
│   ├── models/
│   │   ├── lip_reading_model.py
│   │   ├── lipnet_model.py
│   │   ├── transformer.pt        # Transformer weights
│   │   └── lipnet.weights.h5     # LipNet weights
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   │   ├── GRID/ (video dataset)
│   │   └── LRS2/  (video + viseme tensors)
│   └── src/
│       ├── pages/
│       │   ├── HomePage.js
│       │   ├── LipNetEndToEnd.js
│       │   └── TransformerEndToEnd.js
│       ├── design/
│       │   ├── HomePage.css
│       │   ├── LipNetEndToEnd.css
│       │   └── TransformerEndToEnd.css
│       └── App.js
└── README.md
```

---

## Installation & Setup

### Backend Setup

1. Create virtual environment (recommended):
```bash
python -m venv visoenv
source visoenv/bin/activate  # (Linux/Mac)
visoenv\Scripts\activate     # (Windows)
```

2. Install dependencies:
```bash
pip install -r backend/requirements.txt
```

3. Run Flask server:
```bash
cd backend
python server.py
```

Server will run at **http://127.0.0.1:5000**

---

### Frontend Setup

1. Go to frontend folder:
```bash
cd frontend
```

2. Install dependencies (React + Tailwind):
```bash
npm install
```

3. Start React development server:
```bash
npm start
```

App will run at **http://localhost:3000**

---

## Environment Variables

Static variables are stored in **backend/config.py**, including:
- Dataset paths (`GRID_PATH`, `LRS2_PATH`)
- Frame dimensions and max frames
- Viseme definitions
- Model weight paths (`TRANSFORMER_MODEL_PATH`, `LIPNET_MODEL_PATH`)

---

## How to Use

1. Place video files in `frontend/public/GRID/` (for LipNet) or `frontend/public/LRS2/` (for Transformer).
2. Run Flask backend and React frontend simultaneously.
3. In the UI:
   - Select a video.
   - Click **Predict** under LipNet or Transformer page.
4. See:
   - Predicted visemes / words
   - Ground truth text
   - Accuracy metrics (viseme match %, boundary match %)

---

## Technologies Used

- **Backend**: Flask, PyTorch, TensorFlow, OpenCV
- **Frontend**: React, TailwindCSS
- **Models**: LipNet (CTC), Transformer Encoder-Decoder
- **Dataset**: GRID, LRS2

---

## Deployment Notes

- For production, build frontend:
```bash
cd frontend
npm run build
```
- Serve React build using Flask or host separately.

---

## License
MIT License

