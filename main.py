"""Secure Random Password Generator - Tkinter GUI."""
import secrets
import string
import tkinter as tk
from tkinter import ttk, messagebox

try:
    import pyperclip
except ImportError:
    pyperclip = None

AMBIGUOUS = set("0OIl1")

CHARACTER_SETS = {
    "Uppercase (A-Z)": string.ascii_uppercase,
    "Lowercase (a-z)": string.ascii_lowercase,
    "Numbers (0-9)": string.digits,
    "Symbols (!@#...)": string.punctuation,
}

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Password Generator")
        self.root.geometry("700x700")
        self.root.minsize(620, 640)
        self.root.configure(bg="#f3f6fb")
        self.history = []

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TLabel", background="#f3f6fb", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10), padding=7)
        style.configure("TCheckbutton", background="#f3f6fb", font=("Segoe UI", 10))

        header = tk.Frame(root, bg="#23395d", padx=22, pady=18)
        header.pack(fill="x")
        tk.Label(header, text="SECURE PASSWORD GENERATOR", bg="#23395d",
                 fg="white", font=("Segoe UI", 18, "bold")).pack(anchor="w")
        tk.Label(header, text="Create strong passwords locally on your device",
                 bg="#23395d", fg="#dce6f5", font=("Segoe UI", 10)).pack(anchor="w", pady=(4, 0))

        main = ttk.Frame(root, padding=(22, 18))
        main.pack(fill="both", expand=True)

        ttk.Label(main, text="Password length (8–128)").grid(row=0, column=0, sticky="w")
        self.length_var = tk.IntVar(value=16)
        self.length_spin = ttk.Spinbox(main, from_=8, to=128, textvariable=self.length_var,
                                       width=8, justify="center")
        self.length_spin.grid(row=0, column=1, sticky="w", padx=12, pady=6)

        ttk.Label(main, text="Character types (select at least 2)").grid(
            row=1, column=0, columnspan=2, sticky="w", pady=(12, 4))
        self.type_vars = {}
        for row, label in enumerate(CHARACTER_SETS, start=2):
            var = tk.BooleanVar(value=(label != "Symbols (!@#...)"))
            self.type_vars[label] = var
            ttk.Checkbutton(main, text=label, variable=var).grid(
                row=row, column=0, columnspan=2, sticky="w", pady=3)

        self.ambiguous_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(main, text="Exclude ambiguous characters (0, O, l, 1)",
                        variable=self.ambiguous_var).grid(row=6, column=0, columnspan=3,
                                                         sticky="w", pady=(10, 6))

        ttk.Button(main, text="Generate Password", command=self.generate_password).grid(
            row=7, column=0, sticky="ew", pady=(12, 8))
        ttk.Button(main, text="Copy to Clipboard", command=self.copy_password).grid(
            row=7, column=1, sticky="ew", padx=(10, 0), pady=(12, 8))

        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(main, textvariable=self.password_var,
                                        font=("Consolas", 13), state="readonly")
        self.password_entry.grid(row=8, column=0, columnspan=3, sticky="ew", pady=5)

        strength_frame = ttk.Frame(main)
        strength_frame.grid(row=9, column=0, columnspan=3, sticky="ew", pady=(10, 2))
        ttk.Label(strength_frame, text="Password strength:").pack(side="left")
        self.strength_label = tk.Label(strength_frame, text="Not generated", bg="#f3f6fb",
                                       fg="#667085", font=("Segoe UI", 10, "bold"))
        self.strength_label.pack(side="left", padx=8)
        self.strength_bar = ttk.Progressbar(main, orient="horizontal", mode="determinate",
                                            maximum=100, length=400)
        self.strength_bar.grid(row=10, column=0, columnspan=3, sticky="ew", pady=(4, 12))

        ttk.Label(main, text="Session history (last 5; not saved to disk)").grid(
            row=11, column=0, columnspan=3, sticky="w", pady=(8, 5))
        self.history_list = tk.Listbox(main, height=6, font=("Consolas", 10),
                                       activestyle="dotbox", exportselection=False)
        self.history_list.grid(row=12, column=0, columnspan=3, sticky="nsew")
        ttk.Button(main, text="Use selected history password", command=self.use_history).grid(
            row=13, column=0, columnspan=3, sticky="ew", pady=(8, 0))

        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(12, weight=1)

        tk.Label(root, text="Passwords are kept only in this session. Avoid sharing them.",
                 bg="#f3f6fb", fg="#667085", font=("Segoe UI", 9)).pack(pady=(0, 10))

    def get_selected_sets(self):
        selected = [CHARACTER_SETS[label] for label, var in self.type_vars.items() if var.get()]
        if len(selected) < 2:
            raise ValueError("Select at least two character types.")
        if self.ambiguous_var.get():
            selected = ["".join(ch for ch in chars if ch not in AMBIGUOUS) for chars in selected]
        if any(not chars for chars in selected):
            raise ValueError("One selected character type has no characters after exclusions.")
        return selected

    def generate_password(self):
        try:
            raw_length = self.length_spin.get().strip()
            length = int(raw_length)
            if not 8 <= length <= 128:
                raise ValueError("Password length must be between 8 and 128 characters.")
            sets = self.get_selected_sets()
        except ValueError as exc:
            messagebox.showerror("Invalid settings", str(exc))
            return

        if length < len(sets):
            messagebox.showerror("Invalid length", "Length must be at least the number of selected character types.")
            return

        # Guarantee one character from every selected type, then fill and securely shuffle.
        password_chars = [secrets.choice(chars) for chars in sets]
        combined = "".join(sets)
        password_chars.extend(secrets.choice(combined) for _ in range(length - len(password_chars)))
        secrets.SystemRandom().shuffle(password_chars)
        password = "".join(password_chars)

        self.password_var.set(password)
        strength, score, color = self.calculate_strength(length, len(sets))
        self.strength_label.config(text=strength, fg=color)
        self.strength_bar["value"] = score

        self.history.insert(0, password)
        self.history = self.history[:5]
        self.refresh_history()

        # Automatically copy on generation, as requested.
        self.copy_to_clipboard(show_success=False)

    @staticmethod
    def calculate_strength(length, type_count):
        # A simple educational estimate based on length and character diversity.
        score = min(100, int((length / 32) * 65 + (type_count / 4) * 35))
        if length >= 16 and type_count >= 3:
            return "Strong", max(score, 80), "#16803c"
        if length >= 12 and type_count >= 2:
            return "Medium", max(score, 50), "#b7791f"
        return "Weak", min(score, 45), "#c0392b"

    def refresh_history(self):
        self.history_list.delete(0, tk.END)
        for password in self.history:
            self.history_list.insert(tk.END, password)

    def copy_to_clipboard(self, show_success=True):
        password = self.password_var.get()
        if not password:
            if show_success:
                messagebox.showwarning("No password", "Generate a password first.")
            return
        try:
            if pyperclip is not None:
                pyperclip.copy(password)
            else:
                self.root.clipboard_clear()
                self.root.clipboard_append(password)
                self.root.update()
            if show_success:
                messagebox.showinfo("Copied", "Password copied to clipboard.")
        except Exception as exc:
            if show_success:
                messagebox.showerror("Clipboard error", f"Could not copy password:\\n{exc}")

    def copy_password(self):
        self.copy_to_clipboard(show_success=True)

    def use_history(self):
        selection = self.history_list.curselection()
        if not selection:
            messagebox.showinfo("Select a password", "Choose a password from the history list.")
            return
        password = self.history_list.get(selection[0])
        self.password_var.set(password)
        self.copy_to_clipboard(show_success=False)

def main():
    root = tk.Tk()
    PasswordGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
