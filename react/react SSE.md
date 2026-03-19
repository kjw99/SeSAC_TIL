## 일반 요청 vs 스트리밍

- 지금까지 배운 API 요청은 **서버가 응답을 완성한 후** 한꺼번에 보내는 방식이었다
- ChatGPT처럼 글자가 하나씩 나타나는 것은 **스트리밍** 방식이다
- 서버가 데이터를 **조금씩 보내고**, 클라이언트는 **도착하는 대로** 화면에 표시한다

| 방식 | 동작 | 사용자 경험 |
| --- | --- | --- |
| 일반 요청 | 서버가 전부 완성 → 한꺼번에 전송 | 기다림... → 결과가 한 번에 나타남 |
| 스트리밍 | 서버가 만드는 대로 → 조금씩 전송 | 글자가 실시간으로 나타남 |
- AI 챗봇에서 스트리밍이 중요한 이유:
    - LLM 응답은 수 초가 걸리는데, 일반 요청이면 그동안 화면이 멈춘 것처럼 보인다
    - 스트리밍이면 첫 글자가 바로 나타나므로 사용자가 기다리는 느낌이 줄어든다

---

## SSE (Server-Sent Events)

- 서버에서 클라이언트로 **한 방향으로** 데이터를 스트리밍하는 웹 표준이다
- WebSocket과 달리 **단방향**(서버 → 클라이언트)이라 단순하다
- AI 챗봇처럼 "서버가 계속 보내고, 클라이언트는 받기만 하면 되는" 상황에 적합하다

| 방식 | 방향 | 용도 |
| --- | --- | --- |
| 일반 HTTP | 요청 → 응답 (1회) | 데이터 조회, 생성 등 |
| SSE | 서버 → 클라이언트 (계속) | AI 응답, 실시간 알림 |
| WebSocket | 양방향 (계속) | 채팅, 게임 등 |

### SSE 데이터 형식

- SSE는 텍스트 기반이며, `data:` 접두사로 각 메시지를 구분한다
- 각 메시지는 빈 줄(`\n\n`)로 끝난다

```
data: 안녕

data: 하세

data: 요

data: [DONE]
```

- `[DONE]`은 스트리밍이 끝났음을 알리는 **관례적인 신호**이다 (필수는 아님)

---

## FastAPI에 스트리밍 API 추가하기

- 기존 Todo 백엔드의 `main.py`에 스트리밍 채팅 API를 추가한다
- `StreamingResponse`와 `time`을 import하고, `/chat` 엔드포인트를 추가한다

```python
# main.py - 기존 코드에 추가할 부분

# --- import 추가 ---
from fastapi.responses import StreamingResponse
import time

# --- Chat API (추가) ---

def generate_message():
    """글자를 하나씩 보내는 제너레이터"""
    message = "안녕하세요! 저는 AI 어시스턴트입니다. 무엇을 도와드릴까요?"

    for char in message:
        yield f"data: {char}\n\n"
        time.sleep(0.1)  # 0.1초 간격으로 전송

    yield "data: [DONE]\n\n"

@app.post("/chat")
def chat():
    return StreamingResponse(
        generate_message(),
        media_type="text/event-stream",
    )
```

- `media_type="text/event-stream"`: SSE 형식임을 브라우저에 알린다
- `yield f"data: {char}\n\n"`: SSE 형식에 맞춰 데이터를 보낸다
- `time.sleep(0.1)`: AI 응답이 생성되는 시간을 흉내낸다

---

## React에서 스트리밍 받기

### fetch

- `fetch`는 브라우저에 **내장된** HTTP 요청 API이다 (설치 불필요)
- `axios`는 `fetch`를 더 편리하게 쓸 수 있도록 만든 외부 라이브러리이다
- 스트리밍을 받을 때는 `axios` 대신 `fetch`를 사용한다
- `axios`도 추가 설정으로 스트리밍이 가능하지만, 기본적으로는 응답이 완전히 끝난 후에야 데이터를 반환하므로 스트리밍에는 적합하지 않다
- `fetch`는 응답 본문을 **ReadableStream**으로 제공하여, 도착하는 대로 읽을 수 있다

| 라이브러리 | 스트리밍 지원 | 방식 |
| --- | --- | --- |
| `axios` | 추가 설정 필요 | 기본적으로 응답 완료 후 데이터 반환 |
| `fetch` | 지원 | `response.body` (ReadableStream)로 실시간 읽기 가능 |

```jsx
// axios
const res = await axios.get("/todos");
const data = res.data;

// fetch — 같은 요청
const res = await fetch("http://localhost:8000/todos");
const data = await res.json();
```

- `fetch`는 `baseURL` 설정이 없으므로 **전체 URL**을 직접 써야 한다
- `axios`는 응답 데이터가 `res.data`에 바로 들어있지만, `fetch`는 `res.json()`을 `await`해야 한다
- `axios`는 JSON 전송 시 `Content-Type: application/json` 헤더를 자동으로 붙여주지만, `fetch`는 직접 명시해야 한다
- `fetch`는 HTTP 에러(404, 500 등)에서 에러를 던지지 않는다 — `res.ok`로 직접 확인해야 한다

---

## 스트리밍 처리 코드 이해하기

### fetch로 요청 보내기

```jsx
const response = await fetch("http://localhost:8000/chat", {
  method: "POST",
});
```

### Reader 만들기

```jsx
const reader = response.body.getReader();
const decoder = new TextDecoder();
```

- `response.body`는 **ReadableStream**이다 - 데이터가 도착하는 대로 읽을 수 있는 스트림이다
- `getReader()`로 **Reader**를 만든다 - 스트림에서 데이터를 하나씩 꺼내 읽는 도구이다
- `TextDecoder`는 바이트 데이터를 **문자열로 변환**하는 도구이다

### 반복해서 읽기

```jsx
while (true) {
  const { done, value } = await reader.read();

  if (done) break;

  const text = decoder.decode(value, { stream: true });
  // text 처리...
}
```

- `reader.read()`는 스트림에서 데이터를 **하나씩** 꺼낸다
- `done`이 `true`이면 서버가 스트림을 **닫은 것**이므로 반복을 멈춘다
- `value`는 바이트 데이터이므로 `decoder.decode()`로 문자열로 변환한다
- `{ stream: true }` 옵션은 한글처럼 멀티바이트 문자가 청크 경계에서 잘리는 것을 방지한다

### SSE 데이터 파싱

```jsx
const text = decoder.decode(value, { stream: true });
const lines = text.split("\n");

for (const line of lines) {
  if (line.startsWith("data: ")) {
    const data = line.slice(6); // "data: " 제거 (6글자)

    if (data === "[DONE]") break;

    // data 사용...
  }
}
```

- 서버가 보낸 텍스트에는 `data:`  접두사가 붙어 있으므로 제거해야 한다
- `line.slice(6)`: 문자열의 앞 6글자(`data:` )를 잘라내고 실제 데이터만 추출한다
- `[DONE]`이 오면 스트리밍이 끝난 것이다

---

## 스트리밍 챗봇 만들기

- 위의 단계들을 조합하여 React 컴포넌트로 만들어보자
- 핵심: `useState`로 메시지를 **누적**하고, 도착하는 글자를 하나씩 이어붙인다

```jsx
import { useState } from "react";

const Chat = () => {
  const [input, setInput] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    setAnswer("");
    setLoading(true);

    const response = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: input }),
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const text = decoder.decode(value, { stream: true });
      const lines = text.split("\n");

      for (const line of lines) {
        if (line.startsWith("data: ")) {
          const data = line.slice(6);
          if (data === "[DONE]") break;

          setAnswer((prev) => prev + data);
        }
      }
    }

    setLoading(false);
  };

  // 참고: for문의 break는 for문만 탈출한다 (while문은 계속 진행)
  // 서버가 [DONE] 이후 스트림을 닫으면 done이 true가 되어 while문도 끝난다

  return (
    <div>
      <h2>AI 챗봇</h2>
      <div className="border border-gray-300 p-4 min-h-[100px] mb-4 whitespace-pre-wrap">
        {answer || (loading ? "응답 대기 중..." : "질문을 입력하세요")}
      </div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="메시지를 입력하세요"
        disabled={loading}

      />
      <button onClick={handleSend} disabled={loading}>
        전송
      </button>
    </div>
  );
};

export default Chat;
```

### 코드 흐름 정리

1. 사용자가 메시지를 입력하고 "전송" 버튼을 누른다
2. `setAnswer("")`로 이전 응답을 지운다
3. `fetch`로 서버에 요청을 보낸다
4. `reader.read()`로 스트림에서 데이터를 하나씩 읽는다
5. SSE 형식을 파싱하여 실제 데이터를 추출한다
6. `setAnswer((prev) => prev + data)`로 기존 텍스트에 **이어붙인다**
7. `[DONE]`이 오거나 스트림이 끝나면 반복을 멈춘다
8. `disabled={loading}`으로 스트리밍 중에는 input과 버튼을 비활성화하여, 중복 전송을 방지한다

### setAnswer에서 콜백 함수를 사용하는 이유

- `setAnswer(answer + data)` 대신 `setAnswer((prev) => prev + data)`를 사용한다
- `while` 반복문 안에서 `setAnswer`가 **여러 번** 호출되기 때문이다
- `answer`는 `handleSend`가 시작될 때의 값(`""`)으로 고정되어 있어, `answer + data`를 쓰면 마지막 글자만 남는다
- `(prev) => prev + data`는 항상 **최신 State**를 기반으로 업데이트하므로 글자가 정상적으로 누적된다

```jsx
// ❌ 잘못된 방식 - answer는 항상 ""이므로 마지막 글자만 남는다
setAnswer(answer + data);

// ✅ 올바른 방식 - prev는 항상 현재 최신 값이다
setAnswer((prev) => prev + data);
```

- 이것은 State 심화에서 배운 **함수형 업데이트**와 같은 원리이다

---

## FastAPI 서버 업데이트: 메시지 받기

- 위의 React 코드에서 `body: JSON.stringify({ message: input })`로 메시지를 보내고 있다
- 서버도 이 메시지를 받아서 처리할 수 있도록 수정하자
- `generate_message`를 메시지를 받는 `generate_response`로 변경한다

```python
def generate_response(message: str):
    """사용자 메시지에 따라 응답을 스트리밍하는 제너레이터"""
    response = f"'{message}'에 대한 답변입니다. 이것은 스트리밍 테스트 응답입니다!"

    for char in response:
        yield f"data: {char}\n\n"
        time.sleep(0.1)

    yield "data: [DONE]\n\n"

@app.post("/chat")
def chat(body: dict):
    return StreamingResponse(
        generate_response(body["message"]),
        media_type="text/event-stream",
    )
```

- `BaseModel`은 이미 기존 코드에서 import되어 있으므로 추가할 필요 없다

---

## 대화 기록 관리하기

- 지금까지는 마지막 응답만 보여줬지만, 실제 챗봇은 **대화 기록**을 유지해야 한다
- `messages` 배열에 사용자 메시지와 AI 응답을 순서대로 쌓는다

```jsx
import { useState } from "react";

const ChatHistory = () => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    // AI 응답을 빈 문자열로 먼저 추가한다
    setMessages((prev) => [...prev, { role: "ai", content: "" }]);

    const response = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: input }),
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const text = decoder.decode(value, { stream: true });
      const lines = text.split("\n");

      for (const line of lines) {
        if (line.startsWith("data: ")) {
          const data = line.slice(6);
          if (data === "[DONE]") break;

          setMessages((prev) =>
            prev.map((msg, i) =>
              i === prev.length - 1
                ? { ...msg, content: msg.content + data }
                : msg
            )
          );
        }
      }
    }

    setLoading(false);
  };

  return (
    <div>
      <h2>AI 챗봇</h2>
      <div className="border border-gray-300 p-4 min-h-[200px] mb-4">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`mb-3 ${msg.role === "user" ? "text-right" : "text-left"}`}
          >
            <strong>{msg.role === "user" ? "나" : "AI"}</strong>
            <p className="whitespace-pre-wrap">{msg.content}</p>
          </div>
        ))}
        {loading && messages[messages.length - 1]?.content === "" && (
          <p>응답 대기 중...</p>
        )}
      </div>
      <div>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="메시지를 입력하세요"
          disabled={loading}
        />
        <button onClick={handleSend} disabled={loading}>
          전송
        </button>
      </div>
    </div>
  );
};

export default ChatHistory;
```

---

## 에러 처리

- 스트리밍 요청도 실패할 수 있다 (서버 다운, 네트워크 끊김 등)
- `try/catch`로 에러를 처리한다

```jsx
const handleSend = async () => {
  if (!input.trim()) return;

  // 사용자 메시지는 try 밖에서 추가한다
  // → 에러가 나도 사용자가 보낸 메시지는 화면에 남아있게 하기 위해서이다
  setMessages((prev) => [...prev, { role: "user", content: input }]);
  setInput("");
  setLoading(true);

  try {
    setMessages((prev) => [...prev, { role: "ai", content: "" }]);

    const response = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: input }),
    });

    if (!response.ok) {
      throw new Error(`서버 에러: ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const text = decoder.decode(value, { stream: true });
      const lines = text.split("\n");

      for (const line of lines) {
        if (line.startsWith("data: ")) {
          const data = line.slice(6);
          if (data === "[DONE]") break;

          setMessages((prev) => {
            const updated = [...prev];
            const lastMessage = updated[updated.length - 1];
            updated[updated.length - 1] = {
              ...lastMessage,
              content: lastMessage.content + data,
            };
            return updated;
          });
        }
      }
    }
  } catch (error) {
    // 에러 발생 시 마지막 AI 메시지를 에러 메시지로 교체한다
    setMessages((prev) => {
      const updated = [...prev];
      updated[updated.length - 1] = {
        role: "ai",
        content: `에러가 발생했습니다: ${error.message}`,
      };
      return updated;
    });
  } finally {
    setLoading(false);
  }
};
```

- `response.ok`: HTTP 상태 코드가 200번대인지 확인한다 (axios는 자동으로 에러를 던지지만, fetch는 직접 확인해야 한다)
- 에러가 발생하면 AI 메시지의 내용을 에러 메시지로 교체한다