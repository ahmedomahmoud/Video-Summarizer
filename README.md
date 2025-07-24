# 🎬 Video-Summarizer: AI-Powered Video Shorts Generator

**Video-Summarizer** is a simple yet powerful AI tool that processes a video and automatically generates short highlight clips from key moments. Designed for creators and educators, it helps turn long content into shareable bite-sized videos with minimal effort.

---

## 🚀 Features

- 🧠 AI-powered summarization of video content
- 🔊 Extracts audio and transcribes it to subtitles (SRT)
- 🎯 Identifies highlights and crops them into short video clips
- 🎛️ Clean and simple **Gradio** interface
- ⚙️ Supports videos up to 12 minutes and 20 MB

---

## 🛠️ Tech Stack

- **Python**
- **Gradio** – for the web UI
- **MoviePy** – for video editing
- **Pydub** – for audio extraction
- **OpenAI API** – for generating summaries from transcripts
- **SRT** – for subtitle parsing
- **dotenv** – for environment variable management
- **FFmpeg** – used under the hood (required system dependency)

---

## 📦 Installation

1. **Clone the repository**:

```bash
git clone https://github.com/ahmedomahmoud/Video-Summarizer
cd video-summarizer

```
## 🐍 Set up a virtual environment (optional but recommended)

Create and activate a virtual environment to isolate your project's dependencies:

**Linux/macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

## 📦 Installation (continued)

### ✅ Step 3: Install dependencies

After activating your virtual environment, install the required Python packages:

```bash
pip install -r requirements.txt
```

## ✅ Step 4: Install system dependency (ffmpeg)
This project requires ffmpeg for audio and video processing. Install it based on your system:

Ubuntu/Debian:

```bash
sudo apt install ffmpeg
```

macOS (Homebrew):
```
brew install ffmpeg
```

Windows:

1- Download from https://ffmpeg.org/download.html

2- Extract it.

3- Add the ffmpeg/bin folder to your system PATH.

To verify installation, run:

```bash
ffmpeg -version
```


## 📁 Directory Setup
Before running the app, you must create a directory named clips to store the generated video shorts.

You can create it in either:

* The current working directory:
  ```bash
  mkdir clips
  ```

* in the /tmp directory (recommended for Gradio compatibility):
    ```bash
    mkdir -p /tmp/clips
    ```
⚠️ If this folder does not exist, Gradio will not be able to access or display the generated clips.


## ▶️ Usage
To launch the app:

```bash
python3 ui.py
```
Then follow these steps:

* Open the Gradio interface in your browser.

* Upload a video file (≤ 12 minutes, ≤ 20 MB).

* Choose how many shorts to generate (1–5).

* Click "Generate Shorts".

* View and download your generated clips from the gallery.

## 📋 Video Restrictions
* Maximum duration: 12 minutes

* Maximum file size: 20 MB

* Accepted formats: .mp4, .mov, .webm, etc.

## 📌 To Do / Future Improvements
 * Support for longer videos and larger file sizes

 * Allow user-defined clip durations

 * Add a progress bar or status indicator

 * Enable exporting with hardcoded subtitles

 * Integrate sharing to social platforms or cloud storage


## 🤝 Contributing
Contributions are welcome!

To contribute:

* Fork this repository.

* Create a feature branch:

```bash
git checkout -b feature/your-feature-name
```

* Commit your changes.
* Push to your fork and submit a pull request.

