## Hook

- 일반 함수는 호출이 끝나면 내부 변수가 사라진다

```jsx
// 일반 함수 - 호출할 때마다 count는 항상 0부터 시작
const counter = () => {
  let count = 0;
  count = count + 1;
  return count; // 항상 1
};

counter(); // 1
counter(); // 1 (이전 값을 기억하지 못한다)
```

- React 컴포넌트도 함수이기 때문에, 리렌더링(다시 호출)될 때마다 내부 변수가 초기화된다
- **Hook은 함수가 다시 호출되어도 이전 값을 기억할 수 있게 해주는 특별한 함수이다**
- React가 Hook의 값을 컴포넌트 외부에 별도로 저장해두기 때문에 리렌더링 후에도 값이 유지된다
- Hook은 항상 `use`로 시작한다 (예: `useState`, `useEffect`, `useRef` 등)

### Hook 사용 규칙

- Hook은 컴포넌트의 최상위에서만 호출해야 한다
- 조건문, 반복문 안에서 호출하면 안 된다

```jsx
// ✅ 올바른 사용 - 컴포넌트 최상위에서 호출
const Counter = () => {
  const [count, setCount] = useState(0);
  return <p>{count}</p>;
};
```

```jsx
// ❌ 잘못된 사용 - 조건문 안에서 호출
const Counter = () => {
  if (true) {
    const [count, setCount] = useState(0); // ❌ 에러 발생
  }
  return <p>카운터</p>;
};
```

---

# State

- State는 컴포넌트 내부에서 관리하는 동적인 데이터이다
- State가 변경되면 컴포넌트가 자동으로 다시 렌더링된다
- Props는 부모로부터 전달받는 읽기 전용 데이터, State는 컴포넌트가 스스로 관리하는 데이터이다

| 구분 | Props | State |
| --- | --- | --- |
| 데이터 소유 | 부모 컴포넌트 | 자기 자신 |
| 변경 가능 여부 | 읽기 전용 (변경 불가) | 변경 가능 |
| 변경 시 동작 | 부모가 변경하면 자식도 리렌더링 | State 변경 시 리렌더링 |

## useState 기본 사용법

- `useState`는 React에서 제공하는 가장 기본적인 Hook이다
- `useState(초기값)`을 호출하면 `[현재 상태, 상태 변경 함수]` 배열을 반환한다

```jsx
import { useState } from "react";

const Counter = () => {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>현재 카운트: {count}</p>
    </div>
  );
};

export default Counter;
```

- `count`: 현재 상태 값 (초기값 `0`)
- `setCount`: 상태를 변경하는 함수

---

## State 변경하기

- State를 변경할 때는 반드시 상태 변경 함수(setter)를 사용해야 한다
- 직접 변수에 값을 할당하면 리렌더링이 일어나지 않는다

올바른 State 변경

```jsx
import { useState } from "react";

const Counter = () => {
  const [count, setCount] = useState(0);

  const increase = () => {
    setCount(count + 1); // State 변경 → 리렌더링 발생
  };

  const decrease = () => {
    setCount(count - 1);
  };

  return (
    <div>
      <p>현재 카운트: {count}</p>
      <button onClick={increase}>+1</button>
      <button onClick={decrease}>-1</button>
    </div>
  );
};

export default Counter;
```

### 잘못된 State 변경

```jsx
import { useState } from "react";

const Counter = () => {
  let [count, setCount] = useState(0);

  const increase = () => {
    count = count + 1; // ❌ 직접 변경 → 리렌더링 안 됨
    console.log(count); // 값은 바뀌지만 화면에 반영되지 않는다
  };

  return (
    <div>
      <p>현재 카운트: {count}</p>
      <button onClick={increase}>+1</button>
    </div>
  );
};

export default Counter;
```

---

## 이벤트와 State

- State는 대부분 사용자의 이벤트(클릭, 입력 등)에 의해 변경된다
- 이벤트 핸들러 안에서 setter 함수를 호출하면 State가 변경되고, 화면이 자동으로 업데이트된다
- **이벤트 발생 → setter 호출 → State 변경 → 리렌더링**

### 클릭 이벤트로 State 변경

```jsx
import { useState } from "react";

const Toggle = () => {
  const [isOn, setIsOn] = useState(false);

  const handleToggle = () => {
    setIsOn(!isOn);
  };

  return (
    <div>
      <p>상태: {isOn ? "ON" : "OFF"}</p>
      <button onClick={handleToggle}>토글</button>
    </div>
  );
};

export default Toggle;
```

### 입력 이벤트로 State 변경

```jsx
import { useState } from "react";

const Greeting = () => {
  const [name, setName] = useState("");

  const handleChange = (e) => {
    setName(e.target.value);
  };

  return (
    <div>
      <input type="text" value={name} onChange={handleChange} />
      <p>안녕하세요, {name}님!</p>
    </div>
  );
};

export default Greeting;
```

---

## 여러 개의 State 사용하기

- 하나의 컴포넌트에서 여러 개의 `useState`를 사용할 수 있다

```jsx
import { useState } from "react";

const SignupForm = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [age, setAge] = useState(0);

  const handleSubmit = () => {
    console.log("이름:", name);
    console.log("이메일:", email);
    console.log("나이:", age);
  };

  return (
    <div>
      <input
        type="text"
        placeholder="이름"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <input
        type="email"
        placeholder="이메일"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="number"
        placeholder="나이"
        value={age}
        onChange={(e) => setAge(Number(e.target.value))}
      />
      <button onClick={handleSubmit}>가입</button>
    </div>
  );
};

export default SignupForm;
```