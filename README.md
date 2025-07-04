# Auto Code Generator

An intelligent auto-typing tool that generates C++ code using AI APIs and automatically types it with human-like variations.

## Features

- **Dual API System**: Primary (Google Gemini 2.0 Flash) + Fallback (OpenRouter DeepSeek)
- **Smart Switching**: Manual F4 switching + automatic fallback for failed requests
- **Clipboard Monitoring**: Automatically detects new text and generates code
- **Human-like Typing**: Simulates natural typing patterns with random delays
- **Hotkey Controls**: F8 (pause/resume), ESC (stop), F9 (restart), F4 (switch API)
- **Code Extraction**: Automatically extracts clean C++ code from API responses
- **No Formatting**: Removes tabs and extra spaces for compact output

## Setup

### 1. Install Dependencies
```bash
pip install pyautogui keyboard pyperclip requests
```

### 2. Configure API Keys
Copy the template and add your keys:
```bash
cp config_template.py config.py
```

Edit `config.py` with your actual API keys:
```python
# Primary API (Google Gemini)
PRIMARY_API_KEY = "your-gemini-api-key-here"

# Fallback API (OpenRouter)  
FALLBACK_API_KEY = "your-openrouter-api-key-here"
```

### 3. Run the Program
```bash
python temp.py
```

## Usage

1. **Start the program** - It will monitor your clipboard
2. **Copy any programming problem** to your clipboard
3. **Wait 8 seconds** - The AI will generate and auto-type C++ code
4. **Use hotkeys** to control the typing process

## Controls

- **F8**: Pause/Resume auto-typing
- **ESC**: Stop auto-typing and skip to next run
- **F9**: Restart the last auto-typing session
- **F4**: Switch between Gemini API and OpenRouter API

## API Priority

1. **Gemini 2.0 Flash** (Primary) - Fast and powerful
2. **OpenRouter DeepSeek** (Fallback) - Reliable backup
3. **Manual Override** - F4 to force API selection
4. **Auto Fallback** - Copy same text again if primary fails

## Security

- API keys are stored in `config.py` (ignored by git)
- No hardcoded secrets in the repository
- Use environment variables as alternative

## Author

Created by KISHORE
