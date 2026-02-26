import os
import pandas as pd
import asyncio
import logging

from backend.services.deterministic_engine import DeterministicEngine
from backend.services.visualisation_engine import VisualizationEngine
from backend.services.llm_engine import LLMEngine
from backend.core.exceptions import AppException

logger = logging.getLogger(__name__)


class TitanicAgentService:

    def __init__(self):

        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        DATA_PATH = os.path.join(BASE_DIR, "data", "titanic.csv")

        self.df = pd.read_csv(DATA_PATH)

        self.det_engine = DeterministicEngine(self.df)
        self.vis_engine = VisualizationEngine(self.df)
        self.llm_engine = LLMEngine(self.df)

    # --------------------------------------------------
    # 🔥 Invalid Query Guard (ADD THIS PROPERLY HERE)
    # --------------------------------------------------
    def _is_invalid_query(self, question: str) -> bool:

        q = question.strip()

        # Too short
        if len(q) < 4:
            return True

        # Single random word (e.g., asdsafadsf)
        if len(q.split()) == 1 and q.isalpha():
            return True

        # Must contain at least one dataset-related keyword
        keywords = [
            "passenger", "class", "fare", "age",
            "survived", "embarked", "sex", "titanic"
        ]

        if not any(k in q.lower() for k in keywords):
            if len(q.split()) <= 2:
                return True

        return False

    # --------------------------------------------------
    # MAIN ROUTER
    # --------------------------------------------------
    async def run(self, question: str):

        question = question.strip()

        logger.info("routing_start", extra={"query": question})

        try:

            # 🔥 0️⃣ Invalid Query Check (BEFORE everything)
            if self._is_invalid_query(question):
                logger.info("invalid_query_blocked", extra={"query": question})

                return {
                    "answer": "Please ask a valid question related to the Titanic dataset.",
                    "chart": None,
                    "tokens_input": 0,
                    "tokens_output": 0,
                    "hallucination_detected": False,
                }

            # 1️⃣ Deterministic
            simple = self.det_engine.handle(question)

            if simple:
                logger.info("deterministic_hit", extra={"query": question})

                return {
                    "answer": simple,
                    "chart": None,
                    "tokens_input": 0,
                    "tokens_output": 0,
                    "hallucination_detected": False,
                }

            # 2️⃣ Visualization
            if self.vis_engine.is_visual_request(question):

                logger.info("visualization_hit", extra={"query": question})

                answer, chart = self.vis_engine.generate(question)

                return {
                    "answer": answer,
                    "chart": chart,
                    "tokens_input": 0,
                    "tokens_output": 0,
                    "hallucination_detected": False,
                }

            # 3️⃣ LLM fallback
            logger.info("llm_routing", extra={"query": question})

            answer = await self.llm_engine.answer(question)

            return {
                "answer": answer,
                "chart": None,
                "tokens_input": 0,
                "tokens_output": 0,
                "hallucination_detected": False,
            }

        except asyncio.TimeoutError:

            logger.error("llm_timeout", extra={"query": question})

            raise AppException("Request timeout.", 504)

        except Exception:

            logger.exception("agent_failure", extra={"query": question})

            raise AppException("Failed to process request", 500)