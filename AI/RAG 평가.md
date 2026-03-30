## RAG 평가가 필요한 이유

RAG 파이프라인을 만들면 자연스럽게 이런 질문이 생긴다.

- chunk_size를 500으로 했는데, 300이 더 나을까?
- 검색 결과를 3개 가져오는 게 나을까, 5개가 나을까?
- 프롬프트를 바꿨더니 답변이 좋아진 건가, 나빠진 건가?

사람이 하나하나 읽어보며 판단할 수 있지만, 느리고 주관적이다. **RAGAS**는 LLM을 활용하여 RAG 파이프라인의 품질을 **자동으로 정량 평가**하는 프레임워크이다.

### 반드시 RAGAS를 써야 하나?

아니다. RAG 평가 방법은 여러 가지가 있다.

| 방법 | 특징 | 적합한 상황 |
| --- | --- | --- |
| **수동 스팟체크** | 대표 질문 10~20개를 눈으로 확인 | 초기 개발, 빠른 검증 |
| **RAGAS** | LLM 기반 자동 정량 평가 (Python) | 설정 비교, 파이프라인 튜닝 |
| **직접 LLM-as-Judge** | 도메인 특화 기준으로 직접 평가 구현 | RAGAS 메트릭으로 부족할 때 |
| **사용자 피드백** | 👍👎 버튼으로 실사용 데이터 수집 | 서비스 운영 중 |

실무에서는 이 방법들을 **섞어서** 사용한다. 개발 초기에는 수동 스팟체크로 빠르게 확인하고, 설정을 튜닝할 때 RAGAS로 비교하고, 서비스 운영 중에는 사용자 피드백을 수집한다.

이 노트북에서는 RAGAS를 중심으로 평가하는 방법을 다룬다.

### 평가 진행 순서

RAGAS는 **RAG의 결과물을 받아서 채점하는 도구**이다. RAG 파이프라인 자체를 실행하는 것이 아니라, 이미 실행된 결과를 평가한다.

```
1. 평가 데이터 준비(개발자가 준비)
   - 사람이 질문(user_input)과 정답(reference)을 작성한다

2. RAG 파이프라인 실행
   - 각 질문을 RAG에 넣어서 검색된 문서(retrieved_contexts)와 답변(response)을 수집한다

3. RAGAS에 전달
   - 수집한 4가지(질문, 정답, 검색 문서, 답변)를 RAGAS 형식으로 변환한다

4. 평가 실행
   - RAGAS가 각 메트릭별로 LLM을 호출하여 0~1 점수를 매긴다
   - 예: Faithfulness 평가 시, LLM에게 "이 답변이 검색된 문서에 근거하는가?" 를 판단하게 한다
```

### 평가 메트릭

RAGAS는 다양한 메트릭을 제공한다. 뭘 개선하고 싶은지에 따라 골라 쓴다. 평가 기준이라고 보면 됨.

| 목적 | 메트릭 | 평가 내용 |
| --- | --- | --- |
| 검색이 잘 되나? | **Context Precision** | 검색된 문서 중 관련 있는 문서가 상위에 있는가? |
| 검색이 잘 되나? | **Context Recall** | 정답에 필요한 정보가 검색 결과에 포함되어 있는가? |
| 답변이 정확한가? | **Faithfulness** | 답변이 검색된 문서에 근거하는가? (할루시네이션 없는가?) |
| 답변이 정확한가? | **Response Relevancy** | 답변이 질문에 적절하게 대답하는가? |
| 정답과 일치하나? | AnswerCorrectness | 답변이 정답과 얼마나 일치하는가? |
| 노이즈에 강한가? | NoiseSensitivity | 관련 없는 문서가 섞였을 때 답변이 흔들리는가? |

> 이 외에도 AnswerSimilarity, ContextEntityRecall, AspectCritic 등 다양한 메트릭이 있다
> 

각 메트릭은 0~1 사이의 값을 가지며, 1에 가까울수록 좋다. 처음 평가할 때는 **검색 + 생성을 모두 커버하는 상위 4개**로 시작하고, 필요에 따라 추가하는 것이 일반적이다.

```
질문: "연차 신청 방법은?"

검색 평가:
  Context Precision → 검색된 3개 문서 중 관련 문서가 1위인가?
  Context Recall    → 정답에 필요한 내용이 검색 결과에 다 있는가?

생성 평가:
  Faithfulness       → 답변이 검색된 문서 내용만 사용했는가?
  Response Relevancy → 답변이 질문에 맞게 대답했는가?
```

## 평가 데이터셋 준비

RAG 시스템을 평가하려면 **Golden Dataset**(골든 데이터셋)이 필요하다. 사람이 직접 질문과 기대 정답을 작성해 놓은 기준 데이터로, 자동 평가의 ground truth 역할을 한다.

RAGAS 평가를 위해서는 다음 4가지가 필요하다.

| 필드 | 설명 | 출처 |
| --- | --- | --- |
| `user_input` | 사용자 질문 | 직접 작성 |
| `reference` | 정답 (사람이 작성) | 직접 작성 |
| `retrieved_contexts` | 검색된 문서 리스트 | RAG 파이프라인 실행 |
| `response` | LLM이 생성한 답변 | RAG 파이프라인 실행 |

`user_input`과 `reference`는 사람이 미리 만들어두고(= Golden Dataset), `retrieved_contexts`와 `response`는 RAG 파이프라인을 실행하여 수집한다.

### 문서 로드 및 벡터 스토어 구성

`data/company_rules/` 폴더에 있는 사내 규정 문서(마크다운)를 로드한다. 인사, 보안, 경비처리, IT지원 등 다양한 규정이 포함되어 있으며, 문서 간에 동일한 주제가 여러 규정에 걸쳐 있는 경우도 있다 (예: 재택근무 관련 내용이 인사규정, 재택근무규정, IT지원규정, 보안규정에 분산).

`DirectoryLoader`는 폴더 내 여러 파일을 한 번에 로드하는 LangChain 유틸리티이다. `glob` 파라미터로 로드할 파일 패턴을 지정한다 (예: `*.md`는 마크다운 파일만, `*.txt`는 텍스트 파일만). `loader_cls`로 개별 파일을 읽을 로더 클래스를 지정한다.

```python
import chromadb
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 마크다운 문서 로드
loader = DirectoryLoader("data/company_rules/", glob="*.md", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"})
all_docs = loader.load()
print(f"로드된 문서: {len(all_docs)}개")

# 텍스트 분할
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
splits = splitter.split_documents(all_docs)
print(f"총 {len(splits)}개 청크 생성")

# 벡터 스토어 생성
COLLECTION_NAME = "company_rules"
PERSIST_DIR = "./chroma_db"

client = chromadb.PersistentClient(path=PERSIST_DIR)
existing_names = [c.name for c in client.list_collections()]
if COLLECTION_NAME in existing_names:
    client.delete_collection(COLLECTION_NAME)

vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=embeddings,
    collection_name=COLLECTION_NAME,
    client=client,
)
print(f"벡터 스토어 저장 완료! (컬렉션: {COLLECTION_NAME})")

# Retriever 구성
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
```

### RAG Chain 구성

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

prompt = ChatPromptTemplate.from_messages([
    ("system", """너는 사내 규정 안내 챗봇이야. 아래 검색된 문서를 참고하여 질문에 답변해줘.
검색 결과에 없는 내용은 "해당 정보를 찾을 수 없습니다"라고 답변해.

[검색된 문서]
{context}"""),
    ("human", "{question}"),
])

answer_chain = prompt | llm | StrOutputParser()

def run_rag(question: str) -> dict:
    """검색 → 답변 생성을 순서대로 실행한다."""
    docs = retriever.invoke(question)
    context = format_docs(docs)
    answer = answer_chain.invoke({"context": context, "question": question})
    return {"question": question, "docs": docs, "answer": answer}

# 테스트
result = run_rag("연차는 며칠이야?")
print(f"Q: {result['question']}")
print(f"A: {result['answer']}")
print(f"검색 문서 수: {len(result['docs'])}개")
```

### 평가 데이터셋 생성

`data/company_rules/eval_qa.json`에 미리 작성된 질문-정답 쌍을 로드한다. 난이도별로 easy, medium, hard로 구성되어 있다.

- **easy**: 단일 문서에서 바로 찾을 수 있는 질문 (예: "연차 며칠?")
- **medium**: 같은 문서 내 여러 조항 결합, 패러프레이즈 필요, 또는 동일 내용이 여러 규정에 존재하여 혼동 가능 (예: "자기개발비로 뭘 할 수 있어?")
- **hard**: 3~4개 문서를 동시에 참조해야 완전한 답변 가능 (예: "퇴직할 때 해야 할 일이 뭐야?")

### 평가 질문 작성 가이드

평가 데이터의 품질이 평가 결과의 신뢰도를 결정한다. 질문을 만들 때는 다음 원칙을 따른다.

**난이도를 섞어라**

| 난이도 | 기준 | 예시 |
| --- | --- | --- |
| **easy** | 단일 문서에서 바로 찾을 수 있는 질문 | "연차는 며칠이야?" |
| **medium** | 같은 문서 내 여러 조항 결합, 또는 2개 문서 참조 필요 | "자기개발비로 뭘 할 수 있어?" |
| **hard** | 3개 이상 문서를 종합해야 완전한 답변 가능 | "퇴직할 때 해야 할 일이 뭐야?" |

easy만 있으면 점수가 높게 나와서 문제를 발견할 수 없고, hard만 있으면 점수가 낮아서 기본적인 문제와 구조적인 문제를 구분할 수 없다.

**실제 사용자처럼 질문하라**

사용자는 규정 용어를 모른다. 규정에는 "외부 저장 매체 연결 금지"라고 되어 있지만, 사용자는 "USB 꽂아도 돼?"라고 물어본다. 이렇게 같은 의미를 다른 말로 바꿔 표현하는 것을 패러프레이즈(paraphrase)라고 한다. 패러프레이즈된 질문이 있어야 retriever가 실제 사용 환경에서 잘 작동하는지 테스트할 수 있다.

```
# 좋은 질문 — 사용자가 실제로 물어볼 법한 표현 (패러프레이즈)
"USB 꽂아서 파일 옮겨도 돼?"        ← 원문: "외부 저장 매체 연결 금지"
"결혼하면 회사에서 뭘 해줘?"         ← 원문: "경조사 지원 규정"

# 나쁜 질문 — 문서를 보고 그대로 옮긴 표현
"외부 저장 매체 사용 정책은?"
"경조사 지원 규정의 내용은?"
```

**정답은 구체적으로 작성하라**

```
# 좋은 정답 — 구체적 수치와 조건 포함
"15일"
"주 2회까지 가능. 육아기 직원은 주 3회까지 가능"

# 나쁜 정답 — 모호하거나 너무 김
"인사규정에 따라 부여됨"
"재택근무규정 제3조에 의거하여..."
```

정답이 모호하면 Context Recall 점수가 부정확해진다. RAGAS는 정답과 검색 문서를 비교하여 "필요한 정보가 검색되었는가"를 판단하기 때문이다.

```python
import json

# 평가용 질문 + 정답 로드
with open("data/company_rules/eval_qa.json", encoding="utf-8") as f:
    eval_questions = json.load(f)

print(f"평가 질문 수: {len(eval_questions)}개")
print(f"  easy: {sum(1 for q in eval_questions if q['difficulty'] == 'easy')}개")
print(f"  medium: {sum(1 for q in eval_questions if q['difficulty'] == 'medium')}개")
print(f"  hard: {sum(1 for q in eval_questions if q['difficulty'] == 'hard')}개")

# RAG 파이프라인 실행하여 retrieved_contexts, response 수집
eval_results = []

for item in eval_questions:
    result = run_rag(item["question"])
    eval_results.append({
        "user_input": item["question"],
        "reference": item["expected_answer"],
        "retrieved_contexts": [doc.page_content for doc in result["docs"]],
        "response": result["answer"],
    })

# 결과 확인 (처음 5개만)
for r in eval_results[:5]:
    print(f"\nQ: {r['user_input']}")
    print(f"정답: {r['reference']}")
    print(f"응답: {r['response'][:120]}...")
    print(f"검색 문서 수: {len(r['retrieved_contexts'])}")
```

## RAGAS 평가 실행

위에서 수집한 `eval_results`(질문, 정답, 검색 문서, 답변)를 RAGAS에 전달하여 평가한다.

```python
# evaluate: 평가 실행 함수
# EvaluationDataset / SingleTurnSample: RAGAS가 요구하는 데이터 형식
from ragas import evaluate, EvaluationDataset, SingleTurnSample

# RAGAS 메트릭 (각각 LLM을 호출하여 점수를 매김)
from ragas.metrics import Faithfulness, ResponseRelevancy, LLMContextPrecisionWithReference, LLMContextRecall

# RAGAS는 자체 LLM/Embedding 인터페이스를 사용하므로,
# LangChain 객체를 RAGAS가 이해할 수 있도록 래퍼로 감싸야 한다
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

evaluator_llm = LangchainLLMWrapper(llm)
evaluator_embeddings = LangchainEmbeddingsWrapper(embeddings)

# 메트릭 인스턴스 생성 (각 메트릭에 평가용 LLM을 전달)
metrics = [
    Faithfulness(llm=evaluator_llm),                                          # 답변이 검색 문서에 근거하는가?
    ResponseRelevancy(llm=evaluator_llm, embeddings=evaluator_embeddings),     # 답변이 질문에 적절한가?
    LLMContextPrecisionWithReference(llm=evaluator_llm),                       # 관련 문서가 상위에 검색되었는가?
    LLMContextRecall(llm=evaluator_llm),                                       # 정답에 필요한 정보가 검색되었는가?
]

# eval_results를 RAGAS가 요구하는 형식으로 변환
# SingleTurnSample: 질문 1개에 대한 평가 데이터 (질문, 답변, 검색 문서, 정답)
samples = [SingleTurnSample(**r) for r in eval_results]
eval_dataset = EvaluationDataset(samples=samples)

# 평가 실행
result = evaluate(dataset=eval_dataset, metrics=metrics)

# 전체 평균 점수
# NOTE: answer_relevancy는 답변에서 질문을 역생성한 뒤 원래 질문과 임베딩 유사도를 비교하는 방식이다.
#       한국어는 같은 의미라도 어미/조사 변화가 다양해서 역생성된 질문과 원래 질문의
#       임베딩 유사도가 낮게 나올 수 있다. 절대 점수보다는 상대 비교 용도로 참고할 것.
df = result.to_pandas()
exclude_cols = {"user_input", "retrieved_contexts", "response", "reference"}
metric_cols = [col for col in df.columns if col not in exclude_cols]

print("=== 전체 평균 점수 ===")
for col in metric_cols:
    print(f"  {col}: {df[col].mean():.4f}")
```

```python
# 질문별 상세 결과
df = result.to_pandas()

# 난이도 정보 추가
df["difficulty"] = [q["difficulty"] for q in eval_questions]
df["expected_source"] = [
    q["source"] if isinstance(q["source"], str) else ", ".join(q["source"])
    for q in eval_questions
]

display(df[["user_input", "difficulty"] + metric_cols])

# 난이도별 평균
print("\n=== 난이도별 평균 점수 ===")
for diff in ["easy", "medium", "hard"]:
    sub = df[df["difficulty"] == diff]
    print(f"\n[{diff}] ({len(sub)}개)")
    for col in metric_cols:
        print(f"  {col}: {sub[col].mean():.4f}")
```

### 결과 해석

RAGAS 점수는 **절대적인 품질 기준이 아니다**. Faithfulness 0.75가 좋은 건지 나쁜 건지에 대한 정답은 없다. RAGAS의 진짜 가치는 **설정 A vs 설정 B를 수치로 비교**할 수 있다는 점이다.

```
chunk_size=300 → Faithfulness 0.72, Context Recall 0.65
chunk_size=500 → Faithfulness 0.78, Context Recall 0.81  ← 이쪽이 낫다
```

즉, RAGAS는 "이 RAG가 좋은가?"보다 **"어떤 설정이 더 나은가?"**를 판단하는 A/B 테스트 도구에 가깝다.

| 메트릭 | 낮은 점수일 때 | 개선 방법 |
| --- | --- | --- |
| **Faithfulness** | LLM이 검색 문서에 없는 내용을 지어냄 | 프롬프트에 "검색 결과만 사용해" 강조. 온도(temperature) 낮추기 |
| **Response Relevancy** | 답변이 질문과 동떨어짐 | 프롬프트 개선. 검색 결과의 품질 확인 |
| **Context Precision** | 관련 없는 문서가 상위에 검색됨 | 청크 크기 조정. Re-ranking 적용. MMR 검색으로 중복 제거 |
| **Context Recall** | 정답에 필요한 정보가 검색되지 않음 | 청크 크기 늘리기. 멀티쿼리 Retriever 사용. k값 늘리기 |

난이도별 결과에서 주목할 점:

- **easy** 점수가 낮다면 → 기본적인 chunking이나 embedding에 문제가 있다
- **medium** 점수가 낮다면 → 동일 내용이 여러 문서에 분산되어 있어 retriever 전략 개선이 필요하다
- **hard** 점수가 낮다면 → 여러 문서를 참조하는 검색이 필요하다 (k값 증가, 멀티쿼리 등)

개선 방법이 실제로 효과가 있는지, 아래에서 **수치로 확인**해보자.

## 파이프라인 비교 실험

RAGAS의 진가는 **설정을 바꿔가며 비교**할 때 나온다. 아래에서 k값, chunk_size, retriever 전략을 바꿔가며 점수가 어떻게 달라지는지 실험해보자.

먼저 반복되는 평가 로직을 함수로 만들어둔다.

```python
def evaluate_retriever(retriever, questions, label=""):
    """retriever를 받아서 RAG 실행 → RAGAS 평가 → 결과 DataFrame 반환"""
    answer_chain = prompt | llm | StrOutputParser()

    samples = []
    for item in questions:
        docs = retriever.invoke(item["question"])
        context = format_docs(docs)
        answer = answer_chain.invoke({"context": context, "question": item["question"]})
        samples.append(
            SingleTurnSample(
                user_input=item["question"],
                response=answer,
                retrieved_contexts=[doc.page_content for doc in docs],
                reference=item["expected_answer"],
            )
        )

    evaluator_llm = LangchainLLMWrapper(llm)
    evaluator_embeddings = LangchainEmbeddingsWrapper(embeddings)

    result = evaluate(
        dataset=EvaluationDataset(samples=samples),
        metrics=[
            Faithfulness(llm=evaluator_llm),
            ResponseRelevancy(llm=evaluator_llm, embeddings=evaluator_embeddings),
            LLMContextPrecisionWithReference(llm=evaluator_llm),
            LLMContextRecall(llm=evaluator_llm),
        ],
    )
    scores_df = result.to_pandas()

    if label:
        print(f"\n--- {label} ---")
        exclude = {"user_input", "retrieved_contexts", "response", "reference"}
        for col in [c for c in scores_df.columns if c not in exclude]:
            print(f"  {col}: {scores_df[col].mean():.4f}")

    return scores_df

def print_comparison(results: dict):
    """{"라벨": DataFrame} 딕셔너리를 받아서 비교 표 출력"""
    sample_df = next(iter(results.values()))
    exclude = {"user_input", "retrieved_contexts", "response", "reference"}
    metric_cols = [c for c in sample_df.columns if c not in exclude]

    header = f"{'설정':>20}" + "".join(f" | {col:>10}" for col in metric_cols)
    print(header)
    print("-" * len(header))
    for label, scores_df in results.items():
        row = f"{label:>20}"
        for col in metric_cols:
            row += f" | {scores_df[col].mean():>10.4f}"
        print(row)
```

### 검색 개수(k) 비교

retriever의 `k`(검색 문서 수)를 바꾸면 점수가 어떻게 달라지는지 확인해보자. k가 크면 더 많은 문서를 가져오지만, 관련 없는 문서(노이즈)도 함께 들어올 수 있다.

```python
k_results = {}
for k in [3, 5]:
    ret = vectorstore.as_retriever(search_kwargs={"k": k})
    k_results[f"k={k}"] = evaluate_retriever(ret, eval_questions, label=f"k={k}")

print_comparison(k_results)
```

> k를 늘리면 정답이 포함된 문서를 가져올 확률이 높아지지만, 관련 없는 문서(노이즈)도 함께 들어온다.
> 
> - **k가 작을 때**: Context Precision이 높지만 Recall이 낮을 수 있음 (적게 가져오니 정확하지만 놓치는 문서 발생)
> - **k가 클 때**: Context Recall이 높지만 Precision이 낮을 수 있음 (많이 가져오니 놓치진 않지만 노이즈 증가)
> - 또한 k가 클수록 LLM에 전달되는 컨텍스트가 길어져 **비용 증가**와 **Faithfulness 하락** 가능성이 있다.

### chunk_size 비교

이번에는 chunk_size를 바꿔가며 비교해보자. 같은 문서를 200 / 500 / 1000 크기로 분할하면 검색 품질이 어떻게 달라지는지 확인한다.

```python
chunk_results = {}
for chunk_size in [200, 500, 1000]:
    # persist 없이 메모리에서만 사용 (실험용 임시 데이터)
    test_chunks = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_size // 10
    ).split_documents(all_docs)

    # collection_name을 다르게 지정하여 기존 벡터 스토어와 분리
    test_store = Chroma.from_documents(
        documents=test_chunks,
        embedding=embeddings,
        collection_name=f"eval_chunk_{chunk_size}",
    )
    test_retriever = test_store.as_retriever(search_kwargs={"k": 3})
    chunk_results[f"{chunk_size}"] = evaluate_retriever(test_retriever, eval_questions, label=f"chunk_size={chunk_size}")

print_comparison(chunk_results)
```

> 실험 결과를 보고 어떤 chunk_size가 적합한지 판단할 수 있다. 일반적으로:
> 
> - **작은 청크**: Context Precision이 높지만 Recall이 낮을 수 있음
> - **큰 청크**: Context Recall이 높지만 Precision이 낮을 수 있음
> 
> 이처럼 RAGAS를 활용하면 감이 아닌 **수치 기반**으로 파이프라인을 최적화할 수 있다.
> 

## Retriever 전략별 비교 실험

chunk_size는 "데이터를 어떻게 자를까"에 대한 실험이었다. 이번에는 이전 시간에 배운 **검색 전략** 자체를 바꿔가며 비교한다.

| 전략 | 핵심 아이디어 |
| --- | --- |
| **기본 (similarity)** | 질문과 가장 유사한 청크를 코사인 유사도로 검색 |
| **MMR** | 유사도 + 다양성 균형 — 비슷한 청크끼리 중복을 줄임 |
| **멀티쿼리** | LLM이 질문을 여러 버전으로 바꿔 검색 범위를 넓힘 |

사내 규정 데이터에는 동일한 내용이 여러 문서에 걸쳐 있다 (예: 재택근무 → 인사규정 + 재택근무규정 + IT지원규정 + 보안규정). 이런 환경에서 각 전략이 어떤 차이를 보이는지 확인해보자.

```python
from langchain_classic.retrievers import MultiQueryRetriever

retriever_configs = {
    "similarity (기본)": vectorstore.as_retriever(
        search_type="similarity", search_kwargs={"k": 3}
    ),
    "MMR": vectorstore.as_retriever(
        search_type="mmr", search_kwargs={"k": 3, "fetch_k": 10}
    ),
    "MultiQuery": MultiQueryRetriever.from_llm(
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        llm=llm,
    ),
}

retriever_results = {}
for name, ret in retriever_configs.items():
    retriever_results[name] = evaluate_retriever(ret, eval_questions, label=name)

print_comparison(retriever_results)
```

### 전략별 결과 해석

| 전략 | 기대 효과 | 주의할 점 |
| --- | --- | --- |
| **기본 (similarity)** | 가장 빠르고 단순 | 비슷한 청크가 중복 검색되어 다양성 부족 |
| **MMR** | Context Precision 개선 — 중복 문서를 줄이고 다양한 관점 확보 | lambda 값 튜닝 필요 |
| **멀티쿼리** | Context Recall 개선 — 질문을 다양하게 변형하여 검색 범위 확대 | LLM 호출 1회 추가, 비결정적 |

> 이처럼 RAGAS로 **감이 아닌 수치 기반**으로 전략을 비교할 수 있다. 실무에서는 이 비교 결과를 바탕으로 자신의 데이터에 맞는 최적의 전략을 선택한다.
> 

## 평가 비용 모니터링

RAGAS 평가는 메트릭마다 LLM을 호출하므로, 질문 수와 메트릭 수에 비례하여 API 비용이 발생한다. 평가를 반복할수록 비용이 누적되므로, 실험 전후의 비용을 확인하는 습관이 중요하다.

LangSmith를 사용하면 트레이싱을 통해 비용을 확인할 수 있다. 여기서는 `langchain`의 콜백을 활용하여 간단히 토큰 사용량을 측정하는 방법을 살펴보자.

```python
from langchain_community.callbacks.manager import get_openai_callback

# 콜백으로 토큰 사용량 및 비용 측정
with get_openai_callback() as cb:
    sample_questions = [q for q in eval_questions if q["difficulty"] == "easy"][:5]
    evaluate_retriever(retriever, sample_questions)

print(f"=== 평가 비용 (질문 {len(sample_questions)}개, 메트릭 4개) ===")
print(f"  총 토큰: {cb.total_tokens:,}")
print(f"  프롬프트 토큰: {cb.prompt_tokens:,}")
print(f"  완성 토큰: {cb.completion_tokens:,}")
print(f"  비용: ${cb.total_cost:.4f}")
print(f"\n질문 1개당 평균 비용: ${cb.total_cost / len(sample_questions):.4f}")
print(f"전체 {len(eval_questions)}개 질문 평가 시 예상 비용: ${cb.total_cost / len(sample_questions) * len(eval_questions):.4f}")
```

> RAGAS 평가 비용은 대부분 Faithfulness와 Context Recall 메트릭에서 발생한다 (LLM이 문서를 읽고 판단하는 과정). 비용이 부담되면:
> 
> - 평가 질문 수를 줄이거나 (전체 대신 난이도별 샘플링)
> - 메트릭을 선택적으로 사용하거나 (예: Context Recall만 측정)
> - 평가용 LLM을 저렴한 모델로 교체할 수 있다 (예: gpt-4o-mini)

## 합성 테스트 데이터셋 (TestsetGenerator)

앞에서는 평가용 질문과 정답을 사람이 직접 작성했다. 하지만 문서가 많아지면 일일이 만드는 것은 비현실적이다.

RAGAS의 `TestsetGenerator`는 문서를 읽고 **질문-정답 쌍을 자동으로 생성**해준다. 다양한 난이도의 질문을 만들어주므로 더 폭넓은 평가가 가능하다.

```
문서 → TestsetGenerator → [
    {"user_input": "...", "reference": "...", "retrieved_contexts": [...]},
    {"user_input": "...", "reference": "...", "retrieved_contexts": [...]},
    ...
]
```

```python
from ragas.testset import TestsetGenerator

# 합성 테스트 데이터셋 생성 (내부적으로 LLM을 많이 호출하므로 시간이 오래 걸린다)
generator = TestsetGenerator(
    llm=evaluator_llm,
    embedding_model=evaluator_embeddings,
)

testset = generator.generate_with_langchain_docs(
    documents=all_docs,
    testset_size=1,
)

# 결과 확인
test_df = testset.to_pandas()
for _, row in test_df.iterrows():
    print(f"Q: {row['user_input']}")
    print(f"A: {row['reference'][:100]}...")
    print()
```

```python
# 합성 질문에 대해 RAG 파이프라인 실행
synth_samples = []

for _, row in test_df.iterrows():
    result = run_rag(row["user_input"])
    synth_samples.append(
        SingleTurnSample(
            user_input=row["user_input"],
            response=result["answer"],
            retrieved_contexts=[doc.page_content for doc in result["docs"]],
            reference=row["reference"],
        )
    )

# RAGAS 평가
synth_result = evaluate(
    dataset=EvaluationDataset(samples=synth_samples),
    metrics=metrics,
)

synth_df = synth_result.to_pandas()
exclude_cols = {"user_input", "retrieved_contexts", "response", "reference"}
metric_cols = [col for col in synth_df.columns if col not in exclude_cols]

print("=== 합성 데이터셋 평가 결과 ===")
for col in metric_cols:
    print(f"  {col}: {synth_df[col].mean():.4f}")
```

> `TestsetGenerator`는 단순한 질문뿐만 아니라 추론이 필요한 질문, 여러 문서를 종합해야 하는 질문 등 다양한 유형을 자동으로 생성한다. 실무에서는 수동 작성 + 합성 생성을 섞어서 평가 데이터셋을 구성하는 것이 일반적이다.
> 

---

## 실무에서의 RAG 평가

### 평가는 언제 하는가?

RAGAS를 매일 돌리는 팀은 거의 없다. 실무에서 평가가 필요한 시점은 명확하다.

| 시점 | 하는 일 | 도구 |
| --- | --- | --- |
| **초기 개발** | 대표 질문 10~20개로 눈으로 확인 | 수동 스팟체크 |
| **파이프라인 튜닝** | chunk_size, k, retriever 전략 변경 시 비교 | RAGAS |
| **프롬프트 변경** | 답변 품질이 달라졌는지 확인 | RAGAS 또는 수동 |
| **서비스 운영 중** | 사용자 만족도 추적 | 👍👎 피드백, 로그 분석 |
| **문서 추가/변경** | 기존 답변 품질이 유지되는지 확인 | RAGAS (회귀 테스트) |

### 실무 평가 흐름

실제 프로젝트에서는 다음과 같은 흐름으로 평가를 진행한다.

```
[1단계] 개발 중 — 수동 확인
    → 질문 10~20개로 "대충 되나?" 확인
    → 이 단계에서 RAGAS는 과하다

[2단계] 튜닝 시 — RAGAS 비교
    → 설정 A vs B를 수치로 비교
    → 평가 데이터셋은 20~50개면 충분 (난이도 섞어서)
    → 절대 점수가 아니라 "어느 쪽이 더 나은가"를 본다

[3단계] 배포 후 — 사용자 피드백
    → 👍👎 버튼, 답변 로그 수집
    → 낮은 평가를 받은 질문을 평가 데이터셋에 추가
    → 주기적으로 2단계를 반복
```

### 평가 데이터셋 관리

평가 데이터셋은 한 번 만들고 끝이 아니라 **지속적으로 관리**하는 자산이다.

- 서비스 운영 중 실패한 질문(사용자가 👎를 누른 질문)을 평가 데이터셋에 추가한다
- 문서가 변경되면 해당 문서와 관련된 질문의 정답(reference)도 업데이트한다
- 평가 데이터셋이 커지면 난이도별로 샘플링하여 비용을 절약한다

## LLM-as-Judge: 직접 평가 구현하기

RAGAS의 각 메트릭은 내부적으로 **LLM-as-Judge** 방식을 사용한다. LLM에게 채점 기준을 프롬프트로 주고, 결과를 판단하게 하는 것이다.

예를 들어 Faithfulness 메트릭은 내부적으로 이런 과정을 거친다:

1. 답변에서 주장(claim)을 추출한다
2. 각 주장이 검색된 문서에 근거하는지 LLM에게 판단시킨다
3. 근거 있는 주장의 비율을 점수로 계산한다

### RAGAS vs 직접 구현

|  | RAGAS | 직접 LLM-as-Judge |
| --- | --- | --- |
| **장점** | 검증된 메트릭, 바로 사용 가능 | 도메인 특화 기준 자유롭게 정의 |
| **단점** | 커스텀 기준 추가가 제한적 | 프롬프트 설계와 검증을 직접 해야 함 |
| **적합한 상황** | 범용 RAG 품질 평가 | "존댓말 사용 여부", "법률 용어를 쉽게 풀었는가" 등 |

### 언제 직접 구현하는가?

RAGAS의 기본 메트릭은 **검색 품질**과 **답변의 사실 정확성**을 평가한다. 하지만 다음과 같은 기준은 RAGAS로 평가할 수 없다.

- 답변 톤이 적절한가? (존댓말, 친근한 말투 등)
- 민감한 정보를 노출하지 않는가? (개인정보, 내부 시스템명 등)
- 도메인 용어를 정확히 사용하는가?
- 답변 길이가 적절한가?

이런 경우 LLM에게 직접 채점 기준을 주고 평가시킨다.

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

judge_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 출력 스키마 정의
class CriterionScore(BaseModel):
    score: int = Field(description="1~5점")
    reason: str = Field(description="채점 이유")

class JudgeResult(BaseModel):
    accuracy: CriterionScore = Field(description="답변이 검색된 문서에 근거하는가?")
    completeness: CriterionScore = Field(description="질문에 필요한 정보를 빠짐없이 답변했는가?")
    tone: CriterionScore = Field(description="사내 규정 안내에 적합한 톤인가?")

# 채점 기준을 프롬프트로 정의
judge_prompt = ChatPromptTemplate.from_template("""
당신은 RAG 시스템의 답변 품질을 평가하는 심사관입니다.

[질문]
{question}

[답변]
{answer}

[검색된 문서]
{context}

다음 기준으로 각각 1~5점을 매기고, 이유를 간단히 설명하세요.

1. **정확성(accuracy)**: 답변이 검색된 문서에 근거하는가? 지어낸 내용은 없는가?
2. **완전성(completeness)**: 질문에 필요한 정보를 빠짐없이 답변했는가?
3. **톤(tone)**: 사내 규정 안내에 적합한 톤인가? (너무 딱딱하거나 너무 가볍지 않은가?)
""")

judge_chain = judge_prompt | judge_llm.with_structured_output(JudgeResult)
```

> LLM-as-Judge의 핵심은 **프롬프트에 채점 기준을 명확하게 정의**하는 것이다. 기준이 모호하면 LLM도 일관성 없이 채점한다. "좋은 답변인가?"보다 "검색된 문서에 없는 내용을 포함하는가?"처럼 구체적으로 물어야 한다. 또한 평가용 LLM은 답변 생성용 LLM보다 **같거나 더 높은 성능의 모델**을 사용하는 것이 일반적이다.
>