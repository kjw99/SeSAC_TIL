## JSX

- JavaScript 코드 안에서 HTML과 유사한 문법으로 UI 구조를 작성할 수 있는 JavaScript의 확장 문법
- DOM API를 대체하며, 더 간결하고 직관적인 코드를 작성할 수 있다

**DOM API 코드**

```jsx
const element = document.createElement("h1");
element.textContent = "Hello, World!";
document.body.appendChild(element);
```

**JSX 코드**

```jsx
const element = <h1>Hello, World!</h1>;
```

---

## JSX 문법 규칙

### 1개의 최상위 태그만 반환한다

- 여러 개의 태그를 반환할 수 없다. 반드시 1개의 부모 태그로 감싸야 한다
- **Fragment 태그** `<> </>` 를 사용해서 여러 개의 태그를 감싸고, 반환한다

**에러 코드**

```jsx
// 3개의 태그를 사용하지만 모든 태그를 감싸는 태그가 없다
// 에러 메세지 : Adjacent JSX elements must be wrapped in an enclosing tag
const element = (
  <div>Hello, World!</div>
  <div>Hello, React!</div>
  <div>Hello, JSX!</div>
);
```

**정상 코드**

```jsx
// 3개의 태그를 감싸는 1개의 Fragment 태그가 있다
const element = (
  <>
    <div>Hello, World!</div>
    <div>Hello, React!</div>
    <div>Hello, JSX!</div>
  </>
);
```

---

### 모든 태그는 반드시 닫는다

- **Self-closing 태그** : `<br>`, `<img>`, `<input>` 등은 `<br />`, `<img />`, `<input />` 와 같이 끝에 `/`를 붙여 닫는다
- **일반 태그** : `<div>`, `<h1>`, `<p>` 등은 반드시 쌍으로 작성한다

**에러 코드**

- Self-closing 태그를 제대로 닫지 않은 경우

```jsx
const element1 = <input type="text">;
const element2 = <img src="image.jpg">;
const element3 = <br>;
```

- 일반 태그를 닫지 않은 경우

```jsx
const element4 = <div>내용;
const element5 = <h1>제목;
```

**정상 코드**

- Self-closing 태그를 올바르게 닫은 경우

```jsx
const element1 = <input type="text" />;
const element2 = <img src="image.jpg" alt="설명" />;
const element3 = <br />;
const element4 = <hr />;
```

- 일반 태그를 올바르게 쌍으로 작성한 경우

```jsx
const element5 = <div>내용</div>;
const element6 = <h1>제목</h1>;
const element7 = <p>문단</p>;
const element8 = <span>텍스트</span>;
```

---

### 속성명은 대부분 카멜케이스(camelCase)로 작성한다

- 카멜케이스: 속성명의 첫 글자를 소문자로 작성하고, 나머지 단어의 첫 글자를 대문자로 작성하는 방법
- HTML 처럼 보이겠지만 JSX를 사용중!
- `class`(JavaScript의 예약어) → `className`
- `for`(JavaScript의 예약어) → `htmlFor`
- `onclick` → `onClick`
- `onchange` → `onChange`
- `readonly` → `readOnly`

**HTML 속성명과 JSX 속성명 비교**

```jsx
// HTML 속성명 → JSX 속성명
const examples = (
  <>
    {/* class → className */}
    <div className="my-class">클래스</div>

    {/* onclick → onClick */}
    <button onClick={handleClick}>버튼</button>

    {/* onchange → onChange */}
    <input onChange={handleChange} />

    {/* for → htmlFor */}
    <label htmlFor="username">이름</label>
    <input id="username" />

    {/* readonly → readOnly */}
    <input readOnly={true} />
  </>
);
```

---

### style은 객체로 작성한다

- `style={{key: value}}` 형태로 작성
- 키(CSS 속성명)는 카멜케이스(camelCase)로 작성하며, 값(CSS 값)은 문자열로 작성
- 하이픈()으로 구분된 CSS 속성명은 카멜케이스로 변환한다 (예: `font-size` → `fontSize`)
- 중괄호가 2개인 이유는 JSX 보간법의 중괄호 안에 객체를 작성하기 때문
    - 바깥의 {}는 보간법에 대한 중괄호. 안에 있는 것은 객체에 대한 중괄호.
    - 그래서 바깥에 객체를 생성해서 style에 집어 넣는 것도 가능.

**JSX style 작성**

```jsx
const styleExamples = (
  <div
    style={{
      // background-color → backgroundColor
      backgroundColor: "#f8f9fa",

      // font-size → fontSize
      fontSize: "16px",

      // font-weight → fontWeight
      fontWeight: "bold",

      // text-align → textAlign
      textAlign: "center",

      // line-height → lineHeight
      lineHeight: "1.6",

      // border-radius → borderRadius
      borderRadius: "8px",

      // box-shadow → boxShadow
      boxShadow: "0 2px 4px rgba(0,0,0,0.1)",

      // z-index → zIndex
      zIndex: 1000,

      // margin-top → marginTop
      marginTop: "20px",

      // padding-left → paddingLeft
      paddingLeft: "15px",
    }}
  ></div>
);
```

---

## JSX 보간법(Interpolation)

- 중괄호 `{}`를 사용하여 JSX 내부에 표현식을 삽입하는 방법
    - 표현식에는 하나의 값으로 귀결되는 것들만 올 수 있다! 그래서 if, for 같은건 안댐. 삼항 연산자는 가능
- 문자열 사이에 표현식을 삽입하는 템플릿 리터럴과는 다른 개념
- { } 안에는 자바 스크립트가 된다! 는 느낌.

**변수 삽입**

```jsx
const name = "김철수";
const age = 25;

const greeting = <h1>안녕하세요, {name}님!</h1>;
const profile = <p>나이: {age}세</p>;
```

**표현식 삽입**

```jsx
const a = 10;
const b = 20;

const calculation = <p>계산 결과: {a + b}</p>;
const comparison = <p>더 큰 수: {a > b ? a : b}</p>;
const isAdult = <p>성인 여부: {age >= 18 ? "성인" : "미성년자"}</p>;
```

**함수 호출 삽입**

```jsx
function getCurrentTime() {
  return new Date().toLocaleTimeString();
}

const timeDisplay = <p>현재 시간: {getCurrentTime()}</p>;
const upperCaseName = <h2>{name.toUpperCase()}</h2>;
```

**객체 속성 삽입**

```jsx
const user = {
  name: "이영희",
  email: "younghee@example.com",
  age: 28,
};

const userInfo = (
  <>
    <h1>{user.name}</h1>
    <p>이메일: {user.email}</p>
    <p>나이: {user.age}세</p>
  </>
);
```

**배열 요소 삽입**

```jsx
const colors = ["빨강", "파랑", "초록"];
const numbers = [1, 2, 3, 4, 5];

const colorList = (
  <>
    <p>첫 번째 색상: {colors[0]}</p>
    <p>두 번째 색상: {colors[1]}</p>
    <p>숫자 합계: {numbers[0] + numbers[1] + numbers[2]}</p>
  </>
);
```

---

### 주석은 `{/* */}` 로 작성한다

- HTML 주석 `<!-- -->` 은 JSX에서 사용할 수 없다
- JavaScript 주석 `//`, `/* */` 을 중괄호로 감싸서 사용한다

```jsx
const element = (
  <div>
    {/* 한 줄 주석 */}
    <h1>제목</h1>

    {/*
      여러 줄 주석
      이렇게 작성한다
    */}
    <p>내용</p>
  </div>
);
```