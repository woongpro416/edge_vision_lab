# Day 03 - pytest로 pandas 데이터 처리 함수 검증하기

## 배운 내용

- `pytest`는 `test_`로 시작하는 함수를 자동으로 찾아 실행한다.
- `assert`는 함수의 결과가 기대 조건을 만족하는지 코드로 확인한다.
- `tmp_path`는 실제 프로젝트 폴더를 건드리지 않는 테스트용 임시 폴더다.
- `pytest.raises()`는 잘못된 입력에서 예외가 발생하는지 확인할 때 사용한다.
- 빈 `DataFrame`이어도 `columns=COLUMNS`로 컬럼 구조를 고정하면 후속 처리 코드가 안정적으로 동작한다.
- `Path` 객체는 `/` 연산자로 하위 경로를 이어 붙일 수 있다.

## 실습 내용

- `build_image_dataframe()`이 이미지 파일만 `DataFrame`에 포함하는지 테스트했다.
- `.PNG`처럼 대문자 확장자가 `.png`로 변환되는지 확인했다.
- `.txt` 같은 비이미지 파일이 제외되는지 확인했다.
- 빈 폴더를 입력해도 row는 0개이고 컬럼 구조는 유지되는지 테스트했다.
- 존재하지 않는 폴더를 입력하면 `FileNotFoundError`가 발생하는지 테스트했다.
- `count_by_extension()`이 `.jpg` 2개, `.png` 1개를 올바르게 집계하는지 테스트했다.
- `sort_by_size_desc()`가 `size_bytes` 기준으로 `[300, 200, 100]` 순서가 되도록 정렬하는지 테스트했다.
- `filter_large_files()`가 `min_size_bytes=200` 이상인 파일만 남기는지 테스트했다.
- `min_size_bytes=-1`처럼 잘못된 인자를 넣으면 `ValueError`가 발생하는지 테스트했다.
- `save_csv()`가 없는 출력 폴더를 만들고 CSV 파일을 실제로 생성하는지 테스트했다.

## 핵심 정리

```text
pytest = assert를 test_ 함수 단위로 자동 실행하는 도구

tmp_path = 테스트용 임시 폴더 Path 객체

with pytest.raises(ErrorType):
    에러가 발생해야 하는 코드

columns=COLUMNS = 데이터가 없어도 DataFrame 컬럼 계약 유지

tmp_path / "outputs" / "result.csv" = Path 객체로 저장 경로 만들기

output_path.exists() = 해당 경로에 파일이 실제로 생겼는지 확인
```

## 오늘 헷갈렸던 점

- `python test_d3.py`로 실행하면 pytest 기능인 `tmp_path`가 동작하지 않는다.
- 테스트는 프로젝트 루트에서 `python -m pytest -q`로 실행해야 한다.
- `df["extension"]`은 컬럼 값이고, `df.columns`는 컬럼 이름 목록이다.
- `df[df["extension"] == ".jpg"]`는 조건에 맞는 행만 선택한 `DataFrame`이다.
- `.iloc[0]`은 선택된 값 목록에서 위치 기준으로 첫 번째 값을 꺼낸다.
- `test_filter_large_files()`는 pytest가 실행하는 테스트 함수이고, `filter_large_files()`는 실제로 검증할 함수다.
- `save_csv()`는 저장 작업만 하고 반환값이 없으므로 결과를 변수에 받을 필요가 없다.

## 확인한 코드 패턴

```python
extensions = set(df["extension"])
```

`extension` 컬럼의 값을 중복 없이 확인한다.

```python
assert list(df.columns) == COLUMNS
```

DataFrame의 컬럼 순서가 약속한 구조와 같은지 확인한다.

```python
jpg_row = counts_df[counts_df["extension"] == ".jpg"]
jpg_count = jpg_row["counts"].iloc[0]
```

조건에 맞는 행을 고른 뒤, 특정 컬럼에서 실제 값 하나를 꺼낸다.

```python
sizes = list(sorted_df["size_bytes"])
assert sizes == [300, 200, 100]
```

정렬 결과에서 검증에 필요한 컬럼만 리스트로 꺼내 순서를 확인한다.

```python
with pytest.raises(ValueError):
    filter_large_files(df, min_size_bytes=-1)
```

잘못된 인자에서 기대한 예외가 발생하는지 확인한다.

```python
output_path = tmp_path / "outputs" / "result.csv"
save_csv(df, output_path)
assert output_path.exists()
```

CSV 저장 후 실제 파일이 생성되었는지 확인한다.

## 복습 완료

- Day 02 pandas 패턴을 다시 손으로 입력하고 출력 결과를 확인했다.
- `print()`로 사람이 확인하던 결과를 `assert`로 바꾸는 흐름을 연습했다.
- `groupby().size().reset_index(name="counts")`, `sort_values()`, boolean mask, `df[mask]`, `to_csv(index=False)`를 다시 확인했다.
- 8개 pytest 테스트가 모두 통과하는 것을 확인했다.

## 도메인 연결

공항·관제·모빌리티 Vision 시스템에서도 이미지 수집 폴더에 비이미지 파일이 섞이거나, 빈 입력이 들어오거나, 잘못된 경로가 전달될 수 있다.  
오늘 실습은 이런 입력 검증과 후속 CSV 저장 결과를 자동 테스트로 확인해 안정적인 AI Vision 백엔드 파이프라인을 만드는 기초 단계와 연결된다.

## 다음 복습 기준

```text
1. tmp_path로 테스트용 파일 3개를 만들 수 있는가?
2. 빈 DataFrame을 columns=COLUMNS로 만들 수 있는가?
3. pytest.raises()로 예외 테스트를 작성할 수 있는가?
4. DataFrame에서 조건에 맞는 행을 고르고 값 하나를 꺼낼 수 있는가?
5. Path 객체로 output_path를 만들고 exists()로 저장 결과를 확인할 수 있는가?
```
