# 로컬 LLM

- API 호출 없이 자신의 컴퓨터에서 LLM을 실행해본다
- LangChain의 추상화 덕분에 로컬 모델도 API 모델과 동일한 코드로 사용할 수 있다

## Ollama

로컬에서 LLM을 쉽게 실행할 수 있게 해주는 도구이다. `ollama pull`로 모델을 다운로드하고 `ollama run`으로 실행하면 된다.

- 공식 사이트: [https://ollama.com](https://ollama.com/)
- Llama(Meta), Qwen(Alibaba), Gemma(Google) 등 다양한 오픈소스 모델을 지원한다
- 로컬 API 서버를 띄워주기 때문에 LangChain 등 외부 도구에서 쉽게 연동할 수 있다

## Hugging Face

오픈소스 AI 모델의 **GitHub** 같은 플랫폼이다. LLM뿐만 아니라 이미지, 음성 등 다양한 AI 모델이 공유되어 있다.

- 공식 사이트: [https://huggingface.co](https://huggingface.co/)
- **Models**: 수십만 개의 사전학습 모델을 검색하고 다운로드할 수 있다
- **Datasets**: 학습용 데이터셋 공유 및 다운로드
- **Spaces**: 모델을 웹에서 바로 체험할 수 있는 데모 공간

Ollama 라이브러리에 없는 모델도 Hugging Face에서 GGUF 형식으로 다운로드하면 Ollama로 실행할 수 있다. 이처럼 모델을 모아놓은 플랫폼을 **Model Hub**라고 부른다.

## Transformers vs Ollama

Hugging Face에서는 `transformers`라는 Python 라이브러리도 제공한다. 이 라이브러리를 사용하면 모델을 Python 코드 안에서 직접 로드하고 추론할 수 있다.

하지만 원본 모델은 용량이 크고 GPU가 사실상 필수이기 때문에, 일반 PC에서 돌리려면 **양자화**(quantization)라는 경량화 과정이 필요하다. 양자화란 모델의 가중치를 더 작은 숫자로 압축하는 것으로, 품질을 약간 희생하는 대신 크기와 속도를 크게 개선한다.

그리고 이 양자화된 모델을 쉽게 돌려주는 도구가 바로 **Ollama**이다. 정리하면:

- Hugging Face에서 모델 다운로드 → 양자화(경량화) → **Ollama로 실행**

즉 Ollama는 경량화된 모델을 편리하게 실행하는 런타임이다. 이 강의에서는 복잡한 환경 설정 없이 바로 로컬 LLM을 체험할 수 있는 Ollama를 사용한다.

### API 모델로 체인 만들기

```python
from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("system", "너는 {role} 전문가야. 모든 답변은 한국어로 해줘."),
    ("human", "{question}"),
])

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
parser = StrOutputParser()

chain = prompt | llm | parser

result = chain.invoke({
    "role": "Python",
    "question": "for 문을 설명해줘",
})

print(result)
```

### Ollama 설치

공식 사이트([https://ollama.com](https://ollama.com/))에서 설치 파일을 다운로드한다.

- **macOS**: `brew install ollama` 또는 공식 사이트에서 다운로드
- **Windows**: 공식 사이트에서 설치 파일 다운로드

설치 후 터미널에서 모델을 다운로드한다:

```bash
# 모델 다운로드 (0.5b는 가장 가벼운 모델로, CPU에서도 무리 없이 실행된다)
ollama pull qwen2.5:0.5b

# 서버가 꺼져 있다면 직접 실행
ollama serve
# Error: listen tcp 127.0.0.1:11434: bind: Only one usage of each socket address (protocol/network address/port) is normally permitted.
# 이런 오류가 뜨면 이미 실행 중인 것. 첫 설치할 때 백그라운드로 실행되는 경우가 있음.
# 작업관리자 세부 정보에서 ollama 찾아서 종료하면 됨.
```

```bash
# LangChain Ollama 연동 패키지 설치
uv add langchain-ollama
```

- ollama serve 는 터미널에서 사용하는 명령어. ollama를 실행한다는 것. ollama 서버를 실행하고 아래 코드를 쓰면 서버에서 연산하는 것을 확인 가능.

```python
from langchain_ollama import ChatOllama

# 모델만 교체하면 된다
local_llm = ChatOllama(model="qwen2.5:0.5b", temperature=0)

# 나머지는 동일
chain = prompt | local_llm | parser

result = chain.invoke({
    "role": "Python",
    "question": "for 문을 설명해줘",
})

print(result)
```

### 복잡한 질문으로 비교하기

간단한 질문에서는 차이가 크지 않지만, 추론이 필요한 질문에서는 모델 성능 차이가 뚜렷하게 드러난다.

```python
complex_question = {
    "role": "Python",
    "question": "재귀를 사용하지 않고 피보나치 수열의 n번째 값을 구하는 함수를 작성하고, 시간 복잡도를 분석해줘",
}

print("=== API 모델 (gpt-4o-mini) ===\n")
api_chain = prompt | llm | parser
print(api_chain.invoke(complex_question))

print("\n\n=== 로컬 모델 (qwen2.5:0.5b) ===\n")
local_chain = prompt | local_llm | parser
print(local_chain.invoke(complex_question))
```

- 위 코드를 실행해보면 gpt와 ollama 모델의 답변 차이를 느낄 수 있음.

로컬 모델과 API 모델의 차이를 직접 비교해보자.

| 비교 항목 | 로컬 LLM (qwen2.5:0.5b) | API (gpt-4o-mini) |
| --- | --- | --- |
| 속도 | 느림 (CPU 추론) | 빠름 |
| 품질 | 낮음 (파라미터 수 적음) | 높음 |
| 비용 | 무료 | 토큰당 과금 |
| 인터넷 | 불필요 | 필요 |

코드는 모델 객체만 교체하면 되므로 동일하다. 작은 모델로 개발/테스트하고, 실제 서비스에서는 API 모델을 사용하는 전략도 가능하다.