# Day 26 — Detection Data Contract 독립 구현

## 오늘 목표

여러 Detection을 confidence 기준으로 filtering하는 작은 Python Service를 요구사항만 보고 설계한다. 구현 전에 한 건과 여러 건의 자료형, 함수 Input/Output, Empty Contract를 먼저 결정하고 Happy/Empty pytest로 동작을 검증한다.

## 요구사항

- 한 Detection은 `bbox`, `class_id`, `className`, `confidence` 정보를 가진다.
- 여러 Detection과 `threshold`를 입력받는다.
- `confidence >= threshold`인 Detection만 반환한다.
- Detection이 0건이면 빈 목록을 반환한다.

## 구현 전에 결정한 계약

```text
Detection 한 건: dict
Detection 여러 건: list[dict]
Input: detections(list[dict]), threshold(float)
Output: filtered detections(list[dict])
Empty: [] -> []
```

## `dict`와 `list[dict]` 선택 이유

한 Detection은 필드 이름과 값을 연결해야 하므로 `dict`가 자연스럽다. 예를 들어 `confidence`라는 key로 confidence 값을 읽을 수 있다. 여러 Detection은 0건, 1건, 여러 건을 같은 방식으로 순회해야 하므로 `list[dict]`로 표현한다.

`None`은 결과 목록이 없거나 생성되지 않았다는 다른 상태로 해석될 수 있다. 반면 `[]`는 함수가 정상 실행되었지만 Detection이 0건이라는 뜻이므로, downstream은 별도 `None` 분기 없이 항상 결과를 순회할 수 있다.

## 구현한 Data Flow

```text
detections(list[dict]) + threshold(float)
→ filtering service
→ filtered detections(list[dict])
```

학습용 공항 제한구역 CCTV 흐름에서는 다음처럼 생각할 수 있다.

```text
Camera / Vision Model
→ Adapter
→ 여러 Detection
→ Filtering Service
→ Dashboard / Alarm에 사용할 Detection 목록
```

이는 실제 공항 운영 시스템이 아니라 Data Contract와 Service 책임을 이해하기 위한 학습 예시다.

## 첫 구현 결과

`d26.py`에 filtering 함수를 작성하고 `test_d26.py`에 Happy/Empty pytest를 분리했다. 함수는 입력 목록을 수정하지 않고 새 `results` 목록에 조건을 통과한 원본 Detection dict를 담아 반환한다.

Happy case에서는 confidence `0.87`, `0.72`, `0.62`와 threshold `0.8`을 사용했고, `0.87`인 Detection 1건만 남는지 확인했다. Empty case에서는 `[]` 입력이 `[]`로 반환되는지 확인했다.

## 구현 중 발생한 오류와 원인

- 목록 변수와 반복 중 꺼낸 한 건의 변수 이름을 단수/복수로 섞어 사용했다. 목록은 `list[dict]`, 반복값은 `dict`라는 자료형 관계를 다시 확인했다.
- `dict`인 Detection에 NumPy 배열용 `tolist()`를 적용하려고 했다. 오늘 Detection 계약은 이미 Python `dict`이므로 변환이 필요하지 않았다.
- 반복문 안에서 한 Detection을 바로 반환해 여러 통과 Detection을 모으지 못할 수 있었다. 결과 목록을 만든 뒤 반복이 끝난 후 반환하도록 정리했다.
- `confidence` key의 철자 불일치로 `KeyError`가 발생했다. dict key는 계약의 field 이름과 정확히 같아야 한다.
- 함수 정의만 실행하고 출력이 없다고 생각했다. 함수는 호출되어야 하며, `return` 값은 `print()`하지 않으면 터미널에 자동으로 보이지 않는다.

## pytest

`test_d26.py`에서 다음을 검증했다.

- Happy path: 결과 길이가 1이고 남은 Detection의 confidence가 `0.87`이다.
- Empty case: 빈 입력에 대해 정확히 `[]`가 반환된다.

```text
2 passed
```

Arrange는 mock Detection 목록과 threshold를 준비하는 단계다. Act는 filtering 함수를 호출하는 단계다. Assert는 반환된 목록이 기대한 결과인지 증명하는 단계다.

## Empty Case

빈 입력은 예외나 `None`이 아니라 `[]`를 반환한다. 호출하는 쪽은 결과가 0건, 1건, 여러 건이더라도 항상 `for detection in results`처럼 같은 방식으로 처리할 수 있다.

## 직접 다시 재구현한 결과

`d26_review.py`와 `d26_final.py`에서 기존 구현 파일을 보지 않고 filtering 함수를 다시 작성했다. 함수 이름과 실행용 helper 구조는 달랐지만, Input Contract, Output Contract, Empty Contract, filtering 조건은 첫 구현과 같게 재현했다.

`d26_final.py`의 pytest 실행은 통과했지만 test 함수가 list를 반환해 warning이 발생했다. pytest test 함수는 `assert`로 검증하고 반환값 없이 끝나야 한다는 점을 확인했다. 실제 pytest 파일은 `tests/test_d26.py`로 유지한다.

## Invalid Contract 판단

- `threshold = "0.8"`처럼 문자열이 들어오는 문제는 함수 호출 전 Request Validation 경계에서 막는 것이 자연스럽다.
- Detection dict에 `confidence` key가 없다면 Adapter 또는 이전 단계가 Detection 계약을 깨뜨린 것이다.

오늘 filtering 함수는 유효한 `list[dict]`와 `float` threshold를 받는다고 가정하고 filtering 책임에 집중했다.

## 오늘 스스로 결정한 부분

- 한 Detection은 `dict`, 여러 Detection은 `list[dict]`로 표현한다.
- Empty 결과는 `None` 대신 `[]`로 표현한다.
- 함수 파라미터는 `detections`와 `threshold`이고, 반환값은 filtered `list[dict]`다.
- filtering 함수는 Adapter나 Detection 생성 책임을 갖지 않는다.

## 아직 부족한 부분

- 함수 호출과 함수 정의, 함수 객체와 함수 호출 결과의 차이를 더 빠르게 구분해야 한다.
- pytest test 함수의 `return`과 `assert`의 역할을 더 확실히 구분해야 한다.
- 목록과 반복값의 단수/복수 이름을 일관되게 정해야 한다.

## 다음 학습 포인트

Day 27에서는 새 기술을 추가하지 않고 confidence filtering service의 Happy, Empty, Invalid Contract pytest를 독립 구현한다. 먼저 어떤 invalid 입력을 어느 경계가 책임지는지 판단하고, 필요한 경우에만 테스트 기대 동작을 정한다.

## 면접용 설명

Detection 한 건은 `bbox`, `class_id`, `className`, `confidence`처럼 이름이 있는 속성들의 묶음이라 `dict`로 표현했다. 여러 Detection은 0건, 1건, 여러 건을 같은 방식으로 순회하기 위해 `list[dict]`로 표현했고, 결과가 없을 때는 정상적인 빈 목록을 뜻하는 `[]`를 반환했다. Filtering Service는 Adapter가 만든 Detection 목록과 threshold를 받아 confidence 조건을 통과한 원본 Detection만 새 목록으로 반환하며, pytest로 Happy와 Empty Contract를 검증했다.
