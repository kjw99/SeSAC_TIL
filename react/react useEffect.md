# useEffect

- 컴포넌트가 **렌더링된 후** 특정 작업을 실행하기 위한 Hook이다
- "화면이 그려진 다음에 이 작업을 해줘" 라고 React에 요청하는 것이다
- 주로 다음과 같은 상황에서 사용한다:
    - 페이지가 열리면 서버에서 데이터 가져오기 (API 호출)
    - 검색어가 바뀔 때마다 검색 결과 다시 가져오기
    - 카테고리를 선택할 때마다 해당 카테고리의 상품 목록 가져오기

## 왜 useEffect가 필요할까?

- 컴포넌트 함수 안에 API 호출 코드를 그냥 쓰면 **렌더링될 때마다** 실행된다
- State가 변경되면 컴포넌트가 리렌더링되므로, API 호출이 무한 반복될 수 있다

```jsx
// ❌ 잘못된 방식 - 렌더링될 때마다 API 호출이 실행된다
const App = () => {
  const [data, setData] = useState(null);

  // 이 코드는 렌더링될 때마다 실행된다
  // setData → 리렌더링 → 또 API 호출 → setData → 리렌더링 → 무한 반복!
  const fetchData = async () => {
    const response = await axios.get("https://api.example.com/data");
    setData(response.data);
  };
  fetchData();

  return <div>{data}</div>;
};
```

- `useEffect`를 사용하면 **언제 실행할지** 제어할 수 있다

---

## useEffect 기본 사용법

- `useEffect`는 두 개의 인자를 받는다
    1. **콜백 함수**: 실행할 작업
    2. **의존성 배열(dependency array)**: 언제 실행할지 결정하는 조건

```jsx
useEffect(() => {
  // 실행할 작업
}, [의존성]);
```

### 의존성 배열에 따른 실행 시점

| 의존성 배열 | 실행 시점 |
| --- | --- |
| `[]` (빈 배열) | 컴포넌트가 처음 렌더링될 때 **1번만** 실행 |
| `[value]` | 처음 렌더링 + `value`가 변경될 때마다 실행 |
| 생략 | 처음 렌더링 + **매 렌더링마다** 실행 (성능 문제가 생기기 쉬워 거의 사용하지 않음) |

### 빈 의존성 배열 `[]`

- 컴포넌트가 화면에 처음 나타날 때 **딱 한 번만** 실행된다
- API 호출, 초기 데이터 로딩 등에 가장 많이 사용한다

```jsx
import { useState, useEffect } from "react";

const CounterEmpty = () => {
  const [count, setCount] = useState(0);

  useEffect(() => {
    console.log("처음 한 번만 실행됩니다!");
  }, []); // ← 빈 배열: 처음 1번만 실행

  return (
    <div>
      <p>카운트: {count}</p>
      <button onClick={() => setCount(count + 1)}>+1</button>
    </div>
  );
};

export default CounterEmpty;
```

- 버튼을 아무리 눌러도 콘솔에는 메시지가 **1번만** 출력된다
- `count`가 변경되어 리렌더링이 일어나도 `useEffect`는 다시 실행되지 않는다

### 의존성 배열에 값 넣기 `[value]`

- 배열에 넣은 값이 **변경될 때마다** 콜백 함수가 다시 실행된다
- "이 값이 바뀌면 이 작업을 다시 해줘" 라는 의미이다

```jsx
import { useState, useEffect } from "react";

const CounterValue = () => {
  const [count, setCount] = useState(0);

  useEffect(() => {
    console.log(`count가 ${count}으로 변경되었습니다!`);
  }, [count]); // ← count가 변경될 때마다 실행

  return (
    <div>
      <p>카운트: {count}</p>
      <button onClick={() => setCount(count + 1)}>+1</button>
    </div>
  );
};

export default CounterValue;
```

- 버튼을 누를 때마다 `count`가 변경되고, `useEffect`가 다시 실행된다

### 의존성이 여러 개인 경우

- 배열에 여러 값을 넣을 수 있다
- 배열 안의 값 중 **하나라도** 변경되면 실행된다

```jsx
import { useState, useEffect } from "react";

const Profile = () => {
  const [name, setName] = useState("");
  const [age, setAge] = useState(0);

  useEffect(() => {
    console.log(`이름: ${name}, 나이: ${age}`);
  }, [name, age]); // ← name 또는 age가 변경되면 실행

  return (
    <div>
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="이름"
      />
      <button onClick={() => setAge(age + 1)}>나이 +1 (현재: {age})</button>
    </div>
  );
};

export default Profile;
```

---

## useEffect + Axios로 데이터 가져오기

- Axios는 외부 라이브러리이므로 먼저 설치해야 한다

```bash
npm install axios
```

- 실무에서 가장 많이 사용하는 패턴이다
- 흐름: **컴포넌트 렌더링 → useEffect 실행 → API 호출 → 받은 데이터를 State에 저장 → 리렌더링**
- fetchUsers 의 경우 useEffect 에서만 쓰기 때문에 useEffect 안에서 선언.

```jsx
import { useState, useEffect } from "react";
import axios from "axios";

const UserList = () => {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    const fetchUsers = async () => {
      const response = await axios.get(
        "https://jsonplaceholder.typicode.com/users"
      );
      setUsers(response.data);
    };

    fetchUsers();
  }, []); // ← 빈 배열: 처음 1번만 API 호출

  return (
    <div>
      <h2>사용자 목록</h2>
      <ul>
        {users.map((user) => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default UserList;
```

### useEffect 안에서 async를 사용하는 방법

- `useEffect`의 콜백 함수 자체에는 `async`를 직접 붙일 수 없다
- `useEffect`는 return 값으로 정리 함수만 받을 수 있는데, `async` 함수는 항상 Promise를 반환하기 때문이다
- 내부에 `async` 함수를 별도로 만들어서 호출해야 한다

```jsx
// ❌ 잘못된 방식 - useEffect 콜백에 직접 async를 붙이면 안 된다
useEffect(async () => {
  const response = await axios.get("/api/data");
  setData(response.data);
}, []);
```

```jsx
// ✅ 올바른 방식 - 내부에 async 함수를 만들어서 호출한다
useEffect(() => {
  const fetchData = async () => {
    const response = await axios.get("/api/data");
    setData(response.data);
  };

  fetchData();
}, []);
```

---

## 로딩 상태 관리

- API 호출은 시간이 걸리므로, 데이터를 받아오는 동안 로딩 화면을 보여주는 것이 좋다
- `loading` State를 추가하여 로딩 상태를 관리한다
- 실무에서는 `try/catch`로 에러 처리도 함께 하지만, 여기서는 로딩 상태에 집중한다

```jsx
import { useState, useEffect } from "react";
import axios from "axios";

const UserList = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUsers = async () => {
      const response = await axios.get(
        "https://jsonplaceholder.typicode.com/users"
      );
      setUsers(response.data);
      setLoading(false);
    };

    fetchUsers();
  }, []);

  if (loading) {
    return <p>로딩 중...</p>;
  }

  return (
    <div>
      <h2>사용자 목록</h2>
      <ul>
        {users.map((user) => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default UserList;
```

---

## 에러 처리 (try / catch)

- API 호출은 항상 실패할 가능성이 있다 (서버 다운, 네트워크 끊김, 잘못된 URL 등)
- `try/catch`로 에러를 처리하지 않으면, 에러 발생 시 로딩 화면에서 멈춰버린다
- `error` State를 추가하여 에러 메시지를 화면에 표시한다
- `finally`에 `setLoading(false)`를 넣으면, 성공/실패와 관계없이 로딩이 항상 끝난다
    - `try` 블록 안에 `setLoading(false)`를 넣으면 에러 발생 시 실행되지 않아 로딩 화면에서 멈춘다

```jsx
import { useState, useEffect } from "react";
import axios from "axios";

const UserList = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await axios.get(
          "https://jsonplaceholder.typicode.com/users"
        );
        setUsers(response.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  if (loading) {
    return <p>로딩 중...</p>;
  }

  if (error) {
    return <p>에러 발생: {error}</p>;
  }

  return (
    <div>
      <h2>사용자 목록</h2>
      <ul>
        {users.map((user) => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default UserList;
```

### 에러 처리 없이 vs 에러 처리 후 비교

```jsx
// ❌ 에러 처리 없음 - 에러 발생 시 로딩 화면에서 영원히 멈춘다
useEffect(() => {
  const fetchUsers = async () => {
    const response = await axios.get("https://잘못된주소.com/users");
    setUsers(response.data);
    setLoading(false); // 에러가 나면 이 줄은 실행되지 않는다
  };

  fetchUsers();
}, []);
```

```jsx
// ✅ 에러 처리 있음 - 에러가 나도 로딩이 끝나고 에러 메시지를 보여준다
useEffect(() => {
  const fetchUsers = async () => {
    try {
      const response = await axios.get("https://잘못된주소.com/users");
      setUsers(response.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  fetchUsers();
}, []);
```

---

## 옵셔널 체이닝 (`?.`)으로 안전하게 데이터 접근하기

- API에서 받아온 데이터는 **아직 도착하지 않았거나**, 예상과 다른 구조일 수 있다
- 존재하지 않는 속성에 접근하면 에러가 발생한다
- `?.` (옵셔널 체이닝)을 사용하면 값이 `null`이나 `undefined`일 때 **에러 없이 `undefined`를 반환**한다

### 옵셔널 체이닝 기본 문법

```jsx
// ❌ 일반 접근 - user가 null이면 에러 발생
console.log(user.address.city); // TypeError: Cannot read properties of null

// ✅ 옵셔널 체이닝 - user가 null이면 undefined 반환 (에러 없음)
console.log(user?.address?.city); // undefined
```

### useEffect + API 호출에서 활용

- API로 단일 객체를 가져올 때, 데이터가 도착하기 전에는 State가 `null`이다
- `?.`을 사용하면 데이터가 아직 없을 때도 안전하게 렌더링할 수 있다

```jsx
import { useState, useEffect } from "react";
import axios from "axios";

const UserProfile = () => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const fetchUser = async () => {
      const response = await axios.get(
        "https://jsonplaceholder.typicode.com/users/1"
      );
      setUser(response.data);
    };

    fetchUser();
  }, []);

  return (
    <div>
      <h2>사용자 프로필</h2>
      {/* ❌ user가 null일 때 에러 발생 */}
      {/* <p>이름: {user.name}</p> */}
      {/* <p>도시: {user.address.city}</p> */}

      {/* ✅ 옵셔널 체이닝으로 안전하게 접근 */}
      <p>이름: {user?.name}</p>
      <p>이메일: {user?.email}</p>
      <p>도시: {user?.address?.city}</p>
      <p>회사: {user?.company?.name}</p>
    </div>
  );
};

export default UserProfile;
```

- `user`가 `null`인 동안(API 응답 전)에는 `user?.name`이 `undefined`를 반환하여 아무것도 표시되지 않는다
- API 응답이 도착하면 `setUser`로 State가 업데이트되고, 리렌더링되어 데이터가 표시된다

---

## 의존성 배열을 활용한 API 재호출

- 의존성 배열에 값을 넣으면, 해당 값이 바뀔 때마다 **API를 다시 호출**할 수 있다
- "카테고리가 바뀌면 서버에서 해당 카테고리의 데이터를 다시 가져와줘" 라는 패턴이다

```jsx
import { useState, useEffect } from "react";
import axios from "axios";

const PostList = () => {
  const [userId, setUserId] = useState(1);
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPosts = async () => {
      setLoading(true);
      const response = await axios.get(
        `https://jsonplaceholder.typicode.com/posts?userId=${userId}`
      );
      setPosts(response.data);
      setLoading(false);
    };

    fetchPosts();
  }, [userId]); // ← userId가 변경될 때마다 API를 다시 호출

  return (
    <div>
      <select value={userId} onChange={(e) => setUserId(Number(e.target.value))}>
        <option value={1}>사용자 1</option>
        <option value={2}>사용자 2</option>
        <option value={3}>사용자 3</option>
      </select>
      {loading ? (
        <p>로딩 중...</p>
      ) : (
        <ul>
          {posts.map((post) => (
            <li key={post.id}>{post.title}</li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default PostList;
```

- 사용자를 선택할 때마다 `userId`가 변경되고, `useEffect`가 다시 실행되어 해당 사용자의 게시글을 가져온다

---

## 정리 함수 (Cleanup Function)

- `useEffect`의 콜백 함수에서 `return`으로 함수를 반환하면, 컴포넌트가 화면에서 사라질 때(언마운트) 해당 함수가 실행된다
- 타이머, 이벤트 리스너 등 **정리가 필요한 작업**을 해제할 때 사용한다

```jsx
useEffect(() => {
  // 실행할 작업

  return () => {
    // 정리 함수: 컴포넌트가 사라질 때 실행
  };
}, []);
```

### 타이머 정리 예시

- `setInterval`로 타이머를 설정하면, 컴포넌트가 사라져도 타이머는 계속 동작한다
- 정리 함수가 없는 타이머와 있는 타이머를 비교해보자

```jsx
// BadTimer.jsx
// ❌ 정리 함수가 없는 경우 - 컴포넌트가 사라져도 타이머가 계속 실행된다
import { useState, useEffect } from "react";

const BadTimer = () => {
  const [seconds, setSeconds] = useState(0);

  useEffect(() => {
    const timerId = setInterval(() => {
      console.log("❌ 타이머 실행 중..."); // 컴포넌트가 사라져도 계속 출력된다
      setSeconds((prev) => prev + 1);
    }, 1000);
  }, []);

  return <p>❌ {seconds}초 경과</p>;
};

export default BadTimer;
```

```jsx
// GoodTimer.jsx
// ✅ 정리 함수가 있는 경우 - 컴포넌트가 사라지면 타이머도 해제된다
import { useState, useEffect } from "react";

const GoodTimer = () => {
  const [seconds, setSeconds] = useState(0);

  useEffect(() => {
    const timerId = setInterval(() => {
      console.log("✅ 타이머 실행 중...");
      setSeconds((prev) => prev + 1);
    }, 1000);

    return () => {
      console.log("✅ 타이머 정리!");
      clearInterval(timerId); // 컴포넌트가 사라지면 타이머 해제
    };
  }, []);

  return <p>✅ {seconds}초 경과</p>;
};

export default GoodTimer;
```

```jsx
// TimerContainer.jsx
import { useState } from "react";
import BadTimer from "./BadTimer";
import GoodTimer from "./GoodTimer";

const TimerContainer = () => {
  const [showTimers, setShowTimers] = useState(true);

  return (
    <div>
      <button onClick={() => setShowTimers(!showTimers)}>
        타이머 {showTimers ? "숨기기" : "보이기"}
      </button>
      {showTimers && (
        <div>
          <BadTimer />
          <GoodTimer />
        </div>
      )}
    </div>
  );
};

export default TimerContainer;
```

- "숨기기" 버튼을 누르면 두 타이머 모두 화면에서 사라진다
- 콘솔을 확인하면 `❌ 타이머 실행 중...`은 계속 출력되고, `✅ 타이머 실행 중...`은 멈춘다
- 정리 함수가 없으면 컴포넌트가 사라져도 타이머가 계속 동작하여 메모리 누수가 발생한다

---

## 무한 루프 방지

- 의존성 배열을 잘못 설정하면 **무한 루프**가 발생한다
- `useEffect` 안에서 State를 변경하고, 그 State를 의존성 배열에 넣으면 변경 → 실행 → 변경 → 실행이 끝없이 반복된다
- 의존성 배열을 아예 생략해도 매 렌더링마다 실행되므로 같은 문제가 발생할 수 있다

```jsx
// ❌ 무한 루프 발생 - posts가 변경될 때마다 실행되는데, 실행할 때마다 posts를 변경한다
import { useState, useEffect } from "react";
import axios from "axios";

const PostList = () => {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    const fetchPosts = async () => {
      const response = await axios.get("https://jsonplaceholder.typicode.com/posts");
      setPosts(response.data); // posts 변경 → useEffect 다시 실행 → 무한 반복!
    };

    fetchPosts();
  }, [posts]); // ← posts가 변경될 때마다 실행

  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
};

export default PostList;
```

```jsx
// ✅ 올바른 방식 - 처음 1번만 데이터를 가져온다
useEffect(() => {
  const fetchPosts = async () => {
    const response = await axios.get("https://jsonplaceholder.typicode.com/posts");
    setPosts(response.data);
  };

  fetchPosts();
}, []); // ← 빈 배열: 처음 1번만 실행
```

- useEffect 안에서 변경하는 State를 의존성 배열에 넣지 않도록 주의한다

---

## 의존성 배열에 객체/배열을 넣을 때 주의점

- JavaScript에서 객체와 배열은 참조(reference)로 비교된다
- 내용이 같아도 새로 만들어진 객체/배열은 다른 것으로 판단된다
- 컴포넌트가 리렌더링되면 함수 안의 객체/배열은 **매번 새로 생성**되므로, 의존성 배열에 넣으면 매 렌더링마다 useEffect가 실행된다

```jsx
// JavaScript의 참조 비교
console.log({ name: "철수" } === { name: "철수" }); // false (내용은 같지만 다른 객체)
console.log([1, 2, 3] === [1, 2, 3]); // false (내용은 같지만 다른 배열)
```

```jsx
// ❌ 잘못된 방식 - 매 렌더링마다 options가 새로 생성되어 useEffect가 계속 실행된다
const App = () => {
  const [count, setCount] = useState(0);

  const options = { limit: 10, offset: 0 }; // 렌더링될 때마다 새 객체 생성

  useEffect(() => {
    console.log("API 호출!", options);
  }, [options]); // ← 매번 새 객체이므로 매번 실행된다

  return <button onClick={() => setCount(count + 1)}>+1</button>;
};
```

```jsx
// ✅ 올바른 방식 - 객체 대신 원시값(primitive)을 의존성에 넣는다
const App = () => {
  const [count, setCount] = useState(0);
  const [limit, setLimit] = useState(10);
  const [offset, setOffset] = useState(0);

  useEffect(() => {
    console.log("API 호출!", { limit, offset });
  }, [limit, offset]); // ← 숫자(원시값)는 값으로 비교되므로 실제로 변경될 때만 실행된다

  return <button onClick={() => setCount(count + 1)}>+1</button>;
};
```

- 의존성 배열에는 가능하면 **문자열, 숫자, boolean** 같은 원시값을 넣는다
- 객체나 배열을 넣어야 하는 경우에는 해당 객체 안의 원시값을 꺼내서 넣는 것이 안전하다

---

## StrictMode와 useEffect

- React의 `StrictMode`는 개발 모드에서 **useEffect를 일부러 2번 실행**한다
- 마운트 → 정리 함수 실행 → 다시 마운트 순서로 실행하여, 정리 함수가 제대로 작성되었는지 확인해준다
- 프로덕션(배포) 환경에서는 1번만 실행되므로, 개발 중에만 나타나는 현상이다

```jsx
// main.jsx
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.jsx";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <App />
  </StrictMode>
);
```

- Vite로 프로젝트를 생성하면 `main.jsx`에 `StrictMode`가 기본으로 적용되어 있다
- 개발 중 `useEffect`가 2번 실행되는 것처럼 보이면 StrictMode 때문이므로 정상적인 동작이다
- 정리 함수를 올바르게 작성했다면, 2번 실행되어도 문제가 없다