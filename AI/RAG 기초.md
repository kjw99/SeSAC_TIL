# RAG 기초 - 문서 처리와 임베딩

```python
# 필요한 패키지 설치
# uv add pypdf
from dotenv import load_dotenv

load_dotenv()
```

## RAG (Retrieval-Augmented Generation)

LLM은 학습 데이터에 포함되지 않은 정보에 대해서는 정확하게 답변할 수 없다. 예를 들어 우리 회사의 사내 규정, 최신 제품 매뉴얼, 비공개 문서 등은 LLM이 알 수 없다.

**RAG**는 이 문제를 해결하는 패턴이다. 사용자의 질문과 관련된 문서를 먼저 **검색(Retrieval)** 한 뒤, 그 문서를 LLM의 프롬프트에 함께 넣어서 **응답을 생성(Generation)** 한다.

```
사용자 질문: "연차 신청은 어떻게 해?"

❌ LLM만 사용 → "일반적으로 HR 부서에 문의하세요..." (모호한 답변)
✅ RAG 사용  → 사내 규정 문서 검색 → "사내 포털 > 인사 > 연차 신청에서 가능합니다" (정확한 답변)
```

### RAG 파이프라인 전체 흐름

```
[ 문서 준비 단계 (오프라인) ]
문서 → 로드(DocumentLoader) → 분할(TextSplitter) → 임베딩 → 벡터 DB 저장

[ 질의 응답 단계 (온라인) ]
질문 → 임베딩 → 벡터 DB 검색 → 관련 문서 추출 → LLM에 전달 → 응답 생성
```

이번 시간에는 파이프라인의 각 구성 요소를 하나씩 살펴본다.

## Document Loader

RAG에서 사용할 문서를 로드하는 도구이다. LangChain은 다양한 형식의 문서 로더를 제공한다.

| 로더 | 형식 | 패키지 |
| --- | --- | --- |
| `TextLoader` | `.txt` | `langchain_community` |
| `PyPDFLoader` | `.pdf` | `pypdf` |
| `CSVLoader` | `.csv` | `langchain_community` |
| `WebBaseLoader` | 웹페이지 | `langchain_community` |

모든 로더는 `Document` 객체의 리스트를 반환한다.

```python
# Document 구조
Document(
    page_content="문서의 텍스트 내용...",
    metadata={"source": "파일경로", "page": 0, ...}
)
```

`metadata`는 문서의 출처, 페이지 번호 등 **부가 정보**를 담는 딕셔너리이다. 로더가 자동으로 채워주며, 나중에 검색 결과에서 "이 내용이 어디서 왔는지" 추적할 때 사용한다.

로더마다 문서를 나누는 기준이 다르다. `TextLoader`는 파일 전체를 하나의 Document로 반환하고, `PyPDFLoader`는 페이지 단위로 나누어 반환한다.

아래에서는 텍스트 파일과 PDF 파일을 로드하는 방법을 살펴본다.

### 텍스트 파일 로드

```python
from langchain_community.document_loaders import TextLoader

loader = TextLoader("data/sample_rules.txt", encoding="utf-8")
docs = loader.load()

print(f"문서 수: {len(docs)}")
print(f"metadata: {docs[0].metadata}")
print(f"내용 미리보기:\n{docs[0].page_content[:200]}")
```

### PDF 파일 로드

`PyPDFLoader`는 PDF를 페이지 단위로 분리하여 각 페이지를 하나의 `Document`로 반환한다.

```python
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("data/SPRi AI Brief_9월호_산업동향_0909_F.pdf")
docs = loader.load()

print(f"문서 수 (= 페이지 수): {len(docs)}")
for doc in docs[:3]:  # 처음 3페이지만 미리보기
    print(f"\n--- 페이지 {doc.metadata['page']} ---")
    print(doc.page_content[:200])
```

## Text Splitter (텍스트 분할)

문서를 통째로 임베딩하면 두 가지 문제가 생긴다.

1. **검색 정확도 저하**: 긴 문서 안에 여러 주제가 섞여 있으면, 질문과 관련 없는 내용까지 포함된다
2. **토큰 제한**: LLM의 context window에 긴 문서를 여러 개 넣을 수 없다

따라서 문서를 적절한 크기의 **청크(chunk)** 로 나눈 뒤 각 청크를 임베딩한다.

### 핵심 파라미터

| 파라미터 | 설명 | 예시 |
| --- | --- | --- |
| `chunk_size` | 청크의 최대 크기 (문자 수) | 500 |
| `chunk_overlap` | 인접 청크 간 겹치는 부분 | 50 |

```
원본: [ABCDEFGHIJ]

chunk_size=5, overlap=2:
  청크1: [ABCDE]
  청크2: [DEFGH]
  청크3: [GHIJ]
       ↑ overlap으로 문맥 단절 방지
```

`chunk_overlap`이 있으면 청크 경계에서 문맥이 끊기는 것을 줄일 수 있다.

### RecursiveCharacterTextSplitter

가장 많이 사용되는 분할기이다. `\\n\\n` → `\\n` →  `` → `""` 순서로 분할을 시도하여, 가능한 한 의미 단위(문단, 문장)를 유지한다.

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

# PDF 로드
loader = PyPDFLoader("data/SPRi AI Brief_9월호_산업동향_0909_F.pdf")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)

chunks = splitter.split_documents(docs)

print(f"원본 문서 수: {len(docs)}")
print(f"분할 후 청크 수: {len(chunks)}")

for i, chunk in enumerate(chunks[:6]):
    print(f"\n--- 청크 {i} (길이: {len(chunk.page_content)}, 페이지: {chunk.metadata.get('page')}) ---")
    print(chunk.page_content[:200])
```

### 청킹 전략 비교

`chunk_size`와 `chunk_overlap`은 문서의 특성에 따라 조절한다.

| 문서 유형 | chunk_size | overlap | 이유 |
| --- | --- | --- | --- |
| FAQ, Q&A | 200~400 | 20~50 | 항목이 짧고 독립적이라 작게 잘라도 맥락이 유지됨 |
| 기술 문서, 매뉴얼 | 500~800 | 50~100 | 절차나 설명이 이어지므로 중간 크기가 적절 |
| 법률 문서, 논문 | 800~1200 | 100~200 | 조항 간 맥락이 중요하므로 크게 유지 |

정답은 없다. 문서 특성과 질문 유형에 따라 실험으로 결정해야 한다.

```python
# 청킹 전략별 결과 비교
strategies = [
    {"name": "FAQ/Q&A",    "chunk_size": 300,  "chunk_overlap": 30},
    {"name": "기술 문서",    "chunk_size": 700,  "chunk_overlap": 70},
    {"name": "법률/논문",   "chunk_size": 1000, "chunk_overlap": 150},
]

for s in strategies:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=s["chunk_size"],
        chunk_overlap=s["chunk_overlap"],
    )
    chunks = splitter.split_documents(docs)
    avg_len = sum(len(c.page_content) for c in chunks) / len(chunks)
    print(f"{s['name']:8s} (size={s['chunk_size']}, overlap={s['chunk_overlap']}): {len(chunks)}개 청크, 평균 {avg_len:.0f}자")
```

### 다른 청킹 방법론

`RecursiveCharacterTextSplitter` 외에도 문서 특성에 맞는 분할기가 있다.

| 분할기 | 기준 | 적합한 문서 |
| --- | --- | --- |
| `RecursiveCharacterTextSplitter` | 문자 수 (`\\n\\n` → `\\n` →  `` 순으로 분할) | 범용. 대부분의 경우 이것으로 충분 |
| `TokenTextSplitter` | 토큰 수 | 임베딩 모델의 토큰 제한을 정확히 맞춰야 할 때 |
| `MarkdownHeaderTextSplitter` | 마크다운 헤더 (`#`, `##` 등) | 마크다운 문서. 섹션 구조를 유지하며 분할 |
| `HTMLHeaderTextSplitter` | HTML 헤더 (`h1`, `h2` 등) | 웹페이지 크롤링 결과 |
| `SemanticChunker` | 인접 문장의 임베딩 유사도 | 주제가 자주 바뀌는 문서. 문장마다 임베딩을 호출해서 느림 |

실무에서는 `RecursiveCharacterTextSplitter`가 가장 많이 쓰이고, 마크다운이나 HTML 문서를 다룰 때는 구조 기반 분할기를 사용하면 더 나은 결과를 얻을 수 있다.

> **Parent-Child Chunking**: 검색은 작은 청크(200토큰)로 정확도를 높이고, LLM에는 해당 청크를 포함하는 큰 청크(2000토큰)를 전달하여 맥락을 보존하는 기법이다. 검색 정확도를 끌어올릴 수 있는 효과적인 방법이지만, 구현이 복잡해진다. 대부분의 경우 `chunk_size`와 `chunk_overlap` 튜닝만으로 충분하다.
> 

## 임베딩 (Embedding)

임베딩은 텍스트를 **숫자 벡터(리스트)** 로 변환하는 것이다. 의미가 비슷한 텍스트는 비슷한 벡터로 변환되므로, 벡터 간의 거리를 측정하면 텍스트의 의미적 유사도를 계산할 수 있다.

```
"고양이"  → [0.12, -0.34, 0.56, ...] ─┐
"강아지"  → [0.11, -0.31, 0.55, ...] ─┤ 가까움 (의미 유사)
"자동차"  → [-0.87, 0.42, -0.15, ...] ─ 멂 (의미 다름)
```

- 임베딩 벡터의 차원 수는 모델마다 다르다 (OpenAI `text-embedding-3-small`: 1536차원)
- 벡터의 각 숫자 자체에는 사람이 해석할 수 있는 의미가 없다
- 중요한 것은 벡터 간의 **상대적 거리**이다

### 임베딩 모델 비교

| 모델 | 차원 | 최대 토큰 | 특징 |
| --- | --- | --- | --- |
| `text-embedding-3-small` | 1536 | 8191 | 가볍고 저렴. 대부분의 용도에 충분 |
| `text-embedding-3-large` | 3072 | 8191 | 더 높은 정확도. 비용 2배 |
- `text-embedding-3-small`이 비용 대비 성능이 좋아 일반적으로 권장된다
- 한국어 특화가 필요하면 오픈소스 모델(`multilingual-e5-large`, `bge-m3` 등)도 고려할 수 있다
- 임베딩 모델을 바꾸면 기존 벡터와 호환되지 않으므로 **벡터 DB를 재구축**해야 한다

### chunk_size와 임베딩 모델의 관계

`chunk_size`는 **문자 수** 기준이고, 임베딩 모델의 최대 입력은 **토큰 수** 기준이다. 단위가 다르므로 chunk_size를 정할 때 임베딩 모델의 토큰 제한을 고려해야 한다.

- 한국어는 대략 1글자 ≈ 1~2토큰이므로, `text-embedding-3-small`(최대 8191토큰) 기준 chunk_size 4000자 정도까지는 안전하다
- 일반적인 RAG에서 chunk_size를 500~1000으로 설정하면 토큰 제한에 걸릴 일은 없다
- 청크가 모델의 최대 토큰을 초과하면 뒷부분이 잘려서 임베딩되므로, 검색 품질이 떨어질 수 있다

### 임베딩 비용

임베딩도 API 호출이므로 비용이 발생한다. `text-embedding-3-small` 기준:

| 규모 | 토큰 수 (추정) | 비용 |
| --- | --- | --- |
| 이번 실습 (PDF 108청크) | ~5만 토큰 | ~$0.001 (거의 무료) |
| 사내 문서 1,000페이지 | ~50만 토큰 | ~$0.01 |
| 대규모 문서 10만 페이지 | ~5천만 토큰 | ~$1.0 |
- LLM 호출(GPT-4o 등)에 비하면 **매우 저렴**하지만, 대규모 문서를 반복 임베딩하면 누적된다
- 그래서 벡터 DB에 **한 번 저장하고 재사용**하는 것이 중요하다 — 같은 문서를 매번 임베딩하면 돈 낭비
- 문서가 변경되었을 때만 해당 문서의 벡터를 업데이트하는 것이 실무 패턴

### OpenAI Embedding API

LangChain의 임베딩 모델은 두 가지 메서드를 제공한다.

| 메서드 | 용도 | 입력 |
| --- | --- | --- |
| `embed_query()` | 검색 질문을 임베딩 | 단일 문자열 |
| `embed_documents()` | 저장할 문서를 임베딩 | 문자열 리스트 |

```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# 단일 텍스트 임베딩
vector = embeddings.embed_query("고양이는 귀엽다")

print(f"벡터 차원: {len(vector)}")
print(f"처음 5개 값: {vector[:10]}")
```

```python
# 여러 텍스트를 한 번에 임베딩
texts = [
    "고양이는 귀엽다",
    "강아지는 충성스럽다",
    "Python은 프로그래밍 언어다",
]

vectors = embeddings.embed_documents(texts)

for text, vec in zip(texts, vectors):
    print(f"\"{text}\" → 차원: {len(vec)}, 처음 3개: {vec[:3]}")
```

## 코사인 유사도 (Cosine Similarity)

두 벡터가 얼마나 비슷한 방향을 가리키는지를 측정한다. 값의 범위는 -1 ~ 1이며, 1에 가까울수록 유사하다.

```
cosine_similarity(A, B) = (A · B) / (|A| × |B|)
```

- `A · B`: 두 벡터의 내적 (각 원소를 곱한 후 합산)
- `|A|`: 벡터 A의 크기 (각 원소의 제곱합의 제곱근)

2차원 벡터로 예를 들면 직관적으로 이해할 수 있다.

```
A = [1, 0]   →          B = [1, 1]   ↗
C = [0, 1]   ↑          D = [-1, 0]  ←

cos(A, B) =  0.707   (45도 — 비슷한 방향)
cos(A, C) =  0.0     (90도 — 무관한 방향)
cos(A, D) = -1.0     (180도 — 반대 방향)
```

실제 임베딩은 1536차원이지만 원리는 동일하다. 방향이 비슷하면 유사도가 높고, 다르면 낮다.

| 값 | 의미 |
| --- | --- |
| 1.0 | 완전히 같은 방향 (동일한 의미) |
| 0.0 | 직교 (무관한 의미) |
| -1.0 | 반대 방향 (반대 의미) |

벡터 간 거리를 측정하는 방법에는 코사인 유사도 외에도 유클리드 거리(L2), 내적(Inner Product) 등이 있다. 벡터 DB에서 검색 방식을 설정할 때 선택하게 되며, 텍스트 검색에서는 코사인 유사도가 가장 많이 사용된다.

```python
import math

def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    """두 벡터의 코사인 유사도를 계산한다."""
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(a ** 2 for a in vec1))
    magnitude2 = math.sqrt(sum(b ** 2 for b in vec2))
    return dot_product / (magnitude1 * magnitude2)
```

```python
sentences = [
    "고양이가 소파에서 낮잠을 잔다",
    "고양이가 침대에서 자고 있다",
    "강아지가 공원에서 뛰어놀고 있다",
    "주식 시장이 급락했다",
]

vectors = embeddings.embed_documents(sentences)

# 첫 번째 문장과 나머지 문장의 유사도 비교
base = sentences[0]
print(f"기준: \"{base}\"\n")

for i in range(1, len(sentences)):
    sim = cosine_similarity(vectors[0], vectors[i])
    print(f"  vs \"{sentences[i]}\"")
    print(f"  → 유사도: {sim:.4f}\n")
```

### 임베딩 검색 직접 구현

임베딩과 코사인 유사도를 조합하면 간단한 의미 검색 시스템을 만들 수 있다. 아래 예제는 메뉴 목록을 임베딩한 뒤, 사용자의 자연어 질문으로 가장 관련 있는 메뉴를 찾는다.

이것이 RAG 파이프라인에서 **검색(Retrieval)** 단계의 핵심 원리다. 벡터 DB는 이 과정을 대규모 데이터에서도 빠르게 수행할 수 있도록 최적화한 저장소이다.

```python
menu_items = [
    "김치찌개: 돼지고기와 김치를 넣고 끓인 한국 전통 찌개. 매콤하고 깊은 맛.",
    "된장찌개: 된장과 두부, 야채를 넣은 구수한 찌개. 밥과 잘 어울림.",
    "비빔밥: 밥 위에 각종 나물과 고추장을 얹어 비벼 먹는 요리. 영양이 균형잡힘.",
    "불고기: 간장 양념에 재운 소고기를 구워 먹는 요리. 달콤하고 부드러움.",
    "냉면: 차가운 육수에 면을 말아 먹는 여름 별미. 시원하고 새콤함.",
    "떡볶이: 고추장 양념에 떡을 볶아 만든 길거리 음식. 매콤달콤함.",
    "삼겹살: 돼지 삼겹살을 구워 쌈채소와 함께 먹는 요리. 고소하고 짭짤함.",
    "잡채: 당면과 야채를 간장 양념으로 볶은 요리. 명절과 잔치에 빠지지 않음.",
    "갈비탕: 소갈비를 오래 끓여 만든 맑은 국물 요리. 보양식으로 인기.",
    "해물파전: 해산물과 파를 넣어 부친 전. 비 오는 날 막걸리와 잘 어울림.",
]

menu_vectors = embeddings.embed_documents(menu_items)

queries = ["매운 음식 추천해줘", "여름에 시원하게 먹을 수 있는 음식은?", "고기 요리가 먹고 싶어"]

for query in queries:
    query_vector = embeddings.embed_query(query)

    scores = []
    for i, menu_vec in enumerate(menu_vectors):
        sim = cosine_similarity(query_vector, menu_vec)
        scores.append((sim, menu_items[i]))

    scores.sort(reverse=True)
    print(f'질문: "{query}"')
    for rank, (sim, item) in enumerate(scores[:3], 1):
        print(f"  {rank}. [{sim:.4f}] {item[:40]}...")
    print()
```