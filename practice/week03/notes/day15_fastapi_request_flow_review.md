# Day 15 — FastAPI Request → Endpoint → Helper → Response 흐름 복습

## 오늘 다시 이해한 핵심

FastAPI가 filtering을 수행하는 것이 아니라, 외부 HTTP 요청과 내부 Python 처리 로직을 연결한다. Client가 보낸 confidence threshold는 Request DTO에서 먼저 검증되고, Endpoint는 검증된 threshold만 Helper에 전달한다. Helper는 filtering을 수행한 뒤 InferenceResponse 계약을 만족하는 결과를 반환한다.

## 공항 관제 예시와 Data Flow

공항 관제 Dashboard가 confidenceThreshold 0.8을 보내면 vehicle(0.87)만 남고 person(0.76)은 제외된다.

    Client
    → HTTP JSON
    → FastAPI
    → PredictMockRequest validation
    → Endpoint
    → threshold: float
    → Helper
    → InferenceResponse
    → FastAPI JSON response
    → Client

## 역할과 자료형

- Request DTO: 외부 request JSON이 필요한 필드와 0.0~1.0 범위를 만족하는지 검사한다.
- Endpoint: request: PredictMockRequest에서 threshold: float를 꺼내 Helper에 전달한다.
- Helper: threshold: float를 받아 raw_results와 filtered_results를 만들고 InferenceResponse를 반환한다.
- Response DTO: Dashboard·Alert System·Spring Backend가 약속된 필드와 자료형의 결과를 받게 한다.

## 정상·실패 흐름

- threshold 0.8: raw 2개 중 vehicle만 남아 filtered 1개가 된다.
- threshold 0.7: vehicle과 person이 모두 남아 filtered 2개가 된다.
- threshold 1.1: Request DTO validation이 Endpoint 실행 전에 실패하므로 Helper까지 전달되지 않는다.

## 직접 구현과 테스트

- 직접 구현: PredictMockRequest, mock Helper의 raw → filtered → response 흐름, Test 2의 invalid request 검증.
- 도움을 받아 복습: Endpoint와 TestClient 요청 문법을 역할·입출력 계약으로 다시 정리했다.
- pytest 결과: 정상 threshold 0.8과 invalid threshold 1.1 테스트 2개가 통과했다.

## 운영 연결과 한계

실제 운영에서는 일반 Client가 threshold를 자유롭게 바꾸게 하기보다 서버 정책, 관리자 설정, camera별 configuration, 권한으로 관리할 수 있다. 오늘은 mock detections만 다뤘으며 이미지 업로드, OpenCV, YOLO/ONNX는 구현하지 않았다.

## 면접식 설명

FastAPI POST endpoint에서 Pydantic Request DTO로 Client 입력을 validation하고, Endpoint는 HTTP contract를 Helper에 연결했다. Helper는 threshold filtering과 response DTO 생성을 담당하게 분리해 HTTP 없이도 테스트·재사용할 수 있게 했다.

## 추천 commit message

`feat: add FastAPI request flow review and tests`

## Day 16 이동 Gate

Client부터 Client까지의 흐름, Endpoint와 Helper의 책임 차이, validation이 business logic 전에 필요한 이유, 핵심 블록 재작성까지 4개 항목을 모두 설명할 수 있었다. 다음 진도는 사용자가 원할 때만 시작한다.
