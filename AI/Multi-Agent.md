# Multi-Agent

하나의 Agent로 모든 작업을 처리하면 한계에 부딪힌다. 이번 강의에서는 여러 Agent를 조합하는 패턴인 **Supervisor**와 **Swarm**, 그리고 **Subgraph** 구성 방법을 배운다.

`# uv add langgraph-supervisor langgraph-swarm`

```python
from dotenv import load_dotenv

load_dotenv()
```

## Multi-Agent가 필요한 이유

하나의 Agent가 모든 것을 처리하면 문제가 생긴다.

| 문제 | 설명 |
| --- | --- |
| **프롬프트 비대** | 역할, 규칙, 예시가 너무 길어져서 LLM이 지시를 놓침 |
| **Tool 과다** | Tool이 10개, 20개가 되면 LLM의 Tool 선택 정확도가 하락 |
| **디버깅 어려움** | 하나의 거대한 Agent에서 어디가 잘못됐는지 찾기 힘듦 |

해결: **전문 Agent를 분리하고 협업**시킨다.

```
단일 Agent (모든 Tool)  →  리서치 Agent (검색 Tool)
                           작성 Agent (생성 Tool)
                           검증 Agent (평가 Tool)
```

Agent를 나누면 각 Agent의 프롬프트가 짧아지고, Tool 수가 줄어 정확도가 올라간다.

## Supervisor 패턴

**관리자(Supervisor) Agent**가 작업을 분배하고 결과를 종합하는 패턴이다.

```
                    ┌→ 리서치 Agent ─┐
사용자 → Supervisor ├→ 작성 Agent   ─┤→ Supervisor → 최종 답변
                    └→ 검증 Agent   ─┘
```

동작 방식:

1. Supervisor가 사용자 요청을 분석한다
2. **Structured Output**으로 다음에 호출할 Agent를 결정한다
3. 해당 Agent가 작업을 수행하고 결과를 State에 기록한다
4. Supervisor가 다시 판단 -- 추가 작업이 필요하면 다른 Agent를 호출, 충분하면 종료

핵심: **개발자가 Supervisor의 판단 기준을 설계**한다. 흐름의 제어권이 Supervisor에 집중된다.

## Supervisor 구현

시나리오: 사용자가 주제를 주면 **리서치 → 작성 → 검증** 순서로 보고서를 만든다.

- **researcher**: 주제에 대한 핵심 정보를 조사
- **writer**: 조사 결과를 바탕으로 보고서 작성
- **reviewer**: 보고서를 검토하고 피드백
- **supervisor**: 대화 맥락을 보고 다음에 어떤 Agent를 호출할지 판단

**Supervisor의 핵심은 LLM이 맥락을 보고 동적으로 판단하는 것**이므로, 프롬프트에는 순서 대신 판단 기준을 제공한다.

```python
from typing import Annotated, TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
```

### State 정의

`next` 필드가 핵심이다. Supervisor가 여기에 다음 Agent 이름을 기록하면 conditional_edges가 해당 노드로 라우팅한다.

```python
class SupervisorState(TypedDict):
    messages: Annotated[list, add_messages]
    next: str
```

### Supervisor 라우팅 스키마 (Pydantic)

Supervisor가 Structured Output으로 다음 Agent를 결정한다.

```python
members = ["researcher", "writer", "reviewer"]

class RouteDecision(BaseModel):
    """다음에 호출할 Agent를 결정한다."""
    next: Literal["researcher", "writer", "reviewer", "FINISH"] = Field(
        description="다음에 작업할 Agent 이름. 모든 작업이 끝났으면 FINISH."
    )
```

### 노드 정의

```python
def supervisor(state: SupervisorState):
    """다음에 호출할 Agent를 결정한다."""
    system_prompt = (
        "너는 보고서 작성 프로젝트의 관리자다. "
        "팀원: researcher(조사), writer(작성), reviewer(검토).\n"
        "대화 내용을 보고, 다음에 어떤 팀원이 작업해야 하는지 판단해.\n"
        "- 조사가 부족하면 researcher를 호출해.\n"
        "- 조사가 충분하고 보고서가 없으면 writer를 호출해.\n"
        "- 보고서가 있고 검토가 안 됐으면 reviewer를 호출해.\n"
        "- reviewer가 수정을 요청하면 writer에게 돌려보내.\n"
        "- 검토가 완료되고 승인되면 FINISH."
    )
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = llm.with_structured_output(RouteDecision).invoke(messages)
    return {"next": response.next}

def researcher(state: SupervisorState):
    """주제에 대한 핵심 정보를 조사한다."""
    system_prompt = (
        "너는 리서치 전문가다. 주어진 주제에 대해 핵심 사실 3~5개를 조사하여 정리해."
    )
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

def writer(state: SupervisorState):
    """조사 결과를 바탕으로 보고서를 작성한다."""
    system_prompt = (
        "너는 보고서 작성 전문가다. 조사된 내용을 바탕으로 간결한 보고서를 작성해. "
        "구조: 제목, 개요, 본문, 결론."
    )
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

def reviewer(state: SupervisorState):
    """보고서를 검토하고 피드백을 제공한다."""
    system_prompt = (
        "너는 보고서 검토 전문가다. 보고서의 정확성, 구조, 가독성을 평가하고 "
        "간단한 피드백을 제공해. 수정이 필요 없으면 '승인'이라고 명시해."
    )
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}
```

### 그래프 구성

Supervisor 노드의 `next` 값에 따라 conditional_edges로 다음 Agent 노드를 실행한다. 작업이 끝나면 다시 Supervisor로 돌아온다.

```python
def route_next(state: SupervisorState):
    return state["next"]

builder = StateGraph(SupervisorState)

# 노드 등록
builder.add_node("supervisor", supervisor)
builder.add_node("researcher", researcher)
builder.add_node("writer", writer)
builder.add_node("reviewer", reviewer)

# 시작 → supervisor
builder.add_edge(START, "supervisor")

# supervisor → 조건부 분기
builder.add_conditional_edges(
    "supervisor",
    route_next,
    {
        "researcher": "researcher",
        "writer": "writer",
        "reviewer": "reviewer",
        "FINISH": END,
    },
)

# 각 Agent → 다시 supervisor로
builder.add_edge("researcher", "supervisor")
builder.add_edge("writer", "supervisor")
builder.add_edge("reviewer", "supervisor")

supervisor_graph = builder.compile()
```

```python
from IPython.display import Image, display

display(Image(supervisor_graph.get_graph().draw_mermaid_png()))
```

### 실행

```python
for event in supervisor_graph.stream(
    {"messages": [HumanMessage(content="AI Agent 기술 동향에 대한 보고서를 작성해줘.")]},
    stream_mode="updates",
):
    for node_name, state in event.items():
        if node_name == "supervisor":
            print(f"[supervisor] next → {state['next']}")
        else:
            print(f"\n[{node_name}]")
            print(state["messages"][-1].content[:300])
    print()
```

Supervisor가 `researcher → writer → reviewer → FINISH` 순서로 Agent를 호출한 것을 확인할 수 있다. 각 Agent는 자기 역할만 수행하고, Supervisor가 전체 흐름을 제어한다.

### langgraph-supervisor 패키지

위에서 직접 구현한 Supervisor 패턴을 헬퍼 함수로 간단하게 만들 수도 있다. `langgraph-supervisor` 패키지의 `create_supervisor`를 사용하면 된다.

빠른 프로토타입이나 단순한 구조에는 편리하지만, Supervisor의 판단 로직을 세밀하게 제어하거나 복잡한 State 관리가 필요하면 직접 `StateGraph`로 구성하는 것이 낫다. 원리를 이해한 뒤 상황에 맞게 선택하면 된다.

```python
from langgraph_supervisor import create_supervisor
from langchain.agents import create_agent

# 각 Agent를 create_agent로 생성 (tool 없이 LLM만 사용)
researcher_agent = create_agent(
    model=llm,
    tools=[],
    system_prompt="너는 리서치 전문가다. 주어진 주제에 대해 핵심 사실 3~5개를 조사하여 정리해.",
    name="researcher",
)

writer_agent = create_agent(
    model=llm,
    tools=[],
    system_prompt="너는 보고서 작성 전문가다. 조사된 내용을 바탕으로 간결한 보고서를 작성해. 구조: 제목, 개요, 본문, 결론.",
    name="writer",
)

reviewer_agent = create_agent(
    model=llm,
    tools=[],
    system_prompt="너는 보고서 검토 전문가다. 보고서의 정확성, 구조, 가독성을 평가하고 간단한 피드백을 제공해. 수정이 필요 없으면 '승인'이라고 명시해.",
    name="reviewer",
)

# Supervisor 그래프를 한 줄로 생성
supervisor_app = create_supervisor(
    agents=[researcher_agent, writer_agent, reviewer_agent],
    model=llm,
    system_prompt="너는 보고서 작성 프로젝트의 관리자다. 대화 내용을 보고 적절한 팀원에게 작업을 위임해.",
).compile()

display(Image(supervisor_app.get_graph().draw_mermaid_png()))
```

## Swarm 패턴

Supervisor와 반대 방향의 접근이다. **중앙 관리자 없이** Agent끼리 직접 작업을 넘긴다.

핵심 메커니즘: **handoff** -- 현재 Agent가 `Command(goto="다른_agent")`를 반환하면 그 Agent로 전환된다.

```
사용자 → 항공 Agent ──handoff──→ 호텔 Agent ──handoff──→ 액티비티 Agent → 종료
```

각 Agent가 자기 작업을 마치면 **스스로** 다음 담당 Agent를 결정한다. conditional_edges가 아니라 Agent 내부에서 `Command`로 전환하는 것이 핵심이다.

| 비교 | Supervisor | Swarm |
| --- | --- | --- |
| 전환 결정 | Supervisor가 결정 | 현재 Agent가 결정 |
| 사용 도구 | conditional_edges | Command(goto=...) |
| 중앙 제어 | 있음 | 없음 |

## Swarm 구현

시나리오: **여행사 챗봇** -- 항공 담당, 호텔 담당, 액티비티 담당 Agent가 handoff로 협업한다.

각 Agent가 자기 역할을 수행한 뒤, **LLM이 Structured Output으로 다음 Agent를 직접 결정**한다. Supervisor와 달리 중앙 관리자 없이 Agent 내부에서 handoff가 일어난다.

### State 정의

```python
import operator
from langgraph.types import Command
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

class SwarmState(TypedDict):
    messages: Annotated[list, add_messages]
    travel_plan: Annotated[list, operator.add]

class HandoffDecision(BaseModel):
    """현재 작업 완료 후, 다음에 넘길 Agent를 결정한다."""
    next: Literal["flight_agent", "hotel_agent", "activity_agent", "FINISH"] = Field(
        description="다음에 작업할 Agent. 모든 여행 계획이 완성되면 FINISH."
    )
```

```python
def make_agent(name: str, role_prompt: str):
    """Swarm Agent를 생성한다. 작업 수행 후 LLM이 다음 Agent를 직접 결정한다."""

    def agent(state: SwarmState):
        # 1. 자기 역할 수행
        messages = [SystemMessage(content=role_prompt)] + state["messages"]
        response = llm.invoke(messages)
        print(f"[{name}] {response.content[:200]}")

        # 2. LLM이 다음 Agent를 판단 (handoff)
        handoff_prompt = (
            "너는 여행 계획 팀의 일원이다. 지금까지 대화를 보고, "
            "다음에 어떤 Agent가 작업해야 하는지 판단해.\n"
            "- flight_agent: 항공편 추천이 필요할 때\n"
            "- hotel_agent: 호텔 추천이 필요할 때\n"
            "- activity_agent: 액티비티 추천이 필요할 때\n"
            "- FINISH: 항공편, 호텔, 액티비티가 모두 완성되었을 때"
        )
        handoff_messages = [SystemMessage(content=handoff_prompt)] + state["messages"] + [response]
        decision = llm.with_structured_output(HandoffDecision).invoke(handoff_messages)
        print(f"  → handoff: {decision.next}")

        update = {
            "messages": [response],
            "travel_plan": [f"{name}: {response.content[:100]}"],
        }

        if decision.next == "FINISH":
            return update
        return Command(goto=decision.next, update=update)

    return agent

flight_agent = make_agent(
    "flight_agent",
    "너는 항공편 추천 전문가다. 사용자의 여행 계획을 보고 적절한 항공편을 추천해. 간단하게 항공편 정보만 출력해.",
)

hotel_agent = make_agent(
    "hotel_agent",
    "너는 호텔 추천 전문가다. 앞서 정해진 항공편 정보를 참고하여 적절한 호텔을 추천해. 간단하게 호텔 정보만 출력해.",
)

activity_agent = make_agent(
    "activity_agent",
    "너는 여행 액티비티 추천 전문가다. 앞서 정해진 항공편과 호텔을 참고하여 적절한 액티비티 2~3개를 추천해. 간단하게 출력해.",
)
```

```python
builder = StateGraph(SwarmState)

builder.add_node("flight_agent", flight_agent)
builder.add_node("hotel_agent", hotel_agent)
builder.add_node("activity_agent", activity_agent)

builder.add_edge(START, "flight_agent")
# Swarm에서는 conditional_edges가 필요 없다.
# Command(goto=...)가 다음 노드를 직접 지정하기 때문이다.
# FINISH인 경우 Command 없이 dict를 반환하므로, 각 Agent → END 엣지를 추가한다.
builder.add_edge("flight_agent", END)
builder.add_edge("hotel_agent", END)
builder.add_edge("activity_agent", END)

swarm_graph = builder.compile()
```

`display(Image(swarm_graph.get_graph().draw_mermaid_png()))`

그래프 시각화를 보면 flight_agent에서 hotel_agent, activity_agent로 가는 엣지가 없다. `Command`가 런타임에 동적으로 전환하기 때문이다.

```
result = swarm_graph.invoke({
    "messages": [HumanMessage(content="7월에 도쿄 3박 4일 여행을 계획해줘.")],
    "travel_plan": [],
})

print("\n=== 최종 여행 계획 ===")
for item in result["travel_plan"]:
    print(f"- {item}")
```

각 Agent가 작업을 마친 뒤 **LLM이 다음 Agent를 판단**하고 `Command(goto=...)`로 직접 전환했다. Supervisor 없이 Agent 간 자율 전환이 이루어진 것이다.

Supervisor 패턴과 비교하면, 라우팅 LLM 호출이 중앙(Supervisor 노드)이 아니라 **각 Agent 내부**에 분산되어 있다는 점이 핵심 차이다.

## Supervisor vs Swarm 비교

| 항목 | Supervisor | Swarm |
| --- | --- | --- |
| **제어 방식** | 중앙 관리자가 다음 Agent 결정 | 각 Agent가 스스로 다음 Agent 결정 |
| **구현 방식** | Structured Output + conditional_edges | Command(goto=...) |
| **흐름 가시성** | 높음 (Supervisor 로그에 전체 흐름 기록) | 중간 (각 Agent의 handoff를 추적해야 함) |
| **유연성** | 동적 순서 변경 가능 (Supervisor가 판단) | Agent 내부 로직에 따라 전환 |
| **적합한 상황** | 복잡한 워크플로우, 명확한 역할 분리 | 대화형 서비스, 자연스러운 전환이 필요한 경우 |
| **장점** | 전체 흐름을 한 곳에서 제어, 디버깅 용이 | 간결한 구현, Agent 추가가 쉬움 |
| **단점** | Supervisor가 병목, 프롬프트 설계 중요 | 전체 흐름 파악 어려움, 무한 루프 위험 |

> Swarm은 Agent끼리 서로를 계속 호출하여 무한 루프에 빠질 수 있으므로 `recursion_limit` 설정에 주의한다.
> 

### 선택 기준

- 판단을 **한 곳에 집중**시켜 흐름을 파악하기 쉽게 하려면 → Supervisor
- 판단을 **각 Agent에 분산**시켜 자율적으로 처리하게 하려면 → Swarm
- 실무에서는 **혼합**도 가능하다. Supervisor가 큰 단계를 관리하고, 각 단계 내부에서 Swarm으로 세부 작업을 처리하는 방식.

### langgraph-swarm 패키지

`langgraph-supervisor`와 마찬가지로, Swarm 패턴도 `langgraph-swarm` 패키지로 간단하게 구성할 수 있다. `create_handoff_tool`로 Agent 간 전환 Tool을 만들고, `create_swarm`으로 그래프를 생성한다.

```python
from langgraph_swarm import create_swarm, create_handoff_tool
from langchain.agents import create_agent

# 각 Agent에 handoff tool을 등록하여 다른 Agent로 전환할 수 있게 한다
flight_swarm = create_agent(
    model=llm,
    tools=[
        create_handoff_tool(agent_name="hotel_swarm", description="호텔 추천이 필요할 때"),
        create_handoff_tool(agent_name="activity_swarm", description="액티비티 추천이 필요할 때"),
    ],
    system_prompt="너는 항공편 추천 전문가다. 항공편을 추천한 뒤, 다음 단계의 Agent에게 넘겨라.",
    name="flight_swarm",
)

hotel_swarm = create_agent(
    model=llm,
    tools=[
        create_handoff_tool(agent_name="flight_swarm", description="항공편 추천이 필요할 때"),
        create_handoff_tool(agent_name="activity_swarm", description="액티비티 추천이 필요할 때"),
    ],
    system_prompt="너는 호텔 추천 전문가다. 호텔을 추천한 뒤, 다음 단계의 Agent에게 넘겨라.",
    name="hotel_swarm",
)

activity_swarm = create_agent(
    model=llm,
    tools=[
        create_handoff_tool(agent_name="flight_swarm", description="항공편 추천이 필요할 때"),
        create_handoff_tool(agent_name="hotel_swarm", description="호텔 추천이 필요할 때"),
    ],
    system_prompt="너는 여행 액티비티 추천 전문가다. 액티비티 2~3개를 추천해.",
    name="activity_swarm",
)

swarm_app = create_swarm(
    agents=[flight_swarm, hotel_swarm, activity_swarm],
    default_active_agent="flight_swarm",
).compile()

display(Image(swarm_app.get_graph().draw_mermaid_png()))
```

## Subgraph

Multi-Agent 시스템에서 각 Agent를 **독립적인 그래프로 구성**한 뒤, 부모 그래프의 노드로 등록할 수 있다. 이렇게 등록된 그래프를 **Subgraph**라 한다.

Subgraph를 사용하면 각 Agent를 독립적으로 개발·테스트한 뒤, 더 큰 워크플로우에 조합할 수 있다. Supervisor나 Swarm 패턴의 각 Agent를 Subgraph로 만들면 재사용성이 높아진다.

### 같은 State 스키마를 공유하는 경우

부모와 Subgraph의 State 스키마가 같으면, **컴파일된 그래프를 그대로 `add_node`에 전달**하면 된다.

```python
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from IPython.display import Image, display

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# --- 같은 State 스키마를 공유하는 Subgraph 예제 ---

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# Subgraph 1: 리서치 Agent (독립적으로 구성)
def research_node(state: AgentState):
    system = SystemMessage(content="너는 리서치 전문가다. 주어진 주제의 핵심 사실 3개를 정리해.")
    response = llm.invoke([system] + state["messages"])
    return {"messages": [response]}

research_builder = StateGraph(AgentState)
research_builder.add_node("research", research_node)
research_builder.add_edge(START, "research")
research_builder.add_edge("research", END)
research_graph = research_builder.compile()  # 독립 그래프로 컴파일

# Subgraph 2: 작성 Agent (독립적으로 구성)
def writing_node(state: AgentState):
    system = SystemMessage(content="너는 보고서 작성 전문가다. 이전 내용을 바탕으로 간결한 보고서를 작성해.")
    response = llm.invoke([system] + state["messages"])
    return {"messages": [response]}

writing_builder = StateGraph(AgentState)
writing_builder.add_node("write", writing_node)
writing_builder.add_edge(START, "write")
writing_builder.add_edge("write", END)
writing_graph = writing_builder.compile()  # 독립 그래프로 컴파일

# 부모 그래프: Subgraph를 노드로 등록
parent_builder = StateGraph(AgentState)

# 컴파일된 그래프를 그대로 노드로 추가한다
parent_builder.add_node("researcher", research_graph)
parent_builder.add_node("writer", writing_graph)

parent_builder.add_edge(START, "researcher")
parent_builder.add_edge("researcher", "writer")
parent_builder.add_edge("writer", END)

parent_graph = parent_builder.compile()

display(Image(parent_graph.get_graph().draw_mermaid_png()))
```

```python
# 실행 -- subgraphs=True로 자식 그래프의 실행까지 스트리밍한다
for namespace, chunk in parent_graph.stream(
    {"messages": [HumanMessage(content="LangGraph의 Subgraph 기능에 대해 정리해줘.")]},
    subgraphs=True,
    stream_mode="updates",
):
    for node_name, state in chunk.items():
        prefix = f"{namespace}" if namespace else "(parent)"
        print(f"{prefix} / {node_name}")
        print(state["messages"][-1].content[:300])
        print()
```

### State가 다른 Subgraph

부모와 Subgraph의 State 스키마가 다르면, **래퍼 함수**로 State를 변환한다.

실무에서는 이런 경우가 자주 있다:

- **외부 API 래핑**: 검색 Agent는 `query/results` State로 동작하는데, 부모는 `messages` 기반일 때
- **기존 그래프 재사용**: 이미 만들어둔 독립 그래프를 새 프로젝트에 붙일 때 State가 안 맞는 경우

```python
# --- State가 다른 Subgraph 예제 ---

# Subgraph State (부모와 다름)
class AnalysisState(TypedDict):
    input_text: str
    analysis: str

def analysis_node(state: AnalysisState):
    system = SystemMessage(content="주어진 텍스트를 분석하여 핵심 키워드 3개와 요약을 제공해.")
    response = llm.invoke([system, HumanMessage(content=state["input_text"])])
    return {"analysis": response.content}

analysis_builder = StateGraph(AnalysisState)
analysis_builder.add_node("analyze", analysis_node)
analysis_builder.add_edge(START, "analyze")
analysis_builder.add_edge("analyze", END)
analysis_graph = analysis_builder.compile()

# 부모 State
class ParentState(TypedDict):
    messages: Annotated[list, add_messages]
    report: str

# 래퍼 함수: 부모 State → Subgraph State → 부모 State
def analysis_wrapper(state: ParentState):
    sub_input = {"input_text": state["messages"][-1].content}
    sub_result = analysis_graph.invoke(sub_input)
    return {"report": sub_result["analysis"]}

def report_node(state: ParentState):
    system = SystemMessage(content="분석 결과를 바탕으로 간결한 보고서를 작성해.")
    response = llm.invoke([system, HumanMessage(content=state["report"])])
    return {"messages": [response]}

parent_builder = StateGraph(ParentState)
parent_builder.add_node("analysis", analysis_wrapper)  # 래퍼 함수를 노드로 등록
parent_builder.add_node("report", report_node)
parent_builder.add_edge(START, "analysis")
parent_builder.add_edge("analysis", "report")
parent_builder.add_edge("report", END)

diff_state_graph = parent_builder.compile()
display(Image(diff_state_graph.get_graph().draw_mermaid_png()))
```

```python
result = diff_state_graph.invoke({
    "messages": [HumanMessage(content="최근 AI Agent 기술의 발전 방향과 주요 트렌드를 분석해줘.")]
})

print("[분석 결과 (Subgraph)]")
print(result["report"][:300])
print()
print("[최종 보고서 (부모)]")
print(result["messages"][-1].content[:300])
```

### Subgraph에서 부모 그래프로 이동: Command.PARENT

Subgraph 내부에서 부모 그래프의 특정 노드로 직접 이동해야 할 때는 `Command`의 `graph` 파라미터를 사용한다.

```python
return Command(
    goto="parent_node_name",
    update={"result": "완료"},
    graph=Command.PARENT,  # 부모 그래프로 전환
)
```