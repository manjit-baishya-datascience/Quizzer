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

load_dotenv()


def call_llm(prompt, model, temperature=1, thinking=False):
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=os.environ.get("NVIDIA_API_KEY"),
        timeout=30.0
    )

    try:
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
        return completion.choices[0].message.content

    except NotFoundError:
        raise ValueError(f"Model '{model}' not found — check the model ID is correct and still live on the catalog")

    except AuthenticationError:
        raise ValueError("Invalid or missing NVIDIA_API_KEY — check your .env file")

    except RateLimitError:
        raise ValueError(f"Rate limited / queue congested for model '{model}' — try again shortly or switch provider")

    except APITimeoutError:
        raise ValueError(f"Request to model '{model}' timed out after 30s")

    except APIConnectionError:
        raise ValueError("Could not connect to NVIDIA API — check your internet connection")

    except LengthFinishReasonError:
        raise ValueError(f"Response from model '{model}' was truncated — increase max_tokens or shorten the prompt")

    except ContentFilterFinishReasonError:
        raise ValueError(f"Response from model '{model}' was blocked by a content filter")

    except APIStatusError as e:
        raise ValueError(f"API error ({e.status_code}) calling model '{model}': {e.message}")