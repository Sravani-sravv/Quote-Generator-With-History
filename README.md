# 💬 Quote Generator with History

An AI-powered quote generator built with **Streamlit** and the **Anthropic API**.  
Fetches unique quotes by category and saves them to a local SQLite database.

---

## Features

- 🎲 Generate quotes across 8 categories (Motivation, Wisdom, Stoicism, Love, Humor, Science, Success, Philosophy)
- 💾 Save quotes to a local SQLite database
- ❤️ Like / unlike saved quotes
- 🗂 Filter history by category or liked status
- 📊 Stats — total saved, liked count, unique categories
- 🗑️ Delete individual quotes or clear all history

---

## Project Structure

```
quote_generator/
│
├── app.py            # Main Streamlit application
├── database.py       # SQLite helper functions
├── requirements.txt  # Python dependencies
├── .env.example      # Template for API key
├── .gitignore        # Ignores .env and .db files
└── README.md
```

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/quote-generator.git
cd quote-generator
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your API key
```bash
# Copy the example file
copy .env.example .env       # Windows
# cp .env.example .env       # Mac/Linux

# Open .env and replace the placeholder with your real key
ANTHROPIC_API_KEY=sk-ant-...
```
Get your API key from: https://console.anthropic.com

### 5. Run the app
```bash
streamlit run app.py
```

The app opens automatically at `http://localhost:8501`

---

## Tech Stack

| Layer     | Technology              |
|-----------|------------------------|
| Frontend  | Streamlit               |
| AI / API  | Anthropic Claude (claude-sonnet-4) |
| Database  | SQLite (via sqlite3)    |
| Config    | python-dotenv           |

---

## Author

**Aasfiya Tanveer** — B.Tech CSE, MRECW  
GitHub: [mrecwcsea24502](https://github.com/mrecwcsea24502)  
LinkedIn: [aasfiya-tanveer](https://linkedin.com/in/aasfiya-tanveer-31b5573a2)
