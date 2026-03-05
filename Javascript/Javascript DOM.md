## DOM(Document Object Model)

- HTML 문서를 **트리 구조 형태의 객체(Object)**로 표현한 것이다.
- 웹 페이지를 **동적으로 조작**하기 위해 브라우저와 JavaScript 사이에서 중간 다리 역할을 한다.
- DOM을 통해 **요소 선택 및 조작**, **요소의** **속성 변경**, **이벤트 처리 등을** 할 수 있다.

### HTML 문서와 DOM 트리(Tree) 구조

**HTML 문서**

```html
<!DOCTYPE html>
<html>
  <head>
    <title>DOM 예제</title>
  </head>
  <body>
    <h1 id="title">Hello, World!</h1>
    <p class="content">이것은 문단입니다.</p>
  </body>
</html>

```

**DOM 트리 구조**

```
Document (문서 노드)
└── html (요소 노드)
    ├── head (요소 노드)
    │   └── title (요소 노드)
    │       └── "DOM 예제" (텍스트 노드)
    └── body (요소 노드)
        ├── h1 (요소 노드) [id="title" 속성 보유]
        │   └── "Hello, World!" (텍스트 노드)
        └── p (요소 노드) [class="content" 속성 보유]
            └── "이것은 문단입니다." (텍스트 노드)

```

### 노드(Node)

- HTML 트리의 정보를 표현하는 객체
- HTML 문서의 모든것은 노드로 표현
- 노드의 종류
    - 문서 노드(Document Node)
    - 요소 노드(Element Node)
    - 텍스트 노드(Text Node)
    - 속성 노드(Attribute Node)
    - 주석 노드(Comment Node)

### 간단한 DOM API

**예시**

```html
<html>
  <body>
    <div id="container">
      <h1>Hello, World!</h1>
    </div>
    <script>
      const container = document.querySelector("#container");
      const newH1 = document.createElement("h1");
      newH1.textContent = "Hello, DOM!";
      container.appendChild(newH1);
    </script>
  </body>
</html>

```

# DOM 노드 선택 및 조작

## 노드 선택(Select)

선택자를 활용하여 DOM에서 요소 노드 선택

### `querySelector(selector)`

- **선택자**와 **일치하는 첫 번째 노드** 반환
- 태그, 클래스, 아이디 등 다양한 선택자 사용 가능

```jsx
document.querySelector(selector);

```

**예시**

```jsx
// 태그 이름 선택자
const element = document.querySelector("p");

// 클래스 이름 선택자
const element = document.querySelector(".class-name");

// 아이디 이름 선택자
const element = document.querySelector("#id-name");

```

### `querySelectorAll(selector)`

- 선택자(selector)와 **일치하는 모든 노드를 저장한 NodeList(배열과 유사한)** 반환
- `forEach()`로 반복 가능

```jsx
document.querySelectorAll(selector);

```

**예시**

```jsx
// 모든 p 태그 선택
const elements = document.querySelectorAll("p");

elements.forEach((element, index) => {
  console.log(`문단 ${index + 1}: ${element.textContent}`);
});

```

---

## 노드 조작(Manipulate)

선택한 노드의 텍스트와 속성 조작

### 텍스트 조작

- `textContent` 속성: 노드의 텍스트에 접근
- 노드 내부의 모든 텍스트를 **단순한 문자열**로 취급

**기본 구조**

```jsx
element.textContent = "새로운 텍스트";
```

**예시**

```jsx
const element = document.querySelector("p");

// 텍스트 읽기
console.log(element.textContent);

// 텍스트 수정
element.textContent = "새로운 텍스트";

```

### 속성 조작

- `getAttribute()`: 노드의 속성 값 읽기 메서드
- `setAttribute()`: 노드의 속성 값 조작 메서드
- 속성 직접 접근: `element.속성명`으로 직접 접근 가능

**기본 구조**

```jsx
element.getAttribute("속성명"); // 속성 값 읽기
element.setAttribute("속성명", "새로운 값"); // 속성 값 조작
element.속성명 = "새로운 값"; // 속성 값 조작

```

**예시**

```jsx
const link = document.querySelector("a");

// 속성 값 읽기
console.log(link.getAttribute("href"));

// 속성 값 변경하기
link.setAttribute("href", "https://dailyalgo.kr");

// 속성 직접 접근
console.log(link.href);
link.href = "https://www.naver.com";

```

### 스타일 조작

- `style` 속성을 통해 노드의 인라인 스타일 관리
- CSS의 kebab-case 대신 camelCase 사용

```jsx
const element = document.querySelector("div");

// 개별 스타일 설정
element.style.backgroundColor = "red";
element.style.fontSize = "20px";

// 여러 스타일 한 번에 설정
Object.assign(element.style, {
  color: "white",
  fontWeight: "bold",
  textAlign: "center",
  padding: "10px",
});

```

---

## 클래스 조작

### `classList` (권장)

- `add()`, `remove()`, `toggle()`, `contains()` 메서드로 클래스 조작

**기본 구조**

```jsx
element.classList.add("클래스명"); // 클래스 추가
element.classList.remove("클래스명"); // 클래스 제거
element.classList.toggle("클래스명"); // 클래스 토글 (있으면 제거, 없으면 추가)
element.classList.contains("클래스명"); // 클래스 포함 여부 확인

```

**예시**

```jsx
const element = document.querySelector("div");

element.classList.add("active");

element.classList.remove("inactive");

element.classList.toggle("hidden");

if (element.classList.contains("active")) {
  console.log("활성화 상태입니다.");
}

```

### `className`

- 클래스 전체를 문자열로 관리하는 속성
- 여러 클래스를 한 번에 지정할 때 유용

**기본 구조**

```jsx
element.className = "클래스명";

```

**예시**

```jsx
const element = document.querySelector("div");

element.className = "active hidden";

```

## 예제

```html
<!DOCTYPE html>
<html>
  <head>
    <style>
      .active {
        color: red;
      }
      .hidden {
        display: none;
      }
    </style>
  </head>
  <body>
    <div id="container">
      <h1 id="title">원래 제목</h1>
      <p class="content">원래 내용</p>
      <button id="toggleBtn">토글 버튼</button>
    </div>

    <script>
      // 1. 노드 선택
      const title = document.querySelector("#title");
      const content = document.querySelector(".content");
      const toggleBtn = document.querySelector("#toggleBtn");
      const container = document.querySelector("#container");

      // 2. 텍스트 조작
      title.textContent = "새로운 제목";
      content.textContent = "새로운 내용";

      // 3. 속성 조작
      toggleBtn.setAttribute("disabled", "true");

      // 4. 클래스 조작
      container.classList.add("active");

      // 5. 스타일 조작
      title.style.fontSize = "24px";
      title.style.color = "blue";
    </script>
  </body>
</html>

```

## 요소 노드 생성(Create)

DOM API로 요소 노드 생성

### `document.createElement()`

- 요소 노드 생성 메서드
- 생성한 노드의 텍스트와 속성 조작 가능

```jsx
document.createElement(tagName);

```

**예시**

```jsx
const newDiv = document.createElement("div");
const newP = document.createElement("p");

const newDivWithContent = document.createElement("div");
newDivWithContent.textContent = "Hello World!";
newDivWithContent.setAttribute("id", "greeting");
newDivWithContent.classList.add("container");

```

## 노드 추가(Append)

- 특정 노드에 자식 노드를 추가하는 메서드

### `appendChild()` vs `append()`

```jsx
parent.appendChild(child);
parent.append(child1, child2, "text");

```

**예시**

```jsx
const parent = document.querySelector("#parent");
const newDiv = document.createElement("div");

// appendChild: 노드만 추가
parent.appendChild(newDiv);

// append: 노드와 문자열 모두 추가 가능
parent.append(newDiv, "새로운 텍스트", document.createElement("span"));

```

### body에 대해

- html에서 눈으로 보이는 요소는 body 안에 있는 내용.
- body 자체도 태그임. 내가 div, p 등 각종 노드를 생성해도 body에 속해있지 않으면 의미가 없음.
- 그래서 append를 body 태그에 사용해서 body의 자식 노드로 추가해야 비로소 화면에 보이게 된다.
- `document` 는 html 전체를 가리킨다. 그래서 `document.body` 를 하면 html에서 body 태그를 가리키는 것. 여기에 `document.body.append()` 까지 해야 body에 자식 노드로 추가할 수 있음.

---

## 노드 삭제(Remove)

- 노드를 DOM 트리에서 삭제하는 메서드

### `removeChild()` vs `remove()`

```jsx
parent.removeChild(child);
child.remove();

```

**예시**

```jsx
const parent = document.querySelector("#parent");
const child = document.querySelector("#child");

// removeChild: 부모에서 자식 제거
parent.removeChild(child);

// remove: 자기 자신 제거
child.remove();

```