### UI (User Interface) & UX (User Experience)

- **UI**: 사용자가 마주하는 **시각적인 요소** (버튼, 폰트, 레이아웃 등 눈에 보이는 디자인)
- **UX**: 제품이나 서비스를 이용하며 느끼는 **총체적인 경험을 설계**하는 것 (편의성, 만족도, 논리적 흐름 등)
    - 단순히 눈에 보이는 디자인을 넘어, 사용자가 목표를 달성하는 과정에서 겪는 **모든 상호작용과 감정, 피드백**을 분석하고 최적화한다.
- **관계**: UI는 UX를 구현하는 수단이며, 반응형/적응형 디자인은 다양한 환경에서 최적의 UX를 제공하기 위한 전략이다.

### 반응형 웹 디자인

- 하나의 웹사이트에서 PC, 스마트폰, 태블릿 PC 등 접속 디스플레이 종류에 따라 화면 크기가 자동 변경되는 웹페이지 접근 기법
- 웹사이트를 PC용과 모바일용으로 별개 제작하지 않고 하나의 공용 웹사이트로 다양한 디바이스 대응
- 기기에 상관없이 동일한 URL과 콘텐츠를 사용하여 일관된 경험 제공
- 예시
    - https://www.youtube.com/
    - https://github.com/

### 적응형 웹 디자인

- 서버에서 사용자 기기를 감지하고 다른 버전의 사이트를 제공하는 웹페이지 접근 기법
- 각 기기 유형에 최적화된 별도의 HTML/CSS 제공
- 모바일 전용 UI로 빠른 속도와 기기 특화 기능을 제공하는 데 유리함
- 예시
    - https://www.naver.com/ 와 https://m.naver.com/

### 모바일 퍼스트 (Mobile First)

- 제약이 많은 **모바일 UI를 먼저 설계**한 뒤, 큰 화면으로 확장해 나가는 방식
- 핵심 콘텐츠에 집중하게 하여 군더더기 없는 UX를 만드는 데 유리함

---

## 미디어 쿼리(Media Query)

- 화면 크기, 장치 특성에 따라 CSS 속성을 적용하는 문법
- 반응형 웹 디자인 구현에 사용되며 디바이스에 맞는 레이아웃 제공을 위한 필수 기술

### 기본 구조

```css
@media (조건) {
  /* 조건을 만족할 때 적용될 스타일 */
  선택자 {
    속성: 값;
  }
}

```

### 미디어 쿼리 조건

- `min-width` : 최소 너비 이상일 때
- `max-width` : 최대 너비 이하일 때
- `min-height` : 최소 높이 이상일 때
- `max-height` : 최대 높이 이하일 때
- `orientation` : 장치 방향
    - `landscape` : 가로 방향
    - `portrait` : 세로 방향

## 예제

### 너비 조건

- 너비가 768px 이상일 때 적용
    
    ```css
    @media (min-width: 768px) {
    }
    
    ```
    
- 너비가 767px 이하일 때 적용
    
    ```css
    @media (max-width: 767px) {
    }
    
    ```
    
- 너비가 768px 이상일 때와 767px 이하일 때 다른 스타일을 적용
    
    ```css
    @media (min-width: 768px) {
      /* 768px 이상일 때 적용될 스타일 */
    }
    
    @media (max-width: 767px) {
      /* 767px 이하일 때 적용될 스타일 */
    }
    
    ```
    

### 높이 조건

- 높이가 768px 이상일 때 적용
    
    ```css
    @media (min-height: 768px) {
    }
    
    ```
    
- 높이가 767px 이하일 때 적용
    
    ```css
    @media (max-height: 767px) {
    }
    
    ```
    
- 높이가 768px 이상일 때와 767px 이하일 때 다른 스타일을 적용
    
    ```css
    @media (min-height: 768px) {
      /* 768px 이상일 때 적용될 스타일 */
    }
    
    @media (max-height: 767px) {
      /* 767px 이하일 때 적용될 스타일 */
    }
    
    ```
    

### 장치 방향 조건

- 가로(landscape): 화면 너비가 높이보다 클 때
    
    ```css
    @media (orientation: landscape) {
    }
    
    ```
    
- 세로(portrait): 화면 높이가 너비보다 클 때
    
    ```css
    @media (orientation: portrait) {
    }
    
    ```
    

## Pseudo-class (가상 클래스)

- 요소의 **상태**에 따라 스타일을 적용하는 선택자
- `:hover` — 마우스를 올렸을 때 스타일 변경 가능
- `:focus` — 입력창을 클릭(포커스)했을 때 스타일 변경 가능
- `:active` — 요소를 클릭하고 있는 순간의 스타일
- `:nth-child()` — n번째 자식 요소만 골라서 스타일 적용 가능 (짝수, 홀수 등)

```css
.btn:hover {
  background-color: skyblue;
}
```

---

## Pseudo-element (가상 요소)

- 실제 HTML 태그 없이 **가상의 요소를 삽입**할 수 있는 기능
- `::before` — 요소 앞에 텍스트나 아이콘 등을 삽입
- `::after` — 요소 뒤에 텍스트나 아이콘 등을 삽입
- `::placeholder` — input의 placeholder 텍스트 스타일 변경 가능
- `content` 속성이 필수 (빈 문자열이라도 넣어야 함)

```css
.tag::before {
  content: "#";
  color: gray;
}
/* <span class="tag">CSS</span> → 화면에 "#CSS"로 표시됨 */
```

---

## Shadow (그림자)

- `box-shadow` — 요소(박스)에 그림자 효과
- `text-shadow` — 텍스트에 그림자 효과
- 카드 UI에 입체감을 줄 때, hover 시 그림자를 키워서 떠오르는 느낌을 줄 때 활용
- `box-shadow: x위치 y위치 흐림정도 퍼짐정도 색상;` 형태로 작성

```css
.card {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
```

---

## Transition (전환)

- CSS 속성 값이 변할 때 **즉시 바뀌지 않고 부드럽게 전환**되는 효과
- 예: 버튼에 마우스를 올리면 배경색이 0.3초에 걸쳐 서서히 변함
- `transition: 속성 시간 타이밍 지연시간;` 형태로 작성
- 시간 단위: `0.3s`(초), `500ms`(밀리초)
- 타이밍: `ease`(기본, 천천히→빠르게→천천히), `linear`(일정 속도), `ease-in-out` 등

```css
.box {
  background-color: skyblue;
  transition: background-color 0.3s;
}

.box:hover {
  background-color: tomato;
}
```

---

## Transform (변형)

- 요소를 **이동, 회전, 확대/축소, 기울이기** 할 수 있는 속성
- 다른 요소의 레이아웃에 영향을 주지 않음 (자기 자리 유지하면서 변형)
- `translate(x, y)` — 이동
- `rotate(45deg)` — 회전
- `scale(1.5)` — 확대/축소
- `skew(10deg)` — 기울이기
- Transition과 함께 사용하면 마우스 올렸을 때 카드가 살짝 떠오르는 등의 효과 구현 가능

```css
.card:hover {
  transform: translateY(-5px);
}
```

---

## Animation (애니메이션)

- `@keyframes`로 **여러 단계의 애니메이션**을 정의하는 기능
- Transition은 A→B (2단계)만 가능하지만, Animation은 A→B→C→... 여러 단계 가능
- 반복 재생, 역방향 재생, 무한 반복 등 세밀한 제어 가능
- 로딩 스피너, 바운스 효과, 깜빡이는 텍스트 등에 활용

```css
@keyframes bounce {
  0%   { transform: translateY(0); }
  50%  { transform: translateY(-20px); }
  100% { transform: translateY(0); }
}

.ball {
  animation: bounce 1s ease infinite;
}
```

---

## CSS 변수 (Custom Properties)

- `-변수이름`으로 정의하고 `var(--변수이름)`으로 사용하는 사용자 정의 변수
- 색상, 크기 등 자주 쓰는 값을 한 곳에서 관리 가능
- 값을 바꾸면 사용하는 곳이 전부 한꺼번에 변경됨
- 다크모드/라이트모드 테마 전환에 많이 활용됨

```css
:root {
  --main-color: #3498db;
}

.card {
  background-color: var(--main-color);
}
```

---

## CSS 함수

- `calc()` — CSS 안에서 사칙연산 가능 (예: `width: calc(100% - 200px)`)
- `min()` / `max()` — 여러 값 중 최솟값/최댓값 선택
- `clamp(최소, 기본, 최대)` — 최소~최대 범위 안에서 반응형으로 값 조절 (글씨 크기 등에 유용)

---

## CSS Grid

- Flexbox와 함께 CSS의 핵심 레이아웃 시스템
- Flexbox는 **1차원** (가로 또는 세로 한 방향), Grid는 **2차원** (가로 + 세로 동시 제어)
- 행(row)과 열(column)을 동시에 정의하여 격자 형태의 레이아웃을 쉽게 구성
- 갤러리, 대시보드 등 바둑판 형태의 레이아웃에 적합
- [Grid Garden (Grid 게임)](https://cssgridgarden.com/#ko)

```css
.container {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr; /* 3열 균등 분할 */
  gap: 16px;
}
```

---

## Reset CSS & Normalize CSS

- 브라우저마다 기본적으로 설정된 **기본 스타일(여백, 폰트 크기 등)의 차이를 없애는** 작업
- 모든 브라우저에서 동일한 디자인을 보여주기 위해 스타일을 초기화하거나 보정함
- 보통 프로젝트의 가장 처음에 적용하는 CSS 파일
- Reset CSS
    - 브라우저의 기본 스타일을 **0(Zero)**으로 완전히 초기화하여 백지 상태에서 시작
    - 모든 요소를 직접 디자인해야 함
- Normalize.css
    - 무조건 지우는 대신, **브라우저 간의 오차를 줄이고 버그를 수정**하는 방식
    - 최근 현대적인 웹 개발에서 더 많이 선호되는 방식

---

## BEM (Block Element Modifier)

- CSS 클래스 이름을 짓는 **네이밍 컨벤션** (규칙)
- `block__element--modifier` 형태로 작성
- Block — 독립적인 컴포넌트 (예: `card`)
- Element — Block의 하위 요소, `__`로 연결 (예: `card__title`)
- Modifier — 변형/상태, `-`로 연결 (예: `card__title--active`)
- 클래스 이름만 보고 구조와 역할을 파악할 수 있어 협업에 유리

```html
<div class="card">
  <h2 class="card__title">제목</h2>
  <p class="card__desc">설명</p>
  <button class="card__btn card__btn--primary">확인</button>
</div>
```

---

## Sass/SCSS

- CSS를 더 편리하게 작성할 수 있게 해주는 **CSS 전처리기(Preprocessor)**
- `.scss` 파일로 작성하면 빌드 시 `.css` 파일로 변환됨
- 변수, 중첩(nesting), mixin, 조건문/반복문 등 프로그래밍적 기능 지원
- 현재는 CSS 변수와 기능이 많이 겹쳐서 사용 빈도가 줄어드는 추세이지만, 기존 프로젝트에서 여전히 많이 사용됨

```scss
/* 변수 */
$main-color: #3498db;

/* 중첩 (nesting) */
.card {
  background-color: $main-color;

  &__title {
    font-size: 20px;
  }

  &:hover {
    background-color: darken($main-color, 10%);
  }
}
```

---

## CSS-in-JS (Styled Components)

- JavaScript 코드 안에서 CSS를 직접 작성하는 방식
- React 환경에서 많이 사용됨
- 컴포넌트 단위로 스타일이 자동으로 격리되어 클래스 이름 충돌이 없음
- 순수 CSS 파일을 따로 만들지 않아도 됨
- 대표 라이브러리: **Styled Components**, **Emotion**