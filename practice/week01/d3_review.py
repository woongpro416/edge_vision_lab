# ?? ??: Day 03 Review ? pandas groupby????boolean mask filtering? ?????.

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


counts = df.groupby("extension").size().reset_index(name="counts")
print(counts)


sorted_df = df.sort_values("size_bytes", ascending=False)
print(sorted_df)


mask = df["size_bytes"] >= 200
print(mask)

filtered_df = df[mask]
print(filtered_df)


df.to_csv("review.csv", index=False)


jpg_row = counts[counts["extension"] == ".jpg"]
jpg_count = jpg_row["counts"].iloc[0]
assert jpg_count == 2

assert list(sorted_df["size_bytes"]) == [300, 200, 100]

assert (filtered_df["size_bytes"] >= 200).all()

