## State의 불변성

- React는 State가 변경되었는지 판단할 때 **참조(주소)가 바뀌었는지**를 비교한다
- 객체나 배열을 직접 수정하면 참조가 그대로이기 때문에 React가 변경을 감지하지 못하고, 리렌더링이 일어나지 않는다

```jsx
// ❌ 직접 수정 — 같은 참조이므로 React가 변경을 감지하지 못한다
const handleBirthday = () => {
  user.age = user.age + 1; // 원본 객체를 직접 수정
  setUser(user); // 같은 객체를 전달 → 리렌더링 안 됨
};
```

```jsx
// ✅ 새 객체 생성 — 참조가 바뀌므로 React가 변경을 감지한다
const handleBirthday = () => {
  setUser({ ...user, age: user.age + 1 }); // 새 객체를 전달 → 리렌더링 발생
};
```

- 따라서 객체나 배열 State를 변경할 때는 항상 **새로운 객체/배열을 만들어서** 전달해야 한다
- 이 원칙을 불변성(immutability)이라고 한다

---

## 객체 State

- 객체 State를 변경할 때는 새로운 객체를 만들어서 전달해야 한다
- 스프레드 연산자 `...`를 활용하면 기존 값을 유지하면서 일부만 변경할 수 있다
- 예시를 보면 변수의 경우랑 다르게 객체는 새롭게 생성해서 전달됨.
    - 변수는 setAge(age + 1) 이런 느낌.

```jsx
import { useState } from "react";

const Profile = () => {
  const [user, setUser] = useState({
    name: "현우",
    age: 22,
  });

  const handleBirthday = () => {
    // 새로운 객체를 만들어서 전달
    setUser({ ...user, age: user.age + 1 });
  };

  return (
    <div>
      <p>이름: {user.name}</p>
      <p>나이: {user.age}</p>
      <button onClick={handleBirthday}>생일 축하!</button>
    </div>
  );
};

export default Profile;
```

## 객체 State로 폼 관리하기

- input이 많을 때 각각 `useState`를 만들면 코드가 길어진다
- 하나의 객체 State로 묶고, `name` 속성을 활용하면 하나의 핸들러로 모든 input을 처리할 수 있다

```jsx
import { useState } from "react";

const SignupForm = () => {
  const [form, setForm] = useState({
    name: "",
    email: "",
    age: "",
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = () => {
    console.log(form);
  };

  return (
    <div>
      <input
        name="name"
        placeholder="이름"
        value={form.name}
        onChange={handleChange}
      />
      <input
        name="email"
        placeholder="이메일"
        value={form.email}
        onChange={handleChange}
      />
      <input
        name="age"
        placeholder="나이"
        value={form.age}
        onChange={handleChange}
      />
      <button onClick={handleSubmit}>가입</button>
    </div>
  );
};

export default SignupForm;
```

- `[e.target.name]`: 대괄호 표기법(computed property)으로 input의 `name` 속성에 해당하는 key를 동적으로 변경한다
- input이 늘어나도 `handleChange` 함수를 추가할 필요가 없다

---

## 배열 State

- 배열도 객체와 마찬가지로 새로운 배열을 만들어서 전달해야 한다

### 작성

- 스프레드 연산자로 기존 배열을 복사하고, 새 항목을 추가한다
- key 값을 index로 쓰는 것은 좋지 않음. 근데 지금은 연습용이니까 그냥 쓴다.

```jsx
import { useState } from "react";

const TodoList = () => {
  const [todos, setTodos] = useState(["리액트 공부", "점심 먹기"]);
  const [input, setInput] = useState("");

  const handleAdd = () => {
    if (input.trim() === "") return;
    setTodos([...todos, input]);
    setInput("");
  };

  return (
    <div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />
      <button onClick={handleAdd}>추가</button>
      <ul>
        {todos.map((todo, index) => (
          <li key={index}>{todo}</li>
        ))}
      </ul>
    </div>
  );
};

export default TodoList;
```

### 삭제

- 삭제를 하려면 각 항목을 구별할 수 있어야 한다 → 문자열 배열을 객체 배열로 변경한다
- `filter`를 사용하여 특정 항목을 제외한 새로운 배열을 만든다

```jsx
import { useState } from "react";

const TodoList = () => {
  const [todos, setTodos] = useState([
    { id: 1, text: "리액트 공부" },
    { id: 2, text: "점심 먹기" },
  ]);
  const [input, setInput] = useState("");

  const handleAdd = () => {
    if (input.trim() === "") return;
    setTodos([...todos, { id: Date.now(), text: input }]);
    setInput("");
  };

  const handleDelete = (id) => {
    setTodos(todos.filter((todo) => todo.id !== id));
  };

  return (
    <div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />
      <button onClick={handleAdd}>추가</button>
      <ul>
        {todos.map((todo) => (
          <li key={todo.id}>
            {todo.text}
            <button onClick={() => handleDelete(todo.id)}>삭제</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TodoList;
```

### 수정

- `map`을 사용하여 특정 항목만 변경한 새로운 배열을 만든다

```jsx
import { useState } from "react";

const TodoList = () => {
  const [todos, setTodos] = useState([
    { id: 1, text: "리액트 공부", done: false },
    { id: 2, text: "점심 먹기", done: false },
  ]);
  const [input, setInput] = useState("");

  const handleAdd = () => {
    if (input.trim() === "") return;
    setTodos([...todos, { id: Date.now(), text: input, done: false }]);
    setInput("");
  };

  const handleDelete = (id) => {
    setTodos(todos.filter((todo) => todo.id !== id));
  };

  const handleToggle = (id) => {
    const newTodos = todos.map((todo) => {
      if (todo.id === id) {
        return {
          ...todo,
          done: !todo.done,
        };
      }
      return todo;
    });
    setTodos(newTodos);
  };

  return (
    <div>
      <input
        type="text"
        className="input"
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />
      <button className="button" onClick={handleAdd}>
        추가
      </button>
      <ul>
        {todos.map((todo) => (
          <li key={todo.id} >
            <span onClick={() => handleToggle(todo.id)} className={todo.done ? "line-through" : ""}>{todo.text}</span>
            <button className="button" onClick={() => handleDelete(todo.id)}>
              삭제
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TodoList;
```

---

## State 끌어올리기 (Lifting State Up)

- 여러 컴포넌트가 같은 데이터를 공유해야 할 때, 공통 부모 컴포넌트에서 State를 관리한다
- 부모가 State와 변경 함수를 자식에게 Props로 전달한다
- 모달 열기/닫기, 탭 선택, 검색 필터 등 실무에서 자주 사용되는 패턴이다

```jsx
import { useState } from "react";
import Display from "./Display";
import Controls from "./Controls";

const Container = () => {
  const [count, setCount] = useState(0);

  const increase = () => setCount(count + 1);
  const decrease = () => setCount(count - 1);

  return (
    <div>
      <Display count={count} />
      <Controls increase={increase} decrease={decrease} />
    </div>
  );
};

export default Container;
```

```jsx
const Display = ({ count }) => {
  return <p>현재 카운트: {count}</p>;
};

export default Display;
```

```jsx
const Controls = ({ increase, decrease }) => {
  return (
    <div>
      <button onClick={increase}>+1</button>
      <button onClick={decrease}>-1</button>
    </div>
  );
};

export default Controls;
```

---

## 함수형 업데이트

- `setCount(count + 1)`을 한 함수 안에서 여러 번 호출하면, 모두 같은 `count` 값을 기준으로 계산하기 때문에 한 번만 적용된다

```jsx
const increase = () => {
  setCount(count + 1); // count = 0 → 0 + 1 = 1
  setCount(count + 1); // count = 0 → 0 + 1 = 1 (같은 count 값 사용)
  setCount(count + 1); // count = 0 → 0 + 1 = 1
  // 결과: 1 (3이 아니다!)
};
```

- 이전 State 값을 기반으로 업데이트할 때는 **콜백 함수**를 전달해야 한다
- 콜백 함수의 매개변수(`prev`)에는 가장 최신의 State 값이 들어온다

```jsx
const increase = () => {
  setCount((prev) => prev + 1); // 0 → 1
  setCount((prev) => prev + 1); // 1 → 2
  setCount((prev) => prev + 1); // 2 → 3
  // 결과: 3
};
```

### 함수형 업데이트 전체 예시

```jsx
import { useState } from "react";

const Counter = () => {
  const [count, setCount] = useState(0);

  // ❌ 3씩 증가하지 않는다
  const increaseWrong = () => {
    setCount(count + 1);
    setCount(count + 1);
    setCount(count + 1);
  };

  // ✅ 3씩 증가한다
  const increaseCorrect = () => {
    setCount((prev) => prev + 1);
    setCount((prev) => prev + 1);
    setCount((prev) => prev + 1);
  };

  return (
    <div>
      <p>현재 카운트: {count}</p>
      <button onClick={increaseWrong}>+3 (잘못된 방법)</button>
      <button onClick={increaseCorrect}>+3 (올바른 방법)</button>
    </div>
  );
};

export default Counter;
```