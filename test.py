from moviepy.editor import VideoFileClip
import os

from summarize import summarize_srt


def clip_video(input_path, output_dir, highlights):
    video = VideoFileClip(input_path)

    for i, h in enumerate(highlights["highlights"]):
        start = h["start"]
        end = h["end"]
        summary = h["summary"]

        clip = video.subclip(start, end)

        output_path = os.path.join(output_dir, f"clip_{i+1}.mp4")
        print(f"Saving: {output_path} | {summary}")

        clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

    video.close()

# result = summarize_srt("/home/ahmed/transcription.srt", num_highlights=2)
# clip_video("/home/ahmed/Videos/Camera/Why Do We Dream_.mp4" , "/home/ahmed/linkdev/ws5/clips" , result)
