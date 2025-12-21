import logging
import os
import torch
from AI.freshness_model import FreshnessModel


logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s [%(levelname)s] %(message)s",
    datefmt = "%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


#============================МОДЕЛЬ==============================#
def load_model(model_path = None):
    if not hasattr(load_model, "cache"):
        load_model.cache = {}

    if "model" not in load_model.cache:
        if model_path is None:
            model_path = os.path.join(os.path.dirname(__file__), "models", "freshness_model_cpu.pth")
        if not os.path.exists(model_path):
            logger.error("No model found at {}".format(model_path))
            raise FileNotFoundError(f"Файл модели {model_path} не найден")

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = FreshnessModel()
        state_dict = torch.load(model_path, map_location = device)
        model.load_state_dict(state_dict)
        model.to(device)
        model.eval()

        load_model.cache["model"] = model

    return load_model.cache["model"]

def news_analysis(text: str):
    model = load_model()

    prediction = model.predict(text)[0]
    proba = model.predict_proba(text)[0]

    return prediction, proba
#=================================================================#





#========================ЛОКАЛЬНАЯ ПРОВЕРКА=======================#
### ВЫВОД ТАБЛИЦЫ РЕЗУЛЬТАТОВ
def print_analysis(result_json):
    if not result_json:
        print("Нет данных для отображения")
        return

    print(f"\nЗаголовок: {result_json['summary']['title']}")
    print(f"Текст: {result_json['summary']['text_preview']}")

    print("\nСВОДНАЯ ТАБЛИЦА:")

    columns = [
        ("Модель", "name"),
        ("Результат", "status"),
        ("Уверенность", "confidence"),
        ("Свежие", "prob_fresh"),
        ("Устаревшие", "prob_old"),
    ]

    results = result_json["results"]

    rows = []
    for name, r in results.items():
        rows.append({
            "name": name,
            "status": r["status"],
            "confidence": f"{r['confidence']:.3f}",
            "prob_fresh": f"{r['prob_fresh']:.3f}",
            "prob_old": f"{r['prob_old']:.3f}",
        })
    widths = {}
    for title, key in columns:
        max_data_width = max(
            len(str(row[key])) for row in rows
        ) if rows else 0
        widths[key] = max(len(title), max_data_width) + 2

    def line():
        return "+" + "+".join("-" * widths[key] for _, key in columns) + "+"

    def header():
        return "|" + "|".join(
            f"{title:^{widths[key]}}" for title, key in columns
        ) + "|"

    def row_line(row):
        return "|" + "|".join(
            f"{row[key]:<{widths[key]}}" for _, key in columns
        ) + "|"

    print(line())
    print(header())
    print(line())
    for row in rows:
        print(row_line(row))
    print(line())


### ЗАПУСК
def main():
    ### LOGS
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logger = logging.getLogger(__name__)

    logger.info("Тестирование модели FreshnessModel")

    test_data = [
        "В России введены новые правила для водителей в 2025 году",
        "Apple представила новый iPhone в прошлом месяце",
        "Старый закон 1999 года всё ещё действует"
    ]

    for idx, text in enumerate(test_data, 1):
        prediction, proba = news_analysis(text)
        result_json = {
            "summary": {
                "title": f"Тест {idx}",
                "text_preview": text[:200]
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
        print_analysis(result_json)

    while True:
        print("\n")
        title_news = input("Введите заголовок: ")
        text_news = input("Введите текст: ")

        if not title_news and not text_news:
            logger.info("Выход из программы")
            break

        full_text = f"{title_news}\n{text_news}"
        prediction, proba = news_analysis(full_text)
        result_json = {
            "summary": {
                "title": title_news,
                "text_preview": text_news[:200]
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
        print_analysis(result_json)

if __name__ == "__main__":
    main()
#==================================================================#