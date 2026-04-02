# RAG Agent

ReAct Agent에 Retriever를 Tool로 등록하면 **대화형 RAG**가 된다. 기본 RAG 파이프라인은 질문 하나에 검색 한 번, 답변 한 번이 전부였지만, Agent로 구성하면:

- 검색 없이 답변할 수 있는 질문은 **Tool 호출 생략**
- 여러 Tool을 등록하면 질문에 따라 **적절한 Tool을 선택**
- Checkpointer를 연결하면 **이전 대화를 기억**하면서 검색

| 구분 | 기본 RAG 파이프라인 | RAG Agent |
| --- | --- | --- |
| 검색 판단 | 항상 검색 | LLM이 필요 여부 판단 |
| 대화 기억 | 별도 구현 필요 | Checkpointer로 유지 |
| Tool 확장 | 어려움 | 웹 검색 등 Tool 추가 가능 |

```python
from dotenv import load_dotenv

load_dotenv()
```

## Retriever를 Tool로 변환

RAG 강의에서 만든 Chroma 벡터스토어에 연결하고, `create_retriever_tool`로 Tool을 만든다. 이 함수는 retriever를 감싸서 ReAct Agent가 호출할 수 있는 Tool로 변환한다.

```python
import chromadb
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.tools.retriever import create_retriever_tool

COLLECTION_NAME = "spri_ai_brief"
PERSIST_DIR = "./chroma_db"

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# 기존 벡터스토어에 연결
vectorstore = Chroma(
    embedding_function=embeddings,
    collection_name=COLLECTION_NAME,
    persist_directory=PERSIST_DIR,
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Retriever를 Tool로 변환
retriever_tool = create_retriever_tool(
    retriever,
    name="search_ai_brief",
    description="SPRi AI Brief 문서에서 AI 산업 동향 정보를 검색한다. AI 관련 정책, 기업 동향, 기술 트렌드 등을 질문할 때 사용한다.",
)

print(f"Tool 이름: {retriever_tool.name}")
print(f"Tool 설명: {retriever_tool.description}")
```

`create_retriever_tool`이 하는 일:

1. retriever의 `invoke(query)`를 호출하는 함수를 만든다
2. 검색된 Document들의 `page_content`를 합쳐서 문자열로 반환한다
3. `name`과 `description`으로 LLM이 이 Tool을 언제 사용할지 판단한다

`description`이 중요하다. LLM은 이 설명을 보고 Tool 호출 여부를 결정하므로, **어떤 정보가 들어있는지** 구체적으로 작성해야 한다.

## RAG Agent 구현

Retriever Tool을 ReAct Agent에 등록한다. `create_agent`를 사용하면 표준 ReAct 패턴을 한 줄로 만들 수 있다.

```python
# StateGraph로 직접 구성
graph_builder = StateGraph(MessagesState)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools))
graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")
graph = graph_builder.compile()

# create_agent로 동일한 그래프를 한 줄로 생성
graph = create_agent(model=llm, tools=tools)
```

내부적으로 동일한 구조(`chatbot → tools_condition → ToolNode → chatbot → ...`)가 만들어진다. 커스텀 노드나 분기가 필요 없는 표준 ReAct 패턴이면 `create_agent`가 간결하다. 이후 강의에서 Router, Reflection 같은 커스텀 구조가 필요한 패턴은 다시 `StateGraph`로 직접 구성한다.

```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

graph = create_agent(model=llm, tools=[retriever_tool])

print("RAG Agent 생성 완료")
```

```python
from IPython.display import Image, display

display(Image(graph.get_graph().draw_mermaid_png()))
```

### 테스트

기존 RAG와의 차이를 확인한다. Agent는 질문에 따라 **검색 여부를 스스로 판단**한다.

```python
# 문서 검색이 필요한 질문
question = "AI 반도체 관련 최근 동향을 알려줘"

for event in graph.stream({"messages": [("user", question)]}):
    for node_name, value in event.items():
        last_msg = value["messages"][-1]
        print(f"[{node_name}] {last_msg.type}: {last_msg.content[:200]}")
        if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
            print(f"  Tool 호출: {[tc['name'] for tc in last_msg.tool_calls]}")
        print()
```

```python
# 검색 없이 답변 가능한 질문
question = "안녕하세요!"

for event in graph.stream({"messages": [("user", question)]}):
    for node_name, value in event.items():
        last_msg = value["messages"][-1]
        print(f"[{node_name}] {last_msg.type}: {last_msg.content[:200]}")
        if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
            print(f"  Tool 호출: {[tc['name'] for tc in last_msg.tool_calls]}")
        print()
```

첫 번째 질문에서는 `search_ai_brief` Tool을 호출하고, 두 번째 질문에서는 Tool 호출 없이 바로 응답한다. 기존 RAG 파이프라인은 모든 질문에 대해 무조건 검색을 수행하지만, Agent는 **검색이 필요한 경우에만** Tool을 호출한다.

### 문서 기반 답변만 허용하기

RAG Agent는 검색 결과가 없거나 부족해도 LLM의 일반 지식으로 답변할 수 있다. 하지만 사내 문서 QA, 고객 응대 봇처럼 **승인된 문서에 근거한 답변만** 허용해야 하는 경우도 많다. 이때는 System Prompt로 제어한다.

```python
strict_rag_agent = create_agent(
    model=llm,
    tools=[retriever_tool],
    system_prompt="너는 AI 산업 문서 기반 QA 봇이다. 사용자가 질문하면 반드시 search_ai_brief 도구로 먼저 검색하라. 검색 결과에 관련 정보가 있으면 그 내용을 기반으로 답변하고, 관련 정보가 없으면 '해당 정보를 문서에서 찾을 수 없습니다.'라고 답하라. 문서에 없는 내용을 추측하거나 일반 지식으로 답변하지 마라.",
)

print("문서 기반 RAG Agent 생성 완료")
```

```python
# 문서에 없는 내용을 질문
result = strict_rag_agent.invoke(
    {"messages": [("user", "오늘 날씨 어때?")]}
)
print("질문: 오늘 날씨 어때?")
print(f"답변: {result['messages'][-1].content}")
print()

# 문서에 있는 내용을 질문
result = strict_rag_agent.invoke(
    {"messages": [("user", "AI 관련 최신 동향을 알려줘")]}
)
print("질문: AI 관련 최신 동향을 알려줘")
print(f"답변: {result['messages'][-1].content[:300]}")
```

System Prompt 하나로 Agent의 동작이 달라진다:

- 문서에 없는 질문 → 검색 후 관련 내용이 없으면 "찾을 수 없습니다"로 거절
- 문서에 있는 질문 → 검색 결과 기반으로 답변

용도에 따라 선택하면 된다:

- **개방형**: System Prompt 없이 사용. 문서 + 일반 지식으로 폭넓게 답변
- **제한형**: System Prompt로 문서 기반 답변만 허용. 정확성이 중요한 경우

## 대화형 RAG Agent

Checkpointer를 연결하면 이전 대화를 기억하는 RAG 챗봇이 된다. "아까 검색한 내용에서 더 알려줘"같은 후속 질문이 가능해진다.

```python
from langgraph.checkpoint.memory import MemorySaver

rag_agent = create_agent(
    model=llm,
    tools=[retriever_tool],
    checkpointer=MemorySaver(),
)

print("대화형 RAG Agent 생성 완료")
```

```python
config = {"configurable": {"thread_id": "rag-session-1"}}

# 첫 번째 질문: 문서 검색
result = rag_agent.invoke(
    {"messages": [("user", "구글 제미나이 관련 동향을 알려줘")]},
    config=config,
)
print(result["messages"][-1].content)
```

```python
# 두 번째 질문: 이전 대화를 기억한 후속 질문
result = rag_agent.invoke(
    {"messages": [("user", "그 중에서 가장 중요한 것 하나만 골라줘")]},
    config=config,
)
print(result["messages"][-1].content)
```

- 두 번째 질문은 LangChain을 사용할 때는 까다로운 질문이다. 문서에서 데이터를 가져온 것과 히스토리가 별개이기 때문.

```python
# 세 번째 질문: 검색 없이 대화 맥락으로 답변
result = rag_agent.invoke(
    {"messages": [("user", "위 내용을 영어로 번역해줘")]},
    config=config,
)
print(result["messages"][-1].content)
```

대화 흐름:

1. "구글 제미나이 동향" → `search_ai_brief` Tool 호출 → 문서 기반 답변
2. "가장 중요한 것 하나만" → 이전 답변 맥락에서 선별 (Tool 호출 없이 처리)
3. "영어로 번역" → Tool 호출 없이 대화 맥락으로 처리

Checkpointer가 없었다면 2, 3번 질문에서 "무슨 내용인지 모르겠다"고 답했을 것이다.

## 하이브리드 Agent: RAG + 웹 검색

문서에 없는 최신 정보는 웹 검색으로 보완할 수 있다. Retriever Tool과 웹 검색 Tool을 함께 등록하면, Agent가 질문에 따라 적절한 Tool을 선택한다.

```python
from langchain_tavily import TavilySearch

search = TavilySearch(max_results=3)

hybrid_agent = create_agent(
    model=llm,
    tools=[retriever_tool, search],
    checkpointer=MemorySaver(),
)

print("하이브리드 Agent 생성 완료")
```

`display(Image(hybrid_agent.get_graph().draw_mermaid_png()))`

```python
config = {"configurable": {"thread_id": "hybrid-session-1"}}

# 내부 문서 검색 → search_ai_brief 호출
result = hybrid_agent.invoke(
    {"messages": [("user", "AI Brief 문서에서 엔비디아 관련 내용을 찾아줘")]},
    config=config,
)
print(result["messages"][-1].content)
print()

# 최신 정보 검색 → tavily_search 호출
result = hybrid_agent.invoke(
    {"messages": [("user", "오늘 엔비디아 주가는 얼마야?")]},
    config=config,
)
print(result["messages"][-1].content)
```

LangSmith에서 각 호출의 트레이스를 확인하면, 첫 번째 질문은 `search_ai_brief`, 두 번째 질문은 `tavily_search`를 호출한 것을 볼 수 있다. Agent가 Tool의 `description`을 보고 판단한다:

- "AI Brief 문서에서" → `search_ai_brief` (내부 문서 검색)
- "오늘 주가" → `tavily_search` (실시간 웹 검색)

Tool을 추가하는 것만으로 Agent의 능력이 확장된다. 이것이 Agent 기반 RAG의 핵심 장점이다.