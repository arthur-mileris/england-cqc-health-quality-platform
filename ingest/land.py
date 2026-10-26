import argparse

from ingest.cqc_directory import land_directory


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", choices=["directory"])
    parser.parse_args()
    path = land_directory()
    print(path, path.stat().st_size)


if __name__ == "__main__":
    main()