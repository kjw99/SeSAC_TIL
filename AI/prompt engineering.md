# 프롬프트 엔지니어링

프롬프트 엔지니어링은 대규모 언어 모델이 사용자의 의도를 정확히 파악하고 최적의 결과물을 생성하도록 입력을 설계하고 최적화하는 기술이자 과학이다.

이는 단순한 질문을 넘어, AI에게 문맥, 지침, 예시를 제공하여 원하는 결과물로 유도하는 과정이다.

효과적인 프롬프트를 구성하기 위해서는 모델이 사용자의 의도를 정확히 파악하고 고품질의 결과를 생성할 수 있도록 명확한 구조를 갖추는 것이 중요하다.

### 핵심 구성 요소

- **지시** — 모델이 수행해야 할 구체적인 작업이나 명령이다. "요약하라", "분류하라", "번역하라"와 같이 명확한 동사를 사용하여 모델이 무엇을 해야 하는지 정의하며, 지시는 모호함을 피하고 구체적일수록 좋다.
- **문맥** — 모델이 더 나은 응답을 생성하도록 유도하는 배경 정보나 외부 상황이다. 모델이 상황을 추측하게 하지 말고, "이 작업은 초보자를 위한 것이다"라거나 "첨부된 재무 보고서를 바탕으로 분석하라"와 같이 필요한 정보를 충분히 제공해야 한다.
- **입력 데이터** — 모델이 처리해야 할 실제 내용이다. 요약해야 할 텍스트, 번역할 문장, 답변해야 할 질문 등이 이에 해당한다. 입력 데이터는 프롬프트 내에서 XML 태그나 특수 기호 등을 사용해 지시 사항과 명확히 구분해 주는 것이 좋다.
- **출력 지시자** — 응답의 형식이나 유형을 지정하는 요소이다. "JSON 형식으로 출력해라", "표로 만들어라", "불렛 포인트를 사용해라"와 같이 원하는 결과물의 형태를 명시한다.

### 성능 향상을 위한 추가 요소

- **역할 및 정체성** — AI에게 "당신은 노련한 데이터 과학자입니다"와 같은 페르소나를 부여한다. 이를 통해 모델의 어조, 관점, 스타일을 조정하고 특정 도메인의 전문적인 답변을 유도할 수 있다.
- **예시** — 원하는 입력과 출력의 쌍을 제공하여 모델이 패턴을 학습하게 하는 기법이다. 설명보다 예시가 더 효과적인 경우가 많다.
- **제약 사항** — 모델이 하지 말아야 할 것(부정적 제약)이나 반드시 지켜야 할 규칙(긍정적 제약)을 설정한다. 예를 들어 "전문 용어를 쓰지 마라", "500단어 이내로 작성해라" 등이 있다.
- **구조화 태그** — 프롬프트의 각 부분(지시, 문맥, 예시 등)을 명확히 구분하기 위해 XML 태그(`<context>`, `<instruction>`)나 마크다운 헤더(`#`)를 사용한다.

---

# 핵심 프롬프트 기법

## 1. 제로샷 vs 퓨샷 프롬프팅

- **제로샷 프롬프팅** — 추가적인 예시 없이 모델에게 직접적인 지시나 질문만 제공하는 방식이다.
- **퓨샷 프롬프팅** — 모델이 패턴을 학습할 수 있도록 원하는 입력-출력 예시를 하나 이상 제공하는 기법이다.

퓨샷의 원칙:

- **다양성**: 엣지 케이스를 포함하여 다양한 예시를 제공하면 의도치 않은 패턴 학습을 방지할 수 있다.
- **일관된 형식**: 예시 간의 구조와 형식을 통일해야 모델이 혼란을 겪지 않는다.

```sql
# 제로샷: 예시 없이 바로 질문
prompt_zero = ChatPromptTemplate.from_messages([
    ("human", "다음 문장의 감정을 '긍정', '부정', '중립' 중 하나로 분류해: {sentence}"),
])

chain = prompt_zero | llm | parser
print("=== 제로샷 ===")
print(chain.invoke({"sentence": "이 영화 진짜 재밌었어"}))
```

```sql
# 퓨샷: 예시를 제공하여 패턴 학습
prompt_few = ChatPromptTemplate.from_messages([
    ("system", "사용자의 문장을 '긍정', '부정', '중립' 중 하나로 분류해."),
    ("human", "배송이 정말 빠르고 포장도 깔끔해요"),
    ("ai", "긍정"),
    ("human", "제품이 설명과 달라서 실망했습니다"),
    ("ai", "부정"),
    ("human", "보통이에요. 그냥 쓸만합니다"),
    ("ai", "중립"),
    ("human", "{sentence}"),
])
# for i in prompt_few.messages:
#     print(type(i))

chain = prompt_few | llm | parser
print("=== 퓨샷 ===")
print(chain.invoke({"sentence": "이 영화 진짜 재밌었어"}))
```

같은 감정 분류 태스크지만, 퓨샷은 예시를 통해 "한 단어로만 답하라"는 패턴까지 학습시킨다.

제로샷은 장황한 설명이 붙을 수 있지만, 퓨샷은 예시의 형식을 따라 간결하게 답한다.

퓨샷의 핵심은 **예시의 패턴이 일관되어야** 한다는 것이다.

---

## 2. 역할 부여 (Role Prompting)

AI에게 특정 캐릭터나 직업적 역할을 부여하여 응답의 어조, 관점, 스타일을 조정하는 기법이다.

시스템 프롬프트에 역할을 설정하면, 모델은 해당 도메인의 전문적인 관점을 채택하여 더 깊이 있는 답변을 제공한다.
역할을 구체적으로 설정할수록 답변의 전문성과 일관성이 높아진다.

```sql
# 역할 없이 질문
question = "우리 회사의 레거시 시스템을 지금 리팩토링해야 할까?"

prompt_no_role = ChatPromptTemplate.from_messages([
    ("human", question),
])

chain = prompt_no_role | llm | parser
print("=== 역할 없음 ===")
print(chain.invoke({}))
```

```sql
# 같은 질문, 다른 역할 3개 비교
roles = {
    "CEO": "너는 시리즈B 스타트업 CEO야. 다음 분기 매출 목표가 급하고, 투자자 미팅이 잡혀 있어. 경영 관점에서 답해.",
    "CTO": "너는 이 시스템을 5년째 유지보수하고 있는 CTO야. 기술 부채가 쌓여서 신규 기능 개발 속도가 계속 느려지고 있어. 기술 관점에서 답해.",
    "현직 개발자": "너는 이 레거시 코드를 매일 다루는 3년차 개발자야. 버그 수정할 때마다 다른 곳이 터지고, 테스트도 없어. 솔직하게 답해.",
}

for role_name, role_desc in roles.items():
    prompt = ChatPromptTemplate.from_messages([
        ("system", role_desc),
        ("human", question),
    ])
    chain = prompt | llm | parser
    print(f"=== {role_name} ===")
    print(chain.invoke({}))
    print()
```

같은 질문이라도 역할에 따라 **결론 자체가 달라진다.**

| 역할 | 입장 | 핵심 근거 |
| --- | --- | --- |
| CEO | 지금은 안 돼 | 매출 목표, 투자자 일정, 리소스 부족 |
| CTO | 지금 해야 해 | 기술 부채 누적, 개발 속도 저하, 장기 비용 |
| 개발자 | 제발 해줘 | 매일 고통, 버그 연쇄, 테스트 부재 |

역할을 구체적으로 설정할수록 (상황, 맥락, 이해관계 등) 모델이 해당 입장에 몰입하여 현실적인 답변을 생성한다.

---

# 프롬프트 구조화 및 제어

## 3. 출력 형식 지정

원하는 결과물의 형식을 구체적으로 명시하면 파싱하기 쉽고 일관된 결과를 얻을 수 있다.

- "표로 만들어라", "JSON 형식으로 출력해라"와 같이 명확한 지시를 포함한다.
- "하지 마라"보다는 "하라"는 긍정적 지시가 더 효과적이다.

```sql
# 형식 미지정
prompt_no_format = ChatPromptTemplate.from_messages([
    ("human", "Python, JavaScript, Go를 비교해줘"),
])

chain = prompt_no_format | llm | parser
print("=== 형식 미지정 ===")
print(chain.invoke({}))
```

```sql
# 형식 지정: 표로 출력
prompt_table = ChatPromptTemplate.from_messages([
    ("system", "답변을 마크다운 표 형식으로 작성해. "
               "열은 '언어', '장점', '단점', '주요 사용처'로 구성해."),
    ("human", "Python, JavaScript, Go를 비교해줘"),
])

chain = prompt_table | llm | parser
print("=== 표 형식 ===")
print(chain.invoke({}))
```

```sql
# 형식 지정: JSON으로 출력
prompt_json = ChatPromptTemplate.from_messages([
    ("system", """답변을 아래 JSON 형식으로만 작성해. 추가 설명 없이 JSON만 출력해.

[{{
  "language": "언어명",
  "pros": ["장점1", "장점2"],
  "cons": ["단점1", "단점2"],
  "use_cases": ["사용처1", "사용처2"]
}}]"""),
    ("human", "Python, JavaScript, Go를 비교해줘"),
])

chain = prompt_json | llm | parser
result = chain.invoke({})
print("=== JSON 형식 ===")
print(result)
```

```sql
import json

data = json.loads(result)
for lang in data:
    print(f"{lang['language']}: {', '.join(lang['pros'])}")
```

> **참고:** 프롬프트로 "JSON으로 줘"라고 하면 가끔 형식이 깨질 수 있다. LangChain에서는 `llm.with_structured_output()`을 사용하면 LLM 응답을 Pydantic 객체로 바로 받을 수 있다.

```sql
# 제약 없음
prompt_no_constraint = ChatPromptTemplate.from_messages([
    ("human", "건강하게 오래 사는 방법을 알려줘"),
])

chain = prompt_no_constraint | llm | parser
print("=== 제약 없음 ===")
print(chain.invoke({}))
```

```sql
# 제약 조건 적용
prompt_constrained = ChatPromptTemplate.from_messages([
    ("system", """다음 규칙을 반드시 지켜:
- 3문장 이내로 답변해
- 각 문장 앞에 번호를 붙여
- 마크다운 볼드(**) 없이 plain text로만 써
- '~입니다', '~합니다' 대신 '~이다', '~한다' 체를 써
- 추상적인 조언 대신 구체적인 수치나 행동을 포함해"""),
    ("human", "건강하게 오래 사는 방법을 알려줘"),
])

chain = prompt_constrained | llm | parser
print("=== 제약 조건 적용 ===")
print(chain.invoke({}))
```

---

## 5. 구조화 태그 (XML 태그) 활용

프롬프트 내의 지시사항, 문맥, 예시를 명확히 구분하기 위해 XML 태그를 사용한다.

모델이 프롬프트의 각 부분을 명확하게 파싱하도록 도와 환각을 줄이고 정확도를 높인다.
특히 사용자 입력을 그대로 프롬프트에 넣을 때, 프롬프트 인젝션을 방지하는 효과도 있다.

```sql
prompt_xml = ChatPromptTemplate.from_messages([
    ("system", """아래 <article> 태그 안의 글을 분석해서 다음을 추출해:
1. 핵심 주제 (한 줄)
2. 키워드 3개
3. 한 줄 요약

<article> 태그 밖의 내용은 무시해."""),
    ("human", """<article>
{article}
</article>"""),
])

chain = prompt_xml | llm | parser

article = """최근 AI 기술의 발전으로 소프트웨어 개발 방식이 크게 변화하고 있다.
GitHub Copilot, Cursor 같은 AI 코딩 도구가 보편화되면서
개발자의 역할이 코드 작성에서 코드 검증과 설계로 이동하고 있다.
특히 프롬프트 엔지니어링 능력이 새로운 핵심 역량으로 부상하고 있다."""

print(chain.invoke({"article": article}))
```

---

# 고급 전략 및 최적화

---

## 8. 연쇄적 사고 (Chain of Thought)

복잡한 추론이 필요한 작업에서 모델에게 단계별로 생각하라고 지시하여 논리적 오류를 줄이는 기법이다.

- **기본 CoT** — 프롬프트에 "단계별로 생각하라"는 문구를 추가한다.
- **구조화된 CoT** — 모델이 추론 과정과 최종 답변을 분리하도록 유도한다. 예를 들어, `<thinking>` 태그 안에서 먼저 추론하고 `<answer>` 태그에 답을 내놓게 한다.

수학 문제, 논리적 분석, 복잡한 문서 작성 시 정확도와 일관성이 향상되며, 모델의 사고 과정을 통해 디버깅이 용이해진다.

```sql
# 바로 답하게 하기
prompt_direct = ChatPromptTemplate.from_messages([
    ("human", "가게에 사과가 23개 있었다. 11개를 팔고, 새로 6개를 들여왔다. "
             "다음 날 8개를 더 팔았다. 남은 사과는 몇 개인가?"),
])

chain = prompt_direct | llm | parser
print("=== 바로 답하기 ===")
print(chain.invoke({}))
```

```sql
# 기본 CoT: 단계별 사고 유도
prompt_cot = ChatPromptTemplate.from_messages([
    ("system", "문제를 단계별로 풀어. 각 단계를 명시하고, 마지막에 최종 답을 써."),
    ("human", "가게에 사과가 23개 있었다. 11개를 팔고, 새로 6개를 들여왔다. "
             "다음 날 8개를 더 팔았다. 남은 사과는 몇 개인가?"),
])

chain = prompt_cot | llm | parser
print("=== 기본 CoT ===")
print(chain.invoke({}))
```

```sql
# 구조화된 CoT: 추론과 답변 분리
prompt_structured_cot = ChatPromptTemplate.from_messages([
    ("system", """문제를 풀 때 다음 형식을 따라:

<thinking>
여기서 단계별로 추론한다
</thinking>

<answer>
최종 답만 간결하게 쓴다
</answer>"""),
    ("human", "회사에 직원이 150명 있다. 1분기에 20% 늘었고, "
             "2분기에 15명이 퇴사했다. 현재 직원 수는?"),
])

chain = prompt_structured_cot | llm | parser
print("=== 구조화된 CoT ===")
print(chain.invoke({}))
```

> **참고: 최신 모델의 내장 CoT**
> 
> 
> 최근 출시된 모델들은 CoT가 내장되어 있어 별도 지시 없이도 내부적으로 단계별 추론을 수행한다.
> 
> | 모델 | 기능 |
> | --- | --- |
> | OpenAI `o1`, `o3` | 추론 전용 모델, 내부 추론 후 답변 생성 |
> | OpenAI `GPT-5` | o3 수준의 추론이 기본 모델에 통합 |
> | Anthropic Claude `extended thinking` | 사고 과정을 명시적으로 출력 |
> | Google Gemini `thinking mode` | 내부 추론 체인 활용 |
> 
> "reasoning", "thinking", "CoT" 모두 본질은 같다 — 답변 전에 내부적으로 단계별 사고를 거치는 것이며, 벤더마다 부르는 이름만 다르다.
> 
> 다만 `gpt-4o-mini` 같은 기본 모델에서는 여전히 CoT 프롬프팅이 유효하다. 추론 특화 모델은 비용이 높으므로, 간단한 작업에서는 기본 모델 + CoT 프롬프팅이 더 효율적일 수도 있다.
> 

## 7. 프롬프트 체이닝

복잡한 작업을 한 번에 처리하려 하지 말고, 여러 개의 하위 작업으로 나누어 순차적으로 처리하는 기법이다.

각 단계의 출력을 다음 단계의 입력으로 사용한다.

```
문서 분석 → 요점 추출 → 요약 작성 → 번역
```

각 단계에 모델이 온전히 집중할 수 있어 정확도가 높아지고, 오류 발생 시 원인을 파악하기 쉽다.

```python
# 프롬프트 체이닝: 2단계로 나누어 처리

# 1단계: 주요 주제 추출
prompt_step1 = ChatPromptTemplate.from_messages([
    ("system", "주어진 텍스트에서 주요 주제 3개를 번호 목록으로 추출해."),
    ("human", "{text}"),
])

# 2단계: 추출된 주제로 요약 작성
prompt_step2 = ChatPromptTemplate.from_messages([
    ("system", "아래 주제들을 바탕으로 3줄 요약문을 작성해."),
    ("human", "{topics}"),
])

text = """인공지능 기술이 의료 분야에서 혁신을 일으키고 있다.
딥러닝 기반 영상 진단 시스템은 X-ray와 CT 스캔에서 종양을 99% 정확도로 감지한다.
자연어 처리 기술은 환자 차트를 자동으로 분석하여 의사의 업무 부담을 줄여준다.
신약 개발에서는 AI가 후보 물질 탐색 시간을 수년에서 수개월로 단축시켰다.
다만 의료 AI의 판단에 대한 책임 소재, 환자 데이터 프라이버시 등
해결해야 할 윤리적 과제도 남아 있다."""

# 1단계 실행
chain1 = prompt_step1 | llm | parser
topics = chain1.invoke({"text": text})
print("=== 1단계: 주제 추출 ===")
print(topics)

# 2단계 실행 (1단계 결과를 입력으로)
chain2 = prompt_step2 | llm | parser
summary = chain2.invoke({"topics": topics})
print("\n=== 2단계: 요약 ===")
print(summary)
```

---

## 9. 모델 파라미터 조정 (Temperature)

API를 사용할 경우, 파라미터 조정을 통해 결과의 다양성을 제어할 수 있다.

| 파라미터 | 낮은 값 | 높은 값 |
| --- | --- | --- |
| temperature | 결정론적, 일관된 답변 | 창의적, 다양한 답변 |
| top_p | 높은 확률 토큰만 선택 | 더 다양한 토큰 후보 |

```python
prompt = ChatPromptTemplate.from_messages([
    ("human", "'사랑'을 주제로 시 한 줄을 써줘"),
])

# temperature=0: 매번 같은 결과
llm_cold = ChatOpenAI(model="gpt-4o-mini", temperature=0)
chain_cold = prompt | llm_cold | parser

print("=== temperature=0 (3번 실행) ===")
for i in range(3):
    print(f"  {i+1}: {chain_cold.invoke({})}")

# temperature=1: 매번 다른 결과
llm_hot = ChatOpenAI(model="gpt-4o-mini", temperature=1)
chain_hot = prompt | llm_hot | parser

print("\n=== temperature=1 (3번 실행) ===")
for i in range(3):
    print(f"  {i+1}: {chain_hot.invoke({})}")
```

---

## 11. 긴 컨텍스트 처리

대량의 문서를 처리할 때는 데이터의 위치가 중요하다.

- 긴 문서나 데이터 같은 참조 자료를 프롬프트의 **상단에 배치**하고, 그 뒤에 지시사항과 질문을 배치하면 성능이 향상된다.
- 이는 모델이 문맥을 먼저 파악한 후 지시를 수행하기 때문이다.

```
좋은 구조:  [참조 문서] → [지시사항] → [질문]
나쁜 구조:  [질문] → [참조 문서] (문서가 길면 질문을 잊을 수 있음)
```

### 실전 팁 요약

- **명확하고 구체적으로** — 모호한 표현을 피하고, 정확한 동사와 수치를 사용한다 (예: "짧게 써라" → "500단어 내외로 써라")
- **맥락 제공** — 모델이 추측하지 않도록 필요한 배경 정보, 용어 정의, 참조 문서를 충분히 제공한다
- **반복과 실험** — 처음부터 완벽한 프롬프트는 존재하지 않는다. 결과를 보며 단어를 바꾸거나 정보를 추가/삭제하며 최적화한다
- **복잡한 작업 분해** — 작업이 너무 복잡하면 단계별 지시로 나누거나 프롬프트 체이닝을 고려한다
- **보안 및 안전** — 편향되거나 유해한 콘텐츠 생성을 방지하기 위해 프롬프트 내에서 제약 조건을 명확히 설정한다

이 기법들은 LangChain뿐 아니라 어떤 LLM API를 쓰더라도 동일하게 적용된다.