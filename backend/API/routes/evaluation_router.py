from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
import json

from API.services.evaluation_service import process_evaluation

router = APIRouter()

@router.get("/relevance-ai/evaluation", response_class = HTMLResponse)
async def get_evaluation():
    html_content = """
    <html>
        <head><title>Evaluation Page</title></head>
        <body>
            <h1>Relevance AI Evaluation</h1>
            <form id="evalForm">
                <input type="text" id="title" placeholder="Введите title"/>
                <input type="text" id="text" placeholder="Введите text"/>
                <button type="submit">Отправить</button>
            </form>
            <div id="result"></div>

            <script>
            document.getElementById("evalForm").addEventListener("submit", async function(e) {
                e.preventDefault();

                const title = document.getElementById("title").value;
                const text = document.getElementById("text").value;

                const response = await fetch("/relevance-ai/api/evaluation", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ title: title, text: text })
                });

                const result = await response.json();
                document.getElementById("result").innerText = JSON.stringify(result);
            });
            </script>
        </body>
    </html>
    """
    return HTMLResponse(content = html_content)


@router.post("/relevance-ai/api/evaluation")
async def post_evaluation(request: Request):
    try:
        data = await request.json()

    except json.JSONDecodeError:
        return JSONResponse(
            status_code = 400,
            content = {"status": "error", "message": "Некорректный JSON"}
        )

    result = process_evaluation(data)
    return JSONResponse(content = result)