from typing import TypedDict, Optional

class QuizState(TypedDict):
    video_id: str
    transcript: Optional[str]
    quiz: Optional[list]
    error: Optional[str]