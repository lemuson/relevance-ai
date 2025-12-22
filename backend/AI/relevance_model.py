import os
import torch
import logging
import numpy as np

from AI.freshness_model import FreshnessModel


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


def load_model(model_path=None) -> FreshnessModel:
    if not hasattr(load_model, "cache"):
        load_model.cache = {}

    if "model" not in load_model.cache:
        if model_path is None:
            model_path = os.path.join(
                os.path.dirname(__file__),
                "models",
                "freshness_model_cpu.pth"
            )

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Модель не найдена: {model_path}")

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        model = FreshnessModel()
        state_dict = torch.load(model_path, map_location=device)
        model.load_state_dict(state_dict)
        model.to(device)
        model.eval()

        load_model.cache["model"] = model
        logger.info("FreshnessModel загружена")

    return load_model.cache["model"]


def sigmoid(x: float) -> float:
    return 1 / (1 + np.exp(-x))


def news_analysis(text: str) -> dict:
    model = load_model()

    score = model.predict_raw(text)
    status = "свежие" if score > 0.5 else "устаревшие"

    prob = sigmoid(score)
    confidence = prob if status == "свежие" else (1 - prob)

    return {
        "status": status,
        "score": score,
        "confidence": confidence
    }
