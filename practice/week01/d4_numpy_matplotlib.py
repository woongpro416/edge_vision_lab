# ?? ??: Day 04 ? NumPy ??? detection DataFrame?matplotlib ???? ?????.

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

COLUMNS = ["image_id", "className", "confidence", "zone"]


def practice_numpy_basics() -> None:
    arr1 = np.array([1, 2, 3])
    print(arr1.shape)
    print(arr1.dtype)
    print(arr1[0])

    arr2 = np.array([[1, 2], [3, 4]])
    print(arr2.shape)
    print(arr2.dtype)
    print(arr2[1, 1])

    f_arr = np.array([0.91, 0.6])
    print(f_arr.shape)
    print(f_arr.dtype)


def build_detection_dataframe() -> pd.DataFrame:
    rows = [
        {"image_id": "img001", "className": "person", "confidence": 0.91, "zone": "T1"},
        {"image_id": "img002", "className": "baggage", "confidence": 0.76, "zone": "T1"},
        {"image_id": "img003", "className": "vehicle", "confidence": 0.42, "zone": "T2"},
        {"image_id": "img004", "className": "person", "confidence": 0.88, "zone": "T2"},
        {"image_id": "img005", "className": "baggage", "confidence": 0.31, "zone": "T1"},
    ]

    df = pd.DataFrame(rows, columns=COLUMNS)
    return df


def filter_by_confidence(df: pd.DataFrame, min_confidence: float) -> pd.DataFrame:
    mask = df["confidence"] >= min_confidence
    conf = df[mask]
    return conf


def count_by_class(df: pd.DataFrame) -> pd.DataFrame:
    counts_df = df.groupby("className").size().reset_index(name="counts")
    return counts_df


def save_class_count_plot(counts_df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    x = counts_df["className"]
    y = counts_df["counts"]

    plt.bar(x, y)
    plt.title("Detection Count by Class")
    plt.xlabel("ClassName")
    plt.ylabel("Count")
    plt.savefig(output_path)
    plt.close()


if __name__ == "__main__":
    practice_numpy_basics()

    df = build_detection_dataframe()

    filtered_df = filter_by_confidence(df, min_confidence=0.5)
    counts_df = count_by_class(filtered_df)
    output_path = Path("outputs/class_counts.png")
    save_class_count_plot(counts_df, output_path)

    assert (filtered_df["confidence"] >= 0.5).all()
    assert "className" in counts_df.columns
    assert "counts" in counts_df.columns
    assert output_path.exists()
