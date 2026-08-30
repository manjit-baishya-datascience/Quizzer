from youtube_transcript_api import YouTubeTranscriptApi

ytt_api = YouTubeTranscriptApi()

def fetch_transcript(video_id):
    try:
        transcript = ytt_api.fetch(video_id)
        return transcript
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None

video_id = "4TsJ7t7IBiw"
transcript = fetch_transcript(video_id)

if transcript:
    print("Transcript fetched successfully!")
else:
    print("Transcript fetching failed!")