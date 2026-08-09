# 학습 요약: Day 03 테스트 — pandas DataFrame 처리와 CSV 동작을 pytest로 검증한다.

from d2_3 import build_image_dataframe,count_by_extension, sort_by_size_desc, filter_large_files, COLUMNS, save_csv
import pytest
import pandas as pd



def test_build_image_dataframe_filters_only_images(tmp_path):


    (tmp_path / "a.jpg").write_bytes(b"fake image")


    (tmp_path / "b.PNG").write_bytes(b"fake image")

    (tmp_path / "memo.txt").write_text("not image")

    df = build_image_dataframe(tmp_path)

    extensions = set(df["extension"])

    assert ".jpg" in extensions

    assert ".png" in extensions

    assert ".txt" not in extensions

    assert list(df.columns) == COLUMNS

def test_empty_folder_keeps_columns(tmp_path):

    df = build_image_dataframe(tmp_path)

    assert len(df) == 0

    assert list(df.columns) == COLUMNS


def test_missing_folder_raises_file_not_found(tmp_path):

    missing_dir = tmp_path / "missing"



    with pytest.raises(FileNotFoundError):
        build_image_dataframe(missing_dir)


def test_count_by_extension():

    rows = [
    {"file_name": "a.jpg", "extension": ".jpg", "file_path": "a.jpg", "size_bytes": 100},
    {"file_name": "b.jpg", "extension": ".jpg", "file_path": "b.jpg", "size_bytes": 200},
    {"file_name": "c.png", "extension": ".png", "file_path": "c.png", "size_bytes": 300},
    ]

    df = pd.DataFrame(rows, columns=COLUMNS)

    result = count_by_extension(df)

    jpg_row = result[result["extension"] == ".jpg"]
    jpg_count = jpg_row["counts"].iloc[0]

    png_row = result[result["extension"] == ".png"]
    png_count = png_row["counts"].iloc[0]

    assert jpg_count == 2

    assert png_count == 1


def test_sort_by_size_desc():
    rows = [
        {"file_name": "a.jpg", "extension": ".jpg", "file_path": "a.jpg", "size_bytes": 100},
        {"file_name": "b.png", "extension": ".png", "file_path": "b.png", "size_bytes": 300},
        {"file_name": "c.jpg", "extension": ".jpg", "file_path": "c.jpg", "size_bytes": 200},
    ]

    df = pd.DataFrame(rows, columns=COLUMNS)

    sorted_df = sort_by_size_desc(df)

    sizes = list(sorted_df["size_bytes"])

    assert sizes == [300, 200, 100]

def test_filter_large_files():

    rows = [
        {"file_name": "a.jpg", "extension": ".jpg", "file_path": "a.jpg", "size_bytes": 100},
        {"file_name": "b.png", "extension": ".png", "file_path": "b.png", "size_bytes": 200},
        {"file_name": "c.jpg", "extension": ".jpg", "file_path": "c.jpg", "size_bytes": 300},
    ]


    df = pd.DataFrame(rows, columns=COLUMNS)



    filtered_df = filter_large_files(df, min_size_bytes=200)



    sizes = list(filtered_df["size_bytes"])


    assert sizes == [200, 300]

def test_filter_large_files_rejects_negative_size():

    df = pd.DataFrame([], columns=COLUMNS)


    with pytest.raises(ValueError):
        filter_large_files(df, min_size_bytes=-1)


def test_save_creates_files(tmp_path):

    rows = [
        {
            "file_name": "a.jpg",
            "extension": ".jpg",
            "file_path": "a.jpg",
            "size_bytes": 100,
        }
    ]


    df = pd.DataFrame(rows, columns=COLUMNS)


    output_path = tmp_path / "outputs" / "result.csv"

    save_csv(df, output_path)


    assert output_path.exists()
