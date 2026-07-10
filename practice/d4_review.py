from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

COLUMNS = ["image_id", "className", "confidence", "zone"]


def review_numpy() -> None:
    arr1 = np.array([10, 20, 30])
    print(arr1.shape)
    print(arr1.dtype)
    print(arr1[0])

    arr2 = np.array([[1, 2, 3], [4, 5, 6]])
    print(arr2.shape)
    print(arr2.dtype)
    print(arr2[1, 2])

    f_arr = np.array([0.95, 0.72, 0.41])
    print(f_arr.shape)
    print(f_arr.dtype)


def build_review_dataframe() -> pd.DataFrame:
    rows = [
        {"image_id": "cam001", "className": "person", "confidence": 0.95, "zone": "gate_a"},
        {"image_id": "cam002", "className": "vehicle", "confidence": 0.72, "zone": "road"},
        {"image_id": "cam003", "className": "baggage", "confidence": 0.41, "zone": "gate_a"},
        {"image_id": "cam004", "className": "person", "confidence": 0.83, "zone": "gate_b"},
    ]

    df = pd.DataFrame(rows, columns=COLUMNS)
    return df


def filter_review_confidence(df: pd.DataFrame, min_confidence: float) -> pd.DataFrame:
    mask = df["confidence"] >= min_confidence
    conf = df[mask]
    return conf


def count_review_classes(df: pd.DataFrame) -> pd.DataFrame:
    counts_df = df.groupby("className").size().reset_index(name="counts")
    return counts_df


def save_review_plot(counts_df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    x = counts_df["className"]
    y = counts_df["counts"]

    plt.bar(x, y)
    plt.title("Detection Count")
    plt.xlabel("ClassName")
    plt.ylabel("Count")
    plt.savefig(output_path)
    plt.close()


if __name__ == "__main__":
    review_numpy()

    df = build_review_dataframe()

    filtered_df = filter_review_confidence(df, min_confidence=0.7)
    counts = count_review_classes(filtered_df)
    output_path = Path("outputs/d4_review_class_counts.png")
    save_review_plot(counts, output_path)

    assert (filtered_df["confidence"] >= 0.7).all()
    assert {"className", "counts"}.issubset(counts.columns)
    assert output_path.exists()
