from torchvision.models import resnet18, ResNet18_Weights
import torch.nn as nn

def get_resnet18_model():
    # Load the pretrained model FIRST
    weights = ResNet18_Weights.DEFAULT
    model = resnet18(weights=weights)
    
    # Then modify input layer and output layer
    model.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
    model.fc = nn.Identity()
    
    return model
