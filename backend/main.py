from fastapi import FastAPI
from backend.core.logging_config import setup_logging
from backend.services.agent_service import TitanicAgentService
from backend.schemas.chat import ChatRequest, ChatResponse
from backend.core.exceptions import AppException
from backend.core.exceptions_handler import (
    app_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)

from fastapi.exceptions import RequestValidationError
import logging
import uuid
import time


# Setup logging FIRST
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="Titanic AI Backend", version="1.0")

agent_service = TitanicAgentService()


# ------------------------
# Register Exception Handlers
# ------------------------

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


# ------------------------
# Chat Endpoint
# ------------------------

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):

    request_id = str(uuid.uuid4())[:8]
    start_time = time.time()

    logger.info(
        "chat_received",
        extra={
            "request_id": request_id,
            "query": request.question,
        },
    )

    result = await agent_service.run(request.question)

    latency = round(time.time() - start_time, 3)
    is_visual = result["chart"] is not None

    logger.info(
        "chat_success",
        extra={
            "request_id": request_id,
            "query": request.question,
            "latency": latency,
            "visualization": is_visual,
            "tokens_input": result.get("tokens_input", 0),
            "tokens_output": result.get("tokens_output", 0),
            "hallucination_detected": result.get("hallucination_detected", False),
        },
    )

    return ChatResponse(
        answer=result["answer"],
        chart=result["chart"],
    )


# ------------------------
# Health Endpoint
# ------------------------

@app.get("/health")
def health():
    return {"status": "ok"}