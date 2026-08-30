# quiz_generator.py
import json
from utils.call_llm import llm_call

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
    return raw

def generate_quiz(transcript, model="deepseek-ai/deepseek-v4-pro-0813"):
    prompt = QUIZ_PROMPT_TEMPLATE.format(transcript=transcript)

    raw_output = llm_call(prompt, model=model, temperature=1, thinking=False)
    cleaned = _strip_json_fences(raw_output)

    quiz_data = json.loads(cleaned)
    return quiz_data