# YouTube RAG Assistant

This project is an assistant that uses RAG (Retrieval-Augmented Generation) to answer questions based on the content of YouTube videos.  
It downloads the video, extracts the audio, transcribes it using Faster Whisper, and uses the OpenAI API to answer questions.

## Features

- Download YouTube videos  
- Extract and transcribe audio with Faster Whisper  
- Query the OpenAI API to answer questions  
- Modular and organized structure following PEP-8

## Project Structure

```
yt_sage/
├── run.py                   # Main script to run the assistant
├── yt_sage/
│   ├── __init__.py          # Package initializer
│   ├── cli.py               # Command line interface
│   ├── downloader.py        # Functions for downloading and extracting audio
│   ├── transcriber.py       # Functions for audio transcription
│   ├── openai_client.py     # Client for OpenAI interaction
│   └── utils.py             # General utility functions
├── tests/                   # Unit tests
│   ├── __init__.py
│   ├── test_downloader.py
│   ├── test_transcriber.py
│   ├── test_openai_client.py
│   └── test_utils.py
├── .env                    # Environment variables file (do not upload to Git)
├── .gitignore              # Git ignore file
└── README.md               # Project documentation
```

## How to Use

1. Clone the repository  
2. Set your OpenAI API key in the `.env` file as `OPENAI_API_KEY=your_api_key`  
3. Install dependencies: `pip install -r requirements.txt`  
4. Run the main script: `python run.py`  
5. Paste the YouTube video link and ask questions about the transcribed content

## Notes

- Do not upload the `.env` file with your key to the public repository  
- You can create tests for each module in the `tests` folder to ensure code quality  
- The project is structured to facilitate maintenance and future expansion

---

Project created by Nicholas Tadeu.