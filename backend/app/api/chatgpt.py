from tenacity import retry, stop_after_attempt, wait_exponential
from openai import RateLimitError, AsyncOpenAI
from fastapi import HTTPException
import logging

logger = logging.getLogger()


# ChatGPT interaction function
@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(5))
async def get_chatgpt_response(user_message: str) -> str:
    try:
        client = AsyncOpenAI()
        completion = await client.chat.completions.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": user_message}]
        )
        chatgpt_reply = completion.choices[0].message["content"].strip()
        return chatgpt_reply
    except RateLimitError:
        # Raising error to trigger retry
        logger.error("retrying...")
        raise
    except Exception as e:
        # Raise other errors to handle them in the route function
        logger.critical("another exception")
        raise HTTPException(status_code=500, detail=str(e))
