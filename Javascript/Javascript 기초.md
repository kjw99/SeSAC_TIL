## JavaScript

- HTML과 CSS와 함께 웹 개발의 핵심 언어로, 웹 페이지에 동적인 기능을 추가하는 프로그래밍 언어이다.
- JavaScript는 브라우저에서 실행되며, 사용자의 동작(이벤트)에 따라 반응하는 웹 페이지를 만들 수 있다.
- Node.js의 등장 이후, 웹 페이지 개발 외에도 다양한 환경에서 사용 가능해졌다.

### Node.js

- 브라우저에서 사용하는 V8 자바스크립트 엔진을 브라우저 밖으로 가져와 브라우저 밖에서도 코드를 실행할 수 있게 해주는 환경이다.

[Node.js — Node.js® 다운로드](https://nodejs.org/ko/download)

- node는 최신 버전과 호환성 문제가 있는 경우가 많아, `v22`를 사용할 예정이다.

- node 버전 확인
    
    터미널에서
    
    ```python
    node -v
    ```
    

## JavaScript 코드 작성과 실행

- 웹 브라우저, HTML 문서, Node.js 환경에서 JavaScript 코드 작성과 실행 가능
- JS는 문장이 끝날 때 `;` 을 붙여야 하지만, ASI(Automatic Semicolon Insertion)라는 개발자가 명시적으로 작성하지 않아도 엔진이 적절한 위치에 삽입해준다.
    - 단, 가끔씩 의도하지 않은 위치에 삽입할 수 있다.

### console.log()

- 브라우저 개발자 도구의 콘솔 창에 메세지 출력
- 디버깅 용도로 사용
- 그 밖에 `console.error()`, `console.warn()`, `console.info()`, `console.table()` 등이 있다

**예시**

```jsx
console.log("Hello, World!");
```

### 개발자 도구 내 Console 메뉴

- 브라우저 개발자 도구의 `Console` 메뉴에서 코드 실행 가능

### HTML 문서 `<script>`

- HTML 문서 내에서 `<script>` 를 사용해 JavaScript 코드 작성과 실행
- `<script>` 는 `<body>` 내부 끝에 위치

**예시**

```html
<!DOCTYPE html>
<html>
  <head></head>
  <body>
    <h1>Hello, HTML!</h1>
    <script>
      console.log("Hello, JavaScript!");
    </script>
  </body>
</html>

```

### HTML 문서 외부 JavaScript 파일 불러오기

- JavaScript 코드가 작성된 `.js` 파일을 HTML 문서에서 불러오기
- 여러 HTML 문서에서 동일한 JavaScript 코드 재사용 가능
- 마치 `<link>` 를 사용해 CSS 파일을 불러오는 것과 같다

**예시**

```html
<!DOCTYPE html>
<html>
  <body>
    <h1>Hello, HTML!</h1>
    <script src="./main.js"></script>
  </body>
</html>

```

```jsx
// main.js
console.log("Hello, JavaScript!");

```

### `.js` 확장자 파일

- Node.js 설치 후 `node` 명령어로 `.js` 파일 실행
- 실행 과정
    1. `.js` 파일 생성
    2. 코드 작성
    3. 터미널에서 `node 파일명.js` 실행
