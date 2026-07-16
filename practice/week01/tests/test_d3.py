from d2_3 import build_image_dataframe,count_by_extension, sort_by_size_desc, filter_large_files, COLUMNS, save_csv
import pytest
import pandas as pd



def test_build_image_dataframe_filters_only_images(tmp_path):
    # TODO: tmp_path 안에 a.jpg 파일 만들기
    # 힌트: (tmp_path / "a.jpg").write_bytes(b"fake image")
    (tmp_path / "a.jpg").write_bytes(b"fake image")
    # TODO: tmp_path 안에 b.PNG 파일 만들기
    # 힌트: 대문자 확장자가 .png로 바뀌는지 확인해야 함
    (tmp_path / "b.PNG").write_bytes(b"fake image")
    # TODO: tmp_path 안에 memo.txt 파일 만들기
    (tmp_path / "memo.txt").write_text("not image")
    # TODO: build_image_dataframe(tmp_path) 실행해서 df 변수에 저장
    df = build_image_dataframe(tmp_path)
    # TODO: df["extension"] 값을 set으로 바꾸기
    extensions = set(df["extension"])
    # TODO: ".jpg"가 있는지 assert
    assert ".jpg" in extensions
    # TODO: ".png"가 있는지 assert
    assert ".png" in extensions
    # TODO: ".txt"가 없는지 assert
    assert ".txt" not in extensions
    # TODO: 컬럼 순서가 COLUMNS와 같은지 assert
    assert list(df.columns) == COLUMNS

def test_empty_folder_keeps_columns(tmp_path):
    # TODO: 빈 tmp_path를 build_image_dataframe에 넣기
    df = build_image_dataframe(tmp_path)
    # TODO: row 개수가 0인지 확인
    assert len(df) == 0
    # TODO: 컬럼 순서가 COLUMNS와 같은지 확인
    assert list(df.columns) == COLUMNS


def test_missing_folder_raises_file_not_found(tmp_path):
    # TODO: tmp_path / "missing" 경로 만들기
    missing_dir = tmp_path / "missing"
    # TODO: 실제 폴더는 만들지 않기

    # TODO: pytest.raises(FileNotFoundError)로 build_image_dataframe 실행
    with pytest.raises(FileNotFoundError):
        build_image_dataframe(missing_dir)


def test_count_by_extension():
    # TODO: rows 만들기
    rows = [
    {"file_name": "a.jpg", "extension": ".jpg", "file_path": "a.jpg", "size_bytes": 100},
    {"file_name": "b.jpg", "extension": ".jpg", "file_path": "b.jpg", "size_bytes": 200},
    {"file_name": "c.png", "extension": ".png", "file_path": "c.png", "size_bytes": 300},
    ]
    # TODO: pd.DataFrame(rows, columns=COLUMNS)로 df 만들기
    df = pd.DataFrame(rows, columns=COLUMNS)
    # TODO: count_by_extension(df) 실행
    result = count_by_extension(df)
    # TODO: .jpg 행만 선택
    jpg_row = result[result["extension"] == ".jpg"]
    jpg_count = jpg_row["counts"].iloc[0]
    # TODO: .png 행만 선택
    png_row = result[result["extension"] == ".png"]
    png_count = png_row["counts"].iloc[0]
    # TODO: .jpg count가 2인지 assert
    assert jpg_count == 2
    # TODO: .png count가 1인지 assert
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
    # TODO: 크기가 100, 200, 300인 파일 rows 만들기
    rows = [
        {"file_name": "a.jpg", "extension": ".jpg", "file_path": "a.jpg", "size_bytes": 100},
        {"file_name": "b.png", "extension": ".png", "file_path": "b.png", "size_bytes": 200},
        {"file_name": "c.jpg", "extension": ".jpg", "file_path": "c.jpg", "size_bytes": 300},
    ]

    # TODO: rows를 DataFrame으로 바꾸기
    df = pd.DataFrame(rows, columns=COLUMNS)

    # TODO: min_size_bytes=200으로 filter_large_files 실행
    # 힌트: filtered_df = filter_large_files(df, min_size_bytes=200)
    filtered_df = filter_large_files(df, min_size_bytes=200)

    # TODO: filtered_df의 size_bytes 컬럼을 list로 꺼내기
    # 힌트: sizes = list(filtered_df["size_bytes"])
    sizes = list(filtered_df["size_bytes"])

    # TODO: 200 이상인 [200, 300]만 남았는지 확인
    assert sizes == [200, 300]

def test_filter_large_files_rejects_negative_size():
    #TODO: 빈 DataFrame 만들기
    df = pd.DataFrame([], columns=COLUMNS)

    #TODO: pytest.raises(ValueError) 안에서 filter_large_files 실행
    with pytest.raises(ValueError):
        filter_large_files(df, min_size_bytes=-1)


def test_save_creates_files(tmp_path):
    #TODO: 샘플 rows 만들기
    rows = [
        {
            "file_name": "a.jpg",
            "extension": ".jpg",
            "file_path": "a.jpg",
            "size_bytes": 100,
        }
    ]

    #TODO: rows를 dataFrame으로 바꾸기
    df = pd.DataFrame(rows, columns=COLUMNS)

    #TODO: output_path = tmp_path / "outputs" / "result.csv" 만들기
    output_path = tmp_path / "outputs" / "result.csv"
    #TODO: save_csv(df, output_path) 실행
    save_csv(df, output_path)

    #TODO: output_path.exists()가 True 인지 assert
    assert output_path.exists()