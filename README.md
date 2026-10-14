# RelevanceAI

RelevanceAI - веб-приложение на базе FastAPI и PyTorch, предназначенное для анализа актуальности новостных материалов. Система определяет, является ли текст «актуальным» или «устаревшим», используя обученную нейросетевую модель. Для обучения была использована предобученная RuBERT-модель.

## Использование
Модель автоматически загружается из репозитория Hugging Face ([IlyaZaycev/relevance-news](https://huggingface.co/IlyaZaycev/relevance-news)) при первом запуске (и сохраняется в локальный кэш).

Для запуска достаточно просто клонировать репозиторий:
```BASH
git clone https://github.com/lemuson/RelevanceAI.git
cd RelevanceAI
```

### Запуск через Docker Compose
```BASH
docker compose up -d --build
```

### Запуск вручную

<details>
<summary>Backend</summary>

```BASH
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
cd ..
```

</details>

<details>
<summary>Frontend</summary>

```BASH
cd frontend
npm install
npm run dev
cd ..
```
</details>


## API документация
Запрос POST /relevance-ai/evaluation должен содержать тело:
```JSON
{
  "title": "Заголовок",
  "text": "Текст"
}
```

Запрос возвращает JSON-ответ об актуальности текста в виде:
```JSON
{
  "summary": {
    "title": "Заголовок",
    "text": "Текст"
  },
  "results": {
    "freshness_model": {
      "name": "freshness_model",
      "status": "свежие/устаревшие",
      "score": 0.0,
      "confidence": 0.0
    }
  }
}
```
## Примеры работы
<table style="width: 100%; border-collapse: collapse; border: none;">
  <tr>
    <td align="center" style="border: none; width: 50%;">
      <p><b>Анализ актуальной новости</b></p>
      <img src="https://github.com/user-attachments/assets/39e7a59d-3233-41a9-871a-d0096db03746" width="100%" alt="Пример 1" />
    </td>
  <td align="center" style="border: none; width: 50%;">
    <p><b>Анализ устаревшей новости</b></p>
    <img src="https://github.com/user-attachments/assets/795a6665-c30d-4334-8dde-0b2328278c60" width="100%" alt="Пример 2" />
  </td>
  </tr>
</table>
