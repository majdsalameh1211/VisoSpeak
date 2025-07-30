import os

# === Project Paths ===
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FRONTEND_PUBLIC = os.path.join(PROJECT_ROOT, "frontend", "public")

LRS2_PATH = os.path.join(FRONTEND_PUBLIC, "LRS2")
GRID_PATH = os.path.join(FRONTEND_PUBLIC, "GRID")
MODELS_PATH = os.path.join(PROJECT_ROOT, "backend", "models")

# === Model Weights ===
TRANSFORMER_MODEL_PATH = os.path.join(MODELS_PATH, "transformer.pt")
LIPNET_MODEL_PATH = os.path.join(MODELS_PATH, "lipnet.weights.h5")

# === Frame / Video Params ===
TARGET_FPS = 25
FRAME_WIDTH = 122
FRAME_HEIGHT = 122
MAX_FRAMES = 250  # same used in transformer model
LIP_OUTPUT_SIZE = (112, 112)
MOUTH_LANDMARKS = list(range(61, 81))
PADDING = 10

# === Tokens for Transformer ===
SPECIAL_TOKENS = ["<sos>", "<eos>", "<sow>", "<eow>", "<space>", "<sil>", "<pad>"]
VISEME_TOKENS = [
    "AA", "AE", "AH", "AO", "AW", "AY", "B", "CH", "D", "DH",
    "EH", "ER", "EY", "F", "G", "HH", "IH", "IY", "JH", "K", "L",
    "M", "N", "NG", "OW", "OY", "P", "R", "S", "SH", "T", "TH",
    "UH", "UW", "V", "W", "Y", "Z", "ZH", "sil", "<unk>"
]
ALL_TOKENS = SPECIAL_TOKENS + VISEME_TOKENS
IDX_TO_TOKEN = {idx: tok for idx, tok in enumerate(ALL_TOKENS)}

SOS_IDX = ALL_TOKENS.index("<sos>")
EOS_IDX = ALL_TOKENS.index("<eos>")

# === LipNet Specific Params ===
lipnet_target_frames = 75         # number of frames per video
lipnet_frame_height = 46          # input frame height for LipNet
lipnet_frame_width = 140          # input frame width for LipNet
lipnet_vocab = [x for x in "abcdefghijklmnopqrstuvwxyz'?!123456789 "]
