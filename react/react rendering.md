## 조건부 렌더링(Conditional Rendering)

- 조건에 따라 다른 화면을 사용자에게 보여주는 방법
- **삼항 연산자** 와 **논리 연산자** 로 화면을 제어한다
- 로그인/로그아웃 상태, 경고 메시지, 로딩 스피너 등 다양한 상황에서 활용된다

### JSX에서 값의 렌더링

- JSX의 `{}` 안에 값을 넣으면 화면에 표시할 수 있다
- 단, 모든 값이 화면에 표시되는 것은 아니다

**화면에 표시되는 값**

```jsx
<p>{"hello"}</p>    {/* hello 출력 */}
<p>{42}</p>         {/* 42 출력 */}
<p>{0}</p>          {/* 0 출력 */}
```

**화면에 표시되지 않는 값**

```jsx
<p>{true}</p>       {/* 아무것도 안 보임 */}
<p>{false}</p>      {/* 아무것도 안 보임 */}
<p>{null}</p>       {/* 아무것도 안 보임 */}
<p>{undefined}</p>  {/* 아무것도 안 보임 */}
```

- `true`, `false`, `null`, `undefined`는 화면에 아무것도 표시되지 않는다
- 이 특성을 이용해서 조건부 렌더링을 구현할 수 있다

---

## 삼항 연산자 활용 조건부 렌더링

- 로그인/로그아웃, 로딩/완료, 에러/정상, 활성/비활성 등 두 가지 중 하나의 상태에 따라 화면을 보여줘야 할 때 활용한다.

### 삼항 연산자

- 조건식 결과에 따라 다른 값을 반환하는 연산자

```jsx
조건 ? 참일 때 요소 : 거짓일 때 요소
```

```jsx
let x = 7;

const result = x % 2 === 0 ? "짝수" : "홀수";
console.log(result); // 홀수
```

### 로그인 상태 예시

**LoginStatus.jsx**

```jsx
const LoginStatus = ({ isLogin }) => {
  return (
    <>
      <h1>로그인 상태: {isLogin ? "로그인" : "로그아웃"}</h1>
      <p>{isLogin ? "환영합니다!" : "로그인 해주세요."}</p>
      <button>{isLogin ? "로그아웃" : "로그인"}</button>
    </>
  );
};

export default LoginStatus;
```

**RenderingContainer.jsx**

```jsx
import LoginStatus from "./LoginStatus";

const RenderingContainer = () => {
  return (
    <>
      <LoginStatus isLogin={false} />
      <LoginStatus isLogin={true} />
    </>
  );
};

export default RenderingContainer;
```

---

## 논리 연산자 활용 조건부 렌더링

- 경고 메시지, 안내 문구, 새 알림 뱃지 등 조건이 참일 때만 보여주는 화면에 적합하다

### 논리 연산자 &&

- 왼쪽 조건이 참이면 오른쪽 값을 반환하고, 거짓이면 왼쪽 값을 그대로 반환하는 연산자
- react에서는
    - 왼쪽 조건이 참일 때만 오른쪽 값을 화면에 보여준다.
    - 조건이 거짓이면 아무것도 렌더링하지 않는다

```jsx
조건 && 보여줄 요소;
```

```jsx
let x = 8;
let y = 9;

const result = x % 2 === 0 && "짝수";
const result2 = y % 2 === 0 && "짝수";
console.log(result); // 짝수
console.log(result2); // false
```

### 삼항 연산자와의 차이점

- 삼항 연산자
    - `{조건} ? A : B` {조건}이라면 A를, 아니라면 B를 보여줘
    - 두개의 요소 중 하나는 반드시 보여준다.
- `&&` 연산자
    - `{조건} && A` {조건}라면 A를 보여줘, 아니라면 아무것도 안 보여줘
    - 특정 요소를 보여주거나 보여주지 않는다.

### 관리자 권한 확인 예시

**AdminLink.jsx**

```jsx
const AdminLink = ({ isAdmin }) => {
  return (
    <div>
      <p>현재 권한 : {isAdmin ? "관리자" : "일반 사용자"}</p>

      {isAdmin && <a>관리 페이지 이동</a>}
    </div>
  );
};

export default AdminLink;
```

**RenderingContainer.jsx**

```jsx
import LoginStatus from "./LoginStatus";
import AdminLink from "./AdminLink";

const RenderingContainer = () => {
  return (
    <>
      <LoginStatus isLogin={false} />
      <LoginStatus isLogin={true} />
      <AdminLink isAdmin={false} />
      <AdminLink isAdmin={true} />
    </>
  );
};

export default RenderingContainer;
```

---

## 조건에 따라 className 변경하기

- 삼항 연산자를 사용하여 조건에 따라 다른 CSS 클래스를 적용할 수 있다
- 텍스트뿐만 아니라 스타일도 조건부로 바꿀 수 있다

```jsx
<요소 className={조건 ? "클래스A" : "클래스B"}>
```

**index.css**

```css
.done {
  text-decoration: line-through;
  color: gray;
}
```

**TodoItem.jsx**

```jsx
const TodoItem = ({ text, isDone }) => {
  return (
    <span className={isDone ? "done" : ""}>{text}</span>
  );
};

export default TodoItem;
```

- `isDone`이 `true`면 `"done"` 클래스가 적용되어 취소선이 표시된다
- `isDone`이 `false`면 빈 문자열 `""`이 적용되어 일반 텍스트로 표시된다

### 여러 클래스를 조건부로 조합하기

- 기본 클래스는 항상 적용하고, 조건에 따라 클래스를 추가할 수 있다
- 템플릿 리터럴을 사용하여 여러 클래스를 조합한다

```jsx
<span className={`todo-item ${isDone ? "done" : ""}`}>{text}</span>
```

- `isDone`이 `true`면 `"todo-item done"` (두 클래스 모두 적용)
- `isDone`이 `false`면 `"todo-item "` (기본 클래스만 적용)

**여러 조건을 조합하는 경우**

```jsx
<span className={`todo-item ${isDone ? "done" : ""} ${isImportant ? "important" : ""}`}>
  {text}
</span>
```

- `isDone`이 `true`이고 `isImportant`가 `true`면 `"todo-item done important"`
- `isDone`이 `false`이고 `isImportant`가 `true`면 `"todo-item important"`

## 리스트 렌더링

- 배열에 저장된 여러 개의 데이터를 화면에 렌더링 하는 방법
- 배열의 고차 메서드 `map()` 로 JSX 요소(Element)를 반복적으로 생성한다

### `map()` 메서드

- 배열 내 각 원소에 콜백 함수를 적용하여 원소를 변환한 새로운 배열을 생성한다

```jsx
const newArray = array.map((element) => {
  return 반환값;
});
```

```jsx
const array = [1, 2, 3, 4, 5];
const newArray = array.map((value) => {
  return value * 2;
});
console.log(newArray); // [2, 4, 6, 8, 10]
```

### 배열 데이터 렌더링

**배열 기본 구조 데이터 렌더링**

```jsx
import React from "react";

const Numbers = () => {
  const array = [1, 2, 3, 4, 5];
  return (
    <ul>
      {array.map((el) => (
        <li>{el}</li>
      ))}
    </ul>
  );
};

export default Numbers;

```

**배열 내 객체 데이터 렌더링**

```jsx
const Students = () => {
  const array = [
    { id: 1, name: "철수" },
    { id: 2, name: "영희" },
    { id: 3, name: "동수" },
  ];

  return (
    <>
      {array.map((value) => {
        return (
          <div key={value.id}>
            <span>id:{value.id} / </span>
            <span>name:{value.name}</span>
          </div>
        );
      })}
    </>
  );
}

export default Students;
```

## 리스트 아이템 key 속성

- 리스트 아이템을 구분하는 **고유한 값(식별자)**
- key가 없으면 성능 저하 및 예기치 않은 UI 동작이 발생할 수 있다
- 배열 내 객체에 저장된 고유한 값(식별자)을 key로 사용한다
- 배열의 인덱스는 key로 사용하면 안 된다

```jsx
const newArray = array.map((element) => {
  return <li key={고유값 속성}></li>;
});
```

**객체의 고유한 값을 key로 활용**

```jsx
const TodoList = () => {
  const todos = [
    { id: 1, text: "공부하기" },
    { id: 2, text: "운동하기" },
    { id: 3, text: "휴식하기" },
  ];

  return (
    <ul>
      {todos.map((todo) => (
        // 객체의 고유한 값 id 속성을 key로 활용
        <li key={todo.id}>{todo.text}</li>
      ))}
    </ul>
  );
}

export default TodoList;
```

### **key를 사용하는 이유**

- React가 화면을 업데이트할 때 어떤 요소가 변경되었는지 알기 위한 식별자로 활용한다.
- 리스트에서 특정 항목이 삭제되었을 때, 리액트는 내용을 보고 삭제를 식별하는 것이 아니라 key를 활용하여 식별한다.
    - key가 있는 경우 식별하여 해당 원소만 삭제한다.
    - key가 없는 경우 어떤 항목이 변경되었는지 정확히 알 수 없어 전체 리스트를 다시 렌더링한다.
- 배열의 인덱스(`array.map((item, index) => <li key={index}>`)를 key로 사용하면 안 되는 이유는 항목의 순서가 바뀌거나 삭제될 때 인덱스도 함께 바뀌기 때문에 식별자로서의 의미가 없기 때문이다.