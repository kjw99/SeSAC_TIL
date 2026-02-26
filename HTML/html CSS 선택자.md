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