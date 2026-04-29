import re
from typing import Dict, Any

from youtube_transcript_api import YouTubeTranscriptApi

def extract_youtube_content(url: str) -> Dict[str, Any]:
    """Return transcript data and combined text for a YouTube URL."""
    print(f"Processing YouTube URL: {url}")
    
    try:
        # Extract Video ID from URL as this API takes in Video ID 
        video_id_match = re.search(r'(?:v=|youtu\.be/|embed/|v/|shorts/)([^&\n?#]+)', url)
        if not video_id_match:
            raise ValueError("Could not extract video ID from URL")
        
        video_id = video_id_match.group(1)
        print(f"Extracted video ID: {video_id}")

        # Init api and fetch transcript
        ytt_api = YouTubeTranscriptApi()
        fetched_transcript = ytt_api.fetch(video_id)

        raw_data = fetched_transcript.to_raw_data()

        # Create a simple JSON with text, timestamp and metadata
        transcript_segments = []
        text_segments = []

        for snippet in raw_data:
            segment = {
                "text": snippet["text"],
                "start_time": snippet["start"],
                "duration": snippet["duration"],
                "end_time": snippet["start"] + snippet["duration"],
            }
            transcript_segments.append(segment)
            text_segments.append(snippet["text"])

        combined_text = " ".join(text_segments)

        result = {
            "platform": "youtube",
            "url": url,
            "text": combined_text,
            "transcript": transcript_segments,
            "status": "success",
        }

        print("YouTube content extracted successfully")
        return result
        
    except Exception as e:
        error_data = {
            "platform": "youtube",
            "url": url,
            "status": "error",
            "error": str(e),
        }
        print(f"Error extracting YouTube content: {e}")
        return error_data

