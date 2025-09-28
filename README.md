# SQL Query Generator - Improved Version

## Features

### ✨ New Features Added:
1. **Query History**: Remembers your last 10 queries automatically
2. **Proper Exit**: Menu-based system with clean exit option
3. **Continuous Operation**: Runs in a loop until you choose to exit
4. **History Management**: View, reuse, and clear query history

## Installation

Install the required dependency:
```bash
pip install google-genai
```

## Usage

Run the script:
```bash
python script.py
```

### Menu Options:
1. **Generate new SQL query** - Enter a question to generate SQL
2. **View last query** - See your most recent query
3. **View query history** - Browse all saved queries
4. **Use a previous query** - Reuse or regenerate a past query
5. **Clear history** - Remove all saved queries
6. **Exit** - Properly exit the program

## Features Explained

### Query Memory
- Automatically saves your queries to `query_history.json`
- Keeps the last 10 queries for quick access
- Persists between program runs

### Proper Exit Handling
- Use option 6 to cleanly exit the program
- Press Ctrl+C for emergency exit (with option to save)
- History is automatically saved on exit

### Continuous Operation
- No need to restart the program for multiple queries
- Menu loops until you choose to exit
- Clear navigation between features

## File Structure
- `script.py` - Main program
- `query_history.json` - Stored query history (created automatically)
- `README.md` - This file

## Notes
- The program will create `query_history.json` automatically
- History is limited to 10 queries to prevent excessive storage
- All queries are saved with both the question and generated SQL
