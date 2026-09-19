# Jarvis — Voice-Activated Desktop Assistant

A Python-based voice assistant that listens for the wake word **"Jarvis"**, then executes voice commands — opening websites, playing music/YouTube videos, fetching news headlines, and answering general questions via Google's Gemini API.

## Features

- **Wake-word detection** — always listening for "Jarvis" in the background
- **Website launcher** — opens Google, YouTube, Gmail, Spotify, LinkedIn, Reddit, and more via voice
- **Browser control** — opens links specifically in **Brave**, with automatic fallback to the system default browser if Brave isn't found
- **Private/Incognito browsing** — supports commands like "open YouTube private" or "open private"
- **Music playback**
  - Plays songs from a personal `musicLibrary.py` dictionary (Spotify/SoundCloud/YouTube links)
  - Falls back to a live YouTube search if the requested song isn't in the library
- **News headlines** — fetches and reads out top headlines for India or the USA via NewsAPI
- **General Q&A** — any command that doesn't match a specific action is passed to Google's Gemini model for a conversational response
- **Text-to-speech** — all responses are spoken aloud using `pyttsx3`

## Requirements

- Python 3.10+
- [Brave Browser](https://brave.com/) installed (optional — falls back to default browser)
- A working microphone
- API keys for:
  - [NewsAPI](https://newsapi.org/)
  - [Google Gemini API](https://ai.google.dev/)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/jarvis-assistant.git
   cd jarvis-assistant
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate      # Windows
   source .venv/bin/activate   # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install speechrecognition pyttsx3 pyaudio requests python-dotenv google-genai
   ```
   > `pyaudio` can be tricky to install on Windows. If `pip install pyaudio` fails, try:
   > ```bash
   > pip install pipwin
   > pipwin install pyaudio
   > ```

4. **Set up your environment variables**

   Create a `.env` file in the project root:
   ```env
   NEWS_API_KEY=your_newsapi_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

5. **Set up your music library**

   Copy the template and add your own songs:
   ```bash
   cp musiclibrary_template.py musicLibrary.py
   ```
   Then edit `musicLibrary.py`:
   ```python
   musicList = {
       "Playlist": "https://open.spotify.com/playlist/your_playlist_id",
       "your song name": "https://www.youtube.com/watch?v=...",
   }
   ```

6. **Update the Brave browser path** (if needed)

   In `main.py`, confirm this path matches your install location:
   ```python
   BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
   ```
   Per-user installs are often located at:
   ```
   C:\Users\<username>\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe
   ```

## Usage

Run the assistant:
```bash
python main.py
```

Then simply say **"Jarvis"** to wake it up, wait for the "Jarvis is awake" confirmation, and speak a command. Example commands:

| Command | Action |
|---|---|
| "open google" | Opens Google in Brave |
| "open youtube private" | Opens YouTube in Brave Incognito |
| "play let it happen" | Plays the song from your music library |
| "play [any song name]" | Searches and plays the first YouTube result |
| "open playlist" | Opens your saved Spotify playlist |
| "news india" / "news usa" | Reads out top headlines |
| Anything else | Passed to Gemini for a conversational reply |

## Project Structure

```
.
├── main.py                     # Core assistant logic
├── musicLibrary.py              # Your personal song-to-link mapping (gitignored)
├── musiclibrary_template.py     # Empty template for musicLibrary.py
├── .env                         # API keys (gitignored)
├── .gitignore
└── README.md
```

## Notes & Known Limitations

- Uses Google's free Web Speech API via `speech_recognition` — requires an active internet connection for both wake-word and command recognition.
- `pyttsx3` engine is re-initialized on every `speak()` call to avoid a known issue where repeated calls on a single engine instance silently fail to produce audio.
- YouTube search scraping (`urllib` + regex) is a lightweight workaround and may break if YouTube changes its page structure; consider migrating to the official YouTube Data API for reliability.
- No noise-cancellation beyond `adjust_for_ambient_noise` — recognition accuracy depends heavily on microphone quality and background noise.

## License

MIT License — feel free to fork and customize for your own setup.
