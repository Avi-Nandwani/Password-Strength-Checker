import tkinter as tk
from tkinter import ttk
from password_strength_checker import PasswordStrengthChecker, rating

class PasswordGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Strength Checker")
        self.geometry("400x320")
        self.resizable(False, False)
        self.checker = PasswordStrengthChecker()
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Enter password:", font=("Arial", 12)).pack(pady=(15,2))
        self.entry_var = tk.StringVar()
        entry_frame = ttk.Frame(self)
        entry_frame.pack()
        self.password_entry = ttk.Entry(entry_frame, textvariable=self.entry_var, font=("Arial", 12), width=28, show="*")
        self.password_entry.pack(side=tk.LEFT, padx=(0,5))
        self.password_entry.bind('<KeyRelease>', self.update_strength)
        self.show_var = tk.BooleanVar(value=False)
        self.show_check = ttk.Checkbutton(entry_frame, text="Show", variable=self.show_var, command=self.toggle_show)
        self.show_check.pack(side=tk.LEFT)
        self.strength_label = ttk.Label(self, text="Strength: ", font=("Arial", 11))
        self.strength_label.pack(pady=(12,3))
        self.progress = ttk.Progressbar(self, length=200, mode="determinate", maximum=100)
        self.progress.pack(pady=2)
        ttk.Label(self, text="Suggestions:", font=("Arial", 10)).pack(pady=(10,0))
        self.suggestions_text = tk.Text(self, width=45, height=8, wrap="word")
        self.suggestions_text.pack(padx=4)
        self.suggestions_text.config(state="disabled")

    def toggle_show(self):
        self.password_entry.config(show="" if self.show_var.get() else "*")

    def update_strength(self, event=None):
        pwd = self.entry_var.get()
        result = self.checker.evaluate(pwd)
        percent = int(round(result["score"] / result["total"] * 100))
        self.progress["value"] = percent
        col = "#2ecc40" if percent == 100 else "#ffdc00" if percent >= 62 else "#ff4136"
        self.progress.config(style="custom.Horizontal.TProgressbar")
        style = ttk.Style()
        style.theme_use("default")
        style.configure("custom.Horizontal.TProgressbar", foreground=col, background=col)
        strength = rating(result['score'], result['total'])
        self.strength_label.config(text=f"Strength: {strength} ({percent}%)")
        self.suggestions_text.config(state="normal")
        self.suggestions_text.delete("1.0", tk.END)
        if percent == 100:
            self.suggestions_text.insert(tk.END, "✅ Excellent! Your password meets all criteria.")
        else:
            for sug in result["suggestions"]:
                self.suggestions_text.insert(tk.END, f" - {sug}\n")
        self.suggestions_text.config(state="disabled")

if __name__ == "__main__":
    PasswordGUI().mainloop()
