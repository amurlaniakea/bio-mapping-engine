import argparse

from src.engine.search import SearchEngine
from src.cli.cli_handler import CLIHandler


def main():
    parser = argparse.ArgumentParser(description="Bio-Mapping Engine CLI")
    parser.add_argument("--symptom", help="Search by symptom name")
    parser.add_argument("--zone", help="Search by physical zone")
    parser.add_argument("--author", help="Search by author name")

    args = parser.parse_args()

    engine = SearchEngine()
    handler = CLIHandler(engine)
    handler.handle(args)


if __name__ == "__main__":
    main()
