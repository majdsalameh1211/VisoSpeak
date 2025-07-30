import os
import torch
from models.lip_reading_model import LipReadingModel
from config import (
    IDX_TO_TOKEN, TRANSFORMER_MODEL_PATH
)
from transformer_preprocess import video_to_preprocessed_tensor

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# === Calculate Boundary Match ===
def calculate_boundary_match(pred_tokens, true_tokens):
    pred_boundaries = [i for i, t in enumerate(pred_tokens) if t in ("<sow>", "<eow>")]
    true_boundaries = [i for i, t in enumerate(true_tokens) if t in ("<sow>", "<eow>")]
    if not true_boundaries:
        return 0.0
    matched = sum(1 for idx in true_boundaries if idx in pred_boundaries)
    return round((matched / len(true_boundaries)) * 100, 2)

# === Calculate Viseme Match ===
def calculate_viseme_match(pred_tokens, true_tokens):
    min_len = min(len(pred_tokens), len(true_tokens))
    matches = 0
    total = 0
    for i in range(min_len):
        p, t = pred_tokens[i], true_tokens[i]
        if t == "<pad>" or p == "<pad>":
            continue
        if p not in {"<sos>", "<eos>", "<sow>", "<eow>", "<space>", "<sil>"} and \
           t not in {"<sos>", "<eos>", "<sow>", "<eow>", "<space>", "<sil>"}:
            total += 1
            if p == t:
                matches += 1
    if total == 0:
        return 0.0
    return round((matches / total) * 100, 2)

# === Run Transformer Prediction ===
def run_transformer_prediction(video_name, base_path, update_progress=None):
    try:
        if video_name.endswith(".mp4"):
            video_name = video_name[:-4]

        video_path = os.path.join(base_path, f"{video_name}.mp4")
        viseme_tensor_path = os.path.join(base_path, f"{video_name}_visemes.pt")

        if not os.path.exists(viseme_tensor_path):
            return {"status": "error", "error": f"Viseme tensor not found: {viseme_tensor_path}"}

        if update_progress: update_progress(10, 'Loading ground truth visemes...')
        true_tensor = torch.load(viseme_tensor_path)
        true_tokens = [IDX_TO_TOKEN[idx.item()] for idx in true_tensor]

        if update_progress: update_progress(30, 'Preprocessing video...')
        video_tensor = video_to_preprocessed_tensor(video_path)
        if video_tensor is None:
            return {"status": "error", "error": "Failed to preprocess video"}
        video_tensor = video_tensor.unsqueeze(0).to(device)

        if update_progress: update_progress(50, 'Loading transformer model...')
        model = LipReadingModel().to(device)
        checkpoint = torch.load(TRANSFORMER_MODEL_PATH, map_location=device)
        model.load_state_dict(checkpoint["model_state_dict"])
        model.eval()

        if update_progress: update_progress(70, 'Running prediction...')
        with torch.no_grad():
            logits = model(video_tensor, true_tensor.unsqueeze(0).to(device)[:, :-1])
            pred_ids = logits.argmax(dim=-1).cpu().numpy()[0]

        pred_tokens = ["<sos>"] + [IDX_TO_TOKEN[i] for i in pred_ids]

        viseme_match_percent = calculate_viseme_match(pred_tokens, true_tokens)
        boundary_match_percent = calculate_boundary_match(pred_tokens, true_tokens)

        if update_progress: update_progress(100, 'Prediction complete!')

        return {
            "status": "success",
            "pred_tokens": pred_tokens,
            "true_tokens": true_tokens,
            "viseme_match_percent": viseme_match_percent,
            "boundary_match_percent": boundary_match_percent
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}
