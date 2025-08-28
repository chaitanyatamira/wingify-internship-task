<<<<<<< HEAD
# vwo-genai-internship-assignment
=======
# Blood Test Analyser – Fixed and Working

FastAPI API that accepts a blood test PDF and returns a generated “analysis.” Uses CrewAI for the flow and `pdfplumber` for PDF text extraction. Includes SQLite storage for results.

## Bugs found and how they were fixed

- Agent import path caused ImportError

  - Before: `from crewai.agents import Agent` → ImportError in newer CrewAI versions.
  - After: `from crewai import Agent` (Agent is exported from the top-level package).

- Serper tool import raised TypeError

  - Before: `from crewai_tools.tools.serper_dev_tool import serper_dev_tool as SerperDevTool` then `SerperDevTool()` → “module object is not callable”.
  - After: `from crewai_tools import SerperDevTool` and instantiate directly.

- Undefined PDF loader

  - Before: Referenced `PDFLoader` which didn’t exist.
  - After: Implemented text extraction with `pdfplumber` in `tools.py` and added it to `requirements.txt`.

- Agent validation errors (Pydantic)

  - Before: Wrong key `tool` instead of `tools`, passed raw function callables as tools, referenced undefined `llm`.
  - After: Switched to `tools`, removed invalid tool callables and undefined `llm` so Agents validate.

- Task validation errors

  - Before: Tasks attempted to pass raw function tools.
  - After: Removed invalid `tools` entries from tasks.

- Uvicorn reload not working

  - Before: `uvicorn.run(app, reload=True)` without import string.
  - After: `uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)`.

- Dependency installation issues

  - Adjusted versions in `requirements.txt` where necessary and ensured `pip install -r requirements.txt` succeeds on Windows. If pip warns, upgrade with `python -m pip install --upgrade pip`.

## Project structure

- `main.py` – FastAPI app, endpoints, and DB integration.
- `agents.py` – CrewAI Agent definitions.
- `task.py` – CrewAI Tasks.
- `tools.py` – External tools (Serper instance, PDF reader via `pdfplumber`).
- `db.py` – SQLAlchemy engine/session helpers.
- `models.py` – SQLAlchemy models (`Analysis`).
- `data/` – Sample PDFs.
- `requirements.txt` – Dependencies.

## Requirements

- Python 3.10+
- Windows PowerShell examples below (adapt for your OS)
- OpenAI API key (for live LLM calls)

## Setup

1. Create and activate a virtual environment

```powershell
python -m venv venv
./venv/Scripts/Activate.ps1
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Provide environment variables

- Create a `.env` file in the project root (recommended):
  - `OPENAI_API_KEY=YOUR_KEY`
  - `SERPER_API_KEY=YOUR_KEY` (optional; search tool not used right now)

Or set in the current PowerShell session:

```powershell
$env:OPENAI_API_KEY = "YOUR_KEY"
```

## Run

```powershell
python main.py
```

Open:

- Base: `http://127.0.0.1:8000/`
- Docs: `http://127.0.0.1:8000/docs`

Note: `0.0.0.0` is a bind address; browse with `127.0.0.1` or `localhost`.

## Usage

- Try with the docs (POST `/analyze`) and upload `data/sample.pdf`.

PowerShell example:

```powershell
curl -X POST "http://127.0.0.1:8000/analyze" ^
  -F "file=@data/sample.pdf" ^
  -F "query=Summarise my Blood Test Report"
```

Example success response:

```json
{
  "status": "success",
  "id": 1,
  "query": "Summarise my Blood Test Report",
  "analysis": "...",
  "file_processed": "sample.pdf"
}
```

## API documentation

- GET `/`

  - 200: `{ "message": "Blood Test Report Analyser API is running" }`

- POST `/analyze`

  - Form-data:
    - `file`: PDF (required)
    - `query`: string (optional; default "Summarise my Blood Test Report")
  - Returns: `status`, `id`, `query`, `analysis`, `file_processed`

- GET `/analyses`

  - Returns last 50 analyses: `id`, `file_name`, `query`, `created_at`

- GET `/analyses/{id}`
  - Returns one analysis: `id`, `file_name`, `query`, `analysis`, `created_at`

## Database

- SQLite database file `app.db` is created automatically on startup.
- Model: `Analysis(id, file_name, query, analysis, created_at)`.
- If `/analyses/{id}` returns 404, create a new record via `/analyze` and use that `id`.
- Close DB viewers to avoid SQLite file locks.

## Notes and limitations

- Requires `OPENAI_API_KEY` for live analysis; otherwise `/analyze` returns 500.
- `pdfplumber` extracts text only; scanned PDFs or complex tables may be incomplete.
- The agent prompts are intentionally satirical; outputs are not medical advice.
- `search_tool` is instantiated but not used in the current flow.

# Project Setup and Execution Guide

## Getting Started

### Install Required Libraries

```sh
pip install -r requirement.txt
```

# You're All Not Set!

🐛 **Debug Mode Activated!** The project has bugs waiting to be squashed - your mission is to fix them and bring it to life.

## Debugging Instructions

1. **Identify the Bug**: Carefully read the code and understand the expected behavior.
2. **Fix the Bug**: Implement the necessary changes to fix the bug.
3. **Test the Fix**: Run the project and verify that the bug is resolved.
4. **Repeat**: Continue this process until all bugs are fixed.
>>>>>>> 0a10787 (Initial commit)
