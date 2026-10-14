import csv
from pathlib import Path

CSV_FILE = Path(__file__).parent / "requiredsoftwares.csv"
OUTPUT_FILE = Path(__file__).parent / "latest_versions.csv"


def read_required_softwares():
    with CSV_FILE.open(
        "r",
        newline="",
        encoding="utf-8-sig",
    ) as file:
        reader = csv.DictReader(file)

        required_columns = {"sno", "name", "version", "url"}

        if not reader.fieldnames:
            raise ValueError("CSV file has no header.")

        actual_columns = {
            column.strip()
            for column in reader.fieldnames
        }

        missing = required_columns - actual_columns

        if missing:
            raise ValueError(f"Missing columns: {missing}")

        return [
            {
                key.strip(): (value or "").strip()
                for key, value in row.items()
                if key is not None
            }
            for row in reader
        ]


def main():
    softwares = read_required_softwares()

    print(f"Loaded {len(softwares)} software entries.")

    for software in softwares:
        print(
            f"Software: {software['name']} | "
            f"Requested version: {software['version'] or 'Not specified'}"
        )

    print("\nCSV loading completed successfully.")


if __name__ == "__main__":
    main()