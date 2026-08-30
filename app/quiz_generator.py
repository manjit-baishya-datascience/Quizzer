import os
import json
from datetime import datetime
from utils.call_llm import call_llm
from utils.logger import get_logger

logger = get_logger(__name__)

ARTIFACTS_DIR = "artifacts"
os.makedirs(ARTIFACTS_DIR, exist_ok=True)

QUIZ_PROMPT_TEMPLATE = """Here is the transcript of a YouTube video:

{transcript}

Generate exactly 10 multiple choice questions based on this transcript.

Return ONLY valid JSON, with no extra text, no markdown code fences, and no commentary.
The JSON must be a list of exactly 10 objects, each with this exact structure:

{{
  "question": "the question text",
  "options": ["option A", "option B", "option C", "option D"],
  "correct_answer_index": 0
}}

Rules:
- "options" must always have exactly 4 strings.
- "correct_answer_index" must be an integer from 0 to 3, pointing to the correct option in the "options" list.
- Do not include letters like "A)" or "B)" inside the option text itself.
- Base every question strictly on the transcript content — do not invent facts not present in it.
"""


def _strip_json_fences(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.startswith("json"):
            raw = raw[4:].strip()
    return raw.strip()


def _parse_quiz_json(cleaned: str):
    """
    Parse the model's JSON output. Handles the common failure mode where
    the model returns comma-separated objects without the enclosing
    array brackets, e.g. `{...}, {...}, {...}` instead of `[{...}, {...}]`.
    """
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Retry assuming missing outer array brackets
        if not cleaned.startswith("["):
            wrapped = f"[{cleaned}]"
            try:
                return json.loads(wrapped)
            except json.JSONDecodeError as e:
                raise ValueError(f"Could not parse quiz JSON even after wrapping in brackets: {e}")
        raise

def generate_quiz(transcript, model="deepseek-ai/deepseek-v4-pro-0813"):
    logger.info("Quizzer started")
    prompt = QUIZ_PROMPT_TEMPLATE.format(transcript=transcript)

    raw_output = call_llm(prompt, model=model, temperature=1, thinking=False)

    if raw_output is None:
        raise ValueError("Empty response was received — LLM returned no content")

    logger.info("Questions created")

    cleaned = _strip_json_fences(raw_output)
    quiz_data = _parse_quiz_json(cleaned)
    logger.info("Questions successfully parsed to JSON")
    return quiz_data