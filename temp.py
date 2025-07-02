
import pyautogui
import keyboard
import time
import random
import sys
import pyperclip
import requests
import json

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
        print("F7  : Restart the last auto-typing session with the same text")
        print("----------------\n")
    print_controls()

    last_clipboard = ""
    api_key = "AIzaSyBzeBqXflk2kR3c2x86xPK6awkxQhwsJqA"
    api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": api_key,
    }

    print("[INFO] Monitoring clipboard. Copy any text to send to Gemini API...")
    while True:
        try:
            current_clipboard = pyperclip.paste()
        except Exception:
            current_clipboard = ""
        if current_clipboard and current_clipboard != last_clipboard:
            print("[CLIPBOARD] New text detected. Sending to Gemini API...")
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": f"only c++ program. with custom input.the input  and output format should be same \n{current_clipboard}"
                            }
                        ]
                    }
                ]
            }
            try:
                response = requests.post(api_url, headers=headers, data=json.dumps(payload))
                if response.status_code == 200:
                    data = response.json()
                    # Extract the response text from Gemini API structure
                    result = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                    
                    # Remove code block markers
                    if result.startswith("```cpp"):
                        result = result[6:]  # Remove ```cpp
                    if result.startswith("```"):
                        result = result[3:]  # Remove ```
                    if result.endswith("```"):
                        result = result[:-3]  # Remove trailing ```
                    result = result.strip()  # Remove leading/trailing whitespace
                    
                    print("[API RESPONSE] Will auto-type after 8 seconds:")
                    print(result)
                    time.sleep(8)
                    auto_type(result)
                else:
                    print(f"[ERROR] API returned status {response.status_code}: {response.text}")
            except Exception as e:
                print(f"[ERROR] Failed to contact API: {e}")
            # Clear clipboard after processing
            pyperclip.copy("")
            last_clipboard = ""
        else:
            last_clipboard = current_clipboard
        time.sleep(0.5)

if __name__ == "__main__":
    main()
