import logging

from AI.relevance_model import news_analysis

#========================ЛОГИ=========================#
logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s [%(levelname)s] %(message)s",
    datefmt = "%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)
#=====================================================#


def process_evaluation(data: dict) -> dict:
    title = data.get("title")
    text = data.get("text")

    if not isinstance(title, str) or not isinstance(text, str):
        return {
            "status": "error",
            "message": "Ожидались поля 'title' и 'text' строкового типа",
            "received_data": data
        }

    try:
        prediction, proba = news_analysis(title + text)

        result_json = {
            "summary": {
                "title": title,
                "text": text
            },
            "results": {
                "freshness_model": {
                    "name": "freshness_model",
                    "status": prediction,
                    "confidence": float(proba.max()),
                    "prob_fresh": float(proba[1]),
                    "prob_old": float(proba[0])
                }
            }
        }

        return result_json
    except Exception as exception:
        logger.error(exception)
        return {
            "status": "error",
            "message": str(exception),
            "received_data": data
        }