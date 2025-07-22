import gradio as gr
from videoprocessing import extract_audio , transcribe_and_save_srt, check_video_restrictions
import os
from summarize import summarize_srt , clip_video

def process_video(video_file, num_shorts):
    errors = check_video_restrictions(video_file)
    if errors:
        print(f"Video restrictions not met: {errors}")
        return []

    print(f"Processing video: {video_file} to generate {num_shorts} shorts.")
    audio_path = extract_audio(video_file)
    print(f"Extracted audio saved at: {audio_path}")

    srt_path = transcribe_and_save_srt(audio_path, output_srt_path="/home/ahmed/transcription.srt")
    print(f"Transcription saved as: {srt_path}")

    highlights = summarize_srt(srt_path, num_highlights=num_shorts)
    print(f"Generated highlights: {highlights}")

    clip_paths = clip_video(video_file, "/home/ahmed/linkdev/ws5/clips", highlights)
    print(f"Generated clip files: {clip_paths}")

    return  clip_paths

with gr.Blocks() as demo:
    gr.Markdown("# AI Video Shorts Generator\n**Max 12 minutes, 20 MB limit per upload**")
    gr.Markdown("""
    *Video Restrictions:*
    - Maximum duration: 12 minutes
    - Maximum file size: 20 MB
    """)
    with gr.Row():
            with gr.Column():
                video_input = gr.File(label="Upload Video", file_types=["video"],height=150)
            with gr.Column():
                num_shorts = gr.Slider(label="Number of Shorts", minimum=1, maximum=5, value=2, step=1)
                submit_btn = gr.Button("Generate Shorts")
    with gr.Row():
            output_gallery = gr.Gallery(label="Generated Shorts", show_label=True, elem_id="shorts-gallery")

    

    submit_btn.click(
        fn=process_video,
        inputs=[video_input, num_shorts],
        outputs=output_gallery
    )

if __name__ == "__main__":
    demo.launch()