# Structured Output

테스트 준비

```python
from dotenv import load_dotenv

load_dotenv()
```

```
from langchain_openai import ChatOpenAI

# Structured Output에서는 일관된 결과를 위해 temperature=0이 적합하다
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
```

---

## Structured Output

- LLM의 응답을 정해진 구조(스키마)로 받는 기능
- LLM의 응답은 정형화되어있지 않은 텍스트, 코드에서 활용하기 어려우며, Structured Output은 이 문제를 해결한다
- 자유로운 텍스트 대신 Python 객체로 받을 수 있다
- Pydantic 모델로 스키마를 정의한다

```python
# ❌ 텍스트 응답 — 파싱이 어렵다
# "감정: 부정, 강도: 강함, 근거: '최악'이라는 표현"

# ✅ 구조화된 응답 — 바로 코드에서 사용 가능
# SentimentResult(sentiment='부정', intensity='강함', reason="'최악'이라는 표현")
```

### with_structured_output()

`with_structured_output()`을 사용하면 LLM이 자유 텍스트 대신 지정한 Pydantic 모델 형태로 응답한다. 내부적으로는 OpenAI의 function calling 기능을 활용하여 JSON을 생성하고, 이를 Pydantic 모델로 변환한다.

`Field(description=...)`은 LLM에게 "이 필드에 무엇을 넣어야 하는지" 설명해주는 역할이다. description이 명확할수록 LLM이 정확한 값을 반환한다.

`with_structured_output()`은 내부적으로 function calling을 사용하여 API 레벨에서 스키마를 전달하므로, **별도의 프롬프트(format_instructions)나 파서(OutputParser)가 필요 없다.** 기존의 `prompt | llm | parser` 체인 대신 `structured_llm.invoke()`만으로 Pydantic 객체를 바로 받을 수 있다. 단, 시스템 역할이나 추가 지시가 필요한 경우에는 `prompt | structured_llm` 형태로 프롬프트만 추가하면 된다.

```python
from pydantic import BaseModel, Field

# 출력 스키마 정의
class SentimentResult(BaseModel):
    sentiment: str = Field(description="감정 (긍정/부정/중립)")
    intensity: str = Field(description="강도 (강함/보통/약함)")
    reason: str = Field(description="판단 근거")

structured_llm = llm.with_structured_output(SentimentResult)

result = structured_llm.invoke("이 제품 정말 최악이에요. 다시는 안 살 겁니다.")

print(result)
print(f"\n감정: {result.sentiment}")
print(f"강도: {result.intensity}")
print(f"근거: {result.reason}")
```

### 체인에서 Structured Output 사용하기

```python
from langchain_core.prompts import ChatPromptTemplate

class MovieReview(BaseModel):
    title: str = Field(description="영화 제목")
    rating: int = Field(description="평점 (1-10)")
    pros: list[str] = Field(description="장점 목록")
    cons: list[str] = Field(description="단점 목록")
    summary: str = Field(description="한줄 요약")

prompt = ChatPromptTemplate.from_messages([
    ("system", "너는 영화 평론가야. 주어진 영화 리뷰를 분석해줘."),
    ("human", "{review}"),
])

structured_llm = llm.with_structured_output(MovieReview)
chain = prompt | structured_llm

result = chain.invoke({
    "review": "인터스텔라는 정말 대단한 영화였습니다. 시각적으로 압도적이고 음악도 훌륭했어요. 다만 러닝타임이 너무 길고 중반부가 조금 지루했습니다."
})

print(f"제목: {result.title}")
print(f"평점: {result.rating}/10")
print(f"장점: {result.pros}")
print(f"단점: {result.cons}")
print(f"요약: {result.summary}")
```

### Enum을 활용한 복잡한 스키마

**Enum(열거형)** 은 미리 정해진 값들만 허용하는 타입이다. `str` 대신 Enum을 쓰면 LLM이 임의의 문자열을 반환하는 것을 방지할 수 있다.

```python
from enum import Enum

# str을 상속하면 값이 문자열로 직렬화된다
class Color(str, Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"

print(Color.RED)        # Color.RED
print(Color.RED.value)  # "red"

# ❌ 정의되지 않은 값은 에러
# Color("yellow")  → ValueError
```

- `str` 필드: LLM이 `"긴급"`, `"높음"`, `"상"` 등 자유롭게 반환 → 일관성 없음
- `Enum` 필드: `"high"`, `"medium"`, `"low"` 중 하나만 반환 → 코드에서 안전하게 분기 가능

Pydantic 모델에서 `category: Category`처럼 타입을 Enum으로 지정하면, LLM의 function calling 스키마에 허용 값 목록이 전달되어 정해진 값만 반환하도록 강제된다.

```python
from enum import Enum

class Category(str, Enum):
    BUG = "bug"
    FEATURE = "feature"
    QUESTION = "question"
    DOCS = "docs"

class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class IssueAnalysis(BaseModel):
    category: Category = Field(description="이슈 카테고리")
    priority: Priority = Field(description="우선순위")
    title: str = Field(description="이슈 제목 (간결하게)")
    description: str = Field(description="이슈 설명")
    affected_components: list[str] = Field(description="영향받는 컴포넌트 목록")

structured_llm = llm.with_structured_output(IssueAnalysis)

result = structured_llm.invoke(
    "로그인 페이지에서 비밀번호를 입력하고 엔터를 누르면 화면이 깜빡이면서 입력값이 초기화됩니다. 크롬 브라우저에서만 발생하고, 사파리에서는 정상입니다."
)

print(f"카테고리: {result.category.value}")
print(f"우선순위: {result.priority.value}")
print(f"제목: {result.title}")
print(f"설명: {result.description}")
print(f"영향 컴포넌트: {result.affected_components}")
```

---

## Structured Output 실패 처리

`with_structured_output()`은 function calling 기반이라 스키마 준수율이 매우 높지만, 드물게 실패할 수 있다. 이때는 `.with_retry()`로 체인을 재시도할 수 있다.

```python
# 실패 시 최대 3번 자동 재시도
chain = prompt | structured_llm
safe_chain = chain.with_retry(stop_after_attempt=3)
```

### max_retries vs with_retry

이 둘은 재시도하는 **위치**가 다르다.

```
[LangChain 체인] → [LLM API 요청] → 네트워크/서버 → [응답 수신] → [파싱/검증]
                    ↑ max_retries                       ↑ with_retry
```

|  | `max_retries` | `.with_retry()` |
| --- | --- | --- |
| **설정 위치** | `ChatOpenAI(max_retries=3)` | `chain.with_retry(stop_after_attempt=3)` |
| **재시도 주체** | OpenAI SDK (HTTP 클라이언트) | LangChain (체인) |
| **대상 에러** | 네트워크 에러, 타임아웃, 429 Rate Limit | 파싱 실패, 스키마 불일치 |
| **동작** | 같은 HTTP 요청을 다시 보냄 | 체인 전체를 처음부터 다시 실행 (= LLM 재호출) |
- `max_retries`: **서버가 응답을 안 줄 때** — OpenAI SDK가 같은 요청을 재전송
- `with_retry`: **응답은 왔는데 내용이 잘못됐을 때** — LangChain이 체인을 처음부터 다시 실행하므로 LLM API를 다시 호출한다