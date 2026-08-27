"""
Portfolio-safe example
Project 02 — CSV to SQL Server ETL Automation
"""

from __future__ import annotations

import logging
import os
import traceback
from datetime import datetime
from pathlib import Path

import pandas as pd
import pyodbc


LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / f"etl_{datetime.now():%Y%m%d_%H%M%S}.log"

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

INPUT_DIR = Path(os.getenv("PORTFOLIO_INPUT_DIR", "./data"))
FILE_PREFIX = os.getenv("PORTFOLIO_FILE_PREFIX", "report_part_")
TARGET_TABLE = os.getenv("PORTFOLIO_TARGET_TABLE", "dbo.portfolio_transactions")

DB_CONFIG = {
    "server": os.getenv("PORTFOLIO_SQL_SERVER", "localhost"),
    "database": os.getenv("PORTFOLIO_SQL_DATABASE", "portfolio"),
    "trusted_connection": os.getenv("PORTFOLIO_TRUSTED_CONNECTION", "yes"),
    "trust_server_certificate": os.getenv("PORTFOLIO_TRUST_SERVER_CERTIFICATE", "yes"),
}


def log_and_print(level: str, message: str) -> None:
    print(message)
    getattr(logging, level.lower())(message)


def clean_column(column: str) -> str:
    column = str(column).strip().replace("\ufeff", "")
    column = column.replace(" ", "_").replace(".", "").replace("-", "_")
    column = "".join(c for c in column if c.isalnum() or c == "_")
    return column[:128] if column else "COL"


def dedupe_columns(columns: list[str]) -> list[str]:
    seen: dict[str, int] = {}
    output: list[str] = []

    for column in columns:
        if column not in seen:
            seen[column] = 0
            output.append(column)
        else:
            seen[column] += 1
            output.append(f"{column}_{seen[column]}")

    return output


def detect_delimiter_and_encoding(file_path: Path) -> tuple[str, str]:
    for encoding in ("utf-8-sig", "latin-1"):
        try:
            with file_path.open("r", encoding=encoding) as file:
                first_line = file.readline()
                delimiter = "," if first_line.count(",") > first_line.count(";") else ";"
                return delimiter, encoding
        except UnicodeDecodeError:
            continue

    raise ValueError("Unable to detect a supported text encoding.")


def build_connection_string(config: dict, driver: str) -> str:
    return (
        f"DRIVER={{{driver}}};"
        f"SERVER={config['server']};"
        f"DATABASE={config['database']};"
        f"Trusted_Connection={config['trusted_connection']};"
        f"TrustServerCertificate={config['trust_server_certificate']};"
    )


def connect_with_fallback(config: dict):
    drivers = [
        "ODBC Driver 18 for SQL Server",
        "ODBC Driver 17 for SQL Server",
        "SQL Server",
    ]

    last_error = None
    for driver in drivers:
        try:
            connection = pyodbc.connect(build_connection_string(config, driver), timeout=15)
            log_and_print("info", f"Connected using: {driver}")
            return connection
        except Exception as error:
            last_error = error
            logging.debug("Driver %s failed: %s", driver, error)

    raise RuntimeError("No compatible SQL Server ODBC driver could connect.") from last_error


def upload_csv_to_sql(csv_file: Path, table: str, config: dict, batch_size: int = 5000) -> None:
    delimiter, encoding = detect_delimiter_and_encoding(csv_file)

    df = pd.read_csv(
        csv_file,
        delimiter=delimiter,
        encoding=encoding,
        on_bad_lines="skip",
        dtype=str,
    )

    if df.empty:
        log_and_print("warning", "Input file is empty.")
        return

    clean_columns = dedupe_columns([clean_column(c) for c in df.columns])
    df.columns = clean_columns

    df = df.apply(lambda column: column.astype(str).str.strip())
    df = df.replace({"": pd.NA, "nan": pd.NA, "NaN": pd.NA, "None": pd.NA, "<NA>": pd.NA})
    df = df.astype(object).where(pd.notna(df), None)

    with connect_with_fallback(config) as connection:
        cursor = connection.cursor()
        cursor.fast_executemany = True

        columns_sql = ", ".join(f"[{column}] NVARCHAR(MAX) NULL" for column in clean_columns)
        cursor.execute(
            f"""
            IF OBJECT_ID('{table}', 'U') IS NULL
            BEGIN
                CREATE TABLE {table} (
                    {columns_sql}
                );
            END
            """
        )
        connection.commit()

        placeholders = ", ".join(["?"] * len(clean_columns))
        column_names = ", ".join(f"[{column}]" for column in clean_columns)
        insert_sql = f"INSERT INTO {table} ({column_names}) VALUES ({placeholders})"

        values = df.values.tolist()
        inserted = 0

        for start in range(0, len(values), batch_size):
            batch = values[start:start + batch_size]
            batch_data = [[None if value is None else str(value) for value in row] for row in batch]

            cursor.executemany(insert_sql, batch_data)
            connection.commit()

            inserted += len(batch_data)
            log_and_print("info", f"Processed {inserted:,} / {len(values):,} rows.")

    log_and_print("info", f"ETL completed. Total rows inserted: {inserted:,}")


def latest_matching_csv(folder: Path, prefix: str) -> Path:
    files = [
        path
        for path in folder.iterdir()
        if path.is_file() and path.name.startswith(prefix) and path.suffix.lower() == ".csv"
    ]

    if not files:
        raise FileNotFoundError(f"No CSV files starting with '{prefix}' were found in {folder}")

    return max(files, key=lambda path: path.stat().st_mtime)


def main() -> int:
    try:
        latest_file = latest_matching_csv(INPUT_DIR, FILE_PREFIX)
        log_and_print("info", f"Latest file: {latest_file.name}")
        upload_csv_to_sql(latest_file, TARGET_TABLE, DB_CONFIG)
        return 0
    except Exception:
        logging.error(traceback.format_exc())
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
