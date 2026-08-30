from langgraph.graph import StateGraph, END
from app.state import QuizState
from app.nodes import fetch_transcript_node, generate_quiz_node

def route_after_transcript(state: QuizState) -> str:
    return "generate_quiz" if state["error"] is None else END

def build_graph():
    graph = StateGraph(QuizState)

    graph.add_node("fetch_transcript", fetch_transcript_node)
    graph.add_node("generate_quiz", generate_quiz_node)

    graph.set_entry_point("fetch_transcript")
    graph.add_conditional_edges("fetch_transcript", route_after_transcript, {
        "generate_quiz": "generate_quiz",
        END: END
    })
    graph.set_finish_point("generate_quiz")

    return graph.compile()