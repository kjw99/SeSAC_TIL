- openai api 사용을 위해 OpenAI API Reference를 확인하자.
- https://platform.openai.com/docs/api-reference/introduction
- docs와 api reference 참고!
- 생성형 ai는 데이터를 생성함. 그래서 get이 아니라 post를 사용해야 한다.
    - get은 단순히 데이터를 가져오는 용도. post는 데이터 전송, 생성 등으로 서버에 영향을 줄 수 있음.
- post를 통해 body에 담아서 전달하는 데이터를 payload라고 부른다.
- url : 리소스 식별
- method : 리소스 행동
- params : 리소스 식별에 필요한 정보(리소스에 대한 메타데이터)
- header : http 요청에 대한 메타데이터(데이터를 위한 데이터, 요청을 위한 데이터라는 뜻.)

## OpenAI API 사용

### 핵심 파라미터

- **model**
    - 사용할 모델 버전 (예: `gpt-5`, `gpt-4o` 등)
- **messages**:
    - 대화 내역 배열 (role과 content를 포함한 객체 리스트)
- **temperature**
    - 답변의 창의성 조절. 낮을수록 결정론적, 높을수록 무작위적 (0~2 사이)
    - **0.0 ~ 0.3 (엄격함):** 데이터 추출, 코드 생성, 기술 문서 요약 등 사실 관계가 중요한 작업.
    - **0.7 ~ 1.0 (균형):** 일반적인 대화, 블로그 포스팅, 이메일 작성.
    - **1.2 ~ 1.5 (창의적):** 시 쓰기, 브레인스토밍, 캐릭터 페르소나 연기.
- **max_completion_tokens**
    - 생성할 최대 토큰 수
    - 너무 낮게 설정하면 답변이 중간에 뚝 끊길 수 있음
- **stream**
    - 실시간 답변 생성 여부, 사용자 경험(UX)을 위해 글자가 한 글자씩 써지는 효과
- **top_p**
    - 누적 확률 컷오프. `temperature`와 비슷하나 샘플링 방식이 다름 (보통 둘 중 하나만 조정 권장)
- **response_format**
    - `{"type": "json_object"}`로 설정하여 출력을 JSON으로 강제 가능

---

### messages에서의 Role 구성

`messages` 파라미터는 배열 내에 여러 개의 객체를 담아 대화의 맥락을 전달한다.

- **system - 시스템 설정**
    - 지침 및 페르소나 설정
    - 모델의 성격, 답변 스타일, 제약 조건, 지식 범위를 정의한다.
- **user - 사용자 입력**
    - 사용자의 실제 질문이나 명령
    - 사람이 전달하는 데이터이며, 모델이 구체적으로 수행해야 할 작업 내용이 담긴다.
- **assistant - 모델의 응답**
    - 모델의 이전 응답 기록
    - 이전에 모델이 답변했던 내용이다. 대화의 맥락(Context)을 유지하기 위해 개발자가 이전 대화 기록을 수동으로 배열에 추가해야 한다.

### API 사용 준비

- model에서 원하는 모델을 사용 가능. 가격에 대한 부분은 openai의 docs에서 살펴보자.

```python
import requests
from pprint import pprint
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
URL = "https://api.openai.com/v1/chat/completions"
model = "gpt-4o-mini"
```

### REST API 요청

- 라이브러리 없이 직접 HTTP 통신을 통해 api 호출.

```python
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}"
}

payload = {
    "model": model,
    "messages": [
        {"role": "system", "content": "당신은 친절한 AI 강사입니다."},
        {"role": "user", "content": "Chat Completions API가 뭐야? 2~3문장으로 답변해줘"}
    ]
}

response = requests.post(URL, headers=headers, json=payload)
pprint(response.json())
print(response.json()['choices'][0]['message']['content'])
```

- chatgpt는 생성형 AI이기 때문에 매번 답변이 달라짐.

### OpenAI SDK 활용한 요청

- 그냥 api 쓰는 것은 절차 지향! 순서대로 쓰면 된다.
- 만들어둔 클래스를 바탕으로 안에 있는 동작을 사용하는 방식 - 객체 지향.
- SDK는 객체 지향 방식.
- 공식 라이브러리(OpenAI)를 사용해서 생산성을 높이는 방식.
- 사용 방식은 자유지만, SDK를 사용한 것은 유지보수가 좀 더 편함.
- 추상화가 되어 있음. 자세한 사용법은 검색해서 보던가 ai에게 물어보자.
    - 검색은 openai sdk python 뭐 이런 느낌으로.

```python
from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)

completion = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "user", "content": "Openai SDK를 사용하면 어떤 점이 좋아?"}
    ]
)

print(completion.choices[0].message.content)
```

### System Prompt 비교

- 동일한 질문에 대해 AI의 페르소나(역할)에 따라 답변이 어떻게 달라지는지 확인해 보자.
- 페르소나는 가능한 자세히 만드는 게 더 도움이 된다. 나이, 성별, 습관 뭐.. 등등.. 가능한 자세히!
- “system”의 “role”에 페르소나를 넣으면 더 좋음. 코드에서 prompt라는 페르소나를 user 쪽에 넣을 수도 있지만, 성능 차이가 있음.
- system 부분이 개발자가 건들 수 있는 영역. user 쪽은 사용자가 입력한 데이터들일 테니 개발자 입장에선 관리가 안됨.
    - ai를 써보면 특정 질문 답변을 안하는 것도 이렇게 개발자가 건들 수 있는 부분에서 제어하는 것.
- openai 말고 다른 ai의 api도 비슷한 기능을 제공함.

```python
user_input = "아침 일찍 일어나는 습관의 장점에 대해 말해줘."

personas = {
    "열정적인 셰프": "당신은 요리에 인생을 건 셰프입니다. 인생의 모든 이치를 요리 과정과 재료에 비유하여 설명하세요.",
    "엄격한 헬스 트레이너": "당신은 매우 엄격한 운동 전문가입니다. 강한 어조로 자기관리를 강조하며 답변하세요.",
    "지혜로운 판다": "당신은 대나무 숲에 사는 느긋하고 지혜로운 판다입니다. 느릿느릿하고 평화로운 말투로 조언을 건네세요."
}

for name, prompt in personas.items():
    print(f"--- [{name}] 버전 ---")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
        ]
    )
    print(response.choices[0].message.content)
    print("\n")
```

## Temperature 비교

- Temperature가 높을 수록 무작위성이 늘어나고, 낮을 수록 결정론적. 즉 확실한 답변을 함. 답변의 창의성을 조절하는 것.

```python
creative_topic = "운동화 브랜드의 새로운 슬로건을 5개 제안해줘. 단, '속도'나 '승리' 같은 뻔한 단어는 제외하고 아주 기발하게 작성해줘."
temperatures = [0.3, 0.8, 1.0, 1.3, 1.5, 1.6, 1.8]

for t in temperatures:
    print(f"### 설정값 (Temperature): {t} ###")
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": creative_topic}],
        temperature=t,
        max_completion_tokens=200, 
        timeout=15.0
    )
    print(response.choices[0].message.content)
    print("=" * 50)
```

- 실행 결과를 비교해보면, temperature가 높아질 수록 주제에서 벗어난 이야기가 많이 나오고, 랜덤성 있는 결과물이 나옴. 나중에 가면 아예 한글이 아니라 다른 나라 언어도 섞이면서 제대로 된 답변이 나오지 않는다.
- 답변을 생성할 때 글자 하나 하나를 토큰으로 생각하면서 다음 글자는 어떤 토큰을 쓰는 것이 좋을지 ai가 각 단어마다 확률을 부여함. a = 80%, b = 20% … 이런 느낌으로.
    - temperature의 값이 높아지면 랜덤성을 위해 저 확률이 더 낮아지고 높아지고 하는 것.
- 아래 코드는 다른 예시.

```python
creative_topic = "우리집 강아지의 별명을 3개 지어줘."
temperatures = [0.3, 0.8, 1.0, 1.3, 1.5, 1.6, 1.8]

for t in temperatures:
    print(f"### 설정값 (Temperature): {t} ###")
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": creative_topic}],
        temperature=t,
        max_completion_tokens=200, 
        timeout=15.0
    )
    print(response.choices[0].message.content)
    print("=" * 50)
```

- 코드를 보면 max_completion_tokens 속성이 있는데, 이 토큰이 ai가 인식하는 글자라고 보면 됨.
- 그래서 우리가 질문을 하면 그 텍스트를 토큰으로 바꾼다. ( input 작업 )
    - 이후 토큰을 통해 연산하고, 연산 결과를 다시 텍스트로 바꿔서 보여주는 것. ( output 작업 )
    - 같은 텍스트로 질문하면 이전에 토큰으로 바꿨던 결과가 남아 있는데, 이럴 때는 굳이 다시 토큰으로 바꾸는 작업을 안하고 참고만 하면 됨. 이 경우를 cashed input 작업이라고 함. ( input 작업보다 cashed input 작업이 돈이 덜 들어감 )
    - 모델마다 가격이 다 다르다! 자세한 내용은 docs 참고.
- 영어의 경우 토큰으로 인식하는 단위가 단어로 인식해서 사용되는 토큰 수가 적어짐. 한글은 글자 하나 하나를 토큰으로 인식해서 좀 숫자가 많아진다.
    - 버전에 따라 토큰 인식 방식도 달라짐. 아래 예시는 chatgpt 5 버전.
    - 4 이하 버전으로 가면 “런”, “식” 이런 한 글자 자체를 2개의 토큰으로 나눠서 인식함.
    - 그래서 최신 버전일 수록 한글 영어의 차이가 좁혀지는 중.

![image.png](attachment:3e0d2dbf-a007-42f7-89bf-1c1268c41b54:image.png)

### message 배열을 활용한 대화 맥락 유지 (Context Window)

- Chat Completions API는 상태를 저장하지 않는(Stateless) 방식이므로, 이전 대화 내역을 리스트에 계속 누적해서 보내야 한다.
    - me : 질문1
    - ai : 답변1
    - 첫 질문이 이렇게 끝나면, 다음 질문을 할 때에는
    - me : 질문1 / ai : 답변1 / me : 질문2 / ai : 답변2
    - 이런 느낌으로 이전 기록을 묶어서 다음 질문을 해야 함.

```python
def chat_without_memory(user_input):
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": user_input}
        ]
    )
    
    # 3. 모델의 답변을 기록에 추가 (이것이 맥락 유지의 핵심)
    answer = response.choices[0].message.content
    
    return answer

# 실습 테스트
print("Q1: 내 이름은 jun이야.")
print(f"A1: {chat_without_memory('내 이름은 jun이야')}\n")

print("Q2: 내 이름이 뭐라고?")
print(f"A2: {chat_without_memory('내 이름이 뭐라고?')}")
```

- System이라고 하는 list가 있음.
    - 첫 번째로 System에 대한 걸 넣음. (role = system, content = 당신은 ~~ 입니다)
    - 두 번째로 user의 메시지를 넣음. (사용자의 질문을 위에 system이 넣었던 history에 추가.)
    - 이 두가지를 ai에 넣음. ( 이런 전체 기록을 API에 전송! )
    - 3번째로 어시스턴스로 저장. ( API에 전송하고 받은 답변을 또 history에 추가. ) 이 과정이 맥락 유지의 핵심이다.
    - 4번째로 유저가 또 뭐라고 말함. ( 사실상 여기부터 2 ~ 3 반복인 것 )
    - 여기서 유저의 말만 전달하는게 아니라 1 ~ 3까지 포함해서 히스토리 전체를 전달함
    - 5번째로 또 이런 내용을 어시스턴스로 저장하고 ~~ 반복
    - 이렇게 반복하면 2번 질문부터는 1번 질문에 대한 내용도 AI가 인지할 수 있는 것.
- 이게 대화 맥락 유지를 하는 방법!
    - 이렇게 하면 토큰을 많이 씀. 매번 물어보는 양이 길어지니까.. 실제로 gpt 채팅 하나에서 계속 질문하면 할수록 답변이 느려짐. 유료 버전은 한도가 빨리 올거고..
    - 그래서 이런 문제를 해결하기 위해 대화를 압축하는 방법도 있음. 아니면 토큰 낭비를 막기 위해 윗 부분을 날려버리거나.

```python
# 대화 내역을 저장할 리스트 초기화
history = [
    {"role": "system", "content": "당신은 사용자의 이름을 기억하는 비서입니다."}
]

def chat_with_memory(user_input):
    # 1. 사용자 질문을 기록에 추가
    history.append({"role": "user", "content": user_input})
    
    # 2. 전체 기록을 API에 전송
    response = client.chat.completions.create(
        model=model,
        messages=history
    )
    
    # 3. 모델의 답변을 기록에 추가 (이것이 맥락 유지의 핵심)
    answer = response.choices[0].message.content
    history.append({"role": "assistant", "content": answer})
    
    return answer

# 실습 테스트
print("Q1: 내 이름은 jun이야.")
print(f"A1: {chat_with_memory('내 이름은 jun이야.')}\n")

print("Q2: 내 이름이 뭐라고?")
print(f"A2: {chat_with_memory('내 이름이 뭐라고?')}")
```

### Structured Outputs (구조화된 출력)

- 모델의 답변에서 중요한 정보와 중요하지 않은 정보를 걸러내야 한다. 이러려면 구조화가 잘 되어 있어야 하고, 여기서 가장 쓰는게 json 형태!
- 모델의 답변을 단순 텍스트가 아니라 json 형태로 고정해서 받아보자. 백엔드에서 데이터 처리할 때 필수적임.
- 아래 코드에선 json mode(json_object)로 json format을 활용하지만, 이후에는 pydantic 라이브러리를 활용한 json schema 방식을 통해 명확한 json 응답 형식을 지정함.
    - 우리가 원하는 형태의 json 데이터를 원하기 때문에.
- json.loads() : 텍스트를 우리가 사용하는 리스트나 딕셔너리 형태로 바꿔줌.

```python
import json

response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": "너는 요리사야. 답변은 반드시 JSON 형식으로 해줘."},
        {"role": "user", "content": "떡볶이 레시피 알려줘."}
    ],
    # JSON 모드 활성화
    response_format={"type": "json_object"}
)

# 문자열로 온 답변을 직접 파싱해야 함
res_json = json.loads(response.choices[0].message.content)
print(res_json)
```

### Streaming (실시간 응답 처리)

- stream = True 설정을 통해 활성화.
- 서버는 SSE 프로토콜을 사용하여 응답을 끊지 않고 답변을 조각(Chunk) 단위로 지속적으로 전송함.
    - 원래 서버는 클라이언트가 해달라고 해줄 때만 답변을 한다.
    - SSE를 사용하면 서버가 계속 클라이언트에게 데이터 전달을 하는 것.
- 응답 객체는 제너레이터 형식으로, for 루프를 사용해 활용할 수 있다.
- print()의 flush 속성 : 원래 print는 덩어리가 좀 모일 때 한번에 출력하도록 최적화 되어 있는데, flush는 그걸 그냥 하나씩 출력하도록 만드는 옵션
- 유저에게 전달할 때 사용하면 좋음. 내부적으로 쓸 때에는 별로임.

```python
prompt = "양자 역학에 대해 초등학생도 이해할 수 있게 설명해줘."
print(f"질문: {prompt}\n")
print("답변: ", end="")

response = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": prompt}],
    stream=True 
)

full_response = ""
for chunk in response:
    content = chunk.choices[0].delta.content
    if content:
        print(content, end="", flush=True) # flush 옵션을 통해 출력 버퍼를 즉시 비워 스트리밍 답변이 지연 없이 실시간으로 표시되도록 한다.
        full_response += content

print("\n\n--- 스트리밍 종료 ---")
```

### Python 제너레이터

- Generator란?
- 제너레이터는 모든 결과값을 한번에 메모리에 올리지 않고, 필요할 때마다 값을 하나씩 생성하여 반환하는 특별한 도구.
- 일반 함수(return) : 계산이 끝나면 모든 결과를 한 번에 반환하고 종료.
- 제너레이터(yield) : 값을 하나씩 바깥으로 보내고 그 자리에서 일시 정지.

```python
def simple_generator():
    print("첫 번째 값을 생성합니다.")
    yield "A"
    
    print("두 번째 값을 생성합니다.")
    yield "B"
    
    print("세 번째 값을 생성합니다.")
    yield "C"

gen = simple_generator()

# next()를 호출할 때마다 다음 yield까지 실행됩니다.
print(f"받은 값: {next(gen)}")
print(f"받은 값: {next(gen)}")
print(f"받은 값: {next(gen)}")

```

- 제너레이터는 일회용 값. for를 통해 다 뺀 다음 gen을 호출하면 빈 리스트가 나옴.

```python
gen = simple_generator()

# for loop은 내부적으로 next()를 호출한다.
for text in gen:
    print(text)
```

### Stream API에서 제너레이터 활용하는 이유

- 메모리 효율성
    - AI가 2,000단어의 긴 답변을 생성할 때, 이를 다 만들 때까지 기다렸다가 한 번에 받으면 메모리 점유율이 높아진다.
    - 제너레이터 방식을 쓰면 생성되는 즉시 소비하고 버릴 수 있어 서버 자원을 아낄 수 있다.
- 실시간성
    - 사용자는 AI가 답변을 다 작성할 때까지 빈 화면을 보는 것이 아니라, 첫 글자가 생성되는 즉시 화면에서 확인할 수 있다.

### Logprobs - 확률 확인하기

```python
import math

prompt = "새로 오픈한 조용한 북카페 이름을 한글로 딱 하나만 추천해줘."
response = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": prompt}],
    logprobs=True,
    top_logprobs=3,
    max_completion_tokens=50
)

content = response.choices[0].message.content
logprobs_data = response.choices[0].logprobs.content

print(f"질문: {prompt}")
print(f"답변: {content}\n")
print(f"{'Token':<15} | {'Probability':<12} | {'Top Alternatives'}")
print("-" * 60)

for lp in logprobs_data:
    prob = math.exp(lp.logprob) * 100
    alternatives = [f"{top.token}({math.exp(top.logprob)*100:.1f}%)" for top in lp.top_logprobs]
    print(f"{lp.token:<15} | {prob:>10.2f}% | {', '.join(alternatives)}")
```

```python
질문: 새로 오픈한 조용한 북카페 이름을 한글로 딱 하나만 추천해줘.
답변: "여유로운 페이지" 추천드립니다.

Token           | Probability  | Top Alternatives
------------------------------------------------------------
"               |      97.81% | "(97.8%), '(1.8%), “(0.3%)
여               |      19.47% | 여(19.5%), 책(19.5%), 조(17.2%)
유               |      75.34% | 유(75.3%), 백(24.5%), 운(0.1%)
로운              |      49.34% | 로운(49.3%), 의(20.6%), "(14.1%)
 페이지            |      61.14% |  페이지(61.1%),  책(32.7%),  서(3.0%)
"               |     100.00% | "(100.0%), 들(0.0%), ”(0.0%)
 추천             |      10.18% | <|end|>(31.4%), 는(21.6%),  \xec\x96\xb4\xeb\x96(21.6%)
드립니다            |      37.30% | 합니다(61.5%), 드립니다(37.3%), 해(0.6%)
.               |      99.14% | .(99.1%), !(0.9%), .
(0.0%)
```

- 이런식으로 한 글자 글자마다 각각의 확률이 존재함. 보통 높은 확률의 단어를 쓰지만, 가끔 낮은 확률의 단어를 쓰는 경우도 있어서 색다른 답변이 나오는 것.

### 배운 것들 활용해서 챗봇 만들기

- OpenAI에서 제공하는 라이브러리 사용.
- 터미널에서 작동하는 챗봇으로 제작.
- stream 기능을 통해 답변을 실시간 확인하도록 구현.
- 답변 기록을 저장해둬서 계속 대화가 이어질 수 있도록 구현

```python
from pprint import pprint
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
URL = "https://api.openai.com/v1/chat/completions"
model = "gpt-4o-mini"

client = OpenAI(api_key=OPENAI_API_KEY)

# 대화 내역을 저장할 리스트 초기화
history = [
    # {"role": "system", "content": "당신은 사용자의 이름을 기억하는 비서입니다."}
]

def chat_with_memory(user_input):
    # 1. 사용자 질문을 기록에 추가
    history.append({"role": "user", "content": user_input})    
    # 2. 전체 기록을 API에 전송
    response = client.chat.completions.create(
        model=model,
        messages=history,
        stream=True
    )

    full_response = ""
    for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True) # flush 옵션을 통해 출력 버퍼를 즉시 비워 스트리밍 답변이 지연 없이 실시간으로 표시되도록 한다.
            full_response += content
    
    # 3. 모델의 답변을 기록에 추가 (이것이 맥락 유지의 핵심)
    history.append({"role": "assistant", "content": full_response})    
    

print("안녕하세요. 챗봇입니다. 하고싶은 말을 입력해주세요.")

while True:
    my_message = input("me : ")
    if my_message == "q":
        print("챗봇을 종료합니다.")
        break
    chat_with_memory(my_message)
    print()
```

- 이와 별개로 streamlit 라는 기능이 있는데, python 기반의 오픈소스 웹 애플리케이션 프레임워크라고 함.
- 데이터 사이언스 및 머신러닝 모델을 빠르게 배포하고 공유할 수 있도록 설계된 도구.
- 간단하게 대시보드 구성 가능.
- ai에게 streamlit를 활용해서 챗봇을 만들어달라고 하면 잘 만들어줌. 대충 이런 도구도 있다고 알아두자.

### OpenAI 비동기 처리

- 기존 비동기의 with ~~는 AsyncOpenAI에서 알아서 처리함.

```python
from openai import AsyncOpenAI
import asyncio

async_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def get_food_recommendation(city):
    print(f"[{city}] 맛집 검색 시작...")
    response = await async_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"{city}에 가면 꼭 먹어야 할 음식 딱 한 가지만 추천해줘."}]
    )
    print(f"[{city}] 검색 완료!")
    return f"{city}: {response.choices[0].message.content}"

async def main():
    cities = ["서울", "파리", "뉴욕", "도쿄", "방콕", "로마"]
    tasks = [get_food_recommendation(c) for c in cities]
    
    # 여러 요청을 동시에(병렬로) 처리
    results = await asyncio.gather(*tasks)
    
    print("\n--- [여행자들을 위한 미식 가이드] ---")
    for r in results:
        print(r)

await main()
```

## OpenAI Responses API

- https://platform.openai.com/docs/api-reference/responses
- OpenAI Responses API 사용해보기
- 초반 실행은 비슷함.
- 최근 모델만 사용 가능.

```python
import requests
from pprint import pprint
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
URL = "https://api.openai.com/v1/responses"
model = "gpt-4o-mini"
```

### Chat Completions vs Responses 차이점

- 1. 상태 유지 방식
    - Chat Completions는 매번 전체 대화 내역을 리스트로 묶어 보내야 하지만, Responses API는 previous_response_id를 통해 서버 측에서 이전 응답을 참조하는 상태 중심(Stateful) 상호작용을 지원한다.
- 2. 입력 파라미터
    - 기존의 messages 필드가 input 필드로 대체된다.
    - input은 단순 문자열이나 이미지, 파일 등 다양한 형태를 포함하는 배열로 구성될 수 있다.
- 3. 시스템 메시지
    - role: system 방식 대신 instructions라는 별도의 최상위 파라미터를 사용하여 모델의 페르소나와 지침을 설정한다.
- 4. 응답 구조
    - 결과 데이터가 choices 대신 output 배열에 담겨 반환된다.
- 5. 내장 도구
    - 별도의 세션 관리 없이도 웹 검색(Web Search), 파일 검색(File Search) 등의 도구를 더욱 직접적으로 활용할 수 있다.

### 라이브러리없이 HTTP 통신으로 사용

- message, roll, content 등 설정하는 부분이 간략화됨.
- 아래 코드에서 ‘messages’ 부분과 위의 ‘instructions’, ‘input’을 비교해보자.

```python
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}"
}

payload = {
    "model": model,
    "instructions": "당신은 친절한 AI 강사입니다.",
    "input": "Responses API가 뭐야? 2~3문장으로 답변해줘"
#    "messages": [
#        {"role": "system", "content": "당신은 친절한 AI 강사입니다."},
#        {"role": "user", "content": "Chat Completions API가 뭐야? 2~3문장으로 답변해줘"}
#    ]
}

response = requests.post(URL, headers=headers, json=payload)
res_data = response.json()
pprint(res_data)

if "output" in res_data:
    # output 배열 내부의 첫 번째 메시지 텍스트 추출
    content_text = res_data["output"][0]["content"][0]["text"]
    print(f"\n답변: {content_text}")
```

### OpenAI SDK 사용

- client.responses 리소스를 사용하여 효율적으로 응답 생성.
- 출력할 때도 choise[0].message.content 이렇게 귀찮게 안함.(아래 주석 처리 코드 비교)

```python
from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)

response = client.responses.create(
    model=model,
    input="OpenAI Responses API를 사용하면 어떤 점이 좋아?"
)

# SDK 전용 속성인 output_text를 사용하여 답변 확인
print(response.output_text)
#print(completion.choices[0].message.content)
```

### Instructions (System Prompt) 비교

- 기존의 system role 메시지 대신 instructions 파라미터에 지침을 입력.
- 위의 2가지 경우와 마찬가지로 message 부분과 출력 부분에서 차이점이 있음.

```python
user_input = "아침 일찍 일어나는 습관의 장점에 대해 말해줘."

personas = {
    "열정적인 셰프": "당신은 요리에 인생을 건 셰프입니다. 인생의 모든 이치를 요리 과정과 재료에 비유하여 설명하세요.",
    "엄격한 헬스 트레이너": "당신은 매우 엄격한 운동 전문가입니다. 강한 어조로 자기관리를 강조하며 답변하세요.",
    "지혜로운 판다": "당신은 대나무 숲에 사는 느긋하고 지혜로운 판다입니다. 느릿느릿하고 평화로운 말투로 조언을 건네세요."
}

for name, inst in personas.items():
    print(f"--- [{name}] 버전 ---")
    response = client.responses.create(
        model=model,
        instructions=inst,
        input=user_input
        # messages=[
        #     {"role": "system", "content": prompt},
        #     {"role": "user", "content": user_input}
        # ]
    )
    print(response.output_text)
#    print(response.choices[0].message.content)
    print("\n")
```

### input

- input에는 text뿐만 아니라 메시지 객체, 이미지, 파일 등이 들어갈 수 있다.
- 메시지 객체는 다음과 같은 형식을 가진다.
- https://platform.openai.com/docs/api-reference/responses/create#responses_create-input

```python
{
	'content' : 컨텐츠에 대한 text 또는 list,
	'role' : 'user' / 'assistant' / 'system' / 'developer' 중 하나가 들어감,
	'type' : 'message'
}
```

```python
response = client.responses.create(
    model=model,
    input=[
    {
        "type": "message",
        "role": "user",
        "content": [
            {"type": "input_text", "text": "이 사진에 대해 설명해줘."},
            {"type": "input_image", "image_url": "https://images.dog.ceo/breeds/shiba/shiba-8.jpg"}
        ]
    }
]
)

print(response.output_text)
```

### Temperature 비교

- 무작위성 조절하는 temperature 파라미터는 동일하게 사용 가능.
- 메시지 입력, 결과 출력 이외엔 동일

```python
creative_topic = "운동화 브랜드의 새로운 슬로건을 5개 제안해줘. 단, 기발하게 작성해줘."
temperatures = [0.3, 0.8, 1.0, 1.3, 1.5, 1.6, 1.8]

for t in temperatures:
    print(f"### 설정값 (Temperature): {t} ###")
    response = client.responses.create(
        model=model,
        input=creative_topic,
        temperature=t,
        max_output_tokens=200
    )
    print(response.output_text)
    print("=" * 50)
```

### previous_response_id를 활용한 대화 맥락 유지

- 과거 응답의 id를 전달하여 이전 대화 내용 자동으로 참조.
- id를 통해 기록 관리.
    - previous_response_id 속성을 사용해서 이전의 id를 계속 넘겨받는 방식으로 대화 내용 참고 가능.
    - Chat Completions 에서는 배열을 통해서 대화 내용을 기록하고 해당 기록에 새로운 대화 내용을 추가해서 전체 대화 내용을 매번 보내는 방식으로 대화 내용을 참고하도록 함.

```python

print("Q1: 내 이름은 jun이야.")
res1 = client.responses.create(
    model=model,
    instructions="당신은 사용자의 이름을 기억하는 비서입니다.",
    input="내 이름은 jun이야."
)
print(f"A1: {res1.output_text}\n")

response_id = res1.id
# 두 번째 대화 (이전 ID 전달)
print("Q2: 내 이름이 뭐라고?")
res2 = client.responses.create(
    model=model,
    input="내 이름이 뭐라고?",
    previous_response_id=response_id
)
print(f"A2: {res2.output_text}")
```

### Structured Outputs (JSON 형식 출력)

- text 파라미터의 format 설정을 통해 json 출력 강제.
    - Chat Completions에선 response_format 파라미터를 통해 형식 지정

```python
import json

response = client.responses.create(
    model=model,
    instructions="너는 요리사야. 답변은 반드시 JSON 형식으로 해줘.",
    input="떡볶이 레시피 알려줘. json형식으로 대답해줘.",
    text={
        "format": {"type": "json_object"}
    }
)

res_json = json.loads(response.output_text)
pprint(res_json)
```

### Streaming (실시간 응답 처리)

- streaming=True 설정을 통해 생성되는 즉시 데이터를 수신한다.
- 여기서 hasattr()은 chunk에 있는 .delta에 접근할 수 있는지 체크하는 함수. 이런 안전장치 없으면 에러가 나올 수도 있음.
    - 다른 방식으로 안전 장치를 마련해도 된다!

```python
prompt = "양자 역학에 대해 초등학생도 이해할 수 있게 설명해줘."
print(f"질문: {prompt}\n")
print("답변: ", end="")

stream = client.responses.create(
    model=model,
    input=prompt,
    stream=True
)

for chunk in stream:
    # 스트리밍 시 delta 이벤트를 통해 텍스트 조각을 수신함
    
    if hasattr(chunk, 'delta') and chunk.delta:
        print(chunk.delta, end="", flush=True)

print("\n\n--- 스트리밍 종료 ---")
```

### 비동기 요청

- AsyncOpenAI 사용.

```python
from openai import AsyncOpenAI
import asyncio

async_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def get_food(city):
    print(f"[{city}] 검색...")
    res = await async_client.responses.create(
        model=model,
        input=f"{city}에서 꼭 먹어야 할 음식 한 가지만 추천해줘."
    )
    return f"{city}: {res.output_text}"

async def main():
    cities = ["서울", "파리", "뉴욕", "도쿄", "방콕", "로마"]
    tasks = [get_food(c) for c in cities]
    results = await asyncio.gather(*tasks)
    for r in results:
        print(r)

await main()
```

### id를 활용한 추가 관리 기능( 조회, 삭제, 압축 )

- 생성된 응답을 id로 조회하거나 삭제하고, 긴 대화의 컨텍스트를 압축하는 기능을 제공.
- 응답 생성

```python

response = client.responses.create(
    model=model,
    input="안녕 반가워!"
)

response_id = response.id
print(response.output_text)
```

- 조회

```python
# 응답 조회

retrieved = client.responses.retrieve(response_id)

print(retrieved.output_text)
```

- 삭제

```python
# 응답 삭제
client.responses.delete(response_id)

try:
    # 응답이 삭제가 되서 retrieve할 수 없다.
    client.responses.retrieve(response_id)
except Exception as e:
    print(e)
```

- 압축

```python
# 대화 압축 (대화가 너무 길어질 때 사용)

result = client.responses.compact(
    model=model,
    previous_response_id = response_id
    )
print(result)
```

### 사용 토큰 확인하기

- .usage가 들어가면 토큰에 대한 정보!

```python

response = client.responses.create(
    model=model,
    input='llm에서 사용하는 토큰에 대해 설명해줘.'
)
print(response.output_text)
print("\n")

print(f"입력 토큰: {response.usage.input_tokens}") # 질문(Prompt)에 사용된 토큰
print(f"출력 토큰: {response.usage.output_tokens}") # 답변(Completion)에 사용된 토큰
print(f"합계 토큰: {response.usage.total_tokens}") # 전체 사용 토큰
```

### 요청 전 입력 토큰 확인하기 (tiktoken 사용)

- 나의 질문에 몇 개의 토큰이 사용되는지 확인하는 것이 가능!

```python
import tiktoken

def count_tokens(text, model="gpt-4o-mini"):
    # 모델에 맞는 인코딩 가져오기
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        # 모델명을 찾을 수 없을 때 기본값(o200k) 사용
        encoding = tiktoken.get_encoding("o200k_base")
    
    # 텍스트를 토큰으로 변환(encode)
    tokens = encoding.encode(text)
    
    # 토큰 개수 반환
    return len(tokens)

# 테스트
text = "안녕하세요, 이 문장의 토큰은 몇개일까요?"
print(f"텍스트: {text}")
print(f"토큰 수: {count_tokens(text)}개")
```

### 프롬프트 캐싱

- 프롬프트 캐싱은 자주 반복되는 프롬프트의 앞부분을 서버에 미리 저장해 두었다가, 동일한 요청이 들어오면 다시 계산하지 않고 즉시 재사용하는 기능.
- openai에서는 프롬프트 앞에 1024토큰 단위로 저장하며, 조금이라도 text가 달라지면 재사용하지 못한다.

```python
prompt = "대충 엄청 긴 무언가"

response = client.responses.create(
    model='gpt-4o',
    input=prompt.format(user_input="요약해줘")
)

print(response.usage)
# print(response.output_text)

```

### LLM에서의 도구 사용

- Responses API는 여러 내장 도구들을 가져, text생성 뿐만 아니라 외부 도구와 소통하여 여러 동작들을 할 수 있다.
- web_search, file_search 등 여러 내장 도구 활용 가능.

```python
# web_search tool을 활용하여 웹검색을 통해 실시간 정보에 접근이 가능하다.

response = client.responses.create(
    model=model,
    tools=[{"type": "web_search"}],
    input="오늘 뉴스 알려줘"
)

print(response.output_text)
```