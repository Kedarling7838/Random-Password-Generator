# Random Password Generator

A secure password generator with a Tkinter GUI, cryptographically secure generation using Python's `secrets` module, strength feedback, clipboard integration, ambiguous-character exclusion, and in-memory history.

## Features
- Password length control from 8 to 128 characters
- Choose uppercase, lowercase, numbers, and symbols
- Requires at least two selected character types
- Guarantees at least one character from every selected type
- Uses `secrets`, not `random`, for password generation
- Strength label and visual progress bar
- Copies generated passwords to the clipboard automatically
- Option to exclude ambiguous characters (`0`, `O`, `l`, `1`)
- Last five generated passwords shown in session history only; no password history is written to disk
- Optional beginner CLI implementation

## Requirements
- Python 3.10+ recommended
- Tkinter (usually included with standard Python on Windows)
- `pyperclip` (clipboard fallback is built in)

## Run on Windows
1. Extract the ZIP and open the folder in VS Code.
2. Open PowerShell in the project folder.
3. Install the dependency:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Launch the GUI:

   ```powershell
   python main.py
   ```

## Run the beginner CLI
```powershell
python beginner_cli.py
```

## Security notes
- Passwords are generated locally and are not sent over the network.
- The app does not save passwords to files or a database.
- Passwords remain visible in the app's session history until the app closes. Be careful when screen-sharing or using a shared computer.
- The strength indicator is a simple heuristic, not a formal security audit.
