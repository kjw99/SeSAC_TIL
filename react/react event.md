## 리액트에서의 이벤트 핸들링

- HTML 인라인 이벤트 속성(`onClick`, `onChange` 등)을 사용해서 이벤트 핸들링 함수를 호출한다
- `addEventListener` 메서드는 사용하지 않는다

## addEventListener vs React 이벤트

```jsx
// 기존 JavaScript 방식
const button = document.querySelector("button");

button.addEventListener("click", () => {
  alert("클릭!");
});
```

```jsx
// React 방식
const App = () => {
  const handleClick = () => {
    alert("클릭!");
  };

  return <button onClick={handleClick}>버튼</button>;
};
```

---

## 이벤트 핸들러 전달 방식

### 파라미터가 없을 때

- 함수 참조만 전달한다
- `()` 없이 함수 이름만 작성한다
- 핸들러 함수의 첫 번째 인자로 `event` 객체가 자동으로 전달된다 (사용하지 않으면 안 받아도 된다)

```jsx
// 핸들러 정의
const handleClick = (event) => {
  alert("클릭!");
};

// JSX
<button onClick={handleClick}>버튼</button>
```

### 파라미터가 있을 때

- 화살표 함수로 감싸서 호출한다
- 감싸지 않고 `onClick={handleClick("값")}` 이렇게 쓰면 렌더링 시점에 즉시 실행되므로 주의한다
- 핸들러 함수의 파라미터는 호출 시 전달하는 값에 맞춰서 정의한다

```jsx
// 핸들러 정의
const handleClick = (buttonName) => {
  alert(`${buttonName} 클릭`);
};

// JSX
<button onClick={() => handleClick("1번 버튼")}>1번 버튼</button>
```

### event 객체와 함께 쓸 때

- 화살표 함수의 파라미터로 `event`를 받아서 핸들러에 전달한다
- `event.target.value` 등으로 입력 값에 접근할 수 있다
- 핸들러 함수의 첫 번째 파라미터로 `event`를 받도록 정의한다

```jsx
// 핸들러 정의
const handleChange = (event) => {
  console.log(event.target.value);
};

// JSX
<input type="text" onChange={(event) => handleChange(event)} />
```

### event 객체와 파라미터를 함께 쓸 때

- 화살표 함수에서 `event`와 파라미터를 모두 전달한다
- 핸들러 함수의 파라미터 순서를 호출 시 전달하는 순서에 맞춰서 정의한다

```jsx
// 핸들러 정의
const handleChange = (event, fieldName) => {
  console.log(`${fieldName}: ${event.target.value}`);
};

// JSX
<input onChange={(event) => handleChange(event, "이름")} />
```

---

## 예시

### onClick 이벤트

```jsx
const ClickExample = () => {
  // 파라미터가 없는 함수
  const helloClick = () => {
    alert("Hello, World!");
  };

  // 파라미터가 있는 함수
  const handleClick = (buttonName) => {
    alert(`${buttonName} 클릭`);
  };

  return (
    <div>
      <div onClick={helloClick}>Hello, World!</div>
      <button onClick={() => handleClick("1번 버튼")}>1번 버튼</button>
      <button onClick={() => handleClick("2번 버튼")}>2번 버튼</button>
      <button onClick={() => handleClick("3번 버튼")}>3번 버튼</button>
    </div>
  );
};

export default ClickExample;
```

### onChange 이벤트

- `onChange` 이벤트를 사용해서 입력 이벤트를 처리하는 것을 권장한다
- `onInput` 이벤트는 사용하지 않는다
    - 기존 JavaScript에서 `oninput`은 키 입력마다 즉시 발생하고, `onchange`는 포커스를 잃을 때 발생한다
    - React에서는 `onChange`가 키 입력마다 즉시 발생하므로 (기존 `oninput`과 동일한 동작), `onInput`을 따로 쓸 필요가 없다

```jsx
const ChangeExample = () => {
  const handleChange = (event) => {
    console.log(`입력 이벤트 발생, 입력 값: ${event.target.value}`);
  };

  return (
    <div>
      <input type="text" onChange={(event) => handleChange(event)} />
    </div>
  );
};

export default ChangeExample;
```

### onSubmit 이벤트

- `event.preventDefault()` : 브라우저의 기본 동작(폼 제출 시 페이지 새로고침)을 막는다

```jsx
const SubmitExample = () => {
  const handleSubmit = (event) => {
    event.preventDefault();

    // FormData : form 요소의 입력 값을 쉽게 가져올 수 있는 객체
    const formData = new FormData(event.target);

    // formData.get("name속성값")으로 각 입력 값을 가져온다
    console.log(`이메일 입력 값: ${formData.get("email")}`);
    console.log(`비밀번호 입력 값: ${formData.get("password")}`);
    console.log(`이름 입력 값: ${formData.get("name")}`);
  };

  return (
    <div>
      <form onSubmit={(event) => handleSubmit(event)}>
        <input type="email" name="email" placeholder="Email" />
        <input type="password" name="password" placeholder="Password" />
        <input type="text" name="name" placeholder="Name" />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default SubmitExample;
```

### onKeyDown 이벤트

- 키보드 입력 이벤트를 처리할 때 사용한다
- `event.key`로 어떤 키가 눌렸는지 확인할 수 있다

```jsx
const KeyDownExample = () => {
  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      alert(`입력 값: ${event.target.value}`);
    }
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Enter 키를 눌러보세요"
        onKeyDown={(event) => handleKeyDown(event)}
      />
    </div>
  );
};

export default KeyDownExample;
```

### onFocus / onBlur 이벤트

- `onFocus` : 요소에 포커스가 들어올 때 발생한다
- `onBlur` : 요소에서 포커스가 빠져나갈 때 발생한다

```jsx
const FocusBlurExample = () => {
  const handleFocus = () => {
    console.log("입력창에 포커스가 들어왔습니다");
  };

  const handleBlur = (event) => {
    const value = event.target.value;

    if (value.length < 2) {
      alert("2글자 이상 입력해주세요");
    }
  };

  return (
    <div>
      <input
        type="text"
        placeholder="이름을 입력하세요"
        onFocus={handleFocus}
        onBlur={(event) => handleBlur(event)}
      />
    </div>
  );
};

export default FocusBlurExample;
```

### react 이벤트 종류 확인

[Common components (e.g. div) – React](https://react.dev/reference/react-dom/components/common#common-props)