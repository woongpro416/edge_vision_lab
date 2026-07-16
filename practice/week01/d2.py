from pathlib import Path
import pandas as pd

COLUMNS = ["file_name", "extension", "file_path", "size_bytes"]

def build_sample_dataframe() -> pd.DataFrame:
    rows = [
        {
            "file_name": "airport_01.jpg",
            "extension": ".jpg",
            "file_path": "images/airport_01.jpg",
            "size_bytes": 300_000,
        },
        {
            "file_name": "gate_02.png",
            "extension": ".png",
            "file_path": "images/gate_02.png",
            "size_bytes": 820_000,
        },
        {
            "file_name": "runway_03.jpg",
            "extension": ".jpg",
            "file_path": "images/runway_03.jpg",
            "size_bytes": 1_200_000,
        },
        {
            "file_name": "vehicle_04.jpeg",
            "extension": ".jpeg",
            "file_path": "images/vehicle_04.jpeg",
            "size_bytes": 410_000,
        },
    ]

    #TODO: rows를 DataFrame으로 변환하세요.
    df = pd.DataFrame(rows)
    #TODO: 컬럼 순서를 COLUMNS 기준으로 맞추세요.
    df = df[COLUMNS]
    return df

def count_by_extension(df: pd.DataFrame) -> pd.DataFrame:
    #TODO: extension별 파일 개수를 계산하세요.
    #힌트: groupby("extension").size()
    grouped_df = df.groupby("extension").size().reset_index(name="counts")
    return grouped_df

def sort_by_desc(df: pd.DataFrame) -> pd.DataFrame:
    #TODO: size_bytes 기준 내림차순 정렬하세요.
    sorted_df = df.sort_values("size_bytes", ascending=False)
    return sorted_df

def filter_large_files(df: pd.DataFrame, min_size_bytes: int) -> pd.DataFrame:
    #TODO: size_bytes가 min_size_bytes 이상인 행만 변환하세요
    mask = df["size_bytes"] >= min_size_bytes
    filter_df = df[mask]
    return filter_df

def save_csv(df: pd.DataFrame, output_path: Path) -> None:
    #TODO: 부모 폴더가 없으면 생성하세요.
    output_path.parent.mkdir(parents=True, exist_ok=True)
    #TODO: index 없이 CSV로 저장하세요.
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    df = build_sample_dataframe()

    extension_counts = count_by_extension(df)
    sorted_df = sort_by_desc(df)
    large_files = filter_large_files(df, min_size_bytes=500_000)

    save_csv(extension_counts, Path("outputs/day02_extension_counts.csv"))
    save_csv(large_files, Path("outputs/day02_large_files.csv"))


    print("==========================")
    print(df)
    print("==========================")
    print(count_by_extension)
    print("==========================")
    print(large_files)
    print("==========================")
    print(sorted_df)
    print("==========================")
    
    #TODO: assert 3개 작성
    #1. 전체 row 개수 확인
    assert len(df) == 4
    #2. .jpg 개수 확인
    jpg_count = (df["extension"] == ".jpg").sum()
    assert jpg_count == 2
    #3. large_files에 500_000 미만 파일이 없는지 확인
    assert (large_files["size_bytes"] >= 500_000).all()

    assert sorted_df.iloc[0]["file_name"] == "runway_03.jpg"