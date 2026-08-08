from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
SOUNDS_DIR = ASSETS_DIR / "sounds"
DATA_DIR = BASE_DIR / "data"


def image_path(filename: str) -> str:
    return str(IMAGES_DIR / filename)


def sound_path(filename: str) -> str:
    return str(SOUNDS_DIR / filename)


def data_path(filename: str) -> str:
    return str(DATA_DIR / filename)
