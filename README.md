# GenAI Data Query Assistant

A GenAI-powered Data Query Assistant built with Python, FastAPI, LangChain, and Google Gemini.

## Features
- Upload Excel datasets (.xlsx)
- Ask natural language questions
- AI generates pandas queries automatically
- Returns results + business insights
- Simple dark-themed frontend

## Tech Stack
- Python
- FastAPI
- LangChain (LCEL)
- Google Gemini API
- Pandas
- HTML/CSS/JS

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/GenAI_Data_Assistant.git
cd GenAI_Data_Assistant
```

### 2. Create virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your API key
In `services/query_service.py`, replace:
```python
google_api_key="your-api-key-here"
```

### 5. Run the app
```bash
uvicorn main:app --reload
```

### 6. Open in browser

http://127.0.0.1:8000

## Example Questions
- Which product generated the highest revenue?
- Show top 10 customers by sales.
- Find records where profit is negative.
- Which region has maximum orders?
- Display products with sales greater than 5000.
