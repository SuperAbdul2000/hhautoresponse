from pathlib import Path

def load_cover_letter():
    return Path("app/cover_letter.txt").read_text(
        encoding="utf-8"
    ).strip()