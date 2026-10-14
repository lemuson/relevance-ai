import os
import logging
from huggingface_hub import hf_hub_download
from transformers import AutoModel, AutoTokenizer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

HF_REPO_ID = os.getenv("HF_REPO_ID", "IlyaZaycev/relevance-news")
HF_FILENAME = os.getenv("HF_FILENAME", "freshness_model_cpu.pth")
BASE_MODEL_NAME = "cointegrated/rubert-tiny2"


def init_model():
    logger.info("Загрузка базовой модели и токенизатора: %s", BASE_MODEL_NAME)
    AutoModel.from_pretrained(BASE_MODEL_NAME)
    AutoTokenizer.from_pretrained(BASE_MODEL_NAME)

    logger.info("Загрузка обученных весов с Hugging Face: %s/%s", HF_REPO_ID, HF_FILENAME)
    weight_path = hf_hub_download(repo_id=HF_REPO_ID, filename=HF_FILENAME)
    logger.info("Модель успешно инициализирована и сохранена в кэш: %s", weight_path)


if __name__ == "__main__":
    init_model()
