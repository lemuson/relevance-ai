import torch
import torch.nn as nn
import numpy as np
from transformers import AutoModel, AutoTokenizer

class FreshnessModel(nn.Module):
    def __init__(self, model_name = "cointegrated/rubert-tiny2"):
        super().__init__()
        self.encoder = AutoModel.from_pretrained(model_name)
        hidden_size = self.encoder.config.hidden_size
        self.regressor = nn.Linear(hidden_size, 1)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.MAX_LEN = 128
        self.classes_ = np.array(['устаревшие', 'свежие'])

    def forward(self, input_ids, attention_mask):
        out = self.encoder(input_ids = input_ids, attention_mask = attention_mask)
        cls_vector = out.last_hidden_state[:, 0, :]
        return self.regressor(cls_vector).squeeze(-1)

    def predict(self, texts):
        if isinstance(texts, str):
            texts = [texts]
        predictions = []
        self.eval()
        with torch.no_grad():
            for text in texts:
                enc = self.tokenizer(text, truncation = True, max_length = self.MAX_LEN, padding = "max_length", return_tensors = "pt")
                score = self(enc["input_ids"], enc["attention_mask"]).item()
                predictions.append("свежие" if score > 0.5 else "устаревшие")
        return np.array(predictions)

    def predict_proba(self, texts):
        if isinstance(texts, str):
            texts = [texts]
        probabilities = []
        self.eval()
        with torch.no_grad():
            for text in texts:
                enc = self.tokenizer(text, truncation = True, max_length = self.MAX_LEN, padding = "max_length", return_tensors = "pt")
                raw_score = self(enc["input_ids"], enc["attention_mask"]).item()
                prob_fresh = 1 / (1 + np.exp(-raw_score))
                prob_old = 1 - prob_fresh
                probabilities.append([prob_old, prob_fresh])
        return np.array(probabilities)