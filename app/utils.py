from pathlib import Path

#функция для считывания txt файла с сопроводительным письмом
def load_cover_letter():
    return Path("app/cover_letter.txt").read_text(
        encoding="utf-8"
    ).strip()
