from torchvision.models.video import r3d_18
import torch.nn as nn

def get_3dcnn_model():
    model = r3d_18(pretrained=False)
    model.fc = nn.Linear(model.fc.in_features, 128)  # Optional: adjust output size
    return model
