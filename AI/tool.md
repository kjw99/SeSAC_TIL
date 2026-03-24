## Tool 개념

- Tool은 LLM이 외부 세계와 상호작용할 수 있게 해주는 함수이다
- LLM 자체는 텍스트만 생성할 수 있지만, Tool을 통해 웹 검색, 계산, DB 조회 등을 수행할 수 있다
- LLM이 "이 Tool을 호출해야겠다"고 판단하면, Tool 이름과 인자를 반환한다

```
사용자 질문 → LLM이 판단 → Tool 호출 필요?
  → Yes: Tool 이름 + 인자 반환 → Tool 실행 → 결과를 LLM에 전달 → 최종 응답
  → No: 바로 텍스트 응답
```

예를 들어 사용자가 "서울 날씨 알려줘"라고 하면, LLM은 스스로 날씨를 알 수 없다. 대신 "날씨 검색 Tool을 '서울'이라는 인자로 호출해야겠다"고 판단한다. 개발자가 실제로 Tool을 실행하고 결과를 LLM에 돌려주면, LLM이 그 결과를 자연어로 정리하여 답변한다.

---

## @tool 데코레이터

- Python 함수를 LangChain Tool로 변환하는 가장 간단한 방법
- 함수의 docstring이 Tool의 설명(description)이 된다
- `@tool` 데코레이터를 붙이면 일반 함수가 LangChain Tool 객체로 변환된다. LLM은 이 Tool의 `name`, `description`, `args_schema`를 보고 어떤 Tool을 어떤 인자로 호출할지 판단한다. 따라서 **docstring(설명)과 타입 힌트가 매우 중요하다**.

### Tool 설계 원칙

| 원칙 | 설명 |
| --- | --- |
| 명확한 이름 | `search_weather` > `func1` |
| 구체적인 설명 | "주어진 도시의 현재 날씨 정보를 검색한다" > "데이터를 가져온다" |
| 타입 힌트 필수 | `city: str` — LLM이 어떤 값을 넣어야 하는지 알 수 있다 |
| 예시 포함 | docstring에 입력 예시를 넣으면 정확도가 높아진다 |
| 에러 메시지 | Tool 실행 실패 시 LLM이 이해할 수 있는 메시지를 반환한다 |

**Tool을 나누는 기준**: API 엔드포인트가 아니라 **LLM이 docstring만 보고 언제 쓸지 판단할 수 있는 단위**로 나눈다. 용도가 다르면 분리하고(검색 vs 상세 조회), 파라미터 하나 차이면 합쳐도 된다. 너무 많으면 선택 정확도가 떨어지고, 너무 합치면 파라미터가 복잡해져서 LLM이 헷갈린다.

```python
from langchain_core.tools import tool

@tool
def add(a: int, b: int) -> int:
    """두 숫자를 더한다."""
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """두 숫자를 곱한다."""
    return a * b

# Tool 정보 확인
print(f"이름: {add.name}")
print(f"설명: {add.description}")
print(f"스키마: {add.args_schema.model_json_schema()}")

# Tool 직접 호출
print(f"\nadd(3, 5) = {add.invoke({'a': 3, 'b': 5})}")
```

---

## Tool 바인딩

- LLM에 사용할 수 있는 Tool 목록을 알려주는 것
- `bind_tools()`를 사용한다

`bind_tools()`로 Tool을 바인딩하면, LLM은 사용자의 질문을 보고 두 가지 중 하나를 선택한다.

1. **Tool 호출이 필요한 경우** — `tool_calls`에 호출할 Tool 정보를 담아서 반환 (content는 비어있음)
2. **Tool 호출이 불필요한 경우** — 일반 텍스트 응답을 content에 담아서 반환

중요한 점은, `bind_tools()`만으로는 **Tool이 실제로 실행되지 않는다**. LLM은 "이 Tool을 이 인자로 호출해줘"라고 요청할 뿐이고, 실제 실행은 개발자가 해야 한다.

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_with_tools = llm.bind_tools([add, multiply])

# Tool 호출이 필요한 경우
response = llm_with_tools.invoke("3과 5를 더해줘")
print("content:", response.content)        # 비어있음
print("tool_calls:", response.tool_calls)   # Tool 호출 정보

print()

# Tool 호출이 불필요한 경우
response2 = llm_with_tools.invoke("안녕하세요")
print("content:", response2.content)        # 일반 응답
print("tool_calls:", response2.tool_calls)  # 빈 리스트
```

---

## Function Calling 비교: OpenAI 원시 vs LangChain

| 비교 항목 | OpenAI 원시 | LangChain @tool |
| --- | --- | --- |
| Tool 정의 | JSON 스키마 직접 작성 | Python 함수 + docstring |
| 파라미터 | 수동으로 properties 정의 | 타입 힌트에서 자동 추출 |
| 결과 파싱 | JSON 문자열 수동 파싱 | `tool_calls` 딕셔너리로 제공 |
| 모델 교체 | API별 코드 재작성 | `ChatOpenAI` → `ChatAnthropic` 한 줄 변경 |

```python
# OpenAI 원시 function calling — JSON 스키마를 직접 작성해야 한다
from openai import OpenAI

client = OpenAI()

openai_tools = [
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "두 숫자를 더한다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "integer", "description": "첫 번째 숫자"},
                    "b": {"type": "integer", "description": "두 번째 숫자"},
                },
                "required": ["a", "b"],
            },
        },
    }
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "3과 5를 더해줘"}],
    tools=openai_tools,
)

tc = response.choices[0].message.tool_calls[0]
print(f"OpenAI 원시: name={tc.function.name}, args={tc.function.arguments}")

# LangChain — 함수 + docstring만으로 끝
response2 = llm_with_tools.invoke("3과 5를 더해줘")
print(f"LangChain:   name={response2.tool_calls[0]['name']}, args={response2.tool_calls[0]['args']}")
```

```python
# 다양한 질문으로 테스트
questions = [
    "3과 5를 더한 다음, 그 결과에 2를 곱해줘",
    "서울 날씨 어때?",
    "서울이랑 부산 날씨 비교해줘",
    "안녕하세요!",
]

for q in questions:
    print(f"\n사용자: {q}")
    answer = run_agent(q)
    print(f"Agent: {answer}")
```

**참고**: LLM의 응답은 매번 다를 수 있다. 위 결과에서 불필요한 Tool 호출(`multiply({'a': 2, 'b': 1})` 등)이 포함되기도 하는데, 이는 LLM의 비결정적 특성 때문이다. 실행할 때마다 Tool 호출 순서나 횟수가 달라질 수 있다.