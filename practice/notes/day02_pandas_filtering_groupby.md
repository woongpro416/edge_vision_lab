# Day 02 - pandas filtering, sorting, groupby 기초

## 배운 내용

- pandas `DataFrame`은 여러 개의 `dict` 데이터를 표 형태로 정리해준다.
- `groupby()`는 특정 컬럼의 같은 값끼리 행을 묶는 기능이다.
- `groupby("extension").size()`를 사용하면 확장자별 파일 개수를 셀 수 있다.
- `sort_values()`는 특정 컬럼 값을 기준으로 행을 정렬한다.
- `ascending=False`를 사용하면 큰 값부터 내림차순으로 정렬할 수 있다.
- pandas 조건식은 먼저 `True` / `False` 값으로 이루어진 boolean mask를 만든다.
- `df[mask]` 형태를 사용하면 조건이 `True`인 행만 남길 수 있다.
- `assert`는 조건이 맞으면 아무 출력 없이 통과하고, 조건이 틀리면 `AssertionError`를 발생시킨다.
- `to_csv(index=False)`를 사용하면 DataFrame을 CSV 파일로 저장할 때 불필요한 index 컬럼을 제외할 수 있다.

## 실습 내용

- 이미지 메타데이터 샘플 데이터를 `list[dict]` 형태로 만들었다.
- `file_name`, `extension`, `file_path`, `size_bytes` 컬럼을 가진 `DataFrame`으로 변환했다.
- `extension` 기준으로 이미지 파일 개수를 집계했다.
- `size_bytes` 기준으로 파일 크기를 내림차순 정렬했다.
- `size_bytes`가 특정 기준 이상인 파일만 boolean mask로 필터링했다.
- 분석 결과를 CSV 파일로 저장했다.
- `assert`를 사용해 전체 row 개수, `.jpg` 개수, 필터링 조건을 확인했다.
- 추가 반복 실습으로 공항 관제 이벤트 로그 데이터를 만들고 `zone`별 개수, `confidence` 정렬, `confidence >= 0.8` 필터링을 연습했다.
- Day 01 내용과 합쳐서 `pathlib`로 실제 폴더를 읽고 이미지 파일만 DataFrame으로 만든 뒤, Day 02의 분석 흐름을 적용했다.

## 핵심 정리

```text
DataFrame = 여러 행과 여러 컬럼을 가진 표 형태의 데이터

df["column"] = 특정 컬럼 하나 선택

df["column"] >= value = 각 행이 조건을 만족하는지 검사한 True/False 결과

mask = 조건 결과

df[mask] = 조건이 True인 행만 남긴 DataFrame

groupby("column").size() = column 값별 row 개수 계산

sort_values("column", ascending=False) = column 기준 내림차순 정렬
```

## 오늘 헷갈렸던 점

- `return`이 없는 함수는 계산 결과를 만들었더라도 `None`을 반환한다.
- `"item.name"`은 실제 파일 이름이 아니라 `item.name`이라는 글자 자체다.
- 실제 파일 이름을 넣으려면 따옴표 없이 `item.name`을 사용해야 한다.
- `pd.groupby(...)`가 아니라 `df.groupby(...)`를 사용해야 한다.
- `df["size_bytes"] >= min_size_bytes`는 필터링 결과가 아니라 boolean mask다.
- 실제 필터링된 DataFrame을 얻으려면 `df[mask]`를 반환해야 한다.
- `assert`는 출력용 코드가 아니라 기대 조건을 코드가 직접 검사하는 도구다.
- 조건에 맞는 행이 없으면 빈 DataFrame이 나올 수 있고, 이것은 에러가 아니라 정상적인 결과일 수 있다.

## 확인한 코드 패턴

```python
df = pd.DataFrame(rows, columns=COLUMNS)
```

`rows`를 DataFrame으로 만들고, 컬럼 순서를 `COLUMNS` 기준으로 유지한다.

```python
extension_counts = df.groupby("extension").size().reset_index(name="counts")
```

`extension` 값별로 행을 묶고, 각 확장자의 개수를 계산한 뒤 DataFrame으로 변환한다.

```python
sorted_df = df.sort_values("size_bytes", ascending=False)
```

`size_bytes` 값을 기준으로 큰 파일부터 정렬한다.

```python
mask = df["size_bytes"] >= min_size_bytes
large_files = df[mask]
```

먼저 조건 결과인 boolean mask를 만들고, 그 mask를 사용해 조건에 맞는 행만 선택한다.

```python
assert len(df) == 4
assert (large_files["size_bytes"] >= 500_000).all()
```

DataFrame의 row 개수와 필터링 결과가 기대 조건을 만족하는지 확인한다.

## Day 01과 Day 02 연결

```text
Day 01 = pathlib로 폴더를 읽고 이미지 파일 메타데이터를 수집하는 단계

Day 02 = 수집한 메타데이터 DataFrame을 pandas로 분석하는 단계
```

Day 01에서는 파일 시스템에서 `file_name`, `extension`, `file_path`, `size_bytes`를 모았다.  
Day 02에서는 이 데이터를 기준으로 확장자별 개수 계산, 파일 크기 정렬, 조건 필터링, CSV 저장을 연습했다.

## 도메인 연결

공항·관제·모빌리티 Vision 시스템에서도 모델 추론 전에 입력 폴더의 이미지 파일을 점검해야 한다.  
지원하는 확장자인지, 파일 크기가 조건에 맞는지, 처리할 이미지가 실제로 존재하는지 확인하는 과정이 필요하다.  
오늘 실습은 추론 파이프라인 앞단에서 입력 데이터 품질을 확인하고 분석 가능한 표 형태로 정리하는 기초 단계와 연결된다.

## 다음 복습 기준

```text
1. Path로 폴더를 읽는다.
2. 이미지 확장자만 골라낸다.
3. dict를 rows에 append한다.
4. rows를 DataFrame으로 만든다.
5. df["extension"] == ".jpg" 같은 조건식을 직접 출력해본다.
6. df[mask]로 조건에 맞는 행만 남긴다.
```
