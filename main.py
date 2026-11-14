import sys
from pathlib import Path

# Add the src directory to Python's import path
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from pipeline import run_pipeline


def main():

    run_pipeline("The Hobbit", limit=10)


if __name__ == "__main__":
    main()