from app.graph import build_graph

app = build_graph()

if __name__ == "__main__":
    video_id = "yWgHx0HE8m8"
    result = app.invoke({"video_id": video_id, "transcript": None, "quiz": None, "error": None})

    if result["error"]:
        print(f"Failed: {result['error']}")
    else:
        print(result["quiz"])