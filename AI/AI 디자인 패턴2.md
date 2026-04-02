# Reflection + Evaluator-Optimizer

Agent가 자기 출력을 검토하고 개선하는 두 가지 패턴을 배운다.

| 패턴 | 핵심 | 평가 방식 |
| --- | --- | --- |
| **Reflection** | 생성 → 자기 검토 → 수정 루프 | 정성적 (자연어 피드백) |
| **Evaluator-Optimizer** | 생성 → 루브릭 채점 → 미달 항목 개선 | 정량적 (점수 + pass/fail) |

```python
from dotenv import load_dotenv

load_dotenv()
```

## Reflection 패턴

가장 단순한 자기 개선 루프다.

```
START → generate → reflect → should_continue? → generate (반복)
                                              → END (종료)
```

동작 순서:

1. **generate** 노드가 초안을 작성한다
2. **reflect** 노드가 초안을 읽고 피드백을 준다 (톤, 빠진 정보, 길이 등)
3. **should_continue**가 반복 횟수를 체크한다 — 상한에 도달하면 종료
4. 종료 전이면 피드백을 반영해 다시 generate로 돌아간다

State에 `messages`를 누적하므로 generate 노드는 이전 피드백을 자연스럽게 참고한다.

## Reflection 실습

시나리오: 고객에게 보내는 사과 이메일 초안을 작성하고, 반복적으로 개선한다.

```python
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

class ReflectionState(TypedDict):
    messages: Annotated[list, add_messages]
    iteration: int

MAX_ITERATIONS = 3
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
```

```python
def generate(state: ReflectionState):
    """초안을 작성하거나 피드백을 반영해 수정한다."""
    system = SystemMessage(content=(
        "너는 고객 커뮤니케이션 전문가다. "
        "이전 피드백이 있으면 반영해서 이메일을 수정해. "
        "이메일 본문만 출력해."
    ))
    # 전체 messages를 넘기면 generate는 이전 피드백까지 자연스럽게 참고한다
    response = llm.invoke([system] + state["messages"])
    return {
        # name으로 역할을 구분한다 — reflect에서 generator의 메시지만 골라내기 위함
        "messages": [AIMessage(content=response.content, name="generator")],
        "iteration": state.get("iteration", 0) + 1,
    }

def reflect(state: ReflectionState):
    """초안을 검토하고 구체적인 피드백을 준다."""
    system = SystemMessage(content=(
        "너는 비즈니스 이메일 리뷰어다. "
        "다음 관점에서 피드백을 줘:\n"
        "1. 톤: 진정성 있는 사과인가?\n"
        "2. 빠진 정보: 구체적 해결 방안이 있는가?\n"
        "3. 길이: 간결한가?\n\n"
        "개선이 필요한 부분만 구체적으로 지적해. "
        "잘 된 부분은 언급하지 마."
    ))
    # 리뷰어는 최신 초안만 보면 된다 — 이전 대화 맥락 없이 객관적으로 평가
    last_ai = [m for m in state["messages"] if m.name == "generator"][-1]
    response = llm.invoke([system, HumanMessage(content=last_ai.content)])
    # HumanMessage로 넣는 이유: generate 노드의 LLM 입장에서 피드백은
    # "사용자 지시"처럼 작용해야 하므로 AIMessage가 아닌 HumanMessage로 넣는다
    return {
        "messages": [HumanMessage(content=response.content, name="reviewer")],
    }

def should_continue(state: ReflectionState):
    if state["iteration"] >= MAX_ITERATIONS:
        return "end"
    return "continue"
```

```python
builder = StateGraph(ReflectionState)

builder.add_node("generate", generate)
builder.add_node("reflect", reflect)

builder.add_edge(START, "generate")
builder.add_edge("generate", "reflect")
builder.add_conditional_edges(
    "reflect",
    should_continue,
    {"continue": "generate", "end": END},
)

reflection_graph = builder.compile()
```

```python
from IPython.display import Image, display

display(Image(reflection_graph.get_graph().draw_mermaid_png()))
```

```python
task = "배송이 2주 지연된 고객에게 사과 이메일을 작성해줘. 고객명: 김민수, 주문번호: ORD-2024-1234"

result = reflection_graph.invoke(
    {"messages": [HumanMessage(content=task)], "iteration": 0}
)

print(f"총 반복 횟수: {result['iteration']}")
print(f"총 메시지 수: {len(result['messages'])}")
print("\n" + "=" * 60)

for msg in result["messages"]:
    name = getattr(msg, "name", None) or msg.type
    print(f"\n[{name}]")
    print(msg.content[:500])
    print("-" * 40)
```

반복할수록 피드백이 반영되어 품질이 올라가는 것을 확인할 수 있다. 하지만 Reflection에는 한계가 있다.

- 피드백이 **자연어**라서 "얼마나 좋아졌는지" 정량화할 수 없다
- "충분히 좋다"의 기준이 없으므로 항상 `max_iterations`까지 반복한다
- 반복할수록 피드백이 점점 미세해진다 — 위 출력에서도 3번째 리뷰어는 "깊이 유감스럽게" → "진심으로 안타깝게" 같은 표현 수준의 차이만 지적하는데, 이것이 실질적 개선인지 알 수 없다
- 반복이 많아지면 원래 의도에서 벗어나거나 과하게 수정되는 경우도 있다 (항상 품질이 올라가는 것은 아니다)

이 문제를 해결하는 것이 Evaluator-Optimizer 패턴이다.

## Evaluator-Optimizer 패턴

Reflection과 구조는 비슷하지만 핵심 차이가 있다.

|  | Reflection | Evaluator-Optimizer |
| --- | --- | --- |
| 평가 방식 | 자연어 피드백 | 점수 (1~10) + pass/fail |
| 종료 조건 | 고정 횟수 | 점수 기준 달성 시 조기 종료 |
| 개선 지시 | 전체적 피드백 | 미달 항목만 타겟팅 |
| 재현성 | 낮음 | 높음 (루브릭 고정) |

```
START → generate → evaluate → pass? → END
                      ↓ fail
                   optimize → generate (재시도)
```

시나리오: 마케팅 카피 생성. 루브릭으로 채점하고 미달 시 개선한다.

## 루브릭 설계

루브릭(Rubric)은 **평가 항목과 점수 기준을 정리한 채점표**다. 좋은 루브릭은 구체적이고 측정 가능하다.

| 나쁜 루브릭 | 좋은 루브릭 |
| --- | --- |
| "매력적인가?" | "감정을 자극하는 단어가 1개 이상 포함되어 있는가?" |
| "적절한 길이인가?" | "50자 이상 150자 이하인가?" |
| "좋은 카피인가?" | "행동 유도(CTA)가 포함되어 있는가?" |

Pydantic 모델로 평가 결과를 구조화한다.

```python
from pydantic import BaseModel, Field

class CriterionScore(BaseModel):
    name: str = Field(description="평가 항목명")
    score: int = Field(description="1~10 점수", ge=1, le=10)
    reason: str = Field(description="점수 근거 (1문장)")

class EvaluationResult(BaseModel):
    criteria: list[CriterionScore] = Field(description="각 항목별 평가")
    summary: str = Field(description="전체 평가 요약 (1~2문장)")
```

루브릭은 도메인마다 완전히 달라진다. 마케팅 카피라면 "감정 자극, CTA 포함, 글자 수", 기술 문서라면 "정확성, 재현 가능성, 코드 포함" 등이 핵심 기준이 된다. 설계할 때는 해당 도메인의 핵심 품질 기준을 먼저 정의하고, 각 기준을 측정 가능한 형태로 변환한 뒤, 점수 척도와 합격 기준을 설정한다.

## State와 노드 설계

```python
class EvalOptState(TypedDict):
    task: str          # 입력: 카피 작성 지시
    copy: str          # 현재 카피
    evaluation: dict   # EvaluationResult를 dict로 저장
    iteration: int     # 반복 횟수
    history: list      # 이전 시도 기록 (리듀서: operator.add)
```

`history`의 각 원소는 다음 구조다:

```python
{
    "copy": "이전에 생성한 카피",
    "evaluation": { ... },       # EvaluationResult.model_dump() 결과
    "improvement": "미달 항목에 대한 개선 지시",
}
```

노드별 역할:

| 노드 | 입력 | 출력 | 역할 |
| --- | --- | --- | --- |
| `generate` | task, history | copy | 카피 생성 (history가 있으면 개선 지시 반영) |
| `evaluate` | copy | evaluation, iteration | 루브릭으로 채점 (Structured Output) |
| `optimize` | copy, evaluation | history | 미달 항목만 골라 개선 지시 작성 |

```python
from operator import add

class EvalOptState(TypedDict):
    task: str
    copy: str
    evaluation: dict  # EvaluationResult를 dict로 저장
    iteration: int
    history: Annotated[list, add]

MAX_ITERATIONS = 4
PASS_THRESHOLD = 8
eval_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
```

```python
def generate_copy(state: EvalOptState):
    """마케팅 카피를 생성한다. 이전 평가가 있으면 optimize 노드의 지시를 참고한다."""
    task = state["task"]
    history = state.get("history", [])

    if history:
        last = history[-1]
        prompt = (
            f"작업: {task}\n\n"
            f"이전 카피:\n{last['copy']}\n\n"
            f"개선 지시:\n{last['improvement']}\n\n"
            "위 지시를 반영해서 카피를 다시 작성해. 카피만 출력해."
        )
    else:
        prompt = f"다음 마케팅 카피를 작성해. 카피만 출력해.\n\n작업: {task}"

    response = llm.invoke(prompt)
    return {"copy": response.content}

def evaluate_copy(state: EvalOptState):
    """루브릭에 따라 카피를 채점한다. Structured Output 사용."""
    copy = state["copy"]
    evaluator = eval_llm.with_structured_output(EvaluationResult)

    result = evaluator.invoke(f"""\
다음 마케팅 카피를 평가해.

카피:
{copy}

평가 기준 (각 1~10점):
1. clarity: 메시지가 명확하고 이해하기 쉬운가?
2. emotion: 감정을 자극하는 표현이 있는가?
3. cta: 행동 유도(구매, 클릭 등)가 포함되어 있는가?
4. conciseness: 간결한가? (불필요한 표현 없는가?)""")

    # pass/fail 판정은 LLM이 아닌 코드로 수행한다 — 점수 기반 판정의 핵심은 재현성이다
    evaluation = result.model_dump()
    evaluation["overall_pass"] = all(
        c["score"] >= PASS_THRESHOLD for c in evaluation["criteria"]
    )

    return {
        "evaluation": evaluation,
        "iteration": state.get("iteration", 0) + 1,
    }

def optimize_copy(state: EvalOptState):
    """미달 항목만 골라서 구체적인 개선 지시를 만든다."""
    evaluation = state["evaluation"]
    failed = [c for c in evaluation["criteria"] if c["score"] < PASS_THRESHOLD]
    items = "\n".join(
        f"- {c['name']} ({c['score']}점): {c['reason']}" for c in failed
    )

    return {
        "history": [{
            "copy": state["copy"],
            "evaluation": evaluation,
            "improvement": f"다음 항목을 개선해:\n{items}",
        }],
    }

def should_continue_eval(state: EvalOptState):
    if state["evaluation"]["overall_pass"]:
        return "end"
    if state["iteration"] >= MAX_ITERATIONS:
        return "end"  # 상한 도달 시에도 종료
    return "fail"
```

```python
builder = StateGraph(EvalOptState)

builder.add_node("generate", generate_copy)
builder.add_node("evaluate", evaluate_copy)
builder.add_node("optimize", optimize_copy)

builder.add_edge(START, "generate")
builder.add_edge("generate", "evaluate")
builder.add_conditional_edges(
    "evaluate",
    should_continue_eval,
    {"end": END, "fail": "optimize"},
)
builder.add_edge("optimize", "generate")

eval_opt_graph = builder.compile()

display(Image(eval_opt_graph.get_graph().draw_mermaid_png()))
```

```python
task = "AI 기반 영어 학습 앱 'SmartLingo' 출시 광고 카피. 타겟: 20~30대 직장인. 핵심 가치: 출퇴근 10분으로 영어 실력 향상."

for event in eval_opt_graph.stream({"task": task, "iteration": 0, "history": []}):
    node_name = list(event.keys())[0]
    state_update = event[node_name]

    if node_name == "generate":
        print(f"\n{'=' * 60}")
        print(f"[generate] 카피 생성")
        print(state_update["copy"])

    elif node_name == "evaluate":
        iteration = state_update["iteration"]
        evaluation = state_update["evaluation"]
        status = "PASS ✓" if evaluation["overall_pass"] else "FAIL ✗"
        print(f"\n[evaluate] 반복 {iteration} — {status}")
        for c in evaluation["criteria"]:
            mark = "PASS" if c["score"] >= PASS_THRESHOLD else "FAIL"
            print(f"  {c['name']}: {c['score']}/10 ({mark}) - {c['reason']}")

    elif node_name == "optimize":
        h = state_update["history"][0]
        print(f"\n[optimize] 개선 지시")
        print(h["improvement"])
```

핵심 포인트:

- `evaluate` 노드가 Structured Output으로 **정량 점수**를 반환한다
- `overall_pass` 판정은 LLM이 아닌 **코드로** 수행한다 — 점수를 매기는 건 LLM, 합격 여부는 코드가 결정
- `overall_pass`로 **조기 종료**가 가능하다 (불필요한 반복 방지)
- `optimize` 노드가 **미달 항목만** 타겟팅한다 (이미 좋은 부분은 건드리지 않음)
- `MAX_ITERATIONS`로 무한 반복을 방지한다

주의: 이 예제에서는 같은 LLM이 생성과 평가를 모두 수행한다. 실무에서는 평가에 더 강한 모델을 쓰거나, 생성 모델과 별도의 모델을 사용해서 자기 평가 편향(self-evaluation bias)을 줄이기도 한다.

## Evaluator를 테스트에 재활용하기

Evaluator-Optimizer의 채점 로직은 품질 테스트에 그대로 재활용할 수 있다. 테스트 케이스(입력-기대 품질 기준 쌍)를 미리 작성해두고, 프롬프트를 변경할 때마다 실행해서 점수가 떨어진 케이스가 있는지 확인한다. 프롬프트를 수정하면 기존에 잘 되던 케이스가 망가질 수 있기 때문에, 이런 회귀 테스트가 중요하다. 테스트 케이스는 점진적으로 추가하면 되고, 실무에서는 CI/CD에 넣어 자동화하기도 한다.

# Parallelization

LangGraph에서 여러 노드를 **동시에** 실행하는 방법을 배운다. Fan-out/Fan-in 패턴, Send API, Rate Limiting, 그리고 병렬 처리를 활용한 Voting 패턴까지 다룬다.

```python
from dotenv import load_dotenv

load_dotenv()
```

## 병렬 처리가 필요한 이유

하나의 문서를 3개 관점(법률, 재무, 기술)으로 분석한다고 하자.

**순차 처리:**

```
법률 분석 (3초) → 재무 분석 (3초) → 기술 분석 (3초) = 총 9초
```

**병렬 처리:**

```
법률 분석 (3초) ─┐
재무 분석 (3초) ─┼→ 종합 = 총 3초 + α
기술 분석 (3초) ─┘
```

분석 관점이 서로 독립적이면 병렬로 실행해도 결과가 동일하다. LangGraph는 이런 병렬 실행을 **그래프 구조**로 자연스럽게 표현한다.

## 기본 병렬 노드 (Fan-out / Fan-in)

하나의 노드 뒤에 여러 노드를 연결하면 LangGraph가 자동으로 **병렬 실행**한다.

```
START → prepare ─→ legal_analysis  ─┐
                 ─→ financial_analysis ─┼→ summarize → END
                 ─→ technical_analysis ─┘
```

핵심: State에 `Annotated[list, operator.add]`를 사용해서 각 노드의 결과를 **하나의 리스트에 누적**한다.

```python
import operator
import time
from typing import Annotated, TypedDict

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

class AnalysisState(TypedDict):
    document: str
    analyses: Annotated[list, operator.add]  # 각 분석 결과가 누적됨
    summary: str

def prepare(state: AnalysisState):
    """문서를 확인하고 분석을 시작한다."""
    print(f"[prepare] 문서 길이: {len(state['document'])}자")
    return {}

def legal_analysis(state: AnalysisState):
    result = llm.invoke(
        f"다음 문서를 법률 관점에서 핵심 리스크 2가지를 분석해줘. 간결하게.\n\n{state['document']}"
    )
    print("[legal_analysis] 완료")
    return {"analyses": [f"[법률] {result.content}"]}

def financial_analysis(state: AnalysisState):
    result = llm.invoke(
        f"다음 문서를 재무 관점에서 핵심 포인트 2가지를 분석해줘. 간결하게.\n\n{state['document']}"
    )
    print("[financial_analysis] 완료")
    return {"analyses": [f"[재무] {result.content}"]}

def technical_analysis(state: AnalysisState):
    result = llm.invoke(
        f"다음 문서를 기술 관점에서 핵심 포인트 2가지를 분석해줘. 간결하게.\n\n{state['document']}"
    )
    print("[technical_analysis] 완료")
    return {"analyses": [f"[기술] {result.content}"]}

def summarize(state: AnalysisState):
    all_analyses = "\n\n".join(state["analyses"])
    result = llm.invoke(
        f"다음 3가지 관점의 분석을 종합해서 3줄로 요약해줘:\n\n{all_analyses}"
    )
    return {"summary": result.content}
```

```python
graph_builder = StateGraph(AnalysisState)

graph_builder.add_node("prepare", prepare)
graph_builder.add_node("legal_analysis", legal_analysis)
graph_builder.add_node("financial_analysis", financial_analysis)
graph_builder.add_node("technical_analysis", technical_analysis)
graph_builder.add_node("summarize", summarize)

# Fan-out: prepare → 3개 분석 노드 (병렬)
graph_builder.add_edge(START, "prepare")
graph_builder.add_edge("prepare", "legal_analysis")
graph_builder.add_edge("prepare", "financial_analysis")
graph_builder.add_edge("prepare", "technical_analysis")

# Fan-in: 3개 분석 노드 → summarize
graph_builder.add_edge("legal_analysis", "summarize")
graph_builder.add_edge("financial_analysis", "summarize")
graph_builder.add_edge("technical_analysis", "summarize")
graph_builder.add_edge("summarize", END)

analysis_graph = graph_builder.compile()
display(Image(analysis_graph.get_graph().draw_mermaid_png()))
```

```python
document = """AI 스타트업 A사가 시리즈B 투자 500억원을 유치했다.
핵심 기술은 자체 개발한 경량 LLM으로, 기존 모델 대비 추론 속도가 3배 빠르다.
다만 학습 데이터의 저작권 문제가 일부 제기되고 있으며,
현재 매출 대비 기업가치가 100배 수준이라는 지적도 있다.
올해 하반기 상용화를 목표로 하고 있다."""

start = time.time()
result = analysis_graph.invoke({"document": document})
elapsed = time.time() - start

print(f"\n소요 시간: {elapsed:.1f}초")
print(f"\n=== 분석 결과 ({len(result['analyses'])}개) ===")
for a in result["analyses"]:
    print(a)
    print()
print(f"=== 종합 ===")
print(result["summary"])
```

- `prepare`에서 3개 노드로 **Fan-out** — 같은 출발 노드에서 여러 엣지를 연결하면 된다
- 3개 노드에서 `summarize`로 **Fan-in** — LangGraph가 **모든 선행 노드가 완료될 때까지 대기**한 후 실행한다
- `Annotated[list, operator.add]` 덕분에 각 노드의 결과가 하나의 리스트에 모인다
- 병렬 노드는 동시에 실행되므로 **결과가 리스트에 들어가는 순서는 보장되지 않는다** — 순서가 중요하면 결과에 식별자를 포함시키거나 후처리에서 정렬해야 한다
- 노드 함수가 일반 `def`이고 `invoke`(동기)로 실행해도 **병렬 처리가 된다**. LangGraph는 내부적으로 비동기 런타임 위에서 동작하기 때문에, 그래프 구조상 동시에 실행 가능한 노드는 자동으로 병렬 실행한다. `async def` + `ainvoke`는 노드 안에서 `await`나 `Semaphore` 같은 비동기 기능을 직접 사용할 때만 필요하다.

### 결과 순서가 필요할 때

병렬 노드의 결과는 어떤 노드가 먼저 끝나느냐에 따라 순서가 달라진다. 순서가 중요하면 결과에 **식별자를 포함**시키고 후처리에서 정렬하면 된다.

위 예제의 분석 노드를 수정해서, 결과를 `(순서, 내용)` 튜플로 반환하고 `summarize`에서 정렬하는 방식이다.

```python
class OrderedAnalysisState(TypedDict):
    document: str
    analyses: Annotated[list, operator.add]  # (순서, 내용) 튜플이 누적됨
    summary: str

def ordered_legal(state: OrderedAnalysisState):
    result = llm.invoke(
        f"다음 문서를 법률 관점에서 핵심 리스크 2가지를 분석해줘. 간결하게.\n\n{state['document']}"
    )
    return {"analyses": [(0, f"[법률] {result.content}")]}

def ordered_financial(state: OrderedAnalysisState):
    result = llm.invoke(
        f"다음 문서를 재무 관점에서 핵심 포인트 2가지를 분석해줘. 간결하게.\n\n{state['document']}"
    )
    return {"analyses": [(1, f"[재무] {result.content}")]}

def ordered_technical(state: OrderedAnalysisState):
    result = llm.invoke(
        f"다음 문서를 기술 관점에서 핵심 포인트 2가지를 분석해줘. 간결하게.\n\n{state['document']}"
    )
    return {"analyses": [(2, f"[기술] {result.content}")]}

def ordered_summarize(state: OrderedAnalysisState):
    # 순서대로 정렬
    sorted_analyses = sorted(state["analyses"], key=lambda x: x[0])
    print("정렬된 순서:")
    for order, content in sorted_analyses:
        print(f"  {order}: {content[:30]}...")

    all_analyses = "\n\n".join(content for _, content in sorted_analyses)
    result = llm.invoke(
        f"다음 3가지 관점의 분석을 종합해서 3줄로 요약해줘:\n\n{all_analyses}"
    )
    return {"summary": result.content}

graph_builder = StateGraph(OrderedAnalysisState)
graph_builder.add_node("legal", ordered_legal)
graph_builder.add_node("financial", ordered_financial)
graph_builder.add_node("technical", ordered_technical)
graph_builder.add_node("summarize", ordered_summarize)

graph_builder.add_edge(START, "legal")
graph_builder.add_edge(START, "financial")
graph_builder.add_edge(START, "technical")
graph_builder.add_edge("legal", "summarize")
graph_builder.add_edge("financial", "summarize")
graph_builder.add_edge("technical", "summarize")
graph_builder.add_edge("summarize", END)

ordered_graph = graph_builder.compile()

result = ordered_graph.invoke({"document": document})
print(f"\n=== 종합 ===")
print(result["summary"])
```

## Send API (동적 병렬)

Fan-out/Fan-in은 **컴파일 시점에** 병렬 노드가 고정된다. 하지만 실행 시점에 병렬 태스크 수가 달라져야 하는 경우가 있다.

예시:

- 사용자가 분석할 주제를 1개 줄 수도, 5개 줄 수도 있다
- 검색 결과 수에 따라 병렬 처리할 문서 수가 달라진다

`Send` API는 **런타임에 동적으로** 병렬 노드를 생성한다. 데이터를 나눠서 병렬 처리하고 결과를 합친다는 흐름은 Fan-out/Fan-in과 같지만, **병렬 수가 실행 시점에 결정**된다는 점이 다르다.

`Send(노드이름, state)`를 호출하면 해당 노드의 새 인스턴스를 만들고, 두 번째 인자를 그 노드의 **독립적인 입력 State**로 전달한다. 그래서 병렬 노드용 State(`AnalyzeTopicState`)를 별도로 정의한다 — 그래프 전체 State(`SendState`)와 구분하기 위해서다.

앞에서 `add_conditional_edges`에 전달하는 라우팅 함수는 문자열(노드 이름)을 반환해서 **라우팅**에 사용했다. 여기서는 라우팅 함수가 `Send` 객체를 반환하는데, 이렇게 하면 **동적 병렬**이 된다.

`add_conditional_edges(시작노드, 라우팅함수, 목적지)` — 세 번째 인자는 **가능한 목적지 노드**를 명시한다. 딕셔너리(`{"반환값": "노드이름"}`)나 리스트(`["노드이름"]`) 모두 가능하다. Send는 런타임에 목적지를 결정하기 때문에, 컴파일 시점에 어떤 노드로 갈 수 있는지 명시해줘야 그래프를 구성할 수 있다.

```python
from langgraph.types import Send

class SendState(TypedDict):
    topics: list[str]  # 분석할 주제 목록
    results: Annotated[list, operator.add]  # 분석 결과 누적
    final_report: str

class AnalyzeTopicState(TypedDict):
    """개별 분석 태스크의 입력 State"""
    topic: str

def generate_tasks(state: SendState):
    """주제 목록을 기반으로 병렬 태스크를 동적 생성한다."""
    return [
        Send("analyze_topic", {"topic": topic})
        for topic in state["topics"]
    ]

def analyze_topic(state: AnalyzeTopicState):
    topic = state["topic"]
    result = llm.invoke(f"'{topic}'에 대해 핵심 트렌드를 2문장으로 분석해줘.")
    print(f"[analyze_topic] '{topic}' 완료")
    # AnalyzeTopicState가 아닌 부모 State(SendState)의 results에 병합된다
    return {"results": [f"[{topic}] {result.content}"]}

def make_report(state: SendState):
    all_results = "\n\n".join(state["results"])
    result = llm.invoke(
        f"다음 분석 결과들을 종합해서 보고서 형태로 요약해줘:\n\n{all_results}"
    )
    return {"final_report": result.content}
```

```python
graph_builder = StateGraph(SendState)

graph_builder.add_node("analyze_topic", analyze_topic)
graph_builder.add_node("make_report", make_report)

# generate_tasks가 Send 객체 리스트를 반환 → 동적 Fan-out
graph_builder.add_conditional_edges(START, generate_tasks, ["analyze_topic"])
graph_builder.add_edge("analyze_topic", "make_report")
graph_builder.add_edge("make_report", END)

send_graph = graph_builder.compile()
display(Image(send_graph.get_graph().draw_mermaid_png()))
```

```python
# 주제 3개
result = send_graph.invoke({"topics": ["생성형 AI", "자율주행", "양자컴퓨팅"]})
print(f"분석 수: {len(result['results'])}개")
print(f"\n=== 보고서 ===")
print(result["final_report"])
```

- `Send(노드이름, state)`로 해당 노드의 **새 인스턴스**를 동적으로 생성한다
- `generate_tasks` 함수가 `Send` 객체의 리스트를 반환하면, 리스트 길이만큼 병렬 실행된다
- `add_conditional_edges`의 세 번째 인자 `["analyze_topic"]`은 **가능한 목적지 노드 목록**이다. Send는 런타임에 목적지를 결정하기 때문에 컴파일 시점에 어떤 노드로 갈 수 있는지 명시해줘야 그래프를 구성할 수 있다
- Fan-out과 달리 **런타임에 병렬 수가 결정**된다
- 결과 리스트의 순서는 보장되지 않는다 — 순서가 중요하면 결과에 식별자를 포함시키거나 후처리에서 정렬해야 한다
- `AnalyzeTopicState`는 Send가 전달하는 **입력 스펙**이다. `analyze_topic` 노드가 반환한 `{"results": [...]}`는 `AnalyzeTopicState`에 저장되는 게 아니라, 키 이름이 같은 **부모 State(`SendState`)의 `results`에 자동으로 병합**된다
- 병렬 노드 중 하나가 예외를 발생시키면 **그래프 전체가 실패**한다 — 안정성이 중요하면 노드 내부에서 try/except로 에러를 처리해야 한다

## Rate Limiting

**Rate Limit**은 API 제공자가 일정 시간 내 요청 수를 제한하는 정책이다. 예를 들어 OpenAI API는 분당 요청 수(RPM)와 분당 토큰 수(TPM)에 상한을 두고, 이를 초과하면 `429 Too Many Requests` 에러를 반환한다. 병렬 처리로 동시에 많은 요청을 보내면 이 제한에 걸리기 쉽다.

`asyncio.Semaphore`로 **동시 실행 수를 제한**해서 Rate Limit을 회피할 수 있다.

`Semaphore`는 동시에 접근할 수 있는 수를 제한하는 동기화 도구다. `Semaphore(3)`이면 동시에 3개까지만 실행을 허용하고, 나머지는 자리가 날 때까지 대기한다. `async with semaphore:` 블록에 들어갈 때 자리를 하나 차지하고, 블록을 나올 때 자리를 반환한다.

시나리오: 8개 주제를 분석해야 하지만, LLM API가 동시에 3개까지만 허용하는 상황.

비동기 노드를 사용하므로 `async def`로 노드를 정의하고, 그래프 실행 시 `ainvoke`를 사용한다. `ainvoke`는 `invoke`의 비동기 버전으로, `await`와 함께 사용한다. Jupyter 노트북은 이미 이벤트 루프가 실행 중이라 셀에서 `await`를 바로 쓸 수 있다.

아래 코드에서 `semaphore`를 모듈 레벨에 선언하고, 노드 함수 안에서 클로저로 참조한다. 노드 함수가 호출될 때마다 같은 세마포어를 공유하기 때문에 동시 실행 수 제한이 작동한다.

```python
import asyncio

# asyncio.Semaphore로 동시 호출 수 제한
semaphore = asyncio.Semaphore(3)  # 동시 최대 3개

class RateLimitState(TypedDict):
    topics: list[str]
    results: Annotated[list, operator.add]

class RateLimitItemState(TypedDict):
    topic: str

def dispatch_topics(state: RateLimitState):
    return [
        Send("analyze_with_limit", {"topic": topic})
        for topic in state["topics"]
    ]

async def analyze_with_limit(state: RateLimitItemState):
    topic = state["topic"]
    async with semaphore:
        print(f"[시작] {topic} (현재 동시 실행 중)")
        result = await llm.ainvoke(f"'{topic}'에 대해 한 문장으로 설명해줘.")
        print(f"[완료] {topic}")
        return {"results": [f"[{topic}] {result.content}"]}

graph_builder = StateGraph(RateLimitState)
graph_builder.add_node("analyze_with_limit", analyze_with_limit)

graph_builder.add_conditional_edges(START, dispatch_topics, ["analyze_with_limit"])
graph_builder.add_edge("analyze_with_limit", END)

rate_limit_graph = graph_builder.compile()
display(Image(rate_limit_graph.get_graph().draw_mermaid_png()))
```

```python
topics = ["AI", "블록체인", "IoT", "클라우드", "5G", "메타버스", "드론", "AR/VR"]

result = await rate_limit_graph.ainvoke({"topics": topics})

print(f"총 {len(topics)}개 주제, 동시 최대 3개 제한")
print(f"\n=== 결과 ===")
for r in result["results"]:
    print(r)
```

핵심 포인트:

- `asyncio.Semaphore(N)`으로 동시 실행 수를 N개로 제한한다
- 노드 함수를 `async def`로 정의하고, `async with semaphore:` 블록 안에서 LLM 호출한다
- 그래프 실행 시 `ainvoke`(비동기)를 사용한다
- API Rate Limit 대응뿐 아니라, 메모리/CPU 사용량 제어에도 활용 가능하다

## Voting 패턴

하나의 질문에 대해 **여러 LLM 응답을 동시에 생성**하고, 그 중 최선의 답변을 선택하는 패턴이다.

```
             ┌→ generate_1 ─┐
START → fan_out → generate_2 ─┼→ vote → END
             └→ generate_3 ─┘
```

같은 모델이라도 Temperature를 높이면 다른 답변이 나온다. 이 다양성을 활용해서 품질을 높이는 전략이다. 같은 모델 대신 서로 다른 모델(GPT-4o, Claude, Gemini 등)을 동시에 호출하는 방식도 가능하다. 평가(judge)용 LLM은 정확한 판단이 중요하므로, 생성용보다 고급 모델을 쓰면 효과적이다.

```python
from pydantic import BaseModel, Field

# 다양한 답변을 생성하기 위해 Temperature를 높인 LLM
creative_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.9)
# 평가용 LLM은 일관성을 위해 Temperature=0
judge_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

class VotingState(TypedDict):
    question: str
    candidates: Annotated[list, operator.add]  # 후보 답변 누적
    best_answer: str

class VoteItemState(TypedDict):
    question: str
    candidate_id: int

def generate_candidate(state: VoteItemState):
    """후보 답변을 하나 생성한다."""
    result = creative_llm.invoke(
        f"다음 질문에 창의적이고 유용하게 답변해줘:\n\n{state['question']}"
    )
    candidate_id = state["candidate_id"]
    print(f"[후보 {candidate_id}] 생성 완료")
    return {"candidates": [{"id": candidate_id, "answer": result.content}]}

class VoteResult(BaseModel):
    """투표 결과"""
    best_id: int = Field(description="가장 좋은 답변의 ID (0부터 시작)")
    reason: str = Field(description="선택 이유")

def vote(state: VotingState):
    """후보 답변들 중 최선을 선택한다."""
    candidates = state["candidates"]

    candidates_text = ""
    for c in candidates:
        candidates_text += f"\n--- 후보 {c['id']} ---\n{c['answer']}\n"

    judge = judge_llm.with_structured_output(VoteResult)
    result = judge.invoke(
        f"다음 질문에 대한 여러 답변 후보가 있다. 가장 정확하고 유용한 답변을 골라줘.\n\n"
        f"질문: {state['question']}\n\n"
        f"후보 답변들:{candidates_text}\n\n"
        f"가장 좋은 답변의 ID와 이유를 알려줘."
    )

    best = next(c for c in candidates if c["id"] == result.best_id)
    print(f"\n[투표 결과] 후보 {result.best_id} 선택 — {result.reason}")
    return {"best_answer": best["answer"]}

def fan_out_candidates(state: VotingState):
    """N개의 후보 답변을 병렬 생성한다."""
    n_candidates = 3
    return [
        Send("generate_candidate", {
            "question": state["question"],
            "candidate_id": i,
        })
        for i in range(n_candidates)
    ]

# 그래프 구성
voting_builder = StateGraph(VotingState)
voting_builder.add_node("generate_candidate", generate_candidate)
voting_builder.add_node("vote", vote)

voting_builder.add_conditional_edges(START, fan_out_candidates, ["generate_candidate"])
voting_builder.add_edge("generate_candidate", "vote")
voting_builder.add_edge("vote", END)

voting_graph = voting_builder.compile()
display(Image(voting_graph.get_graph().draw_mermaid_png()))
```

```python
result = voting_graph.invoke({
    "question": "프로그래밍을 처음 배우는 사람에게 파이썬을 추천하는 이유를 설명해줘"
})

print("=== 후보 답변들 ===")
for c in result["candidates"]:
    print(f"\n[후보 {c['id']}] {c['answer'][:150]}...")

print(f"\n=== 최종 선택 ===")
print(result["best_answer"])
```

- **Temperature를 높여서** 다양한 후보를 생성한다 (다양성이 핵심)
- **Judge LLM**은 Temperature=0으로 일관된 평가를 한다
- `with_structured_output`으로 투표 결과를 구조화한다
- Send API로 후보 수를 동적으로 조절할 수 있다 (3개 → 5개 등)
- **활용 예시**: 마케팅 카피 생성, 코드 생성, 번역 등 품질 변동이 큰 작업에서 최선의 결과를 뽑아낸다

## 병렬 처리는 언제 쓰는가

병렬 처리가 **적합한 경우**:

- 독립적인 작업 여러 개를 동시에 처리하여 속도를 높이고 싶을 때
- 동일 문서를 여러 관점으로 동시 분석 후 종합
- 여러 URL을 병렬 크롤링 후 결과 합치기
- 하나의 질문에 대해 여러 LLM 응답을 생성하고 최선을 선택 (Voting)

**주의가 필요한 경우**:

- 작업 간에 의존성이 있을 때 (B가 A의 결과를 필요로 함) → 병렬 처리 불가, 순차 실행해야 한다
- 병렬 작업 수가 많아 Rate Limit에 걸릴 수 있을 때 → Semaphore로 동시 실행 수를 제어
- 결과의 순서가 중요할 때 → 결과에 식별자를 포함시키고 후처리에서 정렬

**판단 기준**: "이 작업들이 서로의 결과를 몰라도 되는가?" → Yes면 병렬화 후보