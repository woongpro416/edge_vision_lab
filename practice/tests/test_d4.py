from d4_numpy_matplotlib import (
    build_detection_dataframe,
    filter_by_confidence,
    count_by_class,
    save_class_count_plot,
)

import pandas as pd


def test_filter_by_confidence_removes_low_confidence_rows():
    df = build_detection_dataframe()
    filtered_df = filter_by_confidence(df, min_confidence=0.5)

    assert (filtered_df["confidence"] >= 0.5).all()
    assert len(filtered_df) == 3


def test_count_by_class_after_filtering():
    df = build_detection_dataframe()
    filtered_df = filter_by_confidence(df, min_confidence=0.5)
    counts_df = count_by_class(filtered_df)

    assert "className" in counts_df.columns
    assert "counts" in counts_df.columns

    person_row = counts_df[counts_df["className"] == "person"]
    person_count = person_row["counts"].iloc[0]
    assert person_count == 2

    baggage_row = counts_df[counts_df["className"] == "baggage"]
    baggage_count = baggage_row["counts"].iloc[0]
    assert baggage_count == 1


def test_save_class_count_plot_creates_png_file(tmp_path):
    counts_df = pd.DataFrame(
        [
            {"className": "person", "counts": 2},
            {"className": "baggage", "counts": 1},
        ]
    )

    output_path = tmp_path / "class_counts.png"
    save_class_count_plot(counts_df, output_path)

    assert output_path.exists()
    assert output_path.suffix == ".png"
