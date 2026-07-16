from pathlib import Path
import pandas as pd

rows = [
    {
        "file_name": "a.jpg",
        "extension": ".jpg",
        "file_path": "images/a.jpg",
        "size_bytes": 100,
    },
    {
        "file_name": "b.png",
        "extension": ".png",
        "file_path": "/images/b.png",
        "size_bytes": 300,
    },
    {
        "file_name": "c.jpg",
        "extension": ".jpg",
        "file_path": "/images/c.jpg",
        "size_bytes": 200,
    }
]

COLUMNS = ["file_name", "extension", "file_path", "size_bytes"]

df = pd.DataFrame(rows, columns=COLUMNS)
print(df)

# TODO: extension 별 개수 세기
counts = df.groupby("extension").size().reset_index(name="counts")
print(counts)

#TODO : size_bytes 내림차순 정렬
sorted_df = df.sort_values("size_bytes", ascending=False)
print(sorted_df)

#TODO: size_bytes가 200 이상인지 mask 만들기
mask = df["size_bytes"] >= 200
print(mask)
#TODO: mask로 필터링하기
filtered_df = df[mask]
print(filtered_df)

#TODO: review.csv로 다시 저장하기
df.to_csv("review.csv", index=False)

#TODO1 :counts 에서 .jpg 개수가 2인지 확인
jpg_row = counts[counts["extension"] == ".jpg"]
jpg_count = jpg_row["counts"].iloc[0]
assert jpg_count == 2
#TODO2: sorted_df의 size_bytes 순서가 [300, 200, 100] 인지 확인
assert list(sorted_df["size_bytes"]) == [300, 200, 100]
#TODO3: filter_df의 size_bytes가 모두 200 이상인지 확인
assert (filtered_df["size_bytes"] >= 200).all()

