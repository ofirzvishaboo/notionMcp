# Notion Learning Assistant

An AI-powered learning assistant that integrates with Notion to help users manage their learning materials, generate summaries, create review questions, and track progress.

## Features

- Generate concise summaries of learning materials
- Create review questions based on content
- Track learning progress in Notion
- Manage assignments and deadlines
- Adaptive learning based on user performance
- Interactive web interface

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Notion API key:
   ```
   NOTION_API_KEY=your_api_key_here
   ```
4. Run the application:
   ```bash
   streamlit run assistant.py
   ```

## Project Structure

- `api_interactions.py`: Notion API integration
- `summaries.py`: Summary generation logic
- `questions.py`: Question generation logic
- `progress_tracker.py`: Progress tracking functionality
- `assistant.py`: Main application driver

## Requirements

- Python 3.9+
- Notion API access
- Internet connection for API calls

## Testing

Run tests using pytest:
```bash
pytest
```