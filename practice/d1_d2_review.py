from pathlib import Path

import pandas as pd

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
COLUMNS = ["file_name", "extension", "file_path", "size_bytes"]

def build_image_dataframe(input_dir: Path) -> pd.DataFrame:
    rows = []

    #TODO 1: input_dir 안의 파일들을 반복문으로 순회하세요.
    #TODO 2: 파일이 아니면 건너뛰세요
    #TODO 3: 확장자를 lower()로 소문자로 변환하세요
    #TODO 4: IMAGE_EXTENSIONS 에 없는 확장자는 건너뛰세요.
    #TODO 5: file_name, extension, file_path, size_bytes를 dict로 만들고 rows 에 추가하세요.
    for item in input_dir.iterdir():
        if item.is_file():
            if item.suffix.lower() in IMAGE_EXTENSIONS:
                row = {
                    "file_name": item.name,
                    "extension": item.suffix.lower(),
                    "file_path": str(item),
                    "size_bytes": item.stat().st_size,
                }
                rows.append(row)


    #TODO 6: 빈 DataFrame일 대도 COLUMNS 구조가 유지되게 처리하세요.
    # 힌트 : pd.DataFrame(rows, coluns=COLUMNS)
    df = pd.DataFrame(rows, columns=COLUMNS)

    return df


def count_by_extension(df: pd.DataFrame) -> pd.DataFrame:
    #TODO : extension 별 개수 세기
    extension_df = df.groupby("extension").size().reset_index(name="counts")
    return extension_df

def sort_by_size_desc(df: pd.DataFrame) -> pd.DataFrame:
    #TODO : size_bytes 기준 내림차순 정렬
    sorted_df = df.sort_values("size_bytes", ascending=False)
    return sorted_df

def filter_large_files(df: pd.DataFrame, min_size_bytes: int) -> pd.DataFrame:
    mask = df["size_bytes"] >= min_size_bytes
    return df[mask]

def save_csv(df:pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    input_dir = Path("data/mixed_files")

    df = build_image_dataframe(input_dir)
    extension_counts = count_by_extension(df)
    sorted_df = sort_by_size_desc(df)
    large_files = filter_large_files(df, min_size_bytes = 1)

    print(df)
    print(extension_counts)
    print(sorted_df)
    print(large_files)


    save_csv(extension_counts,Path("outputs/review_extension_counts.csv"))
    save_csv(large_files, Path("outputs/review_large_files.csv"))

    #TODO assert 3개
    #1. .txt파일이 결과에 포함되지 않았는가?
    assert ".txt" not in set(df["extension"])
    #2. extension 컬럼 값은 전부 IMAGE_EXTENSIONS 안에 있는가?
    assert set(df["extension"]).issubset(IMAGE_EXTENSIONS)
    #3. large_files에는 min_size_bytes 미만 파일이 없는가?
    assert (large_files["size_bytes"] >= 1).all()