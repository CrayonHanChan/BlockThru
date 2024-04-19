import gradio as gr

def play_video():
    return "final_video.mp4"

css = """
video {
    width: 100% !important;
    height: auto !important;
}
"""

app = gr.Interface(
    fn=play_video,
    inputs=[],
    outputs=gr.components.Video(label="Playback"),
    title="Obstacles Detection Demo",
    css=css
)

if __name__ == "__main__":
    app.launch()