import os
from pathlib import Path


def load_secrets() -> None:
    """Load secrets into environment variables."""
    creds_file: Path = Path(__file__).parent.parent.joinpath(".env")
    if not creds_file.exists():
        print("No .env file found.")
        return
    with open(file=creds_file, mode="r", encoding="utf-8") as file:
        lines: list[str] = file.readlines()
        for line in lines:
            if "=" not in line:
                continue
            key, value = line.strip().split(sep="=", maxsplit=1)
            os.environ[key] = value
