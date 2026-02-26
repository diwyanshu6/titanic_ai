import asyncio
import logging

from langchain_groq import ChatGroq
from langchain_experimental.agents import create_pandas_dataframe_agent
from backend.core.config import GROQ_API_KEY, MODEL_NAME

logger = logging.getLogger(__name__)


class LLMEngine:

    def __init__(self, df):

        self.llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name=MODEL_NAME,
            temperature=0,
        )

        self.agent = create_pandas_dataframe_agent(
            self.llm,
            df,
            verbose=False,
            allow_dangerous_code=True,
            max_iterations=20, 
        )

    async def answer(self, question: str):

        logger.info("llm_start", extra={"query": question})

        try:
            result = await self.agent.ainvoke(question)

            logger.info("llm_finish", extra={"query": question})

            return result.get("output", "").strip()

        except Exception as e:

            logger.exception(
                "llm_failed",
                extra={"query": question}
            )

            raise