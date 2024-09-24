import tkinter as tk
import time
import random

def load_text():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()

class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("800x400")
        self.target_text = load_text()
        self.current_text = ""
        self.start_time = None
        self.wpm = 0
        self.create_widgets()

    def create_widgets(self):
        self.instruction_label = tk.Label(self.root, text="Welcome to TurboType, A Speed Typing Test!", font=("Arial", 16), fg="#40E0D0")
        self.instruction_label.pack(pady=10)
        self.start_button = tk.Button(self.root, text="Start Test", command=self.start_test, font=("Arial", 14))
        self.start_button.pack(pady=10)
        self.target_text_display = tk.Text(self.root, font=("Arial", 14), height=2, width=80, wrap="word")
        self.target_text_display.pack(pady=10)
        self.target_text_display.insert("1.0", self.target_text)
        self.target_text_display.config(state='disabled')
        self.target_text_display.pack_forget()
        self.input_text = tk.Entry(self.root, font=("Arial", 14), width=80)
        self.input_text.pack(pady=10)
        self.input_text.bind("<KeyRelease>", self.on_key_press)
        self.input_text.config(state='disabled')
        self.wpm_label = tk.Label(self.root, text="WPM: 0", font=("Arial", 14))
        self.wpm_label.pack(pady=10)
        self.footer_label = tk.Label(self.root, text="Made by Hamza Dayib", font=("Arial", 10), fg="green")
        self.footer_label.place(x=10, y=370)

    def start_test(self):
        self.start_time = time.time()
        self.current_text = ""
        self.input_text.delete(0, tk.END)
        self.input_text.config(state='normal')
        self.input_text.focus()
        self.target_text_display.pack()

    def on_key_press(self, event):
        if not self.start_time:
            self.start_test()
        self.current_text = self.input_text.get()
        self.update_text_highlight()
        time_elapsed = max(time.time() - self.start_time, 1)
        self.wpm = round((len(self.current_text) / (time_elapsed / 60)) / 5)
        self.wpm_label.config(text=f"WPM: {self.wpm}")
        if self.current_text == self.target_text:
            self.end_test()

    def update_text_highlight(self):
        self.target_text_display.config(state='normal')
        self.target_text_display.delete("1.0", tk.END)
        for i, char in enumerate(self.current_text):
            correct_char = self.target_text[i] if i < len(self.target_text) else ''
            color_tag = "correct" if char == correct_char else "incorrect"
            self.target_text_display.insert(tk.END, correct_char, color_tag)
        if len(self.current_text) < len(self.target_text):
            remaining_text = self.target_text[len(self.current_text):]
            self.target_text_display.insert(tk.END, remaining_text)
        self.target_text_display.config(state='disabled')
        self.target_text_display.tag_configure("correct", foreground="green")
        self.target_text_display.tag_configure("incorrect", foreground="red")

    def end_test(self):
        self.input_text.config(state='disabled')
        self.instruction_label.config(text="Test Complete! Press the button to start again.")
        self.start_button.config(text="Restart Test", command=self.restart_test)

    def restart_test(self):
        self.target_text = load_text()
        self.target_text_display.config(state='normal')
        self.target_text_display.delete("1.0", tk.END)
        self.target_text_display.insert("1.0", self.target_text)
        self.target_text_display.config(state='disabled')
        self.input_text.config(state='normal')
        self.input_text.delete(0, tk.END)
        self.wpm_label.config(text="WPM: 0")
        self.start_button.config(text="Start Test", command=self.start_test)
        self.instruction_label.config(text="Welcome to the Speed Typing Test!")
        self.target_text_display.pack_forget()

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTest(root)
    root.mainloop()