# utils/fetch_transcript.py
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
from utils.logger import get_logger

logger = get_logger(__name__)
ytt_api = YouTubeTranscriptApi()

def fetch_transcript(video_id):
    try:
        transcript = ytt_api.fetch(video_id)
        logger.info(f"Transcript fetched successfully for video_id={video_id}")
        return transcript

    except TranscriptsDisabled:
        logger.warning(f"Transcripts disabled for video_id={video_id}")
        raise ValueError(f"Transcripts disabled for video_id={video_id}")

    except NoTranscriptFound:
        logger.warning(f"No transcript found for video_id={video_id}")
        raise ValueError(f"No transcript found for video_id={video_id}")

    except VideoUnavailable:
        logger.error(f"Video unavailable: video_id={video_id}")
        raise ValueError(f"Video unavailable: video_id={video_id}")

    except Exception as e:
        logger.error(f"Unexpected error fetching transcript for video_id={video_id}: {e}")
        raise ValueError(f"Unexpected error fetching transcript for video_id={video_id}: {e}")