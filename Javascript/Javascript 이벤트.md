## 이벤트(Event)

- 웹 페이지에서 발생하는 **특정 사건에 대한 신호**

### 이벤트 종류

| 카테고리 | 이벤트 | 설명 |
| --- | --- | --- |
| 마우스 | `click`, `dblclick`, `mousemove`, `mouseover`, `mouseout` | 마우스 관련 동작 |
| 키보드 | `keydown`, `keyup` | 키보드 입력 |
| 입력 | `input`, `change`, `focus`, `blur` | 폼 요소 상태 변화 |
| 폼 | `submit` | 폼 제출 |
| 문서 | `scroll`, `resize` | 문서/창 크기 변화 |

---

## 이벤트 핸들러(Event Handler) 등록

- 이벤트가 발생했을 때 실행할 함수를 등록하는 방법

### 이벤트 핸들러 등록 방법 종류

| 방법 | 기본 구조 |
| --- | --- |
| HTML 인라인 이벤트 속성 | `onclick="handler()"` |
| JavaScript 이벤트 속성 | `element.onclick = handler` |
| `addEventListener()` | `element.addEventListener(type, handler)` |

### HTML 인라인 이벤트 속성

- HTML 문서의 요소에 특정 이벤트 속성에 대한 이벤트 핸들러를 직접 지정하는 방법
- 하나의 이벤트 속성에 하나의 이벤트 핸들러만 등록 가능
- 구조(HTML)와 동작(JS)를 분리하는 Vanilla(기본) JavaScript에서는 권장하지 않는 방법
- 하지만 구조와 동작을 결합하는 React에서는 권장되는 방법

```html
<button onclick="handleClick()">클릭하세요</button>
<script>
  function handleClick() {
    alert("버튼 클릭됨");
  }
</script>

```

### JavaScript 이벤트 속성

- JavaScript 코드에서 요소의 이벤트 속성에 대한 이벤트 핸들러를 지정하는 방법
- 하나의 이벤트 속성에 하나의 이벤트 핸들러만 등록 가능

```html
<button id="my-button">클릭하세요</button>
<script>
  const button = document.querySelector("#my-button");
  button.onclick = function () {
    alert("버튼 클릭됨");
  };
</script>

```

### `addEventListener()`

- 이벤트 핸들러 등록 메서드
- 하나의 이벤트 속성에 여러 이벤트 핸들러를 등록하는 방법
- 구조와 동작을 분리할 수 있어서 Vanilla JavaScript에서 가장 권장되는 방법

```jsx
element.addEventListener(type, handler, options);

```

**예시**

```jsx
const button = document.querySelector("#my-button");

button.addEventListener("click", function (event) {
  console.log("버튼 클릭됨");
});

```

---

## 이벤트 핸들러 제거

### `removeEventListener()`

- 이벤트 핸들러 제거 메서드
- 이벤트 핸들러를 제거하는 방법

```jsx
element.removeEventListener(type, handler, options);

```

**예시**

```jsx
const button = document.querySelector("#my-button");

button.removeEventListener("click", function (event) {
  console.log("버튼 클릭됨");
});

```

## 이벤트 종류별 예시

**클릭 이벤트**

```jsx
const button = document.querySelector("#button");
button.addEventListener("click", () => {
  alert("버튼 클릭!");
});

```

**포커스 이벤트**

```jsx
const input = document.querySelector("#input");
input.addEventListener("focus", () => {
  input.style.backgroundColor = "yellow";
});

```

**키보드 이벤트**

```jsx
const textInput = document.querySelector("#text-input");
textInput.addEventListener("keydown", (event) => {
  console.log(`눌린 키: ${event.key}`);
});

```

**마우스 이동 이벤트**

```jsx
window.addEventListener("mousemove", (event) => {
  console.log(`마우스 위치: ${event.clientX}, ${event.clientY}`);
});

```

---

## 이벤트 객체 (Event Object)

- 발생한 이벤트(event)의 정보를 담은 이벤트 핸들러의 매개변수
- 관례적으로 `event` 또는 `e`로 표기

### 주요 속성

```jsx
element.addEventListener("click", function (event) {
  // 1. 실제로 클릭된 가장 안쪽 요소
  console.log("실제 클릭 대상 (target):", event.target);

  // 2. 이벤트 리스너가 실제로 호출된 요소 (이벤트가 걸린 부모)
  console.log("리스너가 걸린 대상 (currentTarget):", event.currentTarget);

  // 3. 이벤트 종류 (예: "click")
  console.log("이벤트 타입:", event.type);

  // 4. 마우스 좌표 (브라우저 화면 기준)
  console.log("좌표:", event.clientX, event.clientY);

  // 5. 키보드 이벤트의 경우 (keydown 등에서 유효)
  if (event.key) {
    console.log("입력된 키:", event.key);
  }
});
```

### 주요 메서드

**`event.preventDefault()`**

- 이벤트가 발생했을 때 기본적으로 수행되는 동작을 막는 메서드
- 예를 들면, 폼(form) 제출을 막거나 링크(a) 태그의 기본 동작을 막을 수 있음

```html
<a href="<https://www.google.com>">구글로 이동</a>
<script>
  const link = document.querySelector("a");
  link.addEventListener("click", (event) => {
    event.preventDefault();
  });
</script>

```

## 이벤트 처리 예시

**클릭 이벤트 처리**

```html
<!DOCTYPE html>
<html>
  <head>
    <style>
      .clicked {
        background-color: lightblue;
        color: white;
      }
    </style>
  </head>
  <body>
    <h1>클릭 이벤트 예시</h1>
    <button id="click-btn">클릭하세요</button>

    <script>
      const clickBtn = document.querySelector("#click-btn");
      clickBtn.addEventListener("click", () => {
        alert("버튼이 클릭되었습니다!");
        clickBtn.classList.add("clicked");
      });
    </script>
  </body>
</html>

```

**포커스 이벤트 처리**

```html
<!DOCTYPE html>
<html>
  <head>
    <style>
      .highlight {
        background-color: yellow;
        border: 2px solid orange;
      }
    </style>
  </head>
  <body>
    <h1>포커스 이벤트 예시</h1>
    <input type="text" id="text-input" placeholder="텍스트를 입력하세요" />

    <script>
      const textInput = document.querySelector("#text-input");

      textInput.addEventListener("focus", () => {
        textInput.classList.add("highlight");
        console.log("입력 필드에 포커스됨");
      });

      textInput.addEventListener("blur", () => {
        textInput.classList.remove("highlight");
        console.log("입력 필드에서 포커스 해제됨");
      });
    </script>
  </body>
</html>

```

**키보드 이벤트 처리**

```html
<!DOCTYPE html>
<html>
  <head>
    <style>
      .key-display {
        padding: 10px;
        border: 1px solid #ccc;
        margin: 10px 0;
        background-color: #f9f9f9;
      }
    </style>
  </head>
  <body>
    <h1>키보드 이벤트 예시</h1>
    <input type="text" id="text-input" placeholder="키를 눌러보세요" />
    <div id="key-display" class="key-display">눌린 키가 여기에 표시됩니다</div>

    <script>
      const textInput = document.querySelector("#text-input");
      const keyDisplay = document.querySelector("#key-display");

      textInput.addEventListener("keydown", (event) => {
        keyDisplay.textContent = `입력된 키: ${event.key}`;
        console.log(`눌린 키: ${event.key}`);
      });
    </script>
  </body>
</html>

```

**기본 동작 방지**

```html
<!DOCTYPE html>
<html>
  <head>
    <style>
      .prevented {
        color: red;
        text-decoration: line-through;
      }
    </style>
  </head>
  <body>
    <h1>기본 동작 방지 예시</h1>
    <a href="<https://www.google.com>" id="link">구글로 이동</a>

    <script>
      const link = document.querySelector("#link");

      link.addEventListener("click", (event) => {
        event.preventDefault(); // 링크 이동 방지
        alert("링크 이동이 방지되었습니다!");
        link.classList.add("prevented");
      });
    </script>
  </body>
</html>

```

## 이벤트 전파 (Event Propagation)

이벤트가 발생했을 때 이벤트는 해당 요소에서만 발동하지 않고, 최상위 노드부터 이벤트가 발생한 노드를 거쳐 다시 최상위 노드로 올라간다.

이러한 과정을 이벤트 전파라고하며, 이벤트는 위에서 아래로(캡쳐링) 아래에서 위로(버블링) 전파된다

### 이벤트 전파 3단계

1. 캡처링 단계: 최상위 요소에서 이벤트가 발생한 요소로 내려가는 과정
2. 타겟 단계: 이벤트가 발생한 요소에서 이벤트가 처리되는 과정
3. 버블링 단계: 이벤트가 발생한 요소에서 최상위 요소로 올라가는 과정

---

## 이벤트 버블링 (Event Bubbling)

- 이벤트가 발생한 요소에서 최상위 요소로 올라가는 과정
- 예를 들면, 특정 요소에서 `click` 이벤트가 발생하면, 특정 요소부터 최상위 요소까지 `click` 이벤트가 발생
- 이벤트가 발생한 요소 => `div` => `<body>` => `<html>` => `document` => `window`
- 별도의 옵션이 필요하지 않음
- `event.target`
    - 최초로 이벤트가 발생한 지점
    - 클릭된 실제 요소
- `event.currentTarget`
    - 리스너가 직접 걸려 있는 지점
    - addEventListener를 호출한 바로 그 요소

```html
<!DOCTYPE html>
<html>
  <body>
    <div id="parent" style="padding: 20px; background: #eee;">
      최상위 div (parent)
      <div id="child" style="padding: 20px; background: #ccc;">
        상위 div (child)
        <button id="button">클릭</button>
      </div>
    </div>

    <script>
      const parent = document.querySelector("#parent");
      const child = document.querySelector("#child");
      const button = document.querySelector("#button");

      // 공통 출력 함수
      function logEvent(event) {
        console.log(`[${event.currentTarget.id}] 핸들러 실행`);
        console.log(`- event.target:`, event.target.id);        // 처음 클릭된 요소
        console.log(`- event.currentTarget:`, event.currentTarget.id); // 현재 감지 중인 요소
        console.log("----------------------------");
      }

      parent.addEventListener("click", logEvent);
      child.addEventListener("click", logEvent);
      button.addEventListener("click", logEvent);
    </script>
  </body>
</html>
```

### 이벤트 위임(Event Delegation)

- 여러개의 자식 요소에 각각 이벤트 핸들러를 등록하는 대신, 부모 요소에 이벤트 핸들러를 등록하는 방법
- 자식 요소에 동일한 여러개의 이벤트 핸들러를 등록하지 않고, 부모 요소에 하나의 이벤트 핸들러를 등록해서 성능 향상
- React에서는 이벤트 위임이 기본적으로 적용되어 있음

**예시**

```html
<!DOCTYPE html>
<html>
  <head>
    <style>
      li {
        cursor: pointer;
      }
      .completed {
        text-decoration: line-through;
      }
    </style>
  </head>
  <body>
    <!-- 부모요소 ul -->
    <ul id="listContainer">
      <!-- 자식요소 li -->
      <li>Item 1</li>
      <li>Item 2</li>
      <li>Item 3</li>
    </ul>
    <script>
      const listContainer = document.querySelector("#listContainer");

      listContainer.addEventListener("click", (event) => {
        if (event.target.tagName.toLowerCase() === "li") {
          event.target.classList.toggle("completed");
        }
      });
    </script>
  </body>
</html>

```

---

## 이벤트 캡처링 (Event Capturing)

- 최상위 요소에서 이벤트가 발생한 요소로 내려가는 과정
- 예를 들면, 특정 요소에서 `click` 이벤트가 발생하면, 최상위 요소부터 순차적으로 이벤트가 발생한 요소까지 `click` 이벤트가 발생
- `window` => `document` => `<html>` => `<body>` => `div` => `...` => 이벤트가 발생한 요소

**예시**

- `addEventListener` 메서드의 세 번째 매개변수를 `{capture: true}`로 설정하면 이벤트 캡처링 단계에서 이벤트 처리(이벤트 발생)
- 별도의 옵션이 필요하므로 기본적으로는 발생하지 않음

```html
<!DOCTYPE html>
<html>
  <body>
    <div id="parent">
      <div id="child">
        <button id="button">클릭</button>
      </div>
    </div>
    <script>
      const parent = document.querySelector("#parent");
      const child = document.querySelector("#child");
      const button = document.querySelector("#button");

      // 캡처링 단계에서 이벤트 처리 (세 번째 매개변수: {capture: true})
      parent.addEventListener(
        "click",
        () => {
          console.log("최상위 div 캡처링");
        },
        { capture: true }
      );

      child.addEventListener(
        "click",
        () => {
          console.log("상위 div 캡처링");
        },
        { capture: true }
      );

      button.addEventListener("click", () => {
        console.log("버튼 클릭");
      });

      // 자식 버튼 클릭 시 출력
      // "최상위 div 캡처링"
      // "상위 div 캡처링"
      // "버튼 클릭"
    </script>
  </body>
</html>

```

---

## 이벤트 전파 차단

**`event.stopPropagation()`**

- 이벤트가 상위 요소로 전파(캡처링, 버블링)되는 것을 막는 메서드
- 예를 들면, 중첩된 요소에서 자식 요소의 이벤트가 부모 요소에 영향을 주지 않도록 차단할 때 사용

```html
<!DOCTYPE html>
<html>
  <body>
    <div id="parent">
      <div id="child">
        <button id="button">클릭</button>
      </div>
    </div>
    <script>
      const parent = document.querySelector("#parent");
      const child = document.querySelector("#child");
      const button = document.querySelector("#button");

      parent.addEventListener("click", () => {
        console.log("최상위 div 클릭");
      });

      child.addEventListener("click", (event) => {
        console.log("상위 div 클릭");
        event.stopPropagation(); // 부모 요소로의 이벤트 전파를 막음
      });

      button.addEventListener("click", () => {
        console.log("버튼 클릭");
      });

      // 버튼 클릭 시 출력
      // "버튼 클릭"
      // "상위 div 클릭"
    </script>
  </body>
</html>

```

## 제출(submit) 이벤트

- 사용자가 폼 작성 후, **제출 버튼 클릭** 또는 **Enter 키를 누를 때** 발생하는 이벤트
- `submit` 이벤트는 `form` 태그만 존재하는 이벤트

**기본 구조**

```html
<!DOCTYPE html>
<html>
  <body>
    <form id="my-form">
      <button type="submit">제출</button>
    </form>

    <script>
      const form = document.querySelector("#my-form");

      form.addEventListener("submit", function (event) {
        alert("폼 제출 이벤트 실행");
      });
    </script>
  </body>
</html>

```

### 제출 이벤트 중지

- `이벤트객체.preventDefault()`: 제출 이벤트 중지

**이벤트 중지 후 알림(alert) 출력**

```html
<!DOCTYPE html>
<html>
  <body>
    <form id="my-form">
      <button type="submit">제출</button>
    </form>

    <script>
      const form = document.querySelector("#my-form");

      form.addEventListener("submit", function (event) {
        alert("폼 제출 이벤트 실행");
        event.preventDefault(); // 폼 제출 이벤트 중지
      });
    </script>
  </body>
</html>

```