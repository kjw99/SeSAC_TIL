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

---

## 커스텀 Tool 만들기

### 영화 검색 Tool (TMDB)

TMDB(The Movie Database) API를 Tool로 감싸서, Agent가 영화 정보를 검색할 수 있게 만든다.

```
uv add requests
```

```
TMDB_API_KEY=eyJhbGciOiJIUzI1NiJ9...
```

> [TMDB 사이트](https://www.themoviedb.org/settings/api)에서 무료 API Read Access Token을 발급받을 수 있다.
> 

```python
import os
import requests

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

@tool
def search_movies(query: str) -> str:
    """영화를 검색한다. 영화 제목이나 키워드로 검색할 수 있다. 예: '인셉션', '기생충', '아이언맨'"""
    response = requests.get(
        "https://api.themoviedb.org/3/search/movie",
        headers={"Authorization": f"Bearer {TMDB_API_KEY}"},
        params={
            "query": query,
            "language": "ko-KR",
        },
    )
    data = response.json()
    results = data.get("results", [])[:5]

    if not results:
        return f"'{query}'에 대한 검색 결과가 없습니다."

    output = []
    for movie in results:
        movie_id = movie.get("id")
        title = movie.get("title", "제목 없음")
        year = (movie.get("release_date") or "")[:4]
        rating = movie.get("vote_average", 0)
        overview = movie.get("overview", "줄거리 없음")[:100]
        output.append(f"- [{movie_id}] {title} ({year}) ⭐ {rating}\n  {overview}")
    return "\n".join(output)

# Tool 정보 확인
print(f"name: {search_movies.name}")
print(f"description: {search_movies.description}")
print(f"schema: {search_movies.args_schema.model_json_schema()}")
```

```python
# 영화 검색 Agent
movie_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
movie_agent = movie_llm.bind_tools([search_movies])

questions = [
    "크리스토퍼 놀란 영화 추천해줘",
    "최근 한국 공포영화 뭐가 있어?",
    "인터스텔라 평점 어때?",
]

for q in questions:
    print(f"\n사용자: {q}")
    messages = [HumanMessage(content=q)]
    response = movie_agent.invoke(messages)
    messages.append(response)

    while response.tool_calls:
        for tc in response.tool_calls:
            print(f"  → Tool 호출: {tc['name']}({tc['args']})")
            result = search_movies.invoke(tc["args"])
            messages.append(ToolMessage(content=result, tool_call_id=tc["id"]))
        response = movie_agent.invoke(messages)
        messages.append(response)

    print(f"답변: {response.content}")
```

### 웹 검색 Tool (Tavily)

Agent의 가장 기본적인 외부 Tool. Tavily 검색 API를 활용한다.

```
uv add tavily-python
```

```
TAVILY_API_KEY=tvly-...
```

> [Tavily 사이트](https://tavily.com/)에서 무료 API 키를 발급받을 수 있다.
> 

```python
from tavily import TavilyClient
load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> str:
    """웹에서 최신 정보를 검색한다. 실시간 정보(날씨, 뉴스, 주가 등)가 필요할 때 사용한다."""
    results = tavily_client.search(query=query, max_results=3)
    output = []
    for result in results["results"]:
        output.append(f"제목: {result['title']}")
        output.append(f"내용: {result['content'][:200]}")
        output.append(f"출처: {result['url']}")
        output.append("")
    return "\n".join(output)

# Tool 정보 확인
print(f"name: {web_search.name}")
print(f"description: {web_search.description}")
print(f"schema: {web_search.args_schema.model_json_schema()}")
```

```python
# 웹 검색 Agent
search_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
search_agent = search_llm.bind_tools([web_search])

questions = [
    "오늘 주요 뉴스 알려줘",
    "2026년 개봉 예정인 마블 영화 알려줘",
]

for q in questions:
    print(f"\n사용자: {q}")
    messages = [HumanMessage(content=q)]
    response = search_agent.invoke(messages)
    messages.append(response)

    while response.tool_calls:
        for tc in response.tool_calls:
            print(f"  → Tool 호출: {tc['name']}({tc['args']})")
            result = web_search.invoke(tc["args"])
            messages.append(ToolMessage(content=result, tool_call_id=tc["id"]))
        response = search_agent.invoke(messages)
        messages.append(response)

    print(f"답변: {response.content}")
```

### DB 조회 Tool

실제 데이터베이스에서 정보를 조회하는 Tool이다.

> 여기서는 학습을 위해 용도별 Tool(`search_products`)을 직접 만든다. 실무에서는 LLM이 자연어를 SQL로 변환하는 **Text-to-SQL** 패턴으로 범용 Tool을 만들기도 한다.
> 

```
uv add sqlalchemy psycopg2-binary
```

```
DATABASE_URL=postgresql://postgres:password@localhost:5432/ai_prac
```

```python
import os
from sqlalchemy import create_engine, text

engine = create_engine("postgresql://postgres:1234@localhost:5432/ai_prac")

with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS products"))
    conn.execute(text("""
        CREATE TABLE products (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            category TEXT NOT NULL,
            stock INTEGER NOT NULL
        )
    """))
    conn.execute(text("""
        INSERT INTO products (name, price, category, stock) VALUES
        ('맥북 프로 14', 2390000, '노트북', 15),
        ('갤럭시 S24', 1150000, '스마트폰', 30),
        ('에어팟 프로', 359000, '이어폰', 50),
        ('아이패드 에어', 929000, '태블릿', 20),
        ('LG 그램', 1790000, '노트북', 10)
    """))
    conn.commit()

print("실습용 DB 생성 완료")
```

```python
@tool
def search_products(category: str = "", max_price: int = 0) -> str:
    """상품을 검색한다. category로 카테고리 필터링, max_price로 최대 가격 필터링이 가능하다.
    사용 가능한 카테고리: '노트북', '스마트폰', '이어폰', '태블릿'.
    max_price가 0이면 가격 필터링 없이 전체를 반환한다."""
    conditions = []
    params = {}
    if category:
        conditions.append("category = :category")
        params["category"] = category
    if max_price > 0:
        conditions.append("price <= :max_price")
        params["max_price"] = max_price

    # where 변수는 코드 내부에서만 생성되므로 SQL 인젝션 위험 없음 (값은 :param 바인딩 사용)
    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    query = f"SELECT name, price, category, stock FROM products {where}"

    with engine.connect() as conn:
        rows = conn.execute(text(query), params).fetchall()

    if not rows:
        return "조건에 맞는 상품이 없습니다."

    result = []
    for row in rows:
        result.append(f"- {row[0]}: {row[1]:,}원 ({row[2]}, 재고 {row[3]}개)")
    return "\n".join(result)

# DB 조회 Tool 테스트
print("=== 노트북 카테고리 ===")
print(search_products.invoke({"category": "노트북"}))
print("\n=== 100만원 이하 ===")
print(search_products.invoke({"max_price": 1000000}))
```

### Tool 선택 정확도 향상: Few-shot 예시

Tool이 많아지면 LLM이 잘못된 Tool을 선택하거나, Tool을 써야 하는데 안 쓰는 경우가 생긴다. 시스템 프롬프트에 few-shot 예시를 포함하면 정확도가 크게 올라간다.

```python
from langchain_core.messages import SystemMessage, AIMessage

# Few-shot 예시를 시스템 프롬프트 + 대화 히스토리로 제공
few_shot_messages = [
    SystemMessage(content="""너는 쇼핑 도우미야. 다음 도구를 사용할 수 있어:
- search_products: 상품 검색 (category로 카테고리 필터링, max_price로 최대 가격 필터링)
- multiply: 두 숫자를 곱한다
- search_weather: 날씨 검색

상품 정보는 반드시 search_products로 조회해야 한다. 가격을 추측하지 마라.
계산은 반드시 multiply 도구를 사용해라. 직접 계산하지 마라.
아래 예시처럼 사용자의 의도에 맞는 도구를 정확하게 선택해."""),

    # 예시 1: 카테고리로 상품 검색
    HumanMessage(content="태블릿 뭐 있어?"),
    AIMessage(content="", tool_calls=[{
        "id": "ex1", "name": "search_products", "args": {"category": "태블릿"}
    }]),
    ToolMessage(content="- 아이패드 에어: 929,000원 (태블릿, 재고 20개)", tool_call_id="ex1"),
    AIMessage(content="태블릿은 현재 1개 있습니다!\n- 아이패드 에어: 929,000원"),

    # 예시 2: 검색 → 계산
    HumanMessage(content="스마트폰 2개 사면 얼마야?"),
    AIMessage(content="", tool_calls=[
        {"id": "ex2a", "name": "search_products", "args": {"category": "스마트폰"}},
    ]),
    ToolMessage(content="- 갤럭시 S24: 1,150,000원 (스마트폰, 재고 30개)", tool_call_id="ex2a"),
    AIMessage(content="", tool_calls=[
        {"id": "ex2b", "name": "multiply", "args": {"a": 1150000, "b": 2}},
    ]),
    ToolMessage(content="2300000", tool_call_id="ex2b"),
    AIMessage(content="갤럭시 S24 2개는 총 2,300,000원입니다."),

    # 예시 3: 가격 기준 검색
    HumanMessage(content="100만원 이하 상품 보여줘"),
    AIMessage(content="", tool_calls=[
        {"id": "ex3", "name": "search_products", "args": {"max_price": 1000000}},
    ]),
    ToolMessage(content="- 에어팟 프로: 359,000원 (이어폰, 재고 50개)\n- 아이패드 에어: 929,000원 (태블릿, 재고 20개)", tool_call_id="ex3"),
    AIMessage(content="100만원 이하 상품은 2개입니다!\n- 에어팟 프로: 359,000원\n- 아이패드 에어: 929,000원"),
]

# Few-shot Agent
fewshot_tools = [search_products, multiply, search_weather]
fewshot_tool_map = {t.name: t for t in fewshot_tools}
llm_fewshot = llm.bind_tools(fewshot_tools)

def run_fewshot_agent(user_input: str):
    messages = few_shot_messages + [HumanMessage(content=user_input)]

    while True:
        response = llm_fewshot.invoke(messages)
        messages.append(response)
        if not response.tool_calls:
            return response.content
        for tc in response.tool_calls:
            print(f"  [Tool] {tc['name']}({tc['args']})")
            result = fewshot_tool_map[tc["name"]].invoke(tc["args"])
            messages.append(ToolMessage(content=str(result), tool_call_id=tc["id"]))

# 테스트: search_products → multiply 순서로 호출되어야 한다
print("사용자: 노트북 중에 제일 싼 거 3개 사면 얼마야?")
answer = run_fewshot_agent("노트북 중에 제일 싼 거 3개 사면 얼마야?")
print(f"Agent: {answer}")
```

### Tool 기반 레퍼런스 관리

시스템 프롬프트에 레퍼런스 목록만 노출하고, LLM이 필요한 문서를 Tool로 가져오게 하는 패턴이다. 레퍼런스가 수십 개 이하이고 카테고리가 명확하면 임베딩 유사도(RAG)보다 LLM의 판단이 더 정확할 수 있다.

- **Tool 레퍼런스**: 문서 수가 적고, 카테고리가 명확할 때 적합
- **RAG**: 문서 수가 많고, 키워드가 아닌 의미 기반 검색이 필요할 때 적합

이 아래 예시의 `get_policy` Tool이 바로 이 패턴의 예시이다. 시스템 프롬프트에 "사용 가능한 정책: refund, privacy, shipping"이라고 목록만 알려주고, LLM이 필요한 정책을 Tool로 조회한다.

---

## 여러 Tool을 사용하는 대화형 Agent

계산, 날씨 검색, 정책 조회 Tool을 모두 갖춘 종합 Agent

```python
from langchain_core.messages import SystemMessage

@tool
def get_policy(policy_id: str) -> str:
    """회사 정책 문서를 조회한다. 사용 가능한 policy_id: 'refund'(환불), 'privacy'(개인정보), 'shipping'(배송)"""
    policies = {
        "refund": "구매 후 7일 이내 무조건 환불. 7~30일 미사용 시 수수료 10%. 30일 이후 불가.",
        "privacy": "수집: 이름, 이메일, 전화번호. 보관: 탈퇴 후 30일. 제3자 제공: 배송업체만.",
        "shipping": "기본 2-3일(무료). 빠른배송 당일~1일(3,000원). 도서산간 추가 2일.",
    }
    return policies.get(policy_id, f"'{policy_id}' 정책 없음. 사용 가능: refund, privacy, shipping")

# 종합 Agent
all_tools = [add, multiply, search_weather, get_policy]
all_tool_map = {t.name: t for t in all_tools}

llm_all = llm.bind_tools(all_tools)

system_msg = SystemMessage(content="""너는 도움이 되는 AI 비서야. 다음 도구를 사용할 수 있어:
- add: 두 숫자를 더한다
- multiply: 두 숫자를 곱한다
- search_weather: 도시 날씨 검색
- get_policy: 회사 정책 조회 (refund, privacy, shipping)

필요한 도구를 적극적으로 활용하여 정확한 답변을 해줘.""")

def run_full_agent(user_input: str):
    messages = [system_msg, HumanMessage(content=user_input)]

    while True:
        response = llm_all.invoke(messages)
        messages.append(response)

        if not response.tool_calls:
            return response.content

        for tc in response.tool_calls:
            print(f"  [Tool] {tc['name']}({tc['args']})")
            result = all_tool_map[tc["name"]].invoke(tc["args"])
            messages.append(ToolMessage(content=str(result), tool_call_id=tc["id"]))
```

Tool 개수가 너무 많아도 좋지 않음. 그래서 tool 관리법도 다양함. 연관된 tool 끼리 관리 한다던가..
tool 안에서 다시 LLM을 호출할 수도 있다고 함.

```python
# 종합 Agent 테스트
questions = [
    "서울 날씨 어때?",
    "25000 곱하기 3은?",
    "환불 정책이 어떻게 돼?",
    "서울이랑 부산 날씨 비교해줘",
    "안녕하세요!",
]

for q in questions:
    print(f"\n사용자: {q}")
    answer = run_full_agent(q)
    print(f"Agent: {answer}")
```