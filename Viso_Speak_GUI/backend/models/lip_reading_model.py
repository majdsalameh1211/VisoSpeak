import torch
import torch.nn as nn

# === Constants (MATCH checkpoint) ===
FEATURE_DIM = 512
VOCAB_SIZE = 48
PAD_IDX = 0
MAX_FRAMES = 250

# === Visual Frontend: 3D CNN ===
class VisualFrontend3DCNN(nn.Module):
    def __init__(self, output_dim=FEATURE_DIM):
        super().__init__()
        self.conv1 = nn.Conv3d(1, 32, kernel_size=(3, 5, 5), stride=(1, 2, 2), padding=(1, 2, 2))
        self.conv2 = nn.Conv3d(32, 64, kernel_size=(3, 3, 3), stride=(1, 2, 2), padding=1)
        self.conv3 = nn.Conv3d(64, 128, kernel_size=(3, 3, 3), stride=(1, 2, 2), padding=1)
        self.conv4 = nn.Conv3d(128, 256, kernel_size=(3, 3, 3), stride=(1, 2, 2), padding=1)
        self.relu = nn.ReLU()
        self.pool = nn.AdaptiveAvgPool3d((MAX_FRAMES, 1, 1))
        self.fc = nn.Linear(256, output_dim)

    def forward(self, x):
        x = x.permute(0, 4, 1, 2, 3)  # (B, 1, T, H, W)
        x = self.relu(self.conv1(x))
        x = self.relu(self.conv2(x))
        x = self.relu(self.conv3(x))
        x = self.relu(self.conv4(x))
        x = self.pool(x)  # (B, 256, T, 1, 1)
        x = x.squeeze(-1).squeeze(-1).permute(0, 2, 1)  # (B, T, 256)
        return self.fc(x)  # (B, T, FEATURE_DIM)


# === Transformer Encoder ===
class TransformerEncoder(nn.Module):
    def __init__(self, input_dim=FEATURE_DIM, n_heads=8, num_layers=4, ff_dim=2048, dropout=0.5):
        super().__init__()
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=input_dim, nhead=n_heads, dim_feedforward=ff_dim, dropout=dropout, batch_first=True
        )
        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)

    def forward(self, x):
        return self.encoder(x)


# === Transformer Decoder ===
class VisemeTransformerDecoder(nn.Module):
    def __init__(self, vocab_size=VOCAB_SIZE, emb_dim=FEATURE_DIM, num_layers=4, n_heads=8, ff_dim=2048, dropout=0.4):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, emb_dim, padding_idx=PAD_IDX)
        decoder_layer = nn.TransformerDecoderLayer(
            d_model=emb_dim, nhead=n_heads, dim_feedforward=ff_dim, dropout=dropout, batch_first=True
        )
        self.decoder = nn.TransformerDecoder(decoder_layer, num_layers=num_layers)
        self.fc_out = nn.Linear(emb_dim, vocab_size)

    def forward(self, memory, tgt_tokens):
        tgt_emb = self.embedding(tgt_tokens)
        tgt_mask = nn.Transformer.generate_square_subsequent_mask(tgt_emb.size(1)).to(tgt_emb.device)
        output = self.decoder(tgt=tgt_emb, memory=memory, tgt_mask=tgt_mask)
        return self.fc_out(output)


# === Full Lip Reading Model ===
class LipReadingModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.visual = VisualFrontend3DCNN()
        self.encoder = TransformerEncoder()
        self.decoder = VisemeTransformerDecoder()

    def forward(self, video, viseme_input):
        features = self.visual(video)
        memory = self.encoder(features)
        logits = self.decoder(memory, viseme_input)
        return logits
