# LangChain

- LLM(대형 언어 모델)을 활용한 애플리케이션을 쉽게 만들 수 있게 해주는 Python 프레임워크
- 다양한 LLM 제공자(OpenAI, Google, 로컬 모델 등)를 통일된 인터페이스로 사용할 수 있다
- 프롬프트 관리, 체인 구성, 메모리, Tool 사용 등 LLM 앱에 필요한 기능을 제공한다

### LLM 앱 개발의 흐름

LLM을 활용한 서비스를 만드는 과정은 보통 다음과 같다.

1. **단순 API 호출** — OpenAI API를 직접 호출하여 챗봇을 만든다 (이전 수업에서 완료)
2. **체인 구성** — 프롬프트 + 모델 + 파서를 연결하여 다양한 기능을 만든다
3. **메모리/Tool 추가** — 대화를 기억하고, 외부 도구(검색, DB 등)를 사용한다
4. **RAG** — 자체 문서를 검색하여 LLM에 맥락을 제공한다
5. **Agent** — LLM이 스스로 판단하여 여러 도구를 조합하고 작업을 수행한다

LangChain은 2~5단계를 쉽게 구현할 수 있게 해주는 프레임워크이다.

### LangChain 생태계

LangChain은 하나의 라이브러리가 아니라 여러 패키지로 구성된 생태계이다.

| 패키지 | 역할 | 설명 |
| --- | --- | --- |
| `langchain-core` | 핵심 | 기본 인터페이스, LCEL, 메시지 타입 등 |
| `langchain` | 체인/메모리 | 체인 구성, 메모리, 에이전트 등 고수준 기능 |
| `langchain-openai` | OpenAI 연동 | ChatOpenAI, OpenAI Embeddings 등 |
| `langchain-google-genai` | Google 연동 | ChatGoogleGenerativeAI 등 |
| `langchain-community` | 커뮤니티 통합 | 다양한 서드파티 Tool, 벡터 DB 등 |
| `langgraph` | Agent 프레임워크 | 상태 기반 Agent 구축 (Part 3에서 학습) |

```
langchain-core (핵심)
    ├── langchain (체인/메모리)
    ├── langchain-openai (모델 연동)
    ├── langchain-google-genai (모델 연동)
    ├── langchain-community (커뮤니티)
    └── langgraph (Agent)
```

### 왜 LangChain을 쓰는가?

OpenAI API를 직접 호출해도 LLM 앱을 만들 수 있다. 하지만 기능이 복잡해질수록 직접 구현해야 할 것이 많아진다.

| 기능 | 직접 구현 | LangChain |
| --- | --- | --- |
| 프롬프트 템플릿 | 문자열 포맷팅으로 직접 관리 | `ChatPromptTemplate` |
| 모델 교체 | API별로 코드 재작성 | 한 줄 변경 (`ChatOpenAI` → `ChatGoogleGenerativeAI`) |
| 대화 메모리 | 히스토리 리스트 직접 관리 | `RunnableWithMessageHistory` |
| Tool 사용 | JSON 스키마 직접 작성 + 파싱 | `@tool` 데코레이터 |
| RAG | 임베딩/검색/주입 모두 직접 구현 | `Retriever` + 체인 |
| 체인 연결 | 함수 호출 순서 직접 관리 | ` |

단순한 한 번의 호출이라면 직접 호출이 더 간단하지만, 기능이 추가될수록 LangChain의 가치가 커진다.

## 환경 설정

터미널에서 프로젝트 디렉토리로 이동한 후, 가상환경을 만들고 패키지를 설치한다.

가상환경 생성 + 패키지 설치

```bash
uv init
uv add langchain langchain-openai langchain-google-genai langchain-community python-dotenv ipykernel
```

### ipynb 실행

매 파일마다 kernel 설정을 해주어야 한다.

프로젝트명의 python evironments가 보이지 않으면 vscode를 재시작한다.

노트북 열기 → 우상단 Select Kernel → python environments → uv init을 실행한 프로젝트 명 선택

### API 키 설정

프로젝트 루트에 `.env` 파일을 만들어 API 키를 관리한다.

```
OPENAI_API_KEY=sk-...
```

---

### LangSmith 설정

LangSmith는 LangChain 공식 디버깅/모니터링 플랫폼이다. 체인의 실행 과정을 시각적으로 추적(트레이싱)할 수 있어서, `print()` 디버깅보다 훨씬 효율적이다.

### 왜 LangSmith를 쓰는가?

LLM 앱은 전통적인 소프트웨어와 디버깅 방식이 다르다.

| 전통적 디버깅 | LLM 앱 디버깅 |
| --- | --- |
| 에러 메시지로 원인 파악 | 에러 없이 "이상한 답변"이 나옴 |
| 입력 → 출력이 결정적 | 같은 입력도 다른 출력 가능 |
| 중간 변수를 print로 확인 | 체인 내부 프롬프트/응답을 봐야 함 |

LangSmith는 체인의 각 단계(프롬프트 → LLM → 파서)를 자동으로 기록하여, "LLM에 실제로 어떤 프롬프트가 들어갔고, 어떤 응답이 나왔는지"를 한눈에 볼 수 있게 해준다.

### 설정 방법

**회원가입 및 API 키 발급**

1. [https://smith.langchain.com](https://smith.langchain.com/) 접속
2. 구글/GitHub 계정으로 가입 (무료)
3. 좌측 하단 Settings → API Keys → Create API Key
4. 생성된 키를 복사한다

**.env에 추가**

```
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=lsv2_pt_...
LANGCHAIN_PROJECT=agent-prac
```

이후 모든 LangChain 호출이 **자동으로** LangSmith에 기록된다.

### LangSmith 트레이스에서 볼 수 있는 정보

| 정보 | 설명 | 활용 |
| --- | --- | --- |
| 실행 흐름 | 프롬프트 → LLM → 파서 각 단계의 입출력 | 체인이 의도대로 연결됐는지 확인 |
| 실제 프롬프트 | LLM에 전달된 최종 프롬프트 전문 | 변수 주입이 제대로 됐는지 확인 |
| 토큰 사용량 | 각 호출별 input/output 토큰 수 | 비용 추적 및 최적화 |
| 소요 시간 | 각 단계별 레이턴시 | 병목 구간 파악 |
| 에러 위치 | 체인 중간 에러 발생 시 정확한 단계 | 디버깅 시간 단축 |

체인이 복잡해질수록 (메모리, Tool, RAG 등) LangSmith의 가치가 커진다. 이번 수업에서는 코드를 실행할 때마다 LangSmith 트레이스를 함께 확인하는 습관을 들이자.

### 환경변수 불러오기

```sql
from dotenv import load_dotenv

load_dotenv()
```

---

## 직접 호출 vs LangChain 비교

```sql
# OpenAI API 직접 호출
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "너는 친절한 한국어 번역가야."},
        {"role": "user", "content": "Hello, how are you?"},
    ],
)

print(response.choices[0].message.content)
```

```sql
# LangChain으로 호출
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatOpenAI(model="gpt-4o-mini")

messages = [
    SystemMessage(content="너는 친절한 한국어 번역가야."),
    HumanMessage(content="Hello, how are you?"),
]

response = llm.invoke(messages)
print(response.content)
```

직접 호출과 LangChain 호출은 결과가 동일하다. 그렇다면 왜 LangChain을 쓸까?

1. **모델 교체가 쉽다** — `ChatOpenAI`를 `ChatGoogleGenerativeAI`로 바꾸면 끝
2. **체인 구성** — 여러 단계의 LLM 호출을 파이프라인으로 연결할 수 있다
3. **생태계** — 메모리, Tool, RAG 등 다양한 기능이 이미 구현되어 있다

여기서 사용한 `invoke()`는 LangChain의 핵심 메서드이다. LangChain의 모든 구성 요소(LLM, 프롬프트, 파서, 체인 등)는 **Runnable**이라는 공통 인터페이스를 구현하고 있고, `invoke()`는 이 인터페이스의 기본 실행 메서드이다.

즉 `llm.invoke(messages)`는 "이 메시지 리스트를 LLM에 보내고 응답을 받아라"라는 뜻이다. 이후 배울 `prompt.invoke()`, `chain.invoke()` 등도 모두 같은 패턴이므로, **LangChain에서 무언가를 실행할 때는 `invoke()`를 쓴다**고 기억하면 된다.

---

## ChatModel

- LangChain에서 LLM을 사용하기 위한 객체
- 메시지 리스트를 입력받아 AI 응답 메시지를 반환한다

| 메시지 타입 | 역할 | 설명 |
| --- | --- | --- |
| `SystemMessage` | system | LLM의 역할과 행동을 설정 |
| `HumanMessage` | user | 사용자의 입력 |
| `AIMessage` | assistant | LLM의 응답 |

```sql
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

messages = [
    SystemMessage(content="너는 Python 전문가야."),
    HumanMessage(content="리스트 컴프리헨션이 뭐야?"),
]

response = llm.invoke(messages)
print(response.content)
```

### LLM 모델 전환

LangChain의 추상화 덕분에 모델 교체가 한 줄이면 된다.
당연히 다른 ai 쓰려면 key 입력해둬야 한다.

```sql
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

llm_openai = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_google = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0)

messages = [HumanMessage(content="Python의 장점 3가지를 알려줘")]

print("=== OpenAI ===")
print(llm_openai.invoke(messages).content)

print("\n=== Google ===")
print(llm_google.invoke(messages).content)
```

---

## PromptTemplate

- 프롬프트를 템플릿화하여 변수를 동적으로 주입할 수 있게 한다
- 반복적인 프롬프트 작성을 줄이고, 재사용성을 높인다

```sql
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "너는 {role} 전문가야. 모든 답변은 한국어로 해줘."),
    ("human", "{question}"),
])

# 변수를 주입하여 메시지 생성
messages = prompt.invoke({
    "role": "Python",
    "question": "데코레이터가 뭐야?",
})

print(messages)
```

`ChatPromptTemplate`은 메시지 리스트의 틀을 미리 만들어놓는 것이다.

- `{role}`, `{question}` 같은 중괄호 부분이 변수
- `invoke()`로 실제 값을 넣으면 완성된 메시지 리스트가 만들어진다

이 템플릿을 LLM과 연결하면 체인이 된다.

---

## OutputParser

- LLM의 응답을 원하는 형태로 변환하는 역할
- `llm.invoke()`의 반환값은 `AIMessage` 객체인데, `StrOutputParser`는 여기서 `content` 문자열만 깔끔하게 꺼내준다

```sql
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()

# AIMessage에서 content 문자열만 추출
result = parser.invoke(response)
print(result)
```

---

## LCEL 파이프라인 (LangChain Expression Language)

- `|` 연산자로 프롬프트, 모델, 파서를 연결하여 체인을 구성한다
- 데이터가 왼쪽에서 오른쪽으로 흘러간다

```
입력 → PromptTemplate → ChatModel → OutputParser → 출력
```

```sql
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("system", "너는 {role} 전문가야."),
    ("human", "{question}"),
])

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
parser = StrOutputParser()

# LCEL 파이프라인
chain = prompt | llm | parser

result = chain.invoke({
    "role": "Python",
    "question": "리스트와 튜플의 차이가 뭐야?",
})

print(result)
```

`chain = prompt | llm | parser`는 세 단계를 하나로 연결한 것이다.

1. `prompt` — 변수를 받아 메시지 리스트를 만든다
2. `llm` — 메시지를 받아 AI 응답을 생성한다
3. `parser` — AI 응답에서 문자열만 추출한다

이 체인에 `invoke()`를 호출하면 데이터가 순서대로 흘러가며, 최종 결과물(문자열)이 반환된다.

### Prompt Chaining 패턴

- 하나의 체인 출력을 다음 체인의 입력으로 연결하는 패턴
- LCEL의 `|` 파이프라인이 곧 Prompt Chaining이다
- 복잡한 작업을 작은 단계로 나누어 처리할 수 있다

`RunnableLambda`로 감싸는 이유: `chain1`의 출력은 `str`이지만, `chain2`의 입력은 `{"text": ...}` 딕셔너리여야 하기 때문이다. 타입 변환 어댑터 역할을 한다.

```sql
from langchain_core.runnables import RunnableLambda

# 1단계: 주제에 대한 설명 생성
prompt1 = ChatPromptTemplate.from_messages([
    ("system", "너는 기술 블로거야. 주어진 주제에 대해 간단히 설명해줘."),
    ("human", "{topic}"),
])

# 2단계: 설명을 초보자용으로 쉽게 변환
prompt2 = ChatPromptTemplate.from_messages([
    ("system", "너는 초보자를 위한 튜터야. 다음 설명을 초등학생도 이해할 수 있게 바꿔줘."),
    ("human", "{text}"),
])

chain1 = prompt1 | llm | parser
chain2 = prompt2 | llm | parser

# RunnableLambda로 체인 연결
combined_chain = chain1 | RunnableLambda(lambda x: {"text": x}) | chain2

result = combined_chain.invoke({"topic": "REST API"})
print(result)
```

### RunnablePassthrough

LCEL 파이프라인에서 자주 사용되는 유틸리티 Runnable이다.

| Runnable | 역할 | 사용 시점 |
| --- | --- | --- |
| `RunnablePassthrough` | 입력을 그대로 다음 단계로 전달 | 여러 입력을 조합할 때 |
| `RunnableLambda` | 커스텀 함수를 파이프라인에 삽입 | 중간 변환이 필요할 때 |

**왜 `RunnablePassthrough`가 필요한가?**

LCEL 체인은 기본적으로 이전 단계의 출력이 다음 단계의 입력으로 들어간다. 그런데 프롬프트에 변수가 여러 개일 때 문제가 생긴다.

```python
# 프롬프트에 context와 question 두 변수가 필요한 경우
prompt = "Context: {context}\\n질문: {question}"
```

이때 사용자 입력(`question`)은 그대로 전달하면서, 다른 값(`context`)은 별도로 만들어서 합쳐야 한다. `RunnablePassthrough`는 이 "그대로 전달" 역할을 한다.

- `RunnablePassthrough()` — 입력을 그대로 통과시킨다
- `RunnablePassthrough.assign(key=fn)` — 입력을 유지하면서 새 키-값을 추가한다

RAG에서 가장 많이 쓰이는 패턴이다. 사용자의 질문은 유지하면서, 검색 결과를 context로 추가해야 하기 때문이다.

```sql
from langchain_core.runnables import RunnablePassthrough

# RunnablePassthrough: 입력을 그대로 통과시키면서 다른 값과 조합
# RAG에서 "검색 결과 + 원래 질문"을 함께 전달할 때 핵심적으로 사용된다

prompt = ChatPromptTemplate.from_messages([
    ("system", "다음 context를 참고하여 질문에 답해줘.\n\nContext: {context}"),
    ("human", "{question}"),
])

# RunnablePassthrough.assign(): 기존 입력을 유지하면서 새 키를 추가
chain_with_passthrough = RunnablePassthrough.assign(
    context=lambda x: f"Python은 1991년에 만들어진 프로그래밍 언어입니다. 귀도 반 로섬이 개발했습니다."
) | prompt | llm | parser

result = chain_with_passthrough.invoke({"question": "Python은 누가 만들었어?"})
result = chain_with_passthrough.invoke({"question": "Python은 누가 만들었어?", "contenxt" : "Python은 1991년에 만들어진 프로그래밍 언어입니다. 귀도 반 로섬이 개발했습니다."})

# {"question": "Python은 누가 만들었어?"} => {"question": "Python은 누가 만들었어?", "contenxt" : "Python은 1991년에 만들어진 프로그래밍 언어입니다. 귀도 반 로섬이 개발했습니다."}
print(result)
```

`RunnablePassthrough.assign()`은 기존 입력 딕셔너리를 그대로 유지하면서 새 키를 추가한다. RAG에서 가장 흔한 패턴은 다음과 같다:

```python
# RAG 패턴 미리보기 (#4에서 실제 구현)
chain = (
    RunnablePassthrough.assign(context=retriever)  # question은 유지, context 추가
    | prompt
    | llm
    | parser
)
```

---

## 비용 모니터링

- LLM API는 토큰 단위로 과금된다
- 모든 실습에서 "이 호출이 얼마짜리인지" 인식하는 습관을 들인다

LangChain은 `get_openai_callback()`이라는 비용 추적 도구를 제공한다. `with` 블록 안에서 실행된 모든 LLM 호출의 토큰 수와 비용을 자동으로 합산해준다.

```sql
# 토큰 사용량 직접 확인
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

response = llm.invoke([HumanMessage(content="안녕하세요")])
print(response.usage_metadata)
```

```sql
# 콜백으로 비용 추적
from langchain_community.callbacks import get_openai_callback

with get_openai_callback() as cb:
    result = chain.invoke({"role": "Python", "question": "클래스가 뭐야?"})
    print(f"토큰 수: {cb.total_tokens}")
    print(f"비용: ${cb.total_cost:.6f}")

print(f"\n응답: {result[:100]}...")
```

### LangSmith로 확인하기

환경 설정에서 LangSmith를 세팅했다면, 위 비용 추적 코드를 실행하는 것만으로 트레이스가 자동 기록된다. [https://smith.langchain.com](https://smith.langchain.com/) 에 접속하여 방금 실행한 체인의 트레이스를 직접 확인해보자.

- 체인의 각 단계(프롬프트 → LLM → 파서)를 펼쳐서 입출력을 비교해보자
- 토큰 사용량과 소요 시간이 코드에서 출력한 값과 일치하는지 확인해보자

---

## LLM API 에러 핸들링

LLM API 호출은 네트워크를 통해 외부 서버에 요청을 보내는 것이기 때문에, 다양한 이유로 실패할 수 있다.

| 에러 | HTTP 코드 | 원인 | 대응 |
| --- | --- | --- | --- |
| Rate Limit | 429 | 짧은 시간에 너무 많은 요청 | 자동 재시도 (`max_retries`) |
| Timeout | 408/504 | 서버 응답이 너무 느림 | 타임아웃 설정 (`request_timeout`) |
| Server Error | 500 | OpenAI 서버 장애 | 재시도 또는 fallback 모델 |
| Auth Error | 401 | API 키가 잘못됨 | `.env` 파일 확인 |

LangChain은 이런 상황에 대비한 옵션을 제공한다.

```sql
from langchain_openai import ChatOpenAI

# max_retries: Rate limit(429), 서버 에러(500) 시 자동 재시도 횟수
# request_timeout: 응답이 이 시간(초) 안에 안 오면 에러 발생
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    max_retries=3,
    request_timeout=30,
)

# with_fallbacks: 메인 모델이 실패하면 백업 모델로 자동 전환
# 예: gpt-4o가 장애일 때 gpt-4o-mini로 대체
llm_main = ChatOpenAI(model="gpt-4o", temperature=0)
llm_backup = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_safe = llm_main.with_fallbacks([llm_backup])

# llm_safe.invoke()는 gpt-4o를 먼저 시도하고,
# 실패하면 gpt-4o-mini로 자동 전환된다
result = llm_safe.invoke("안녕하세요")
print(result.content)
```

`max_retries=3`으로 설정하면 에러 발생 시 자동으로 재시도한다. 대기 시간은 1초 → 2초 → 4초처럼 점점 늘어나는데, 이를 **exponential backoff**라고 한다. 무한히 빠르게 재시도하면 Rate limit이 더 심해지기 때문이다.

`with_fallbacks()`는 메인 모델이 완전히 실패했을 때 다른 모델로 자동 전환해준다. 실무에서는 비싼 모델을 메인으로, 저렴한 모델을 백업으로 두는 패턴이 흔하다.

실습 중 에러가 발생하면 당황하지 말고:

1. **429 에러** → 잠시 기다렸다가 다시 실행
2. **401 에러** → `.env` 파일의 API 키 확인
3. **500 에러** → OpenAI 서버 문제이므로 잠시 후 재시도

---

## LLM 응답 캐싱

개발 중에는 같은 프롬프트를 반복 실행하면서 후처리 로직만 수정하는 경우가 많다. 이때 매번 API를 호출하면 비용이 낭비된다. `InMemoryCache`를 설정하면 동일한 입력에 대해 캐시된 응답을 즉시 반환한다.

```sql
import time
from langchain_core.globals import set_llm_cache
from langchain_core.caches import InMemoryCache

set_llm_cache(InMemoryCache())

# 첫 번째 호출 — API 호출 발생
start = time.time()
result1 = llm.invoke("Python이 뭐야?")
print(f"첫 번째 호출: {time.time() - start:.2f}초")

# 두 번째 호출 — 캐시에서 즉시 반환
start = time.time()
result2 = llm.invoke("Python이 뭐야?")
print(f"두 번째 호출: {time.time() - start:.2f}초 (캐시)")

# 실습이 끝나면 캐시를 꺼두자
set_llm_cache(None)
```

---

## 비결정성 관리

- 같은 프롬프트를 여러 번 실행하면 매번 다른 결과가 나올 수 있다
- 디버깅할 때는 결과를 고정하는 것이 중요하다

| 설정 | 효과 |
| --- | --- |
| `temperature=0` | 가장 확률이 높은 토큰만 선택 → 거의 같은 결과 |
| `temperature=1` | 확률 분포대로 랜덤 선택 → 다양한 결과 |
| `seed=42` | 내부 랜덤 시드 고정 → 더 높은 재현성 |

개발/디버깅 중에는 `temperature=0`으로 고정하고, 서비스에서는 용도에 따라 조절하는 것이 좋다.

---

## batch와 stream

`invoke()`가 "하나 보내고, 하나 받기"라면:

- `batch()` — 여러 입력을 한 번에 보내고, 결과 리스트를 받는다 (병렬 처리)
- `stream()` — 하나를 보내고, 응답을 토큰 단위로 조각(chunk)씩 받는다

| 메서드 | 입력 | 출력 | 비동기 버전 |
| --- | --- | --- | --- |
| `invoke()` | 하나 | 하나 | `ainvoke()` |
| `batch()` | 리스트 | 리스트 | `abatch()` |
| `stream()` | 하나 | 이터레이터 (chunk) | `astream()` |

### batch

여러 입력을 동시에 처리할 때 사용한다. 내부적으로 병렬 실행되므로 하나씩 `invoke()`를 반복하는 것보다 빠르다.

```sql
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("system", "한 문장으로 답해줘."),
    ("human", "{question}"),
])

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
chain = prompt | llm | StrOutputParser()

# invoke를 3번 반복하는 대신, batch로 한 번에 처리
results = chain.batch([
    {"question": "Python이 뭐야?"},
    {"question": "JavaScript가 뭐야?"},
    {"question": "Rust가 뭐야?"},
])

for r in results:
    print(r)
    print()
```

`max_concurrency`로 동시 실행 수를 제한할 수도 있다. API rate limit이 있을 때 유용하다.

```sql
# 동시에 최대 2개씩만 실행
results = chain.batch(
    [
        {"question": "Go가 뭐야?"},
        {"question": "Swift가 뭐야?"},
        {"question": "Kotlin이 뭐야?"},
        {"question": "C++이 뭐야?"},
    ],
    config={"max_concurrency": 2},
)

for r in results:
    print(r)
    print()
```

### stream

ChatGPT처럼 응답이 한 글자씩 나타나게 하려면 `stream()`을 사용한다. 긴 응답을 기다리지 않고 바로바로 출력할 수 있어서 UX가 좋아진다.

```sql
# stream — 토큰 단위로 응답을 받는다
for chunk in chain.stream({"question": "Python의 장점 3가지를 알려줘"}):
    print(chunk, end="", flush=True)

print()  # 줄바꿈
```

`stream()`의 각 chunk는 토큰 단위의 문자열 조각이다. `end=""`로 출력하면 이어 붙여지면서 자연스러운 스트리밍 효과가 난다.

### astream (비동기 스트리밍)

FastAPI나 비동기 환경에서는 `astream()`을 사용한다. `stream()`과 동일하지만 `async for`로 받는다.

```sql
# astream — 비동기 스트리밍 (FastAPI, 비동기 환경에서 사용)
async for chunk in chain.astream({"question": "FastAPI가 뭐야?"}):
    print(chunk, end="", flush=True)

print()
```

Jupyter 노트북은 이벤트 루프가 이미 실행 중이라 `async for`를 셀에서 바로 쓸 수 있다. 일반 Python 스크립트에서는 `asyncio.run()`으로 감싸야 한다.

```python
# 일반 스크립트에서 사용할 때
import asyncio

async def main():
    async for chunk in chain.astream({"question": "FastAPI가 뭐야?"}):
        print(chunk, end="", flush=True)

asyncio.run(main())
```

### 1. 말투 변환기 체인

같은 문장을 다양한 말투로 변환하는 체인을 만들어보자.

- 입력: `"이 기능은 다음 주까지 구현이 어려울 것 같습니다."`
- 변환할 말투: `["해적", "조선시대 임금", "츤데레 애니메이션 캐릭터"]`

예상 출력:

```
해적: 이 기능은 다음 주까지 구현하기 힘들 것 같다, 이 바다의 사나이가 말하는 거다!
조선시대 임금: 이 기능은 다음 주까지 구현하기 어려울 것이니라. 과인이 심히 염려하노라.
츤데레 애니메이션 캐릭터: 다, 다음 주까지 구현이 어렵다고?! 별로 신경 쓰이는 건 아니지만... 좀 더 시간이 필요할 뿐이야!
```

```sql
# 말투 변환기 체인을 구현해보세요

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("system", """말투변환 전문가야. 다음 규칙을 지켜서 문장의 말투를 변경시켜줘.
- 설명 제외하고 변환된 문장만 출력해.
- {tone}의 특징을 최대한 살려서 변환해줘.
     """),
    ("human", "{text}"),
])

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
parser = StrOutputParser()

chain = prompt | llm | parser
text = "이 기능은 다음 주까지 구현이 어려울 것 같습니다."

for tone in ["해적", "조선시대 임금", "츤데레 애니메이션 캐릭터"]:
    result = chain.invoke({'text' : text, 'tone' : tone})
    print(f"{tone} - {result}")
```

### 2. 감정분석기 체인 (few-shot)

텍스트의 감정을 분석하는 체인을 만들어보자.

- few-shot 예시를 프롬프트에 포함하여 출력 형식을 일관되게 유지한다

예상 출력:

```
입력: 이 제품 정말 최악이에요. 다시는 안 살 겁니다.
분석:
- 감정: 부정
- 강도: 강함
- 근거: "최악", "다시는 안 살 겁니다"와 같은 강한 부정 표현 사용

입력: 괜찮은 것 같아요. 가격 대비 무난합니다.
분석:
- 감정: 중립
- 강도: 약함
- 근거: "괜찮은", "무난"과 같은 중립적 표현 사용

입력: 완전 대박! 인생 최고의 구매였어요!
분석:
- 감정: 긍정
- 강도: 강함
- 근거: "완전 대박", "인생 최고"와 같은 강한 긍정 표현 사용
```

```sql
# 감정분석기 체인을 구현해보세요

prompt_few = ChatPromptTemplate.from_messages([
    ("system", "너는 감정 분석 전문가야. 사용자의 감정을 분석해줘. 감정에는 `부정`, `긍정`, `중립`만 사용해"),
    ("human", "이 제품 정말 최악이에요. 다시는 안 살 겁니다."),
    ("ai", """
- 감정: 부정
- 강도: 강함
- 근거: "최악", "다시는 안 살 겁니다"와 같은 강한 부정 표현 사용
"""),
    ("human", "괜찮은 것 같아요. 가격 대비 무난합니다."),
    ("ai", """
- 감정: 중립
- 강도: 약함
- 근거: "괜찮은", "무난"과 같은 중립적 표현 사용"""),
    ("human", "완전 대박! 인생 최고의 구매였어요!"),
    ("ai", """
- 감정: 긍정
- 강도: 강함
- 근거: "완전 대박", "인생 최고"와 같은 강한 긍정 표현 사용
    """),
    ("human", "{sentence}"),
])
# for i in prompt_few.messages:
#     print(type(i))

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

chain = prompt_few | llm | parser

result = chain.invoke("와 이 제품 너무 좋아요! 또 살듯!")
print(result)

result = chain.invoke("내 생에 이런 제품은 처음봤습니다;;")
print(result)
```

### 3. 번역기 체인

구글 번역기처럼 입력 언어와 출력 언어를 지정할 수 있는 번역 체인을 만들어보자.

- 같은 체인으로 다양한 언어 쌍을 처리할 수 있어야 한다

예상 출력:

```
한→영: The weather is really nice today. I want to go for a walk.
영→일: 今日は本当にいい天気ですね。散歩に行きたいです。
```

```sql
# 번역기 체인을 구현해보세요

prompt = ChatPromptTemplate.from_messages([
    ("system", """번역 전문가야. 다음 규칙을 지켜서 문장을 {original_language}에서 {target_language}로 번역해줘.
- 최종 번역된 문장만 출력해.
- 직역하지 말고 해당 언어에 맞는 자연스러운 표현을 선택해줘.
- 입력받은 text가 {original_language}가 아니라면 "번역 실패"를 반환해줘
     """),
    ("human", "{text}"),
])

chain = prompt | llm | parser

text = "오늘 날씨가 정말 좋군. 산책가고 싶어."

result = chain.invoke({"original_language" : "한국어", "target_language" : "영어", "text" : text})
print(result)

result = chain.invoke({"original_language" : "한국어", "target_language" : "일본어", "text" : text})
print(result)

result = chain.invoke({"original_language" : "일본어", "target_language" : "영어", "text" : text})
print(result)

```

### 4. QA 체인 (RunnablePassthrough 활용)

`RunnablePassthrough.assign()`을 사용하여, 고정된 배경지식을 자동으로 붙여주는 QA 체인을 만들어보자.

- 배경지식: `"FastAPI는 Python 기반의 고성능 웹 프레임워크이다. Starlette과 Pydantic을 기반으로 하며, 자동 API 문서 생성과 타입 검증을 지원한다."`
- 사용자는 `{"question": "..."}` 만 넘기면 context가 자동으로 붙어야 한다

예상 출력:

```
Q: FastAPI는 뭘 기반으로 만들어졌어?
A: FastAPI는 Starlette과 Pydantic을 기반으로 만들어졌습니다.

Q: FastAPI가 자동으로 해주는 게 뭐야?
A: API 문서 자동 생성과 타입 검증을 지원합니다.
```

```sql
# QA 체인을 구현해보세요 (RunnablePassthrough.assign 활용)

prompt = ChatPromptTemplate.from_messages([
    ("system", """다음 <context>에 맞추서 질문에 대답해줘.
     <context>에 없는 내용은 "제공된 정보에 없습니다"로 대답해.

     <context>
     {context}
     </context>
     """),
    ("human", "{question}"),
])

data = "FastAPI는 Python 기반의 고성능 웹 프레임워크이다. Starlette과 Pydantic을 기반으로 하며, 자동 API 문서 생성과 타입 검증을 지원한다."

context_chain =  RunnablePassthrough.assign(
    context=lambda x: data
)| prompt | llm | parser

normal_prompt = ChatPromptTemplate.from_messages([
    ("system", """다음 질문에 대답해줘"""),
    ("human", "{question}"),
])

normal_chain = normal_prompt | llm | parser

result = context_chain.invoke({"question" : "FastAPI는 뭘 기반으로 만들어졌어?"})
print(result)

result = context_chain.invoke({"question" : "FastAPI가 자동으로 해주는 게 뭐야?"})
print(result)

result = context_chain.invoke({"question" : "django에 대해서 설명해줘"})
print(result)

# 일반 chain

result = normal_chain.invoke({"question" : "FastAPI는 뭘 기반으로 만들어졌어?"})
print(result)

result = normal_chain.invoke({"question" : "django에 대해서 설명해줘"})
print(result)

```