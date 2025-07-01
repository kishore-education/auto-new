# pip install pyautogui
import pyautogui
import keyboard
import time
import random
import sys

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
    print("PROGRAM IS CREATED BY KISHORE\n")
    def print_controls():
        print("\n--- Controls ---")
        print("F8  : Pause/Resume auto-typing")
        print("ESC : Stop auto-typing and skip to next run")
        print("F7  : Restart the last auto-typing session with the same text")
        print("----------------\n")
    print_controls()
    for i in range(100):
        print(f"\nRun {i+1}/100: Please enter your text (end with 'end'). Starting in 8 seconds...")
        text_to_type = get_multi_line_text()
        print_controls()
        time.sleep(8)  # Reduced wait before typing
        auto_type(text_to_type)

if __name__ == "__main__":
    main()
