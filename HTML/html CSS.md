## CSS(Cascading Style Sheets)

- 웹 페이지의 **스타일을 정의**하는 스타일 시트 언어

### HTML과 CSS

- **HTML** : 웹 페이지의 구조와 내용을 정의
- **CSS** : 웹 페이지의 스타일을 정의
    
    ```html
    <!-- HTML만 사용한 경우 -->
    <!-- 웹 페이지의 구조와 내용을 정의 -->
    <h1>웹사이트 제목</h1>
    <p>이것은 기본 텍스트입니다.</p>
    
    <!-- CSS를 적용한 경우 -->
    <!-- 웹 페이지의 디자인과 스타일을 정의 -->
    <h1 style="color: blue; font-size: 32px;">웹사이트 제목</h1>
    <p style="color: gray; font-size: 16px;">
      이것은 스타일이 적용된 텍스트입니다.
    </p>
    ```
    

---

## CSS 기본 구조

- **선택자**, **속성**, **값**으로 구성된다

```css
선택자 {
  속성: 값;
}
```

### 선택자(Selector)

- 스타일을 적용할 HTML 요소를 선택한다

```css
/* h1 태그를 선택 */
h1 {
}

/* class가 "title"인 요소를 선택 */
.title {
}

/* id가 "header"인 요소를 선택 */
#header {
}
```

### 속성(Property)과 값(Value)

- 속성 : 스타일(글자 색, 크기, 너비, 높이 등)의 종류
- 값 : 스타일의 구체적인 값

```css
p {
  color: red; /* 빨간색 */
  font-size: 16px; /* 16픽셀 크기 */
  background-color: yellow; /* 노란색 배경 */
}
```

### CSS 작성 규칙

- 속성과 값은 `:` 으로 구분한다
- 각 선언은 `;` 으로 끝낸다
- 선언들은 `{}` 로 감싼다

---

## CSS 적용 방법

### 인라인 스타일(Inline Style)

- HTML 요소의 `style` 속성에 직접 CSS를 작성하는 방법
- 해당 요소에만 스타일이 적용된다
    
    ```html
    <p style="color: blue; font-size: 20px;">
      이 텍스트는 파란색이며, 크기는 20px입니다.
    </p>
    ```
    

### 내부 스타일 시트(Internal Style Sheet)

- HTML 문서의 `<head>` 내부에 `<style>` 태그를 사용하여 CSS 코드를 작성하는 방법
    
    ```html
    <!DOCTYPE html>
    <html lang="ko">
      <head>
        <style>
          h1 {
            color: blue;
            text-align: center;
          }
    
          p {
            color: gray;
            font-size: 16px;
          }
        </style>
      </head>
      <body>
        <h1>웹사이트 제목</h1>
        <p>이것은 스타일이 적용된 문단입니다.</p>
      </body>
    </html>
    
    ```
    

### 외부 스타일 시트(External Style Sheet)

- 외부 CSS 파일을 만들어 HTML 문서에 연결하는 방법
1. 외부 CSS 파일 작성
    
    ```css
    /* styles.css 파일 */
    h1 {
      color: blue;
      text-align: center;
    }
    
    p {
      color: gray;
      font-size: 16px;
      line-height: 1.5;
    }
    
    .highlight {
      background-color: yellow;
      padding: 5px;
    }
    
    ```
    
2. HTML 문서에서 외부 CSS 불러오기
    
    ```html
    <!DOCTYPE html>
    <html lang="ko">
      <head>
        <link rel="stylesheet" href="styles.css" />
      </head>
      <body>
        <h1>웹사이트 제목</h1>
        <p>이것은 외부 CSS가 적용된 문단입니다.</p>
        <p class="highlight">이것은 강조된 문단입니다.</p>
      </body>
    </html>
    
    ```
    

---

## 브라우저 개발자 도구

- 웹 브라우저의 개발자 도구를 사용하여 CSS를 확인하고 수정할 수 있다

### 개발자 도구 열기

- **Windows/Linux** : `F12` 키 또는 `Ctrl + Shift + I`
- **Mac** : `Cmd + Option + I`
- **마우스** : 웹 페이지에서 우클릭 → "검사" 또는 "요소 검사"

### 주요 기능

**Elements(요소) 메뉴**

- HTML 구조를 확인할 수 있다
- 요소를 선택하여 해당 요소의 CSS를 확인할 수 있다

**Styles(스타일) 패널**

- 선택된 요소에 적용된 CSS 규칙을 확인할 수 있다
- 실시간으로 CSS 값을 수정하여 결과를 미리 볼 수 있다
- 체크박스를 해제하여 특정 스타일을 임시로 비활성화할 수 있다

**Computed(계산된 스타일) 패널**

- 요소에 최종적으로 적용된 모든 CSS 값을 확인할 수 있다
- 상속받은 스타일과 직접 적용된 스타일을 구분하여 볼 수 있다

# CSS 선택자(Selector)

## 선택자

- 스타일을 적용할 HTML 요소를 선택하는 방법
- 태그(tag), 클래스(class), 아이디(id) 등으로 요소를 선택한다

## 기본 선택자

### 전체 선택자(Universal Selector)

- 문서 내 모든 요소 선택
    
    ```css
    * {
      속성: 값;
    }
    ```
    
- 모든 요소에 공통된 스타일을 적용할 때 활용한다
- 활용 예시
    
    ```css
    * {
      /* 모든 요소의 글자를 빨간색으로 만들기 */
      color: red;
    }
    ```
    

### 태그 선택자(Type Selector)

- 특정 태그의 모든 요소를 선택
- `태그명` 형태로 작성한다
    
    ```css
    태그명 {
      속성: 값;
    }
    ```
    
- 활용 예시
    
    ```css
    /* 모든 p 태그의 글자를 파란색으로 만들기 */
    p {
      color: blue;
    }
    
    /* 모든 h1 태그의 글자를 크고 굵게 만들기 */
    h1 {
      font-size: 32px;
      font-weight: bold;
    }
    ```
    

### 클래스 선택자(Class Selector)

- 특정 클래스의 모든 요소를 선택
- 여러 요소에 같은 클래스를 사용할 수 있다
- 하나의 요소에 여러 클래스를 사용할 수 있다
- 재사용성이 높다
- `.클래스명` 형태로 작성한다
    
    ```css
    .클래스명 {
      속성: 값;
    }
    ```
    
- HTML 문서에서 클래스 작성
    
    ```html
    <p class="highlight">강조된 문단</p>
    <div class="highlight">강조된 영역</div>
    ```
    
- CSS 문서에서 클래스 선택자 작성
    
    ```css
    .highlight {
      /* 클래스가 highlight인 요소의 배경을 노란색으로 만들기 */
      background-color: yellow;
      font-weight: bold;
    }
    ```
    
- 활용 예시
    
    ```html
    <!-- 2개의 클래스가 적용된 버튼 요소 -->
    <button class="button warning">버튼</button>
    ```
    
    ```css
    /* 버튼 스타일 */
    .button {
      padding: 10px 20px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
    }
    
    /* 경고 메시지 스타일 */
    .warning {
      color: red;
      font-weight: bold;
      border: 1px solid red;
    }
    ```
    

### 아이디 선택자(ID Selector)

- 고유한 id 속성을 가진 요소 하나를 선택
- 문서에서 유일한 요소를 선택할 때 사용한다
- `#아이디명` 형태로 작성한다
    
    ```css
    #아이디명 {
      속성: 값;
    }
    ```
    
- HTML 문서에서 id 작성
    
    ```html
    <header id="main-header">메인 헤더</header>
    ```
    
- CSS 문서에서 id 선택자 작성
    
    ```css
    #main-header {
      background-color: navy;
      color: white;
      padding: 20px;
    }
    ```
    
- 활용 예시
    
    ```html
    <header id="main-header">메인 헤더</header>
    ```
    
    ```css
    #main-header {
      background-color: navy;
      color: white;
      padding: 20px;
    }
    ```
    

### 속성 선택자(Attribute Selector)

- 특정 속성을 가진 요소를 선택
- `[속성명]` 형태로 작성한다
    
    ```css
    [속성명] {
      속성: 값;
    }
    ```
    
- 활용 예시
    
    ```html
    <input type="text" />
    <input type="password" placeholder="비밀번호" />
    <input type="email" placeholder="이메일" />
    ```
    
    ```css
    [type="text"] {
      color: red;
    }
    
    [placeholder] {
      color: blue;
    }
    ```
    

---

## 결합자

- HTML 요소들 간의 관계를 기반으로 요소를 선택하는 방법

### 자식 결합자

- 특정 부모 요소의 바로 아래 자식 요소만 선택
- **`부모선택자 > 자식선택자`** 형태로 작성한다
    
    ```css
    부모선택자 > 자식선택자 {
      속성: 값;
    }
    ```
    
- 활용 예시
    
    ```html
    <div>
      <p>이것은 div의 자식 p입니다.</p>
      <span>
        <p>이것은 div의 손자 p입니다.</p>
      </span>
    </div>
    ```
    
    ```css
    div > p {
      color: red;
      font-weight: bold;
    }
    ```
    

### 자손 결합자

- 특정 부모 요소 안에 있는 모든 하위 요소를 선택
- `부모선택자 후손선택자` 형태로 작성한다
    
    ```css
    부모선택자 후손선택자 {
      속성: 값;
    }
    ```
    
- 활용 예시
    
    ```html
    <div>
      <p>이것은 div의 자손 p입니다.</p>
      <span>
        <p>이것은 div의 자손 p입니다.</p>
      </span>
    </div>
    ```
    
    ```css
    div p {
      color: blue;
      font-style: italic;
    }
    
    ```
    

- 그 외에도
    - 일반 형제 결합자 (`~`)
        
        선택한 요소의 뒤에 나오는 모든 형제 요소를 선택
        
    - 인접 형제 결합자 (`+`)
        
        선택한 요소 바로 다음에 오는 형제 요소 하나만 선택
        
    
    등이 있다.
    

---

## 그룹 선택자(Group Selector)

- 여러 선택자에 동일한 스타일을 적용할 때 사용
- `선택자1, 선택자2, 선택자3` 형태로 작성한다
    
    ```css
    선택자1,
    선택자2,
    선택자3 {
      속성: 값;
    }
    ```
    
- 활용 예시
    
    ```html
    <h1>제목 1</h1>
    <h2>제목 2</h2>
    <h3>제목 3</h3>
    ```
    
    ```css
    /* 제목 태그들에 같은 스타일 적용 */
    h1,
    h2,
    h3 {
      color: navy;
      font-family: Arial, sans-serif;
    }
    ```
    

## 전체 예제

```html
<header id="header">
  <h1>CSS 선택자 학습하기</h1>
</header>

<div class="container">
  <h2>기본 선택자</h2>
  <p>이것은 container의 자식 p입니다.</p>

  <div class="content">
    <p>이것은 일반 문단입니다.</p>
    <p class="highlight">이것은 강조된 문단입니다.</p>
    <p>이 문단에는 <span>기울임 글씨</span>가 포함되어 있습니다.</p>
  </div>

  <div class="warning">
    <h3>주의사항</h3>
    <p>이것은 경고 메시지입니다.</p>
  </div>
</div>

```

```css
/* 전체 초기화 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* 태그 선택자 */
body {
  font-family: Arial, sans-serif;
  line-height: 1.6;
}

h1 {
  color: navy;
  font-size: 28px;
  margin-bottom: 20px;
}

p {
  color: #333;
  margin-bottom: 15px;
}

/* 아이디 선택자 */
#header {
  background-color: #f4f4f4;
  padding: 20px;
  text-align: center;
}

/* 클래스 선택자 */
.highlight {
  background-color: yellow;
  padding: 5px;
  font-weight: bold;
}

.warning {
  color: red;
  border: 2px solid red;
  padding: 10px;
  margin: 10px 0;
}

/* 자식 선택자 */
.container > p {
  font-size: 18px;
  color: blue;
}

/* 후손 선택자 */
.content span {
  font-style: italic;
  color: green;
}

/* 그룹 선택자 */
h2,
h3,
h4 {
  color: #666;
  border-bottom: 1px solid #ddd;
  padding-bottom: 5px;
}

```

## 연습하기

[CSS Diner](https://flukeout.github.io/)

## CSS 우선순위

- 요소에 2개 이상의 스타일이 적용될 때 우선순위에 따라 적용되는 스타일을 결정한다.
- 선택자의 범위가 좁을수록 우선순위가 높아진다.

### 우선순위

- **!important**: CSS 속성을 **강제로 우선시**하는 키워드. 최대한 사용하지 않는 것이 좋다.
    
    ```css
    p {
      color: blue !important;
    }
    
    ```
    
- **요소 인라인 스타일** : 요소에 직접 적용된 스타일
    
    ```html
    <p style="color: red;">p 태그 요소</p>
    
    ```
    
- **id 선택자**: 요소에 고유한 식별자를 부여하여 스타일을 적용하는 방법
    
    ```html
    <p id="bold">bold 아이디 요소</p>
    
    ```
    
    ```css
    #bold {
      color: red;
    }
    
    ```
    
- **class 선택자**: 요소에 공통적인 특성을 부여하여 스타일을 적용하는 방법
    
    ```html
    <p class="italic">italic 클래스 요소</p>
    
    ```
    
    ```css
    .italic {
      color: blue;
    }
    
    ```
    
- **tag 선택자**: 요소의 타입을 기반으로 스타일을 적용하는 방법
    
    ```html
    <p>p 태그 요소</p>
    
    ```
    
    ```css
    p {
      color: blue;
    }
    
    ```
    
- **나중에 작성된 스타일 코드**: 우선 순위가 같은 경우 나중에 작성된 스타일이 우선순위가 높다.
    
    ```css
    span {
      color: blue;
    }
    
    span {
      color: red;
    }
    
    ```
    

## 예시 코드

```html
<head>
  <style>
    p {
      color: gray;
    }
    p {
      color: red;
    }

    .my-class {
      color: blue;
    }

    #my-id {
      color: green;
    }

    .force-style {
      color: black !important;
    }
  </style>
</head>
<body>

  <p>1. 그냥 태그 (Red - gray를 덮어씀)</p>

  <p class="my-class">2. class있는 태그 (Blue)</p>

  <p id="my-id" class="my-class">3. class, id있는 태그 (Green)</p>

  <p id="my-id" class="my-class" style="color: orange;">
    4. class, id, 인라인 태그 (Orange)
  </p>

  <p id="my-id" class="my-class force-style" style="color: orange;">
    5. class, id, 인라인, !important 태그 (Black)
  </p>

</body>
```

# CSS 속성

## 텍스트 관련 속성

### color

- 텍스트의 색상 지정
    
    ```css
    p {
      color: blue;
    }
    
    h1 {
      color: #ff5733;
    }
    
    span {
      color: rgb(255, 99, 71);
    }
    
    ```
    

### font-size

- 텍스트의 크기 지정
    
    ```css
    p {
      font-size: 16px;
    }
    
    h1 {
      font-size: 2em;
    }
    
    span {
      font-size: 150%;
    }
    
    ```
    

### font-weight

- 텍스트의 두께(굵기) 지정
- 단어 값으로는 `normal`, `bold`, `bolder`, `lighter`가 있다
- 숫자값(100~900)도 사용 가능하다
    
    ```css
    p {
      font-weight: normal;
    }
    
    h1 {
      font-weight: bold;
    }
    
    span {
      font-weight: 700;
    }
    
    ```
    

### text-align

- 텍스트의 정렬 방식 지정
- block 요소에만 적용된다.
- 값으로는 `left`, `center`, `right`, `justify`가 있다
    
    ```css
    p {
      text-align: left;
    }
    
    h1 {
      text-align: center;
    }
    
    div {
      text-align: right;
    }
    
    ```
    

---

## 너비와 높이

### width

- 요소의 너비 지정
- 값으로는 `auto`, `px`, `%`, `em`, `rem`, `vw`, `vh` 등이 있다
    
    ```css
    div {
      width: 100px; /* 요소의 너비를 100픽셀로 설정 */
    }
    
    ```
    

### height

- 요소의 높이 지정
- 값으로는 `auto`, `px`, `%`, `em`, `rem`, `vw`, `vh` 등이 있다
    
    ```css
    div {
      height: 200px; /* 요소의 높이를 200픽셀로 설정 */
    }
    
    ```
    

### min-width 와 max-width

- 요소의 최소 너비와 최대 너비 지정
- 값으로는 `auto`, `px`, `%`, `em`, `rem`, `vw`, `vh` 등이 있다
    
    ```css
    div {
      min-width: 300px; /* 요소의 최소 너비를 300픽셀로 설정 */
    }
    
    div {
      max-width: 500px; /* 요소의 최대 너비를 500픽셀로 설정 */
    }
    
    ```
    

### min-height 와 max-height

- 요소의 최소 높이와 최대 높이 지정
- 값으로는 `auto`, `px`, `%`, `em`, `rem`, `vw`, `vh` 등이 있다
    
    ```css
    div {
      min-height: 100px; /* 요소의 최소 높이를 100픽셀로 설정 */
    }
    
    div {
      max-height: 400px; /* 요소의 최대 높이를 400픽셀로 제한 */
    }
    
    ```
    

### 상대 크기

- 너비와 높이를 상대적 크기로 지정
- 값으로는 `auto`, `px`, `%`, `em`, `rem`, `vw`, `vh` 등이 있다
    
    ```css
    div {
      width: 50vw; /* 뷰포트 너비의 50% */
    }
    
    div {
      height: 100vh; /* 뷰포트 높이의 100%, 즉 화면 전체 높이 */
    }
    
    div {
      width: 80%; /* 부모 요소 너비의 80% */
      height: 60%; /* 부모 요소 높이의 60% */
    }
    
    ```
    

---

## 배경 관련 속성

### background-color

- 요소의 배경 색상 지정
    
    ```css
    div {
      background-color: lightblue;
    }
    
    p {
      background-color: #ffebcd;
    }
    
    h1 {
      background-color: rgba(255, 99, 71, 0.5);
    }
    
    ```
    

### background-image

- 요소의 배경에 이미지 설정
    
    ```css
    div {
      background-image: url("background.jpg");
    }
    
    p {
      background-image: url("<https://example.com/image.png>");
    }
    
    h1 {
      background-image: linear-gradient(to right, red, yellow);
    }
    
    ```
    

### background-repeat

- 배경 이미지의 반복 방식 지정
- 값으로는 `repeat`, `no-repeat`, `repeat-x`, `repeat-y`가 있다
    
    ```css
    div {
      background-repeat: no-repeat; /* 배경 이미지를 반복하지 않음 */
    }
    
    p {
      background-repeat: repeat-x; /* 배경 이미지를 가로로 반복 */
    }
    
    h1 {
      background-repeat: repeat-y; /* 배경 이미지를 세로로 반복 */
    }
    
    ```
    

---

## 기타 속성

### opacity

- 요소의 투명도 설정
- 값은 0(완전 투명)에서 1(완전 불투명)까지 설정할 수 있다
    
    ```css
    div {
      opacity: 0.5; /* 요소의 투명도를 50%로 설정 */
    }
    
    p {
      opacity: 0.7; /* 요소의 투명도를 70%로 설정 */
    }
    
    img {
      opacity: 0.3; /* 요소의 투명도를 30%로 설정 */
    }
    
    ```
    

### cursor

- 요소 위에 마우스를 올렸을 때 커서 모양 지정
- 값으로는 `pointer`, `default`, `text`, `move`, `not-allowed`, `help`, `wait`, `crosshair`, 등이 있다
    
    ```css
    a {
      cursor: pointer; /* 마우스를 올렸을 때 포인터 모양으로 변경 */
    }
    
    p {
      cursor: text; /* 마우스를 올렸을 때 텍스트 모양으로 변경 */
    }
    
    div {
      cursor: move; /* 마우스를 올렸을 때 이동 모양으로 변경 */
    }
    
    ```
    

### visibility

- 요소의 가시성 설정
- 값으로는 `visible`, `hidden`, `collapse`가 있다
- 웹 페이지내에서 차지하는 공간은 유지한다.
    
    ```css
    div {
      visibility: hidden; /* 요소를 숨김 */
    }
    
    p {
      visibility: visible; /* 요소를 보임 */
    }
    
    h1 {
      visibility: collapse; /* 요소를 숨김 */
    }
    
    ```
    

# CSS 단위 (Units)

## 절대 단위 (Absolute Units)

- 해상도와 무관하게 항상 동일한 크기를 유지한다
- 고정된 크기가 필요한 경우에 사용한다

### px (픽셀)

- 화면의 물리적인 픽셀 단위를 기준으로 한다
- 1px은 화면의 한 픽셀 크기를 의미한다
- 가장 일반적으로 사용되는 단위
    
    ```css
    .box {
      width: 100px;
      height: 50px;
      font-size: 16px;
    }
    
    ```
    

---

## 상대 단위 (Relative Units)

- 화면의 크기나 다른 요소의 크기를 기준으로 계산된다
- 현대의 반응형 웹 디자인 구현을 위해 꼭 알아야 한다

### % (백분율)

- 부모 요소의 크기에 대한 비율
- 반응형 레이아웃 구현에 유용
    
    ```css
    .container {
      width: 50%; /* 부모 요소 너비의 50% */
      height: 80%; /* 부모 요소 높이의 80% */
    }
    
    ```
    

### em

- 부묘 요소의 글꼴 크기를 기준으로 한 상대 단위
- 중첩된 요소에서는 누적 계산된다
    
    ```css
    .text {
      font-size: 2em; /* 부모 글꼴 크기의 2배 */
      margin: 1em; /* 부모 글꼴 크기만큼의 여백 */
    }
    
    ```
    

### rem (루트 em)

- 루트 요소(`<html>` 요소)의 글꼴 크기를 기준으로 한 상대 단위
- 중첩된 요소의 영향을 받지 않는다
- 기본값: 16px
    
    ```css
    .heading {
      font-size: 1.5rem; /* 루트 요소 글꼴 크기의 1.5배 */
      padding: 2rem; /* 루트 요소 글꼴 크기의 2배만큼 패딩 */
    }
    
    ```
    

---

## 뷰포트 단위 (Viewport Units)

- 웹 브라우저에서 **눈에 보이는** 웹 페이지 영역
- 브라우저 창의 크기에 따라 변한다

### vw (뷰포트 너비)

- 뷰포트(Viewport)의 너비를 기준으로 한 상대 단위
- 1vw는 뷰포트 너비의 1%를 의미한다
    
    ```css
    .full-width {
      width: 100vw; /* 뷰포트 너비의 100% */
    }
    
    .half-width {
      width: 50vw; /* 뷰포트 너비의 50% */
    }
    
    ```
    

### vh (뷰포트 높이)

- 뷰포트(Viewport)의 높이를 기준으로 한 상대 단위
- 1vh는 뷰포트 높이의 1%를 의미한다
    
    ```css
    .full-height {
      height: 100vh; /* 뷰포트 높이의 100%, 즉 화면 전체 높이 */
    }
    
    .section {
      height: 50vh; /* 뷰포트 높이의 50% */
    }
    
    ```
    

### 뷰포트 단위 활용 예시

```css
/* 전체 화면 */
.full-screen {
  width: 100vw;
  height: 100vh;
  background-color: #f0f0f0;
}

/* 반응형 폰트 크기 */
.responsive-font {
  font-size: 4vw; /* 화면이 작아지면 글자도 작아짐 */
}

```

---

## 모바일 최적화 단위

- 모바일 환경에 최적화된 요소의 크기를 조절하는 단위
- 모바일 환경의 주소 표시줄, 하단 툴바 같은 동적 UI를 포함하여 계산하는 단위
- 화면 회전으로 너비와 높이가 변할 때 동적으로 크기를 조절하는 단위
- 기존 `vw`, `vh` 단위는 동적 UI를 포함하지 않고 계산하기 때문에 모바일 환경에 최적화된 요소의 크기를 조절하는 데 적합하지 않을 수 있다

### 다이나믹 뷰포트 (Dynamic Viewport)

### dvh, dvw

- 동적 UI의 유무에 따라 동적으로 높이를 계산하는 단위
- 동적 UI의 유무 또는 화면 회전으로 너비/높이가 변할 때 동적으로 크기를 조절한다
    
    ```css
    .mobile-section {
      height: 100dvh; /* 동적 UI 변화에 따라 조절되는 높이 */
    }
    
    ```
    

### svh, svw (Small Viewport)

- 동적 UI가 있을 때를 기준으로 너비/높이를 계산하는 가장 작은 단위
    
    ```css
    .small-viewport {
      height: 100svh; /* 동적 UI가 있을 때의 최소 높이 */
    }
    
    ```
    

### lvh, lvw (Large Viewport)

- 동적 UI가 없을 때를 기준으로 너비/높이를 계산하는 가장 큰 단위
    
    ```css
    .large-viewport {
      height: 100lvh; /* 동적 UI가 없을 때의 최대 높이 */
    }
    
    ```
    

### 주의사항

- 잦은 UI 변화로 인해 사용자 경험에 악영향을 줄 수 있다
- 브라우저 지원 여부를 확인하고 사용해야 한다

---

## 단위 선택 팁

### 텍스트 크기

- **rem**: 일관된 크기가 필요한 경우
- **em**: 부모 요소에 따라 상대적으로 조절이 필요한 경우
- **px**: 정확한 크기가 필요한 경우

### 레이아웃

- **%**: 부모 요소 기준 상대적 크기
- **vw, vh**: 뷰포트 기준 크기
- **px**: 고정 크기

### 여백과 패딩

- **rem**: 일관된 간격
- **em**: 텍스트 크기에 비례하는 간격
- **px**: 정확한 간격

## 색상 표현 방법

### 색상 이름

- 색상 이름을 사용하여 색상을 표현
    
    ```css
    color: red;
    color: blue;
    color: green;
    
    ```
    

### 16진수 표현

- 16진수 표현을 사용하여 색상을 표현
- `#` 기호 뒤에 6자리 또는 3자리 16진수로 표현
    
    ```css
    color: #ff0000; /* 빨강 */
    color: #00ff00; /* 녹색 */
    color: #f00; /* 3자리 축약형 빨강 */
    
    ```
    

### RGB 표현

- RGB 표현을 사용하여 색상을 표현
- Red, Green, Blue 각각 0-255 범위의 값으로 표현
    
    ```css
    color: rgb(255, 0, 0); /* 빨강 */
    color: rgb(0, 255, 0); /* 녹색 */
    color: rgb(0, 0, 255); /* 파랑 */
    
    ```
    

### RGBA 표현

- RGBA 표현을 사용하여 색상과 투명도를 표현
- RGB + Alpha(투명도), Alpha는 0.0(완전 투명) ~ 1.0(완전 불투명) 범위
    
    ```css
    color: rgba(255, 0, 0, 1); /* 완전 불투명한 빨강 */
    color: rgba(255, 0, 0, 0.5); /* 50% 투명한 빨강 */
    color: rgba(0, 0, 0, 0); /* 완전 투명한 검정 */
    
    ```
    

### OKLCH 표현

- 인간의 시각 시스템에 가깝게 설계된 새로운 색상 표현 방법
- 빛의 밝기, 채도, 색조를 제어해서 색상을 표현
- **L(Lightness)** : 빛의 밝기, 1에 가까울수록 밝다(0~1)
- **C(Chroma)** : 채도, 0에 가까울수록 무채색이 된다(0~0.4)
- **H(Hue)** : 색조, 0도는 빨강, 120도는 녹색, 240도는 파랑(0~360도)
    
    ```css
    color: oklch(0.7 0.25 0); /* 밝은 빨강 */
    color: oklch(0.7 0.25 120); /* 밝은 녹색 */
    color: oklch(0.7 0.25 240); /* 밝은 파랑 */
    
    ```
    

## CSS 상속

- 부모 요소에 지정된 스타일 속성이 자식 요소에게 전달되는 작동 방식
- 상속되는 속성과 상속되지 않는 속성으로 구분할 수 있다

### 상속되는 속성 목록

text와 관련된 속성들은 대부분 상속된다.

- `color`: 글자 색상
- `font-family`: 글꼴 종류
- `font-size`: 글자 크기
- `line-height`: 줄 간격
- `text-align`: 텍스트 정렬
- `visibility`: 요소의 가시성
    
    ```html
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <style>
          div {
            color: green;
            font-size: 30px;
          }
        </style>
      </head>
    
      <body>
        <div>
          <p>p 태그 요소</p>
          <span>span 태그 요소</span>
        </div>
      </body>
    </html>
    
    ```
    

### 상속되지 않는 속성 목록

- `margin`: 외부 여백
- `padding`: 내부 여백
- `border`: 테두리
- `width`, `height`: 크기
- `background`: 배경

## 박스 모델(Box Model)

- 브라우저가 요소의 너비와 높이를 계산할 때 사용하는 기준
    
    ![출처 : https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_box_model](https://prod-files-secure.s3.us-west-2.amazonaws.com/f2678325-6f7b-4a25-b188-86c42030d6d5/462ac5b5-efac-4363-b147-63c126197556/image.png)
    
    출처 : https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_box_model
    

### 박스 모델 구성요소

- **콘텐츠(Content)**: 텍스트나 이미지가 들어가는 실제 내용
- **패딩(Padding)**: 콘텐츠와 테두리 사이의 공간으로, 요소 내부의 여백
- **테두리(Border)**: 요소의 가장자리를 둘러싸는 테두리로, 두께, 스타일, 색상을 설정할 수 있다.
- **마진(Margin)**: 요소 바깥의 공간으로, 다른 요소들과의 간격

### 콘텐츠(Content)

- 요소의 실제 내용을 담는 영역
- `width` 와 `height` 속성으로 크기가 제어된다

### 패딩(Padding)

- 콘텐츠와 테두리 사이의 내부 여백
- `padding` 속성을 사용해 상/하/좌/우 내부 여백을 설정할 수 있다
    
    ```html
    <div class="padding-box">패딩 박스</div>
    
    ```
    
    ```css
    .padding-box {
      width: 200px;
      height: 100px;
      color: white;
      background-color: lightgreen;
      padding: 100px 20px 30px 40px;
      /* 상, 우, 하, 좌  패딩 */
    }
    
    ```
    

### 테두리(Border)

- 요소의 가장자리를 둘러싸는 선으로, 두께, 스타일, 색상을 설정할 수 있다.
- `border` 속성을 사용해 테두리의 크기와 스타일을 제어할 수 있다
    
    ```html
    <div class="border-box"></div>
    
    ```
    
    ```css
    .border-box {
      width: 200px;
      height: 100px;
      background-color: lightyellow;
      border: 5px dotted darkblue;
      /* 테두리 두께, 스타일, 색상 */
    }
    
    ```
    

### 마진(Margin)

- 요소의 바깥쪽 공간으로, 다른 요소와의 간격을 설정한다.
- `margin` 속성을 사용해 요소 간의 상/하/좌/우 간격을 설정할 수 있다
    
    ```html
    <div class="margin-box"></div>
    <div class="margin-box"></div>
    <div class="margin-box"></div>
    <div class="margin-box"></div>
    
    ```
    
    ```css
    .margin-box {
      width: 200px;
      height: 100px;
      background-color: lightpink;
      margin: 10px 5px 50px 50px;
      /* 상, 우, 하, 좌 각각의 마진 */
    }
    
    ```
    

### Margin 중첩(Margin Collapse)

- 두 요소의 마진이 겹쳐질 때 더 큰 값이 적용된다
    
    ```html
    <div>
      <div class="box box-d"></div>
      <div class="box box-e"></div>
      <div class="box box-f"></div>
    </div>
    
    ```
    
    ```css
    .box {
      height: 80px;
    }
    
    .box-d {
      background-color: lightgreen;
      margin: 20px 0; /* 상하 20px 마진 */
    }
    
    .box-e {
      background-color: lightblue;
      margin: 40px 0; /* 상하 40px 마진 */
    }
    
    .box-f {
      background-color: lightpink;
      margin: 60px 0; /* 상하 60px 마진 */
    }
    
    ```
    

### Margin과 Padding 비교

- Margin은 다른 요소와의 여백을 설정
- Padding은 요소 내부의 여백을 설정
    
    ```html
    <div>
      <div class="box margin"></div>
      <div class="box padding"></div>
    </div>
    
    ```
    
    ```css
    .box {
      background-color: white;
      border: 3px solid lightcoral;
      border-radius: 8px;
      height: 120px;
    }
    
    .margin {
      margin: 100px;
      /* 경계선 바깥쪽에 100px 여백 */
    }
    
    .padding {
      padding: 100px;
      /* 경계선 안쪽에 100px 여백 */
    }
    
    ```
    

---

## box-sizing

- 요소의 크기를 계산할 때, 패딩과 테두리를 포함할지 여부를 결정하는 속성

### `content-box` (기본값)

- 콘텐츠 영역으로만 너비와 높이를 계산한다.

### `border-box` (선호)

- 패딩과 테두리를 포함한 영역을 너비와 높이를 계산한다
- `content-box` 보다 직관적이기 때문에 선호된다

```html
<div class="content-box">box-sizing: content-box</div>
<div class="border-box">box-sizing: border-box</div>

```

```css
.content-box {
  width: 200px;
  height: 100px;
  padding: 20px;
  border: 5px solid black;
  background-color: lightblue;
  box-sizing: content-box;
  /* 기본값: 패딩과 테두리 제외한 크기 */
  margin-bottom: 20px;
}

.border-box {
  width: 200px;
  height: 100px;
  padding: 20px;
  border: 5px solid black;
  background-color: lightgreen;
  box-sizing: border-box;
  /* 패딩과 테두리 포함한 크기 */
}

```

# CSS 디스플레이 속성

## 디스플레이(Display)

- 요소가 웹 페이지에서 어떻게 배치되고, 공간을 차지할지를 결정하는 속성
- 각 요소는 디스플레이 속성에 따라 인라인, 블록 또는 레이아웃 방식을 따르게 된다

## 디스플레이 속성 종류

### inline

- 수평으로 배치되며, 요소는 자식 요소의 크기만큼 공간을 차지한다
- 줄을 바꾸지 않고 다른 인라인 요소와 한 줄에 나란히 위치한다
- 너비와 높이를 지정할 수 없다
- 예시 태그: `span`, `a`, `img`, `input`, `label`, `button`

### block

- 수직으로 배치되며, 요소는 한 줄 전체를 차지한다
- 블록 요소는 자동으로 줄이 바뀌며 너비와 높이를 지정할 수 있다
- 예시 태그: `div`, `p`, `h1`, `h2`, `h3`, `h4`, `h5`, `h6`, `ul`, `ol`, `li`, `table`, `form`

### inline-block

- inline 요소처럼 한 줄에 나란히 수평으로 배치되지만 block 요소처럼 너비와 높이를 지정할 수 있다
- 두 속성의 장점을 결합한 속성
- 예시 태그: `input`, `textarea`, `select`, `button`

### none

- 요소를 숨긴다
- 해당 요소는 웹 페이지에서 보이지 않으며 공간도 차지하지 않는다
- 예시 태그: `script`, `style`, `link`, `meta`

![image1](./image/image1.png)

### 예시 코드

```html
<div class="inline">inline 속성 div</div>
<div class="inline">inline 속성 div</div>

<div class="block">block 속성 div</div>
<div class="block">block 속성 div</div>

<div class="inline-block">inline-block 속성 div</div>
<div class="inline-block">inline-block 속성 div</div>

```

```css
/* div 태그 공통 스타일 속성 */
div {
  width: 200px;
  height: 200px;
}

.inline {
  display: inline;
  border: red 1px solid;
}

.block {
  display: block;
  border: blue 1px solid;
}

.inline-block {
  display: inline-block;
  border: green 1px solid;
}

```