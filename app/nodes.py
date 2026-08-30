from utils.fetch_transcript import fetch_transcript
from app.quiz_generator import generate_quiz
from app.state import QuizState

def fetch_transcript_node(state: QuizState) -> QuizState:
    try:
        state["transcript"] = fetch_transcript(state["video_id"])
        state["error"] = None
    except ValueError as e:
        state["transcript"] = None
        state["error"] = str(e)
    return state

def generate_quiz_node(state: QuizState) -> QuizState:
    try:
        state["quiz"] = generate_quiz(state["transcript"])
        state["error"] = None
    except (ValueError, Exception) as e:
        state["quiz"] = None
        state["error"] = str(e)
    return state