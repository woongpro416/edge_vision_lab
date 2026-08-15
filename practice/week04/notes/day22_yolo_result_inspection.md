# Day 22 학습일지 — 실제 YOLO Result와 Service Adapter 연결

1. 오늘 목표: YOLO result와 Adapter 연결을 이해했다.
2. 새 핵심: `Results`/`Boxes`에서 bbox, class id, confidence를 읽는다.
3. mock 차이: `raw_results`는 서비스 dict, 실제 결과는 library 객체와 tensor 값이다.
4. Data Flow: image → preprocess → Result → Adapter → raw_results → filtering → `DetectionResult`.
5. 자료형 경계: 외부 값을 Python `list`, `int`, `float`, `dict`로 변환한다.
6. Adapter 역할: key mapping과 class name 조회만 담당하며 threshold는 모른다.
7. 구현 코드: `zip()`, bbox/id int 변환, names mapping, Day 21 Adapter 재사용.
8. pytest: field 변환과 기존 pipeline 연결 테스트 2개가 통과했다.
9. 직접 구현: 반복·변환·append와 review 실행을 직접 작성했다.
10. Codex 도움: 공식 구조, 함수 계약, TODO 순서, 테스트 피드백을 지원받았다.
11. 막힌 개념: object/dict, `zip()`, float bbox와 `list[int]` DTO 경계.
12. 현재 한계: `ultralytics` 미설치이며 int bbox는 소수점 정밀도를 잃을 수 있다.
13. 다음 학습: 실제 `Results` 확인 뒤 같은 Adapter 경계를 연결한다.
14. 면접 설명: 모델 변경은 Adapter에 격리하고 raw contract와 DTO/API를 유지한다.
