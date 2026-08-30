import os
from openai import (
    OpenAI,
    NotFoundError,
    AuthenticationError,
    RateLimitError,
    APITimeoutError,
    APIConnectionError,
    LengthFinishReasonError,
    ContentFilterFinishReasonError,
    APIStatusError,
)
from dotenv import load_dotenv
from utils.logger import get_logger

logger = get_logger(__name__)
load_dotenv()

def call_llm(prompt, model, temperature=1, thinking=False):
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=os.environ.get("NVIDIA_API_KEY")
    )

    try:
        logger.info(f"LLM call started")
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            top_p=0.95,
            max_tokens=16384,
            seed=42,
            extra_body={"chat_template_kwargs": {"thinking": thinking}},
            stream=False
        )
        logger.info(f"LLM call completed")
        return completion.choices[0].message.content

    # simplified error message
    except NotFoundError:
        logger.error(f"Model '{model}' not found — check the model ID is correct and still live on the catalog")
        raise ValueError(f"Model '{model}' not found — check the model ID is correct and still live on the catalog")

    # simplified error message
    except AuthenticationError:
        logger.error("Invalid or missing NVIDIA_API_KEY — check your .env file")
        raise ValueError("Invalid or missing NVIDIA_API_KEY — check your .env file")
    # branches to a different provider if available
    except RateLimitError:
        logger.error(f"Rate limited / queue congested for model '{model}' — try again shortly or switch provider")
        raise ValueError(f"Rate limited / queue congested for model '{model}' — try again shortly or switch provider")

    # simplified error message
    except APIConnectionError:
        logger.error("Could not connect to NVIDIA API — check your internet connection")
        raise ValueError("Could not connect to NVIDIA API — check your internet connection")

    # retry with greater max token length
    except LengthFinishReasonError:
        logger.error(f"Response from model '{model}' was truncated — increase max_tokens or shorten the prompt")
        raise ValueError(f"Response from model '{model}' was truncated — increase max_tokens or shorten the prompt")

    # flags inappropriate content - could be a good feature ahead!
    except ContentFilterFinishReasonError:
        logger.error(f"Response from model '{model}' was blocked by a content filter")
        raise ValueError(f"Response from model '{model}' was blocked by a content filter")

    # pass everything else as is
    except APIStatusError as e:
        logger.error(f"API error ({e.status_code}) calling model '{model}': {e.message}")
        raise ValueError(f"API error ({e.status_code}) calling model '{model}': {e.message}")