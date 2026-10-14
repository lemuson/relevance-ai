import os
import torch
import logging
import numpy as np

from huggingface_hub import hf_hub_download

from AI.freshness_model import FreshnessModel

HF_REPO_ID = os.getenv("HF_REPO_ID", "IlyaZaycev/relevance-news")
HF_FILENAME = os.getenv("HF_FILENAME", "freshness_model_cpu.pth")


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
            model_path = os.getenv("MODEL_PATH")
            if not model_path:
                local_path = os.path.join(
                    os.path.dirname(__file__),
                    "models",
                    "freshness_model_cpu.pth"
                )
                if os.path.exists(local_path):
                    model_path = local_path
                else:
                    logger.info("Локальный файл модели не найден. Скачивание с Hugging Face (%s)...", HF_REPO_ID)
                    model_path = hf_hub_download(repo_id=HF_REPO_ID, filename=HF_FILENAME)

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Модель не найдена: {model_path}")

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        model = FreshnessModel()
        state_dict = torch.load(model_path, map_location=device)
        model.load_state_dict(state_dict)
        model.to(device)
        model.eval()

        load_model.cache["model"] = model
        logger.info("FreshnessModel успешно загружена из: %s", model_path)

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
