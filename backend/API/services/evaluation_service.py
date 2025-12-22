import logging
from AI.relevance_model import news_analysis


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


def process_evaluation(data: dict) -> dict:
    title = data.get("title")
    text = data.get("text")

    if not isinstance(title, str) or not isinstance(text, str):
        return {
            "status": "error",
            "message": "Поля 'title' и 'text' должны быть строками",
            "received_data": data
        }

    try:
        analysis = news_analysis(title + " " + text)

        return {
            "summary": {
                "title": title,
                "text": text
            },
            "results": {
                "freshness_model": {
                    "name": "freshness_model",
                    "status": analysis["status"],
                    "score": round(analysis["score"], 4),
                    "confidence": round(analysis["confidence"], 4)
                }
            }
        }

    except Exception as exc:
        logger.exception("Ошибка анализа")
        return {
            "status": "error",
            "message": str(exc),
            "received_data": data
        }
