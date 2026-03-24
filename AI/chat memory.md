# 대화 메모리 (Chat Memory)

---

## 대화 메모리 (Chat Memory)

- LLM은 기본적으로 이전 대화를 기억하지 못한다 (Stateless)
- 매 호출마다 대화 히스토리를 함께 전달해야 맥락을 유지할 수 있다
- LangChain은 대화 히스토리를 자동으로 관리해주는 메모리 시스템을 제공한다

### 메모리 없는 대화의 문제

LLM은 이전 대화를 기억하지 못한다.

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 첫 번째 질문
response1 = llm.invoke([HumanMessage(content="내 이름은 철수야")])
print("응답1:", response1.content)

# 두 번째 질문 — 기억 못함!
response2 = llm.invoke([HumanMessage(content="내 이름이 뭐였지?")])
print("응답2:", response2.content)
```

### 수동으로 히스토리 관리하기

이전 대화를 기억하게 하려면 매번 대화 내용을 함께 보내야 한다.

```python
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# 대화 히스토리를 직접 관리
history = [
    SystemMessage(content="너는 친절한 상담사야."),
]

# 첫 번째 대화
history.append(HumanMessage(content="내 이름은 철수야"))
response1 = llm.invoke(history)
history.append(response1)

# 두 번째 대화 — 이전 대화가 히스토리에 포함됨
history.append(HumanMessage(content="내 이름이 뭐였지?"))
response2 = llm.invoke(history)
history.append(response2)

print(response2.content)  # 기억함!
```

이 방식은 동작하지만, 매번 히스토리를 직접 관리해야 하므로 번거롭다.

---

## RunnableWithMessageHistory

- 체인에 메모리를 연결하여 대화 히스토리를 자동으로 관리한다
- `InMemoryChatMessageHistory`: 메모리에 대화를 저장하는 저장소
- `get_session_history`: 세션 ID를 받아 해당 세션의 히스토리를 반환하는 함수. 세션 ID가 다르면 서로 독립된 대화가 된다. (예: 사용자별로 다른 session_id)

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
parser = StrOutputParser()

# MessagesPlaceholder: 대화 히스토리가 삽입될 위치
prompt = ChatPromptTemplate.from_messages([
    ("system", "너는 친절한 상담사야."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])

chain = prompt | llm | parser

# 세션별 메모리 저장소 (session_id → InMemoryChatMessageHistory 매핑)
store = {}

# session_id로 히스토리를 조회/생성하는 함수
def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# RunnableWithMessageHistory: 체인을 감싸서 히스토리 자동 관리
# - 호출 시 저장소에서 히스토리를 꺼내 prompt의 history 자리에 주입
# - 응답 후 사용자 입력과 AI 응답을 자동으로 히스토리에 저장
chain_with_memory = RunnableWithMessageHistory(
    chain,                              # 감쌀 체인
    get_session_history,                # 세션 히스토리 조회 함수
    input_messages_key="input",         # 사용자 입력이 들어오는 키
    history_messages_key="history",     # 프롬프트에서 히스토리가 주입될 키
)
```

```python
# 대화 실행
config = {"configurable": {"session_id": "user_1"}}

response1 = chain_with_memory.invoke({"input": "내 이름은 철수야"}, config=config)
print("응답1:", response1)

response2 = chain_with_memory.invoke({"input": "내 이름이 뭐였지?"}, config=config)
print("응답2:", response2)  # 이번에는 기억한다!
```

```python
# 세션별 대화 분리 확인
config_user2 = {"configurable": {"session_id": "user_2"}}

response = chain_with_memory.invoke({"input": "내 이름이 뭐야?"}, config=config_user2)
print("user_2에게 물어봄:", response)  # user_2는 이름을 모른다
```

### 실무에서의 히스토리 관리

`InMemoryChatMessageHistory`는 프로세스가 종료되면 대화가 사라진다. 실무에서는 영속적인 저장소를 연결하여 사용한다.

`get_session_history` 함수만 교체하면 저장소를 바꿀 수 있다. 나머지 코드는 그대로 유지된다. 아래는 PostgreSQL 연동 예시이다.

**프로덕션에서의 선택지**:

| 방식 | 적합한 경우 |
| --- | --- |
| `RunnableWithMessageHistory` + PostgreSQL/Redis 등 | 단순한 대화형 서비스. 간단하고 충분히 실용적 |
| DB 직접 관리 (FastAPI + custom) | 히스토리 저장/조회 타이밍, 토큰 관리 등 세밀한 제어가 필요할 때 |
| LangGraph State + Checkpointer | 복잡한 워크플로우, 다중 에이전트, 중단/재개가 필요할 때 |

복잡도가 낮으면 `RunnableWithMessageHistory`로 충분하고, 요구사항이 복잡해질수록 아래 방식이 더 적합하다.

### Postgres에서의 예시

**사전 준비**: PostgreSQL에 `chat_history_db` 데이터베이스를 미리 생성해야 한다.

```python
# PostgreSQL 히스토리 저장소 예시
from langchain_postgres import PostgresChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import psycopg
import uuid

# DB 연결
conn = psycopg.connect("postgresql://postgres:1234@localhost:5432/chat_history_db")

# 테이블 자동 생성 (최초 1회)
table_name = "chat_history"
PostgresChatMessageHistory.create_tables(conn, table_name)

# get_session_history만 교체 — 나머지는 InMemory 때와 동일
def get_pg_session_history(session_id: str):
    return PostgresChatMessageHistory(
        table_name,
        session_id,
        sync_connection=conn,
    )

chain_with_pg = RunnableWithMessageHistory(
    chain,
    get_pg_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

# 대화 실행 — 프로세스를 재시작해도 히스토리가 유지된다
# PostgresChatMessageHistory는 session_id가 UUID 형식이어야 한다
session_id = str(uuid.uuid4())
config = {"configurable": {"session_id": session_id}}

response1 = chain_with_pg.invoke({"input": "내 이름은 영희야"}, config=config)
print("응답1:", response1)

response2 = chain_with_pg.invoke({"input": "내 이름이 뭐였지?"}, config=config)
print("응답2:", response2)
```

---

## 토큰 제한 관리

- 대화가 길어지면 히스토리의 토큰 수가 모델의 context window를 초과할 수 있다
- 초과하면 API 에러가 발생하므로 사전에 관리해야 한다

| 방법 | 장점 | 단점 |
| --- | --- | --- |
| `trim_messages` | 간단, 최근 대화 정확 | 오래된 맥락 유실 |
| 대화 요약 | 맥락 보존 | 요약 시 LLM 호출 필요 (추가 비용) |

실무에서는 두 방법을 조합하여 "요약 + 최근 N턴"을 사용하는 경우가 많다.

### trim_messages

`max_tokens` 예산 안에 들어가는 최근 메시지들만 유지한다. 메시지 내용을 중간에서 자르지 않고, 메시지 단위로 오래된 것부터 버린다. 유지되는 메시지 수(N)는 고정값이 아니라 각 메시지의 토큰 수에 따라 동적으로 결정된다.

```python
from langchain_core.messages import trim_messages, SystemMessage, HumanMessage, AIMessage

# 긴 대화 히스토리 시뮬레이션
long_history = [
    SystemMessage(content="너는 친절한 상담사야."),
    HumanMessage(content="안녕하세요"),
    AIMessage(content="안녕하세요! 무엇을 도와드릴까요?"),
    HumanMessage(content="Python에 대해 알려줘"),
    AIMessage(content="Python은 프로그래밍 언어입니다..."),
    HumanMessage(content="FastAPI도 알려줘"),
    AIMessage(content="FastAPI는 Python 웹 프레임워크입니다..."),
    HumanMessage(content="내 이름은 철수야"),
    AIMessage(content="안녕하세요 철수님!"),
    HumanMessage(content="내 이름이 뭐였지?"),
]

trimmer = trim_messages(
    max_tokens=80,              # 토큰 제한을 작게 설정하여 trim 효과 확인
    strategy="last",            # 최근 메시지부터 유지
    token_counter=llm,          # LLM의 토크나이저로 토큰 수 계산
    include_system=True,        # system 메시지는 항상 포함
    start_on="human",           # human 메시지부터 시작하도록 보장
)

trimmed = trimmer.invoke(long_history)

print("원본 메시지 수:", len(long_history))
print("트리밍 후 메시지 수:", len(trimmed))
print("\n트리밍 후 메시지:")
for msg in trimmed:
    print(f"  [{msg.type}] {msg.content[:50]}")
```

### 대화 요약 전략

`trim_messages`는 단순히 오래된 메시지를 잘라내는 것이다. 이 경우 초반 맥락이 완전히 사라진다. 대안으로, LLM을 사용하여 이전 대화를 요약하고 그 요약을 유지하는 방법이 있다.

| 방식 | 동작 | 장점 | 단점 |
| --- | --- | --- | --- |
| `trim_messages` | 오래된 메시지 삭제 | 간단, 비용 없음 | 초반 맥락 완전 유실 |
| 대화 요약 | LLM이 대화를 요약 | 핵심 맥락 보존 | 요약 시 추가 LLM 호출 비용 |
| **요약 + 최근 N턴** | 요약 + 최근 대화 유지 | 맥락 + 정확성 모두 확보 | 구현 복잡도 약간 증가 |

실무에서는 세 번째 방식(요약 + 최근 N턴)을 가장 많이 사용한다. #7 LangGraph에서는 이 로직을 노드 + 조건 분기로 자동화하는 패턴을 배운다.

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
parser = StrOutputParser()

# 대화 요약 체인
summarize_prompt = ChatPromptTemplate.from_messages([
    ("system", "다음 대화 내용을 핵심만 간결하게 요약해줘. 사용자의 이름, 주요 관심사, 중요한 정보를 빠뜨리지 마."),
    ("human", "{conversation}"),
])

summarize_chain = summarize_prompt | llm | parser

# 긴 대화 히스토리 시뮬레이션
long_history = [
    HumanMessage(content="안녕, 나는 철수야"),
    AIMessage(content="안녕하세요 철수님!"),
    HumanMessage(content="나는 백엔드 개발자야. Python을 주로 써"),
    AIMessage(content="Python 백엔드 개발자시군요! FastAPI나 Django를 사용하시나요?"),
    HumanMessage(content="FastAPI를 좋아해. 요즘 AI 쪽에 관심이 많아"),
    AIMessage(content="FastAPI + AI 조합이 요즘 인기가 많죠!"),
    HumanMessage(content="맞아, LangChain을 배우고 있어"),
    AIMessage(content="좋은 선택이에요! LangChain으로 다양한 AI 앱을 만들 수 있습니다."),
]

# 대화를 텍스트로 변환하여 요약
conversation_text = "\n".join([
    f"{'사용자' if isinstance(m, HumanMessage) else 'AI'}: {m.content}"
    for m in long_history
])

summary = summarize_chain.invoke({"conversation": conversation_text})
print("=== 대화 요약 ===")
print(summary)

# 요약 + 최근 2턴을 합쳐서 새 히스토리 구성
new_history = [
    SystemMessage(content=f"이전 대화 요약: {summary}"),
    # 최근 2턴만 유지
    long_history[-2],  # HumanMessage
    long_history[-1],  # AIMessage
]

print("\n=== 새 히스토리 (요약 + 최근 2턴) ===")
for msg in new_history:
    print(f"  [{msg.type}] {msg.content[:80]}")
```

### Long-term Memory 개념 소개

지금까지 다룬 메모리는 **Short-term Memory** (세션 내 대화 기억)이다. PostgreSQL에 저장하더라도 세션 단위의 대화 원문을 보관하는 것이므로 Short-term Memory에 해당한다.

**Long-term Memory**는 대화 원문이 아니라, 대화에서 **추출한 지식**을 별도 저장소에 축적하여 세션 간에 공유하는 것이다.

| 구분 | Short-term Memory | Long-term Memory |
| --- | --- | --- |
| 범위 | 현재 대화 세션 | 세션을 넘어선 기억 |
| 저장 대상 | 대화 원문 (메시지 리스트) | 대화에서 추출한 지식/선호도 |
| 예시 | "아까 철수라고 했었지" | "이 사용자는 Python 백엔드 개발자다" |
| 저장소 | 대화 히스토리 (메모리, DB) | 별도 DB (벡터 DB 등) |

**동작 흐름**:

```
세션 1: "나는 철수야, Python 백엔드 개발자야"
  → 지식 추출: {이름: 철수, 역할: 백엔드 개발자, 언어: Python}
  → 벡터 DB에 저장

세션 2: (일주일 후) "프레임워크 추천해줘"
  → 벡터 DB에서 사용자 정보 검색
  → "이 사용자는 Python 백엔드 개발자입니다"를 프롬프트에 주입
  → Python 기반 프레임워크(FastAPI, Django) 추천 가능
```