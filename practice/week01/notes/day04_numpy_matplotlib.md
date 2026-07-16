# Day 04 - NumPy shape와 pandas 시각화 기초

## 배운 내용

- `NumPy array`는 `shape`와 `dtype`을 가진 배열 객체다.
- Python `list`는 단순 값 목록이고, `NumPy array`는 배열의 형태와 데이터 타입을 확인할 수 있다.
- `shape`는 배열의 구조를 나타낸다. 1차원 배열은 `(개수,)`, 2차원 배열은 `(행, 열)` 형태다.
- `dtype`은 배열 안 값의 데이터 타입이다.
- `indexing`은 배열이나 DataFrame에서 위치 또는 컬럼명으로 값을 꺼내는 방식이다.
- pandas boolean mask를 사용하면 `confidence` 기준으로 detection 결과를 필터링할 수 있다.
- `groupby().size().reset_index(name="counts")`로 `className`별 탐지 개수를 집계할 수 있다.
- matplotlib `bar plot`으로 집계 결과를 png 이미지로 저장할 수 있다.

## 실습 내용

- 1차원 NumPy 배열과 2차원 NumPy 배열을 만들고 `shape`, `dtype`, indexing 결과를 출력했다.
- confidence 값을 담은 float 배열을 만들고 `float64` 타입을 확인했다.
- mock detection 데이터를 `list[dict]`로 작성한 뒤 pandas `DataFrame`으로 변환했다.
- `confidence >= 0.5` 조건으로 신뢰도 낮은 detection을 제외했다.
- 필터링된 결과를 `className` 기준으로 집계했다.
- 집계 결과를 `outputs/class_counts.png`로 저장했다.
- 같은 흐름을 `d4_review.py`에 다시 작성해 복습했다.
- pytest로 confidence 필터링, className 집계, png 파일 저장을 검증했다.

## 핵심 정리

```text
NumPy array = shape와 dtype을 가진 배열 객체

shape = 배열의 형태
1차원 shape = (개수,)
2차원 shape = (행, 열)

dtype = 배열 안 값의 데이터 타입

mask = 조건 결과로 만들어진 True/False Series
df[mask] = 조건이 True인 행만 남긴 DataFrame

groupby("className").size().reset_index(name="counts")
= className별 row 개수를 counts 컬럼으로 집계

plt.bar(x, y)
= x축 이름과 y축 값을 사용해 막대그래프 생성

plt.savefig(output_path)
= 현재 그래프를 이미지 파일로 저장
```

## 오늘 헷갈렸던 점

- `Path`는 경로 객체를 만드는 클래스이고, `Path("outputs/file.png")`가 실제 경로 객체다.
- `Path("outputs / file.png")`처럼 공백을 넣으면 의도와 다른 경로가 될 수 있다.
- plot 저장 함수에는 원본 `df`가 아니라 `className`, `counts` 컬럼이 있는 `counts_df`를 넘겨야 한다.
- `assert`는 조건이 맞으면 아무 출력 없이 통과한다.
- pandas와 matplotlib 부분이 실행되어도 `print()`가 없으면 NumPy 출력만 보일 수 있다.

## 확인한 코드 패턴

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])
print(arr.shape)
print(arr.dtype)
print(arr[1, 2])
```

2차원 배열의 형태, 데이터 타입, 특정 위치 값을 확인한다.

```python
mask = df["confidence"] >= 0.5
filtered_df = df[mask]
```

confidence 조건을 boolean mask로 만들고, 조건에 맞는 행만 선택한다.

```python
counts_df = df.groupby("className").size().reset_index(name="counts")
```

className별 탐지 개수를 DataFrame 형태로 집계한다.

```python
output_path = Path("outputs/class_counts.png")
output_path.parent.mkdir(parents=True, exist_ok=True)
plt.bar(counts_df["className"], counts_df["counts"])
plt.savefig(output_path)
plt.close()
```

집계 결과를 막대그래프로 저장한다.

## 테스트 정리

- `filter_by_confidence()`는 confidence가 낮은 detection을 제거하는지 검증했다.
- `count_by_class()`는 필터링 후 `person`과 `baggage` 개수가 맞는지 검증했다.
- `save_class_count_plot()`은 png 파일이 실제로 생성되는지 검증했다.
- Day 04 기준 총 11개 pytest 테스트가 통과했다.

## 도메인 연결

공항·관제·모빌리티 Vision 시스템에서는 탐지 결과를 confidence 기준으로 걸러내고, className별 탐지량을 시각화해 관제 대시보드의 기본 통계로 활용할 수 있다.

## 다음 복습 기준

```text
1. Python list와 NumPy array의 차이를 설명할 수 있는가?
2. 1차원과 2차원 shape를 보고 구조를 말할 수 있는가?
3. boolean mask와 df[mask]의 차이를 설명할 수 있는가?
4. className별 counts DataFrame을 만들 수 있는가?
5. matplotlib으로 png 파일을 저장하고 Path로 존재 여부를 확인할 수 있는가?
```
