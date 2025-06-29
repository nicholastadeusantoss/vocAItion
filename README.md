# vocAItion

**vocAItion** is a proof-of-concept (PoC) for an AI-powered resume enhancement assistant. It helps users rewrite and improve their previous job descriptions using OpenAI's API, through an interactive command-line flow.

## 🚀 Features

- Load resumes in `.txt` or `.pdf` format
- Automatically extract professional experiences using GPT
- Let the user select one experience to improve
- Generate tailored questions to refine the selected experience
- Rewrite the experience based on the user’s answers

## 📁 Project Structure

```
vocAItion/
├── app/
│   ├── main.py                   # Main entrypoint for the CLI POC
│   ├── sections/
│   │   └── experience.py         # Experience processing logic (extract, improve)
│   ├── utils/
│   │   ├── file_loader.py        # Handles loading PDF or TXT files
│   │   ├── openai_client.py      # Wrapper around OpenAI API
│   │   └── prompts.py            # Loads prompt templates
├── prompts/
│   ├── experience_extract_prompt.txt
│   ├── experience_questions_prompt.txt
│   └── experience_improve_prompt.txt
├── data/                         # Folder for uploading resumes (.pdf/.txt)
│   └── sample_resume.pdf
├── .env                          # API key for OpenAI
├── .gitignore
├── requirements.txt
└── README.md
```

## 🛠️ Setup & Usage

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Add your OpenAI API key

Create a `.env` file in the root with:

```
OPENAI_API_KEY=your-api-key-here
```

### 3. Add a resume

Place your `.pdf` or `.txt` resume in the `data/` folder.

### 4. Run the app

```bash
python -m app.main
```

Project created by Nicholas Tadeu.