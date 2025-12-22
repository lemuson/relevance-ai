import torch
import torch.nn as nn
import numpy as np
from transformers import AutoModel, AutoTokenizer


class FreshnessModel(nn.Module):
    def __init__(self, model_name="cointegrated/rubert-tiny2"):
        super().__init__()

        self.encoder = AutoModel.from_pretrained(model_name)
        hidden_size = self.encoder.config.hidden_size

        self.regressor = nn.Linear(hidden_size, 1)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        self.MAX_LEN = 128
        self.classes_ = np.array(["устаревшие", "свежие"])

    def forward(self, input_ids, attention_mask):
        out = self.encoder(
            input_ids=input_ids,
            attention_mask=attention_mask
        )
        cls_vector = out.last_hidden_state[:, 0, :]
        return self.regressor(cls_vector).squeeze(-1)

    def predict_raw(self, text: str) -> float:
        enc = self.tokenizer(
            text,
            truncation=True,
            max_length=self.MAX_LEN,
            padding="max_length",
            return_tensors="pt"
        )

        self.eval()
        with torch.no_grad():
            score = self(
                enc["input_ids"],
                enc["attention_mask"]
            ).item()

        return float(score)

    def predict(self, text: str) -> str:
        score = self.predict_raw(text)
        return "свежие" if score > 0.5 else "устаревшие"