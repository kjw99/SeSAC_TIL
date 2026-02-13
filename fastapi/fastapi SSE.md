## SSE

SSE(Server-Sent Events)는 서버가 클라이언트에게 실시간으로 데이터를 밀어주는(push) HTTP 기반 프로토콜이다.

- 일반 API
클라이언트 → 요청 → 서버가 처리 → 응답 한 번에 전달 → 연결 종료
- SSE
클라이언트 → 요청 → 서버가 연결을 유지하면서 데이터를 여러 번 전송 → 완료 후 종료

### 언제 사용하는가?

- LLM 스트리밍
    
    ChatGPT처럼 글자가 하나씩 나타나는 것
    
- 실시간 알림
    
    새 메시지, 주문 상태 변경 등
    
- 라이브 피드
    
    주식 시세등
    

### **WebSocket과의 차이**

WebSocket은 클라이언트 ↔ 서버 양방향 통신이다.
SSE는 서버 → 클라이언트 단방향 통신이다.

LLM API처럼 "서버가 일방적으로 보내는" 상황에서는 SSE가 더 간단하고 적합하다.
HTTP 기반이라 별도 프로토콜 없이 동작하고, 자동 재연결도 브라우저가 알아서 해준다.

### SSE 프로토콜 형식

SSE의 최소 형식은 `data: 내용\n\n`이다. Content-Type은 반드시 `text/event-stream`이어야 한다.

```
data: 첫 번째 메시지

data: 두 번째 메시지
```

- `data:` 뒤에 전달할 내용을 넣는다
- 빈 줄(`\n\n`)이 하나의 이벤트가 끝났음을 의미한다

---

## 일반 API vs SSE

- 일반 API (기존 방식)

```
클라이언트: "안녕하세요라고 말해줘"
                    ↓
서버: (전체 응답을 다 만들 때까지 대기... 3초)
                    ↓
서버: "안녕하세요! 저는 AI 어시스턴트입니다." (한 번에 전달)
```

사용자는 3초 동안 **아무것도 보이지 않다가** 한꺼번에 결과를 받는다.

### SSE (스트리밍 방식)

```
클라이언트: "안녕하세요라고 말해줘"
                    ↓
서버: "안" → "녕" → "하" → "세" → "요" → "!" → ... (토큰 단위로 즉시 전달)
```

사용자는 첫 글자부터 바로 보이기 시작한다. ChatGPT가 이 방식이다.

---

## FastAPI에서 SSE 구현하기

routers/sse_router.py 생성 후 main.py 에 등록한다.

### 카운트다운 엔드포인트

`StreamingResponse`는 generator를 순회하면서 `yield`된 값을 클라이언트에게 하나씩 전송한다.

- generate()는 return 대신 yield 를 사용.
- yield는 실행되고 return 처럼 종료되는 것이 아니라 계속 진행.

```python
# routers/sse_router.py

import time
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/sse", tags=["SSE (Server-Sent Events)"])

@router.get("/countdown")
def sse_countdown():
    def generate():
        for i in range(5, 0, -1):
            # SSE 형식: "data: 내용\n\n" (빈 줄이 이벤트 구분자)
            yield f"data: {i}\n\n"
            time.sleep(1)
        yield "data: 발사!\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
```

---

### Fake LLM 스트리밍

실제 LLM API를 사용하기 전에, 동일한 패턴을 시뮬레이션하는 엔드포인트이다.

```python
@router.get("/fake-llm")
def fake_llm_stream():
    fake_response = "안녕하세요! 저는 AI 어시스턴트입니다."
    tokens = list(fake_response)  # 한 글자씩 토큰으로 분리

    def generate():
        for token in tokens:
            yield f"data: {token}\n\n"
            time.sleep(0.05)
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
```

---

## 실제 OpenAI API 스트리밍

- 라이브러리 설치

```bash
uv add openai
```

- `.env` 파일에 API 키를 추가한다.

```
OPENAI_API_KEY=sk-여기에-본인-키-입력
```

```python
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@router.get("/chat-normal")
def openai_chat_normal(message: str = "안녕하세요, 자기소개 해주세요."):
    """
    OpenAI API 일반 응답 (스트리밍 X)
    → 전체 응답이 한 번에 도착 (스트리밍과 비교용)
    """
    response = client.responses.create(
        model="gpt-4o-mini",
        instructions="2문장 이내로 대답해줘.",
        input=[{"role": "user", "content": message}],
    )
    return {"message": response.output_text}
    
    
@router.get("/chat")
def openai_chat(message: str = "안녕하세요, 자기소개 해주세요."):
    """
    실제 OpenAI API 스트리밍
    → GPT가 생성하는 답변이 토큰 단위로 실시간 도착
    """
    stream = client.responses.create(
        model="gpt-4o-mini",
        instructions="2문장 이내로 대답해줘.",
        input=[{"role": "user", "content": message}],
        stream=True,
    )

    def generate():
        for event in stream:
            if event.type == "response.output_text.delta":
                yield f"data: {event.delta}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")

```