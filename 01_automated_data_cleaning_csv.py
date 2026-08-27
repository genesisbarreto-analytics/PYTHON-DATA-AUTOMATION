"""
Portfolio-safe example
Project 01 — Automated Data Cleaning & CSV Generation
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from urllib.parse import quote

import pandas as pd


DEFAULT_IMAGE_URL = "https://example.com/assets/campaign-image.png"

REQUIRED_COLUMNS = {
    "session_id",
    "customer_id",
    "user_id",
    "phone",
    "name",
    "subtype",
}


def encode_value(value: object) -> str:
    text = "" if value is None else str(value).strip()
    return quote(text, safe="")


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    mapping = {
        "IDSesion": "session_id",
        "RutUsuario": "user_id",
        "RutAmdocs": "customer_id",
        "Telefono": "phone",
        "Nombre": "name",
        "SubType": "subtype",
    }
    return df.rename(columns={k: v for k, v in mapping.items() if k in df.columns})


def build_parameters(row: pd.Series) -> str:
    params = [
        ("customer", row["customer_id"]),
        ("user", row["user_id"]),
        ("name", row["name"]),
        ("session", row["session_id"]),
        ("subtype", row["subtype"]),
        ("phone", row["phone"]),
    ]
    return "&" + "&".join(f"{key}={encode_value(value)}" for key, value in params)


def generate_campaign_csv(source_file: Path, image_url: str, output_file: Path | None = None) -> Path:
    if not source_file.exists():
        raise FileNotFoundError(f"Source file not found: {source_file}")

    df = pd.read_excel(source_file, dtype=str, keep_default_na=False)
    df = normalize_columns(df)

    missing = sorted(REQUIRED_COLUMNS.difference(df.columns))
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(missing))

    for column in REQUIRED_COLUMNS:
        df[column] = df[column].astype(str).str.strip()

    valid_mask = df["phone"].str.fullmatch(r"569\d+")
    valid_rows = df.loc[valid_mask].copy()

    result = pd.DataFrame({
        "phone": valid_rows["phone"],
        "image_url": image_url,
    })
    result["payload"] = valid_rows.apply(build_parameters, axis=1)

    if output_file is None:
        output_file = source_file.with_name(f"{source_file.stem}_portfolio_output.csv")

    result.to_csv(
        output_file,
        index=False,
        encoding="utf-8",
        quoting=csv.QUOTE_MINIMAL,
        lineterminator="\n",
    )

    if not result["phone"].str.fullmatch(r"569\d+").all():
        raise RuntimeError("Validation failed: invalid phone values found.")

    if len(result) != int(valid_mask.sum()):
        raise RuntimeError("Validation failed: unexpected row count.")

    print(f"Output file: {output_file}")
    print(f"Source rows: {len(df):,}")
    print(f"Included rows: {len(result):,}")
    print(f"Excluded rows: {len(df) - len(result):,}")

    return output_file


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a validated campaign CSV from an Excel source.")
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--image-url", default=DEFAULT_IMAGE_URL)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    generate_campaign_csv(args.source, args.image_url, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
