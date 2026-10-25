"""Beginner command-line random password generator."""
import secrets
import string

SETS = {
    "uppercase": string.ascii_uppercase,
    "lowercase": string.ascii_lowercase,
    "numbers": string.digits,
    "symbols": string.punctuation,
}

def main():
    while True:
        try:
            length = int(input("Password length (minimum 8): ").strip())
            if length < 8:
                print("Error: password length must be at least 8.")
                continue
        except ValueError:
            print("Error: enter a whole number for the length.")
            continue

        print("Choose character types by entering y or n.")
        selected = []
        for name, chars in SETS.items():
            answer = input(f"Include {name}? (y/n): ").strip().lower()
            if answer in ("y", "yes"):
                selected.append(chars)
            elif answer not in ("n", "no"):
                print("Please enter y or n. Start again.")
                break
        else:
            if len(selected) < 2:
                print("Error: select at least two character types.")
                continue
            password_chars = [secrets.choice(chars) for chars in selected]
            all_chars = "".join(selected)
            password_chars.extend(secrets.choice(all_chars) for _ in range(length - len(password_chars)))
            secrets.SystemRandom().shuffle(password_chars)
            print("\\nGenerated password:", "".join(password_chars))

        again = input("\\nGenerate another password? (y/n): ").strip().lower()
        if again not in ("y", "yes"):
            break

if __name__ == "__main__":
    main()
