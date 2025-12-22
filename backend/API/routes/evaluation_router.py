from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
import json

# Импорт твоего сервиса (оставляем как есть)
from API.services.evaluation_service import process_evaluation

router = APIRouter()


@router.get("/relevance-ai/evaluation", response_class=HTMLResponse)
async def get_evaluation():
    html_content = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Relevance AI Evaluation</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
        <style>
            :root {
                --primary: #4F46E5;
                --primary-hover: #4338ca;
                --bg-color: #F3F4F6;
                --card-bg: #FFFFFF;
                --text-main: #1F2937;
                --text-muted: #6B7280;
                --success: #10B981;
                --error: #EF4444;
            }

            * { box-sizing: border-box; margin: 0; padding: 0; }

            body {
                font-family: 'Inter', sans-serif;
                background-color: var(--bg-color);
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                color: var(--text-main);
            }

            .container {
                background: var(--card-bg);
                padding: 2.5rem;
                border-radius: 16px;
                box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
                width: 100%;
                max-width: 420px;
                text-align: center;
            }

            h1 {
                font-size: 1.5rem;
                margin-bottom: 2rem;
                color: var(--text-main);
                font-weight: 600;
            }

            /* Floating Label Styles */
            .input-group {
                position: relative;
                margin-bottom: 1.5rem;
                text-align: left;
            }

            .input-field {
                width: 100%;
                padding: 12px 16px;
                font-size: 1rem;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                outline: none;
                transition: border-color 0.2s, box-shadow 0.2s;
                background: transparent;
            }

            .input-field:focus {
                border-color: var(--primary);
                box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
            }

            /* Placeholder logic */
            .input-label {
                position: absolute;
                left: 14px;
                top: 14px;
                color: var(--text-muted);
                pointer-events: none;
                transition: 0.2s ease all;
                background-color: var(--card-bg);
                padding: 0 4px;
            }

            .input-field:focus ~ .input-label,
            .input-field:not(:placeholder-shown) ~ .input-label {
                top: -9px;
                left: 10px;
                font-size: 0.75rem;
                color: var(--primary);
                font-weight: 600;
            }

            button {
                width: 100%;
                padding: 12px;
                background-color: var(--primary);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 1rem;
                font-weight: 600;
                cursor: pointer;
                transition: background-color 0.2s;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 48px;
            }

            button:hover {
                background-color: var(--primary-hover);
            }

            button:disabled {
                background-color: #9CA3AF;
                cursor: not-allowed;
            }

            /* Loader */
            .loader {
                border: 3px solid rgba(255, 255, 255, 0.3);
                border-radius: 50%;
                border-top: 3px solid #fff;
                width: 20px;
                height: 20px;
                animation: spin 1s linear infinite;
                display: none;
            }

            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }

            /* Results Section */
            #result-container {
                margin-top: 2rem;
                opacity: 0;
                transform: translateY(10px);
                transition: opacity 0.3s, transform 0.3s;
                display: none; /* Hidden initially */
            }

            #result-container.visible {
                opacity: 1;
                transform: translateY(0);
                display: block;
            }

            .status-box {
                padding: 1rem;
                border-radius: 8px;
                font-weight: 700;
                font-size: 1.1rem;
                margin-bottom: 0.5rem;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }

            .status-box.fresh {
                background-color: #D1FAE5;
                color: #065F46;
                border: 1px solid #34D399;
            }

            .status-box.outdated {
                background-color: #FEE2E2;
                color: #991B1B;
                border: 1px solid #F87171;
            }

            .score-text {
                font-size: 0.9rem;
                color: var(--text-muted);
                font-weight: 500;
            }

            .score-value {
                font-weight: 700;
                color: var(--text-main);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Relevance AI</h1>
            <form id="evalForm">
                <div class="input-group">
                    <input type="text" id="title" class="input-field" placeholder=" " required />
                    <label for="title" class="input-label">Заголовок</label>
                </div>

                <div class="input-group">
                    <input type="text" id="text" class="input-field" placeholder=" " required />
                    <label for="text" class="input-label">Текст</label>
                </div>

                <button type="submit" id="submitBtn">
                    <span class="btn-text">Отправить</span>
                    <div class="loader"></div>
                </button>
            </form>

            <div id="result-container">
                <div id="statusBox" class="status-box"></div>
                <div class="score-text">
                    Актуальность: <span id="scoreValue" class="score-value">0%</span>
                </div>
            </div>
        </div>

        <script>
        document.getElementById("evalForm").addEventListener("submit", async function(e) {
            e.preventDefault();

            const titleInput = document.getElementById("title");
            const textInput = document.getElementById("text");
            const btn = document.getElementById("submitBtn");
            const btnText = btn.querySelector(".btn-text");
            const loader = btn.querySelector(".loader");
            const resultContainer = document.getElementById("result-container");
            const statusBox = document.getElementById("statusBox");
            const scoreValue = document.getElementById("scoreValue");
            if (!titleInput.value || !textInput.value) {
                alert("Пожалуйста, заполните оба поля.");
                return;
            }

            // UI Loading State
            btn.disabled = true;
            btnText.style.display = "none";
            loader.style.display = "block";
            resultContainer.classList.remove("visible");

            try {
                const response = await fetch("/relevance-ai/api/evaluation", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ title: titleInput.value, text: textInput.value })
                });

                const result = await response.json();

                // UI Reset
                btn.disabled = false;
                btnText.style.display = "block";
                loader.style.display = "none";
                const freshnessResult = result.results && result.results.freshness_model;

                if (!freshnessResult) {
                    console.error("Не найден результат freshness_model в ответе API:", result);
                    alert("Не удалось получить корректный результат от сервера.");
                    return;
                }

                const status = freshnessResult.status;
                const score = freshnessResult.score;
                const isRelevant = status === "свежие"; 

                if (isRelevant) {
                    statusBox.textContent = "АКТУАЛЬНО";
                    statusBox.className = "status-box fresh";
                } else {
                    statusBox.textContent = "НЕ АКТУАЛЬНО";
                    statusBox.className = "status-box outdated";
                }

                scoreValue.textContent = Math.round(score * 100) + "%";
                resultContainer.classList.add("visible");

            } catch (error) {
                console.error("Error:", error);
                btn.disabled = false;
                btnText.style.display = "block";
                loader.style.display = "none";
                alert("Произошла ошибка при обработке запроса.");
            }
        });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@router.post("/relevance-ai/api/evaluation")
async def post_evaluation(request: Request):
    try:
        data = await request.json()
    except json.JSONDecodeError:
        return JSONResponse(
            status_code = 400,
            content = { "status": "error", "message": "Некорректный JSON" }
        )

    result = process_evaluation(data)
    return JSONResponse(content = result)