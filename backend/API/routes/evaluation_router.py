import json
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from API.services.evaluation_service import process_evaluation

router = APIRouter()


@router.post("/relevance-ai/api/evaluation")
async def post_evaluation(request: Request):
    try:
        data = await request.json()
    except json.JSONDecodeError:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": "Некорректный JSON"}
        )

    result = process_evaluation(data)
    return JSONResponse(content=result)