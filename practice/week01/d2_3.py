# 학습 요약: Day 02~03 — pandas DataFrame을 만들고 CSV로 저장·읽기를 연습한다.

from pathlib import Path

import pandas as pd


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
COLUMNS = ["file_name", "extension", "file_path", "size_bytes"]


def build_image_dataframe(input_dir: Path) -> pd.DataFrame:
    rows = []

    if not input_dir.exists():
        raise FileNotFoundError(input_dir)

    for item in input_dir.iterdir():
        if not item.is_file():
            continue

        extension = item.suffix.lower()

        if extension not in IMAGE_EXTENSIONS:
            continue

        row = {
            "file_name": item.name,
            "extension": extension,
            "file_path": str(item),
            "size_bytes": item.stat().st_size,
        }
        rows.append(row)

    return pd.DataFrame(rows, columns=COLUMNS)


def count_by_extension(df: pd.DataFrame) -> pd.DataFrame:
    counts = df.groupby("extension").size().reset_index(name="counts")
    return counts


def sort_by_size_desc(df: pd.DataFrame) -> pd.DataFrame:
    sorted_df = df.sort_values("size_bytes", ascending=False)
    return sorted_df


def filter_large_files(df: pd.DataFrame, min_size_bytes: int) -> pd.DataFrame:
    if min_size_bytes < 0:
        raise ValueError("min_size_bytes must be non-negative")

    mask = df["size_bytes"] >= min_size_bytes
    return df[mask]


def save_csv(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    input_dir = Path("data/mixed_files")

    df = build_image_dataframe(input_dir)
    extension_counts = count_by_extension(df)
    sorted_df = sort_by_size_desc(df)
    large_files = filter_large_files(df, min_size_bytes=1)

    print("=== df ===")
    print(df)

    print("=== extension_counts ===")
    print(extension_counts)

    print("=== sorted_df ===")
    print(sorted_df)

    print("=== large_files ===")
    print(large_files)

    save_csv(extension_counts, Path("outputs/review2_extension_counts.csv"))
    save_csv(large_files, Path("outputs/review2_large_files.csv"))

    assert ".txt" not in set(df["extension"])
    assert set(df["extension"]).issubset(IMAGE_EXTENSIONS)
    assert (large_files["size_bytes"] >= 1).all()
    assert list(df.columns) == COLUMNS
