from pathlib import Path
import pandas as pd

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
COLUMNS = ["file_name", "extension", "file_path", "size_bytes"]

def scan_image_files(folder_path: str) -> pd.DataFrame:
    folder = Path(folder_path)

    if not folder.is_dir():
        raise ValueError(f"폴더가 존재하지 않습니다")

    rows = []

    for item in folder.iterdir():
        if item.is_file():
            if item.suffix.lower() in IMAGE_EXTENSIONS:
                files_info = {
                    "file_name": item.name,
                    "extension": item.suffix.lower(),
                    "file_path": str(item),
                    "size_bytes": item.stat().st_size,
                }
                rows.append(files_info)
    return pd.DataFrame(rows, columns=COLUMNS)


def test_missing_folder():
    try:
        scan_image_files("data/not_exists")
        assert False
    except ValueError:
        assert True


def test_empty_folder():
    df = scan_image_files("data/empty_images")
    assert len(df) == 0
    assert list(df.columns) == COLUMNS


def test_mixed_files():
    df = scan_image_files("data/mixed_files")
    extensions = list(df["extension"])

    assert ".txt" not in extensions
    for ext in extensions:
        assert ext in IMAGE_EXTENSIONS


def test_uppercase_extensions():
    df = scan_image_files("data/case_images")
    extensions = list(df["extension"])

    assert len(df) == 3
    for ext in extensions:
        assert ext in IMAGE_EXTENSIONS


def test_image_folder():
    df = scan_image_files("data/images")
    assert len(df) >= 1
    assert df.loc[0, "extension"] in IMAGE_EXTENSIONS

if __name__ == "__main__":
    df = scan_image_files("data/images")
    print(df)

    test_missing_folder()
    test_empty_folder()
    test_mixed_files()
    test_uppercase_extensions()
    test_image_folder()
    print("모든 테스트 통과")