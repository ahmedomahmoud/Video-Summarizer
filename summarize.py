from openai import OpenAI
import srt
import json
from dotenv import load_dotenv
import os
from moviepy.editor import VideoFileClip

def clip_video(input_path, output_dir, highlights):
    video = VideoFileClip(input_path)
    output_paths = []
    for i, h in enumerate(highlights["highlights"]):
        start = h["start"]
        end = h["end"]
        summary = h["summary"]

        clip = video.subclip(start, end)

        output_path = os.path.join(output_dir, f"clip_{i+1}.mp4")
        print(f"Saving: {output_path} | {summary}")

        clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
        output_paths.append(output_path)
    video.close()
    return output_paths
# Load API key from .env

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Step 1: Parse the SRT into segments
def srt_to_text_segments(srt_path):
    with open(srt_path, "r", encoding="utf-8") as f:
        srt_content = f.read()
    subs = list(srt.parse(srt_content))
    segments = [
        {
            "start": round(sub.start.total_seconds()),
            "end": round(sub.end.total_seconds()),
            "text": sub.content.replace("\n", " ")
        }
        for sub in subs
    ]
    return segments  # You may limit if needed for large files

# Step 2: Define structured output (function calling)
tools = [
    {
        "type": "function",
        "function": {
            "name": "extract_highlights",
            "description": "Extract key video highlights from a transcript.",
            "parameters": {
                "type": "object",
                "properties": {
                    "highlights": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "start": {
                                    "type": "number",
                                    "description": "Start time of the clip in seconds"
                                },
                                "end": {
                                    "type": "number",
                                    "description": "End time of the clip in seconds"
                                },
                                "summary": {
                                    "type": "string",
                                    "description": "Short description of the highlight"
                                }
                            },
                            "required": ["start", "end", "summary"]
                        }
                    }
                },
                "required": ["highlights"]
            }
        }
    }
]

# Step 3: Main summarization function using function calling
def summarize_srt(srt_path, num_highlights=1):
    segments = srt_to_text_segments(srt_path)
    print(f"Extracted {len(segments)} segments from SRT.")
    print(f"first segment: {segments[0] if segments else 'No segments found'}")
    segment_text = json.dumps(segments, indent=2)

    response = client.chat.completions.create(
        model="gpt-4o",  # Use gpt-4o or gpt-3.5-turbo
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant that extracts key highlights from video transcripts. "
                    "You will receive a list of transcript segments and number of desired  highlights to return , you and must return structured highlights."
                    "Return results in the exact JSON format of the function schema."
                ),
                "role": "user",
                "content": (
                    f"You are given a list of transcript segments from a video. "
                    f"Extract {num_highlights} highlights (each less than 60 seconds). "
                    f"\n\nTranscript:\n{segment_text}"
                )
            }
        ],
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "extract_highlights"}}
    )

    # Access the structured function call output
    arguments = response.choices[0].message.tool_calls[0].function.arguments
    result = json.loads(arguments)
    return result

# Run and print result
# result = summarize_srt("/home/ahmed/transcription.srt", num_highlights=3)
# print(type(result))
# print()

# print(json.dumps(result, indent=2))


