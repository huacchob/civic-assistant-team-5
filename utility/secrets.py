import os
from pathlib import Path


def load_secrets():
    """Load secrets into environment variables."""
    creds_file: Path = Path(__file__).parent.parent.joinpath(".env")
    with open(file=creds_file, mode="r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            key, value = line.strip().split("=", 1)
            os.environ[key] = value
