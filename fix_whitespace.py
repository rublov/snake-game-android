"""Fix trailing whitespace in files"""
import os

files_to_fix = [
    'leaderboard.py',
    'Snake Game.py',
    'create_splash.py'
]

for filepath in files_to_fix:
    if not os.path.exists(filepath):
        print(f"Skipping {filepath} - not found")
        continue

    with open(filepath, encoding="utf-8") as src:
        lines = src.readlines()

    # Remove trailing whitespace from each line
    cleaned_lines = [
        f"{line.rstrip()}\n" if line.endswith("\n") else line.rstrip()
        for line in lines
    ]

    with open(filepath, "w", encoding="utf-8") as dst:
        dst.writelines(cleaned_lines)

    print(f"✓ Fixed {filepath}")

print("\nDone!")
