# RAG 파이프라인 + 고도화

```python
# 필요한 패키지 설치
# uv add rank-bm25
```

```python
from dotenv import load_dotenv

load_dotenv()
```

## RAG Chain

검색 결과를 LLM에 전달하여 **질문에 대한 답변을 생성**하는 전체 파이프라인을 구성한다.

- 문서 로드
    - 답변 생성에 사용할 데이터가 들어있는 문서를 읽어온다.
- 청킹
    - 문서를 임의의 크기로 나눠서 각각 청크로 만들고 임베딩하는 것. 문서를 통째로 임베딩하면 검색 정확도가 떨어지고, 토큰 제한도 있어서. 청크 설정은 한 청크의 최대 크기(문자 수), 인접 청크 간 겹치는 부분(문맥이 끊기는 것을 방지하기 위함.)
    - 임베딩 : 텍스트를 숫자 벡터로 변환하는 것. 의미가 비슷한 텍스트는 비슷한 벡터로 변환됨. 그래서 벡터 간 거리 측정으로 텍스트의 의미적 유사도 계산 가능
- 벡터 DB 저장
    - 벡터 DB : 대량의 데이터를 하나씩 비교하며 검색할 수 없으니까 데이터를 위치 정보로 저장하고 거리를 재는 방식으로 검색하는 DB.
- 질문
    - 문서에 있는 데이터를 참고해서 답변을 하게 한다. 문서에 정보가 없으면 없다고 출력하도록 프롬프트를 설정.
    - 프롬프트 | LLM | Parser 이런식으로 체인을 만들고 invoke()를 통해 질문함.
- 이후 관련 문서 추출 → 프롬프트 주입 → LLM 응답 생성 과정이 진행됨.

```
문서 로드 → 청킹 → 벡터 DB 저장 → 질문 → Retriever(벡터 검색) → 관련 문서 추출 → 프롬프트에 주입 → LLM 응답 생성
```

### 문서 로드 + 벡터 DB 구축

```python
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

COLLECTION_NAME = "spri_ai_brief"
PERSIST_DIR = "./chroma_db"

# 문서 로드 → 분할
loader = PyPDFLoader("data/SPRi AI Brief_9월호_산업동향_0909_F.pdf")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

print(f"총 {len(chunks)}개 청크를 벡터 DB에 저장합니다...")

# 기존 컬렉션이 있으면 삭제 (중복 방지)
client = chromadb.PersistentClient(path=PERSIST_DIR)
existing_names = [c.name for c in client.list_collections()]
if COLLECTION_NAME in existing_names:
    client.delete_collection(COLLECTION_NAME)

# 벡터 스토어 생성 + 문서 저장 — client를 공유하여 일관된 경로 사용
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name=COLLECTION_NAME,
    client=client,
)

print(f"저장 완료! (컬렉션: {COLLECTION_NAME})")
```

### 기본 RAG Chain 구성

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

def format_docs(docs):
    """검색된 문서 리스트를 하나의 텍스트로 합치는 함수"""
    return "\n\n".join(doc.page_content for doc in docs)

prompt = ChatPromptTemplate.from_messages([
    ("system", """너는 AI 산업 동향 전문가야. 아래 검색된 문서를 참고하여 질문에 답변해줘.
검색 결과에 없는 내용은 "해당 정보를 찾을 수 없습니다"라고 답변해.

[검색된 문서]
{context}"""),
    ("human", "{question}"),
])

# 단계별 RAG
question = "오픈AI의 차세대 모델에 대해 설명해줘"

# 1. 검색
docs = retriever.invoke(question)

# 2. 문서 포매팅
context = format_docs(docs)

chain = prompt | llm | StrOutputParser()

# 3. 프롬프트 구성 + LLM 호출
response = (prompt | llm | StrOutputParser()).invoke(
    {"context": context, "question": question}
)

# response = chain.invoke({"context": context, "question": question})

print(response)

# 출처 확인
print("\n=== 출처 ===")
for i, doc in enumerate(docs):
    print(f"  [{i+1}] 페이지 {doc.metadata.get('page', '?')}: {doc.page_content[:200]}...")

```

### 하나의 Chain으로 합치기

위에서 단계별로 나눠 실행한 것을 LCEL로 하나의 chain으로 합칠 수 있다.

![img3.png](./AI_img/img3.png)

`{"context": retriever | format_docs, "question": RunnablePassthrough()}` 부분에서 딕셔너리가 chain 안에 들어가면 각 key의 값이 **동시에 실행**되고, 결과가 같은 key의 딕셔너리로 합쳐져서 다음 단계(prompt)에 전달된다.

### 체인 vs 함수

|  | 체인 (LCEL) | 함수 |
| --- | --- | --- |
| **호출** | `chain.invoke(question)` 한 줄 | 함수 안에서 각 단계를 직접 호출 |
| **비동기/스트리밍** | `.ainvoke()`, `.stream()`, `.astream()` 한번에 사용 가능 | 일일이 명시해야 함 |
| **중간 값 접근** | 어려움 (docs 등을 꺼내려면 구조가 복잡해짐) | 쉬움 (변수로 바로 접근) |
| **디버깅** | LangSmith 트레이싱으로 각 단계 자동 추적 | print/breakpoint로 직접 확인 |

> 스트리밍이 필요하면 체인, 중간 값(검색된 문서 등)이 필요하면 함수 방식이 적합하다. 실무에서는 두 방식을 섞어 쓰는 경우가 많다.
> 
- 위에서 retriever.invoke() → format_docs() 함수 실행 → chain 실행을 하나의 함수에 담아서 한번에 하는 것.
- RunnablePassthrough()는 입력을 그대로 다음 단계로 넘길 때 사용. 여러 입력을 조합하기 위한 것.
- 해당 코드에선 context에는 값을 추가하고 question은 입력 그대로 그냥 넘기게 됨.
- invoke()의 값이 rag_chain 전체 체인의 input.
- context에선 input을 통해 retriever에 넣어서 관련 문서 검색 후 format_docs로 정리.
- question에는 아무 처리 없이 통과 시킨다. 즉, question = input값이 됨.
- 그래서 RunnablePassthrough()를 쓴 것. 이거 없으면 LLM이 질문이 뭔지 파악이 안됨.
- prompt에서 context, question의 값이 필요하고, 이를 맨 앞의 딕셔너리 과정에서 넘겨준 것.
- LLM은 prompt를 참고해서 답변을 생성함.

```python
# 하나의 chain으로 합치기
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

response = rag_chain.invoke("오픈AI의 차세대 모델에 대해 설명해줘")
print(response)

```

```python
# 검색 결과에 없는 질문
response = rag_chain.invoke("삼성전자의 2024년 매출은?")
print(response)
```

### Citation 패턴 (Grounded Generation)

LLM이 생성한 답변이 어떤 원본 문서에 근거하는지 사용자에게 보여주는 방식이다. 신뢰성 확보와 할루시네이션 검증에 핵심적인 보조 수단이다.

| 패턴 | 설명 | 예시 |
| --- | --- | --- |
| **Inline Citation** | 답변 내에 `[1]`, `[2]` 등 참조 번호 삽입 | 학술 논문 스타일 |
| **Source List** | 답변 하단에 참조 문서 목록을 별도로 표시 | Perplexity AI 스타일 |
| **Structured Citation** | JSON 등 구조화된 포맷으로 답변+citation 출력 | Function calling 활용 |

```python
citation_prompt = ChatPromptTemplate.from_messages([
    ("system", """너는 AI 산업 동향 전문가야. 아래 검색된 문서를 참고하여 질문에 답변해줘.

규칙:
1. 답변의 각 문장 끝에 출처 번호를 [1], [2] 형태로 표시해
2. 검색 결과에 없는 내용은 절대 만들어내지 마
3. 답변할 수 없으면 "해당 정보를 찾을 수 없습니다"라고 답변해

[검색된 문서]
{context}"""),
    ("human", "{question}"),
])

def format_docs_with_index(docs):
    """문서에 번호를 붙여 포매팅한다. 페이지 번호도 함께 표시하여 LLM이 참조할 수 있게 한다."""
    return "\n\n".join(
        f"[{i+1}] (페이지 {doc.metadata.get('page', '?')}) {doc.page_content}"
        for i, doc in enumerate(docs)
    )

def citation_rag(question: str):
    """검색 → 답변 생성을 한 번에 처리하여 retriever 이중 호출을 방지한다."""
    docs = retriever.invoke(question)
    context = format_docs_with_index(docs)
    answer = (citation_prompt | llm | StrOutputParser()).invoke(
        {"context": context, "question": question}
    )
    return answer, docs

question = "AI 기업들의 최근 제품 출시 현황을 알려줘"
answer, source_docs = citation_rag(question)

print("=== 답변 (출처 포함) ===")
print(answer)

print("\n=== 참조 문서 ===")
for i, doc in enumerate(source_docs):
    print(f"  [{i+1}] (출처 : {doc.metadata.get('source', '?')}) (페이지 {doc.metadata.get('page', '?')}) {doc.page_content[:200]}...")
```

### 문서 추가 (10월호)

메타데이터 필터링을 실습하려면 여러 문서가 필요하다. 9월호에 이어 10월호를 추가로 저장한다.

```python
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 10월호 PDF 로드 → 분할
loader = PyPDFLoader("data/SPRi AI Brief_10월호_산업동향_1002_F.pdf")
docs_oct = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks_oct = splitter.split_documents(docs_oct)

# 기존 벡터 스토어에 추가 (9월호는 이미 저장되어 있음)
ids = vectorstore.add_documents(chunks_oct)
print(f"10월호 {len(chunks_oct)}개 청크 추가 완료")

# 검색 확인 — 10월호 내용이 검색되는지 확인
results = vectorstore.similarity_search("10월 AI 동향", k=2)
for doc in results:
    print(f"\n[페이지 {doc.metadata.get('page')}] {doc.page_content[:100]}...")
```

### 메타데이터 필터링

벡터 검색은 의미적 유사도만 보기 때문에, 원하지 않는 문서가 섞일 수 있다. 메타데이터 필터링을 사용하면 **특정 조건에 맞는 문서만** 검색 대상으로 한정할 수 있다.

```
전체 검색: "AI 동향" → 9월호 + 10월호 결과 섞임
필터 검색: "AI 동향" + source=9월호 → 9월호 결과만
```

```python
# 메타데이터 확인 — PyPDFLoader는 source, page를 자동으로 넣어준다
sample = vectorstore.similarity_search("AI", k=1)
print(f"메타데이터 예시: {sample[0].metadata}")
```

```python
# 특정 source(파일)로 필터링하여 검색
results_filtered = vectorstore.similarity_search(
    "AI 동향",
    k=3,
    filter={"source": "data/SPRi AI Brief_9월호_산업동향_0909_F.pdf"},
)

print("=== 9월호만 검색 ===")
for doc in results_filtered:
    print(f"  [{doc.metadata['source']}] {doc.page_content[:80]}...")

# 필터 없이 검색 (비교)
results_all = vectorstore.similarity_search("AI 동향", k=3)

print("\n=== 전체 검색 ===")
for doc in results_all:
    print(f"  [{doc.metadata['source'].split('/')[-1]}...] {doc.page_content[:80]}...")
```

```python
# 특정 페이지 범위로 필터링
results_page = vectorstore.similarity_search(
    "AI 동향",
    k=3,
    filter={"page": 0},  # 첫 페이지만
)

print("=== 첫 페이지만 검색 ===")
for doc in results_page:
    print(f"  [페이지 {doc.metadata['page']}] {doc.page_content[:80]}...")
```

메타데이터 필터링은 문서가 많아질수록 중요해진다. 예를 들어 여러 부서의 문서가 벡터 DB에 섞여 있을 때, 사용자의 부서에 해당하는 문서만 검색하도록 할 수 있다.

## MMR (Maximal Marginal Relevance)

유사도 검색은 질문과 가장 비슷한 문서를 순서대로 반환한다. 그런데 상위 결과들이 서로 비슷한 내용이면, 같은 이야기만 반복하게 된다.

MMR은 **유사도가 높으면서도 결과끼리 중복이 적도록** 다양성을 함께 고려하는 검색 전략이다.

- `search_type="similarity"` (기본값): 유사도가 높은 순서대로 반환
- `search_type="mmr"`: 유사도 + 다양성을 균형 있게 반환

**언제 쓸까?**

|  | similarity | MMR |
| --- | --- | --- |
| **적합한 경우** | "제미나이 2.5 딥씽크의 출시일"처럼 정답이 하나인 구체적 질문 | "제미나이"처럼 여러 측면이 있는 넓은 질문 |
| **결과 특성** | 가장 관련도 높은 문서를 놓치지 않음 | 비슷한 문서끼리 중복을 줄여 다양한 관점을 확보 |

실무에서는 서비스 특성에 맞게 하나를 골라 고정하는 경우가 대부분이다. 질문마다 동적으로 전략을 바꾸는 것은 LLM 호출이 추가되고 판단이 틀릴 위험도 있어서 잘 쓰지 않는다.

MMR은 구체적 질문에서도 유사도 높은 문서를 포함하기 때문에 크게 손해보지 않는다. 그래서 **MMR을 기본으로 두고 `lambda_mult`로 비중을 조절**하는 것이 현실적이다. (`1.0`이면 similarity와 동일, `0.0`이면 최대 다양성)

```python
# 일반 유사도 검색
sim_retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5},
)

# MMR 검색
mmr_retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 5, "fetch_k": 20, "lambda_mult": 0.3},
)

query = "제미나이"

print("=== 일반 유사도 검색 ===")
for doc in sim_retriever.invoke(query):
    src = doc.metadata.get('source', '').split('_')[1] if '_' in doc.metadata.get('source', '') else ''
    print(f"  - [{src} p.{doc.metadata.get('page', '?')}] {doc.page_content[:80]}...")

print("\n=== MMR 검색 ===")
for doc in mmr_retriever.invoke(query):
    src = doc.metadata.get('source', '').split('_')[1] if '_' in doc.metadata.get('source', '') else ''
    print(f"  - [{src} p.{doc.metadata.get('page', '?')}] {doc.page_content[:80]}...")

```

## 멀티쿼리 Retriever

사용자의 질문 하나로는 관련 문서를 충분히 찾지 못할 수 있다. 멀티쿼리 Retriever는 LLM을 사용하여 **원래 질문을 여러 관점으로 변형**한 뒤, 각 변형 질문으로 검색하여 결과를 합친다.

```
원래 질문: "휴가 정책 알려줘"
  ↓ LLM이 변형
질문 1: "연차 유급휴가 부여 기준은?"
질문 2: "특별 휴가 종류와 일수는?"
질문 3: "휴가 신청 절차는 어떻게 되나?"
  ↓ 각각 검색
결과를 합쳐서 중복 제거 → 더 풍부한 context
```

```python
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
import logging

# Jupyter에서 로그 출력을 위해 기본 핸들러 설정
logging.basicConfig()
logging.getLogger("langchain_classic.retrievers.multi_query").setLevel(logging.INFO)

multi_retriever = MultiQueryRetriever.from_llm(
    retriever=retriever,
    llm=llm,
)

# 모호한 질문 → LLM이 여러 관점으로 변환하여 검색
docs = multi_retriever.invoke("우려해야 하는 것은?")

print(f"\n검색된 문서 수: {len(docs)}")
for i, doc in enumerate(docs):
    print(f"\n--- 결과 {i+1} (페이지 {doc.metadata.get('page')}) ---")
    print(doc.page_content[:200])
```

## HyDE (Hypothetical Document Embeddings)

멀티쿼리가 "질문을 여러 버전으로 바꿔서 검색"하는 접근이라면, HyDE는 전혀 다른 발상이다.

**가상의 답변을 먼저 생성**하고, 그 답변의 임베딩으로 검색한다. 질문과 문서는 형태가 다르지만(질문 vs 서술문), 가상 답변과 실제 문서는 형태가 비슷하므로 임베딩 유사도가 더 높을 수 있다.

```
일반 검색:
  "AI 규제 동향은?" → 임베딩 → 검색

HyDE:
  "AI 규제 동향은?" → LLM이 가상 답변 생성
  → "EU는 AI Act를 통해 위험도 기반 규제 체계를 도입했고..."
  → 가상 답변을 임베딩 → 검색
```

가상 답변이 정확할 필요는 없다. **실제 문서와 비슷한 형태**이기만 하면 검색 품질이 올라간다.

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 가상 답변 생성 프롬프트
hyde_prompt = ChatPromptTemplate.from_messages([
    ("system", "질문에 대한 답변을 작성해줘. 정확하지 않아도 괜찮으니 관련 내용을 서술형으로 작성해."),
    ("human", "{question}"),
])

# 가상 답변 생성 → 임베딩 → 검색을 하나의 chain으로 구성
hyde_chain = hyde_prompt | llm | StrOutputParser()
hyde_retriever_chain = hyde_chain | (lambda answer: vectorstore.similarity_search(answer, k=3))

question = "AI 반도체 시장의 전망은?"

# 1. 가상 답변 확인
hypothetical_answer = hyde_chain.invoke({"question": question})
print("=== 가상 답변 ===")
print(hypothetical_answer[:300])

# 2. HyDE chain으로 검색
print("\n=== HyDE 검색 결과 ===")
hyde_docs = hyde_retriever_chain.invoke({"question": question})
for i, doc in enumerate(hyde_docs):
    print(f"\n--- HyDE 결과 {i+1} (페이지 {doc.metadata.get('page')}) ---")
    print(doc.page_content[:200])

# 3. 일반 검색과 비교
print("\n=== 일반 검색 결과 ===")
normal_docs = vectorstore.similarity_search(question, k=3)
for i, doc in enumerate(normal_docs):
    print(f"\n--- 일반 결과 {i+1} (페이지 {doc.metadata.get('page')}) ---")
    print(doc.page_content[:200])
```

HyDE는 LLM 호출이 한 번 추가되므로 비용과 지연이 발생한다. 검색 품질이 확실히 개선되는 경우에만 사용하자. 특히 질문이 짧거나 추상적일 때 효과가 크고, 구체적인 키워드 검색에는 오히려 불리할 수 있다.

## Hybrid Search (하이브리드 검색)

벡터 검색은 의미적 유사도를 잘 잡지만, **정확한 키워드 매칭**에는 약할 수 있다. 예를 들어 "GPT-4o"라는 고유명사를 검색할 때, 벡터 검색은 "대규모 언어 모델"과 관련된 문서를 가져올 수 있지만 정확히 "GPT-4o"가 포함된 문서를 놓칠 수 있다.

**하이브리드 검색**은 키워드 검색(BM25)과 벡터 검색을 결합하여 두 방식의 장점을 모두 활용한다.

> **BM25**는 키워드 기반의 문서 랭킹 알고리즘으로, Elasticsearch 등 검색엔진의 기본 랭킹 함수다. 문서에 검색어가 얼마나 자주 등장하는지(TF)와 그 단어가 얼마나 희귀한지(IDF)를 조합하여 점수를 매긴다.
> 

```
질문: "GPT-4o 성능"

키워드 검색 (BM25): "GPT-4o"가 포함된 문서 → 정확한 매칭
벡터 검색:          "대규모 언어 모델 성능 평가" 관련 문서 → 의미적 매칭

하이브리드: 두 결과를 합쳐서 → 정확하면서도 의미적으로 관련된 문서
```

| 검색 방식 | 강점 | 약점 |
| --- | --- | --- |
| **키워드 (BM25)** | 고유명사, 정확한 용어 매칭 | 동의어, 의미적 유사성 못 잡음 |
| **벡터 (Embedding)** | 의미적 유사도, 동의어 처리 | 정확한 키워드 매칭에 약함 |
| **하이브리드** | 두 방식의 장점 결합 | 구현 복잡도 증가, 가중치 튜닝 필요 |

> `BM25Retriever.from_documents()`는 전체 문서를 메모리에 올린다. 지금처럼 문서가 적을 때는 괜찮지만, 문서가 수만~수십만 건이면 비효율적이다. 실무에서는 Elasticsearch나 OpenSearch 같은 외부 검색엔진의 BM25를 사용하는 것이 일반적이다.
> 

```python
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever

# 앞에서 만든 chunks(9월호 + 10월호)를 그대로 사용
bm25_retriever = BM25Retriever.from_documents(chunks + chunks_oct, k=3)
vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 하이브리드 Retriever (가중치: BM25 40% + 벡터 60%)
hybrid_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.4, 0.6],
)

# 비교 테스트
query = "저작권"

print("=== 벡터 검색 ===")
for doc in vector_retriever.invoke(query):
    print(f"  {doc.page_content[:80]}...")

print("\n=== BM25 검색 ===")
for doc in bm25_retriever.invoke(query):
    print(f"  {doc.page_content[:80]}...")

print("\n=== 하이브리드 검색 ===")
for doc in hybrid_retriever.invoke(query):
    print(f"  {doc.page_content[:80]}...")
```

## Re-ranking

벡터 검색은 의미적 유사도 기반이라 항상 가장 관련 있는 문서가 1위가 되지는 않는다. Re-ranking은 검색된 문서를 **다시 정렬**하여 정확도를 높이는 기법이다.

```
벡터 검색 (k=10, 넉넉하게)
  ↓
Re-ranker가 질문과 각 문서의 관련성을 정밀 평가
  ↓
상위 3개만 최종 선택
```

여기서는 LLM을 활용한 Re-ranking을 구현한다. 문서마다 LLM을 호출하므로 비용과 지연이 발생한다는 점에 주의하자. 실무에서는 Re-ranking 전용 외부 서비스/모델을 사용하는 것이 일반적이다.

| 방식 | 설명 | 비고 |
| --- | --- | --- |
| **LLM Re-ranking** | LLM에게 관련성 평가를 맡김 | 비용 높음 (문서 수 × LLM 호출) |
| **Cohere Reranker** | Cohere사의 Re-ranking 전용 API | 외부 API 키 필요 |
| **Cross-Encoder** | `sentence-transformers` 라이브러리의 Re-ranking 모델 | 로컬 실행, 모델 다운로드 필요 |

전용 서비스/모델이 LLM 대비 빠르고 저렴하면서 정확도도 비슷하거나 더 높다. 여기서는 원리를 이해하기 위해 LLM 방식으로 구현한다.

```python
from pydantic import BaseModel, Field

class RelevanceScore(BaseModel):
    score: int = Field(description="관련성 점수 (0~10)")
    reason: str = Field(description="점수 근거")

SCORING_PROMPT = "질문: {question}\n\n문서: {content}\n\n이 문서가 질문에 답변하는 데 얼마나 관련이 있는지 0~10점으로 평가해줘."

def rerank(question: str, docs: list, top_k: int = 3) -> list:
    """LLM을 사용하여 문서를 재순위한다.
    주의: 문서 개수만큼 LLM을 호출하므로 비용과 지연이 비례하여 증가한다.
    실무에서는 각 문서 평가가 독립적이므로 asyncio.gather로 병렬 호출하면 훨씬 빠르다.
    """
    scoring_llm = llm.with_structured_output(RelevanceScore)

    scored = []
    for doc in docs:
        result = scoring_llm.invoke(
            SCORING_PROMPT.format(question=question, content=doc.page_content)
        )
        scored.append((doc, result.score, result.reason))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]

# 넉넉하게 검색한 뒤 re-ranking (6개 문서 → LLM 6회 호출)
query = "각국 정부의 AI 규제 정책"
initial_docs = vectorstore.similarity_search(query, k=6)

all_scored = rerank(query, initial_docs, top_k=6)

print(f"질문: {query}\n")

# 1) 전체 문서 점수
print("=== 전체 문서 점수 ===")
for doc, score, reason in all_scored:
    print(f"  [{score}점] {reason}")
    print(f"    → (p.{doc.metadata.get('page')}) {doc.page_content[:80]}...\n")

# 2) 상위 3개만 선택
print("=== Re-ranking 후 상위 3개 선택 ===")
for doc, score, reason in all_scored[:3]:
    print(f"  [{score}점] (p.{doc.metadata.get('page')}) {doc.page_content[:80]}...")
```

---

## SQL Chain (자연어 → SQL)

지금까지는 **문서**(PDF 등 비정형 데이터)에서 정보를 검색하는 RAG를 다뤘다. 하지만 데이터가 **DB 테이블**에 정형화되어 있다면? 임베딩이나 벡터 검색 없이, 자연어 질문을 SQL로 변환하여 직접 조회하는 것이 더 정확하다.

| 상황 | 적합한 방식 |
| --- | --- |
| 사내 규정, 매뉴얼, 논문 등 문서 검색 | **RAG** |
| 매출, 주문, 사용자 통계 등 DB 조회 | **SQL Chain** |
| 둘 다 필요 | RAG + SQL Chain 조합 (Tool로 분기) |

### DB 연결 + 테이블 확인

```python
from langchain_community.utilities import SQLDatabase

# PostgreSQL 연결
# .env에 DATABASE_URL이 설정되어 있어야 함 (예: postgresql://user:password@localhost:5432/dbname)
import os

# include_tables로 노출할 테이블을 제한하면 민감한 테이블(개인정보 등) 접근을 차단할 수 있다
db = SQLDatabase.from_uri(
    os.getenv("DATABASE_URL"),
    include_tables=["products"],  # 허용할 테이블만 명시
)

# 연결된 DB의 테이블 목록 확인
print("테이블 목록:", db.get_usable_table_names())

# 테이블 스키마 확인 — LLM이 SQL을 생성하려면 스키마를 알아야 한다
print(db.get_table_info())
```

### SQL Chain 구성

`create_sql_query_chain`은 테이블 스키마를 프롬프트에 포함시켜 LLM이 올바른 SQL을 생성하도록 한다.

```python
from langchain_classic.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool

# 자연어 → SQL 변환 체인
sql_chain = create_sql_query_chain(llm, db)

# SQL 실행 도구
execute_query = QuerySQLDatabaseTool(db=db)

# 자연어 질문으로 SQL 생성
question = "가장 비싼 상품 3개를 알려줘"
sql_query = sql_chain.invoke({"question": question})

# LLM이 "SQLQuery: SELECT ..." 형태로 생성할 수 있으므로 접두어 제거
sql_query = sql_query.strip().removeprefix("SQLQuery:").strip()

print("생성된 SQL:")
print(sql_query)
```

```python
# 생성된 SQL을 실제로 실행
result = execute_query.invoke(sql_query)
print("쿼리 결과:")
print(result)
```

### SQL 생성 + 실행 + 자연어 응답

SQL 실행 결과를 다시 LLM에 넘겨서 사용자가 읽기 좋은 자연어로 변환한다.

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# 자연어 응답 프롬프트
answer_prompt = ChatPromptTemplate.from_messages([
    ("system", """주어진 SQL 쿼리와 실행 결과를 바탕으로 사용자의 질문에 자연어로 답변해줘.
답변에 SQL 쿼리를 포함하지 마."""),
    ("human", """질문: {question}
SQL 쿼리: {query}
실행 결과: {result}"""),
])

# 단계별 실행
question = "가장 비싼 상품 3개를 알려줘"

# 1) 자연어 → SQL 생성
sql_query = sql_chain.invoke({"question": question})
sql_query = sql_query.strip().removeprefix("SQLQuery:").strip()
print("생성된 SQL:", sql_query)

# 2) SQL 실행
result = execute_query.invoke(sql_query)
print("실행 결과:", result)

# 3) 자연어 응답 생성
answer_chain = answer_prompt | llm | StrOutputParser()
response = answer_chain.invoke({"question": question, "query": sql_query, "result": result})
print("\n최종 응답:", response)
```

```python
# 하나의 체인으로 합치기 — 함수 방식
def run_sql_chain(input: dict) -> dict:
    question = input["question"]
    sql_query = sql_chain.invoke({"question": question})
    sql_query = sql_query.strip().removeprefix("SQLQuery:").strip()
    result = execute_query.invoke(sql_query)
    print(f"SQL: {sql_query}")
    return {"question": question, "query": sql_query, "result": result}

full_chain = run_sql_chain | answer_prompt | llm | StrOutputParser()

print(full_chain.invoke({"question": "재고가 가장 많은 상품은?"}))
```

```python
# 같은 체인을 RunnablePassthrough 방식으로 구성
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from operator import itemgetter

clean_sql = RunnableLambda(lambda x: {**x, "query": x["query"].strip().removeprefix("SQLQuery:").strip()})

full_chain_v2 = (
    RunnablePassthrough.assign(query=sql_chain)  # 질문 → SQL 생성
    | clean_sql  # 접두어 제거
    | RunnablePassthrough.assign(result=itemgetter("query") | execute_query)  # SQL 실행
    | answer_prompt
    | llm
    | StrOutputParser()
)

print(full_chain_v2.invoke({"question": "재고가 가장 많은 상품은?"}))
```

```python
# 다양한 질문 테스트
test_questions = [
    "전체 상품 수는 몇 개야?",
    "재고가 가장 적은 상품은?",
]

for q in test_questions:
    print(f"Q: {q}")
    print(f"A: {full_chain.invoke({'question': q})}")
    print()
```

SQL Chain은 LLM이 생성한 SQL을 그대로 실행하므로, **실무에서는 반드시 읽기 전용 DB 계정을 사용**해야 한다. LLM이 생성한 SQL은 본질적으로 신뢰할 수 없는 입력이므로, 애플리케이션 코드가 아니라 DB 엔진에서 막는 것이 가장 확실하다. DB 계정에 `SELECT` 권한만 부여하면 `DELETE`, `DROP` 같은 위험한 쿼리가 생성되더라도 DB가 거부한다. 또한 `include_tables` 파라미터로 LLM이 접근할 수 있는 테이블을 제한하면 민감한 데이터(개인정보 등) 노출을 방지할 수 있다.

## Conversational RAG (대화형 RAG)

지금까지의 RAG Chain은 **단발성 질문**만 처리한다. 하지만 실제 챗봇에서는 이런 대화가 자연스럽다.

```
사용자: EU의 AI 규제 정책은?
AI:     EU는 AI Act를 통해 위험도 기반 규제 체계를 도입했습니다...
사용자: 그거 언제부터 시행돼?           ← "그거"가 뭔지 모름
```

"그거"는 대화 맥락을 봐야 "EU AI Act"를 가리킨다는 걸 알 수 있다. 하지만 Retriever는 "그거 언제부터 시행돼?"로 검색하면 관련 문서를 찾지 못한다.

**해결**: 대화 히스토리를 참고하여 **질문을 재작성**한 뒤 검색한다.

```
원래 질문: "그거 언제부터 시행돼?"
  ↓ 대화 히스토리 참고하여 재작성
재작성: "EU AI Act의 시행 시기는?"
  ↓ 재작성된 질문으로 검색
관련 문서 검색 → LLM 응답
```

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import HumanMessage, AIMessage

# 질문 재작성 프롬프트
rewrite_prompt = ChatPromptTemplate.from_messages([
    ("system", "주어진 대화 히스토리와 후속 질문을 보고, 후속 질문을 독립적인 질문으로 재작성해라. 재작성된 질문만 출력해라."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "후속 질문: {question}\n\n재작성된 질문:"),
])

rewrite_chain = rewrite_prompt | llm | StrOutputParser()

# 테스트: 대화 맥락이 있는 질문 재작성
history = [
    HumanMessage(content="구글의 AI 관련 소식은?"),
    AIMessage(content="구글은 제미나이 모델을 발표하고 AI 서비스를 확장하고 있습니다."),
]

rewritten = rewrite_chain.invoke({
    "history": history,
    "question": "그거 성능이 어때?",
})
print(f"재작성된 질문: {rewritten}")
```

```python
# 대화형 RAG Chain 전체 구성
answer_prompt = ChatPromptTemplate.from_messages([
    ("system", """아래 검색된 문서를 참고하여 질문에 답변해줘.
검색 결과에 없는 내용은 "해당 정보를 찾을 수 없습니다"라고 답변해.

[검색된 문서]
{context}"""),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])

def create_conversational_rag_chain(retriever, llm):
    # 질문 재작성 체인을 내부에서 생성하여 외부 의존성 제거
    _rewrite_prompt = ChatPromptTemplate.from_messages([
        ("system", "주어진 대화 히스토리와 후속 질문을 보고, 후속 질문을 독립적인 질문으로 재작성해라. 재작성된 질문만 출력해라."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "후속 질문: {question}\n\n재작성된 질문:"),
    ])
    _rewrite_chain = _rewrite_prompt | llm | StrOutputParser()

    def process(inputs):
        # 1. 질문 재작성
        rewritten = _rewrite_chain.invoke({
            "history": inputs["history"],
            "question": inputs["question"],
        })
        print(f"  [재작성] {inputs['question']} → {rewritten}")

        # 2. 재작성된 질문으로 검색
        docs = retriever.invoke(rewritten)
        context = "\n\n".join(doc.page_content for doc in docs)
        print(f"  [검색] {len(docs)}개 문서 검색됨")

        # 3. 답변 생성
        answer = (answer_prompt | llm | StrOutputParser()).invoke({
            "context": context,
            "history": inputs["history"],
            "question": inputs["question"],
        })

        return {"answer": answer, "rewritten_question": rewritten}

    return process

conv_rag = create_conversational_rag_chain(retriever, llm)

# 대화 시뮬레이션
history = []

# 첫 번째 질문
q1 = "구글의 AI 관련 소식은?"
result1 = conv_rag({"question": q1, "history": history})
print(f"A: {result1['answer'][:200]}")

# 히스토리 업데이트
history.extend([
    HumanMessage(content=q1),
    AIMessage(content=result1["answer"]),
])

# 두 번째 질문 (대명사 사용)
q2 = "그거 성능이 어때?"
result2 = conv_rag({"question": q2, "history": history})
print(f"A: {result2['answer'][:200]}")
```

Conversational RAG의 핵심은 **질문 재작성**이다. 대화 히스토리 전체를 Retriever에 넣는 것이 아니라, LLM이 맥락을 이해하고 독립적인 검색 쿼리로 변환하는 것이 포인트다. 이렇게 하면 기존 RAG Chain과 Retriever를 그대로 재사용할 수 있다.

---

## 검색 고도화 기법 비교

| 기법 | 장점 | 단점 | 효과가 큰 상황 | 조합 |
| --- | --- | --- | --- | --- |
| **Multi-Query** | 모호한 질문을 다양한 관점으로 확장하여 검색 범위를 넓힘 | LLM 호출 1회 추가, 비결정적(매번 결과 다름) | 질문이 짧거나 애매할 때 | + Re-ranking, + Hybrid |
| **HyDE** | 질문과 문서 사이의 표현 차이를 줄여 검색 품질 향상 | LLM 호출 1회 추가, 가상 답변이 틀리면 오히려 악화 | 질문이 추상적이고 문서가 서술형일 때 | + Re-ranking (Hybrid와는 비추) |
| **Re-ranking** | 벡터 유사도만으로 놓치는 관련성을 LLM이 정밀 평가 | 문서 수만큼 LLM 호출 (비용·지연 큼) | 검색 정확도가 중요하고 비용 여유가 있을 때 | 모든 기법과 조합 가능 |
| **Hybrid Search** | 의미 검색 + 키워드 검색을 결합하여 상호 보완 | BM25 인덱스를 별도 관리해야 함 | 고유명사·약어 등 정확한 키워드 매칭이 필요할 때 | + Multi-Query, + Re-ranking |

> 위 기법들은 단독으로도 쓰지만, **조합하여 사용**하는 것이 일반적이다. 예를 들어 "Hybrid Search → Re-ranking"이나 "Multi-Query → Re-ranking" 조합이 실무에서 자주 사용된다. 다만 HyDE + Hybrid는 HyDE가 생성한 가상 답변이 키워드 매칭을 방해할 수 있어 조합 효과가 떨어진다. 어떤 조합이든 **평가(Evaluation)를 통해 실제 효과를 측정**해야 한다.
> 

---

## 벡터 DB 업데이트/삭제 전략

실무에서는 문서가 추가되거나 수정, 삭제되므로 벡터 DB도 함께 관리해야 한다.

| 상황 | 전략 |
| --- | --- |
| 새 문서 추가 | `add_documents()` |
| 문서 수정 | 기존 삭제 → 재삽입 |
| 문서 삭제 | ID 기반 삭제 |
| 전체 재구축 | 컬렉션 삭제 후 재생성 |

### 문서 삭제

`add_documents`가 반환한 ID를 사용하여 특정 문서를 삭제할 수 있다. 아래는 방금 추가한 10월호를 삭제했다가 다시 추가하는 예시이다.

```python
# ID로 삭제
vectorstore.delete(ids)
print(f"10월호 {len(ids)}개 청크 삭제 완료")

# 삭제 확인 — 10월호 내용을 검색해도 나오지 않아야 한다
results = vectorstore.similarity_search("10월 AI 산업 동향", k=3)
if results:
    for doc in results:
        print(f"  - {doc.metadata.get('source', '?')} (p.{doc.metadata.get('page', '?')})")
else:
    print("검색되지 않음")
```

```python
# 다시 추가 (문서 수정 시에도 삭제 → 재삽입 패턴을 사용)
ids = vectorstore.add_documents(chunks_oct)
print(f"10월호 {len(ids)}개 청크 재추가 완료")

```

### 메타데이터 기반 삭제

`add_documents`가 반환한 ID를 매번 기억하기는 어렵다. 실무에서는 **메타데이터 조건으로 삭제**하는 것이 더 일반적이다. 예를 들어 "9월호 문서만 전부 삭제"하거나, "특정 사용자가 업로드한 문서만 삭제"하는 식이다.

Chroma는 내부 클라이언트의 `get()` + `delete()`를 조합하여 메타데이터 기반 삭제를 할 수 있다.

```python
# 메타데이터 조건으로 문서 조회 → 삭제
# 예: 10월호 PDF에서 온 문서만 삭제
# 주의: _collection은 Chroma의 private 속성이다. 공식 API가 아니므로 버전 업데이트 시 변경될 수 있다.
collection = vectorstore._collection

# 조건에 맞는 문서의 ID 조회
oct_source = "data/SPRi AI Brief_10월호_산업동향_1002_F.pdf"
results = collection.get(where={"source": oct_source})
print(f"10월호 문서 수: {len(results['ids'])}")

# 조회된 ID로 삭제
if results["ids"]:
    collection.delete(ids=results["ids"])
    print(f"10월호 {len(results['ids'])}개 청크 삭제 완료")

# 삭제 확인
results_after = collection.get(where={"source": oct_source})
print(f"삭제 후 10월호 문서 수: {len(results_after['ids'])}")

# 다시 추가 (이후 실습을 위해)
ids = vectorstore.add_documents(chunks_oct)
print(f"10월호 {len(ids)}개 청크 재추가 완료")
```