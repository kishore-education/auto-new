
import pyautogui
import keyboard
import time
import random
import sys
import pyperclip
import requests
import json
import os

# Try to import API keys from config file
try:
    from config import PRIMARY_API_KEY, FALLBACK_API_KEY
except ImportError:
    # Fallback to environment variables or empty strings
    PRIMARY_API_KEY = os.getenv('PRIMARY_API_KEY', '')
    FALLBACK_API_KEY = os.getenv('FALLBACK_API_KEY', '')
    if not PRIMARY_API_KEY or not FALLBACK_API_KEY:
        print("WARNING: API keys not found!")
        print("Please either:")
        print("1. Create a config.py file with PRIMARY_API_KEY and FALLBACK_API_KEY")
        print("2. Set environment variables PRIMARY_API_KEY and FALLBACK_API_KEY")
        print("3. Edit this file to add your keys directly (not recommended for git)")
        sys.exit(1)

def get_multi_line_text():
    """Collects multi-line input from the user until 'end' is entered."""
    lines = []
    for line in sys.stdin:
        line = line.strip()  # Remove trailing whitespace
        if line == 'end':
            break
        lines.append(line)
    # Removed unnecessary sleep for speed
    return '\n'.join(lines)  # Join lines for text processing

def auto_type(text, sleep_time=0.2):
    """Types the given text with simulated human-like variations. Pauses/resumes on Ctrl+Alt press."""
    paused = [False]
    stopped = [False]
    restart = [False]

    def toggle_pause():
        paused[0] = not paused[0]
        if paused[0]:
            print("[PAUSED] Press F8 again to resume...")
        else:
            print("[RESUMED] Auto typing continues...")

    def stop_typing():
        stopped[0] = True
        print("[STOPPED] ESC pressed. Exiting auto-typing.")

    def restart_typing():
        restart[0] = True
        print("[RESTART] F9 pressed. Restarting last auto-typing.")
        # Select all and backspace before restarting
        pyautogui.hotkey('ctrl', 'shift', 'end')
        pyautogui.press('backspace')

    # Register hotkeys
    keyboard.add_hotkey('F8', toggle_pause)
    keyboard.add_hotkey('esc', stop_typing)
    keyboard.add_hotkey('F9', restart_typing)

    while True:
        for char in text:
            if stopped[0] or restart[0]:
                break
            while paused[0]:
                if stopped[0] or restart[0]:
                    break
                time.sleep(0.1)
            if stopped[0] or restart[0]:
                break
            pyautogui.typewrite(char)
            time.sleep(random.uniform(0.01, 0.03))
            if random.random() < 0.01:
                time.sleep(random.uniform(0.1, 0.3))
            if random.random() < 0.005:
                pyautogui.typewrite(random.choice('abcdefghijklmnopqrstuvwxyz'))
                time.sleep(0.03)
                pyautogui.press('backspace')
        if stopped[0]:
            break
        if restart[0]:
            restart[0] = False
            print("[RESTARTED] Typing restarted.")
            continue
        break
    if not stopped[0]:
        pyautogui.hotkey('ctrl', 'shift', 'end')
        pyautogui.press('backspace')
    keyboard.remove_hotkey('F8')
    keyboard.remove_hotkey('esc')
    keyboard.remove_hotkey('F9')

def main():

    """Main execution flow for the program."""
    # Clear clipboard at the start
    pyperclip.copy("")
    print("PROGRAM IS CREATED BY KISHORE\n")

    def print_controls():
        print("\n--- Controls ---")
        print("F8  : Pause/Resume auto-typing")
        print("ESC : Stop auto-typing and skip to next run")
        print("F9  : Restart the last auto-typing session with the same text")
        print("F4  : Switch between Gemini API and OpenRouter API")
        print("----------------\n")
    print_controls()

    last_clipboard = ""
    last_failed_clipboard = ""  # Track text that failed with primary API
    use_primary_api = [True]  # Use list to allow modification in nested function
    
    def switch_api():
        use_primary_api[0] = not use_primary_api[0]
        if use_primary_api[0]:
            print("[API SWITCH] Switched to Gemini API (Primary)")
        else:
            print("[API SWITCH] Switched to OpenRouter API (Fallback)")
    
    # Register F4 hotkey for API switching
    keyboard.add_hotkey('f4', switch_api)
    
    # Primary API (Google Gemini)
    primary_api_key = PRIMARY_API_KEY
    primary_api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    primary_headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": primary_api_key,
    }
    
    # Fallback API (OpenRouter)
    fallback_api_key = FALLBACK_API_KEY
    fallback_api_url = "https://openrouter.ai/api/v1/chat/completions"
    fallback_headers = {
        "Authorization": f"Bearer {fallback_api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/kishore-education/auto-new",
        "X-Title": "Auto Code Generator",
    }

    print("[INFO] Monitoring clipboard. Copy any text to send to Gemini API (Primary) or OpenRouter API (Fallback)...")
    while True:
        try:
            current_clipboard = pyperclip.paste()
        except Exception:
            current_clipboard = ""
        if current_clipboard and current_clipboard != last_clipboard:
            # Determine which API to use - check manual switch first, then fallback logic
            manual_fallback = not use_primary_api[0]
            auto_fallback = (current_clipboard == last_failed_clipboard)
            use_fallback = manual_fallback or auto_fallback
            
            if use_fallback:
                if manual_fallback:
                    print("[CLIPBOARD] New text detected. Using OpenRouter API (Manual Switch)...")
                else:
                    print("[CLIPBOARD] Same text detected again. Using OpenRouter API (Auto Fallback)...")
                api_url = fallback_api_url
                headers = fallback_headers
                payload = {
                    "model": "deepseek/deepseek-r1-0528-qwen3-8b:free",
                    "messages": [
                        {
                            "role": "user",
                            "content": f"only c++ program. with custom input.the input and output format should be same \n{current_clipboard}"
                        }
                    ]
                }
            else:
                print("[CLIPBOARD] New text detected. Sending to Gemini API (Primary)...")
                api_url = primary_api_url
                headers = primary_headers
                payload = {
                    "contents": [
                        {
                            "parts": [
                                {
                                    "text": f"only c++ program. with custom input.the input and output format should be same \n{current_clipboard}"
                                }
                            ]
                        }
                    ]
                }
            try:
                response = requests.post(api_url, headers=headers, data=json.dumps(payload))
                if response.status_code == 200:
                    data = response.json()
                    
                    # Extract the response text based on API type
                    if use_fallback:
                        # OpenRouter API structure
                        result = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                    else:
                        # Gemini API structure
                        candidates = data.get("candidates", [])
                        if candidates:
                            content = candidates[0].get("content", {})
                            parts = content.get("parts", [])
                            if parts:
                                result = parts[0].get("text", "")
                            else:
                                result = ""
                        else:
                            result = ""
                    
                    # Extract only content inside ```cpp ``` blocks
                    if "```cpp" in result:
                        # Find the start of the cpp code block
                        start_marker = result.find("```cpp")
                        if start_marker != -1:
                            # Move past the ```cpp marker
                            start_pos = start_marker + 6
                            # Find the end marker
                            end_marker = result.find("```", start_pos)
                            if end_marker != -1:
                                result = result[start_pos:end_marker]
                            else:
                                result = result[start_pos:]
                    elif "```" in result:
                        # Handle generic code blocks
                        start_marker = result.find("```")
                        if start_marker != -1:
                            start_pos = start_marker + 3
                            # Skip language identifier if present
                            newline_pos = result.find("\n", start_pos)
                            if newline_pos != -1:
                                start_pos = newline_pos + 1
                            end_marker = result.find("```", start_pos)
                            if end_marker != -1:
                                result = result[start_pos:end_marker]
                            else:
                                result = result[start_pos:]
                    
                    result = result.strip()  # Remove leading/trailing whitespace
                    
                    # Remove all tab spaces and extra whitespace, keep only newlines
                    lines = result.split('\n')
                    cleaned_lines = []
                    for line in lines:
                        # Remove all tabs and leading/trailing spaces from each line
                        cleaned_line = line.replace('\t', '').strip()
                        cleaned_lines.append(cleaned_line)
                    result = '\n'.join(cleaned_lines)
                    
                    print("[API RESPONSE] Will auto-type after 8 seconds:")
                    print(result)
                    time.sleep(8)
                    auto_type(result)
                    # Reset failed clipboard since this worked
                    last_failed_clipboard = ""
                else:
                    print(f"[ERROR] API returned status {response.status_code}: {response.text}")
                    if not use_fallback:
                        # Mark this text as failed for primary API
                        last_failed_clipboard = current_clipboard
                        print("[INFO] This text will use fallback API if copied again.")
            except Exception as e:
                print(f"[ERROR] Failed to contact API: {e}")
                if not use_fallback:
                    # Mark this text as failed for primary API
                    last_failed_clipboard = current_clipboard
                    print("[INFO] This text will use fallback API if copied again.")
            # Clear clipboard after processing
            pyperclip.copy("")
            last_clipboard = ""
        else:
            last_clipboard = current_clipboard
        time.sleep(0.5)
    
    # Clean up hotkey when program ends
    keyboard.remove_hotkey('f4')

if __name__ == "__main__":
    main()
