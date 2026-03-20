## TypeScript

- TypeScript는 JavaScript에 타입(Type)을 추가한 언어이다
- `.js` 대신 `.ts` (또는 React에서는 `.tsx`) 파일을 사용한다
- 코드를 실행하기 전에 **타입 오류를 미리 잡아준다**
- 현재 대부분의 React 프로젝트에서 TypeScript를 사용한다

### 왜 쓰는가?

```jsx
// JavaScript - 실행해봐야 에러를 알 수 있다
const user = { name: "홍길동", age: 25 };
console.log(user.email); // undefined (에러 안 남, 버그 발견 어려움)
```

```tsx
// TypeScript - 작성 시점에 에러를 알려준다
const user: { name: string; age: number } = { name: "홍길동", age: 25 };
console.log(user.email); // ❌ 빨간 줄 — 'email' 속성이 없습니다
```

- 자동완성이 정확해진다 (IDE가 어떤 속성/함수가 있는지 알려줌)
- 팀 프로젝트에서 다른 사람이 만든 함수의 사용법을 타입만 보고 파악할 수 있다

---

## React + TypeScript 프로젝트 생성

```bash
npm create vite@7 my-app -- --template react-ts
```

- 기존 `react` 템플릿 대신 `react-ts`를 사용하면 된다
- 파일 확장자가 `.jsx` → `.tsx`, `.js` → `.ts`로 바뀐다

---

## 기본 타입

```tsx
// 변수 타입
const name: string = "홍길동";
const age: number = 25;
const isStudent: boolean = true;
const hobbies: string[] = ["코딩", "게임"];
```

## interface

- **객체의 구조(모양)를 정의**하는 문법이다
- "이 객체에는 어떤 속성이 있고, 각 속성의 타입은 무엇인지"를 미리 선언한다
- `interface`로 정의해두면, 그 구조와 다른 객체를 만들려고 할 때 에러가 난다

```tsx
interface User {
  name: string;
  age: number;
}

const user1: User = { name: "홍길동", age: 25 };   // ✅ OK
const user2: User = { name: "홍길동" };             // ❌ age가 빠졌다고 에러
const user3: User = { name: "홍길동", age: "스물" }; // ❌ age는 number여야 한다
```

- `type`으로도 동일하게 가능하다 — 둘은 거의 같고, 팀 컨벤션을 따르면 된다
- 보통 Props나 API 응답 같은 객체 구조에는 `interface`를 많이 쓴다

## 제네릭

- `함수이름<타입>()`처럼 함수 뒤에 `<타입>`을 붙이는 문법을 제네릭(Generic)이라고 한다
- "이 함수가 다룰 데이터의 타입을 알려주는 것"이다
- TypeScript가 타입을 추론할 수 없을 때 (초기값이 `null`, 빈 배열 등) 제네릭으로 알려준다
- `|`는 **유니온 타입**으로, "A 또는 B"를 의미한다 — `User | null`은 "User이거나 null"

```tsx
useState<User | null>()   // 이 state는 User이거나 null이다
useState<User[]>()        // 이 state는 User 배열이다
axios.get<Post[]>("/api") // 이 API 응답은 Post 배열이다
```

---

## Props에 타입 지정하기

- React + TypeScript에서 가장 많이 하는 작업이다
- `interface`로 Props의 타입을 정의한다

```tsx
interface UserCardProps {
  name: string;
  age: number;
  email?: string; // ?는 선택적(optional) — 안 넘겨도 된다
}

const UserCard = ({ name, age, email }: UserCardProps) => {
  return (
    <div>
      <h2>{name} ({age}세)</h2>
      {email && <p>{email}</p>}
    </div>
  );
};

// 사용
<UserCard name="홍길동" age={25} />          // ✅ OK
<UserCard name="홍길동" age={25} email="a@b.com" /> // ✅ OK
<UserCard name="홍길동" />                   // ❌ age가 빠졌다고 에러
<UserCard name="홍길동" age="스물다섯" />     // ❌ age는 number여야 한다
```

- Props 타입이 정의되어 있으면, 컴포넌트를 사용할 때 **잘못된 Props를 넘기면 에러**가 난다
- 실수로 빠뜨리거나 잘못된 타입을 넘기는 버그를 방지할 수 있다
- 함수도 타입으로 지정할 수 있다 — Props로 콜백을 넘길 때 사용한다

```tsx
interface ButtonProps {
  label: string;
  onClick: () => void;                  // 매개변수 없는 함수
  onChange?: (value: string) => void;   // 선택적 함수
}
```

### children 타입

- 레이아웃처럼 자식 요소를 감싸는 컴포넌트에서는 `children`의 타입을 지정한다

```tsx
interface LayoutProps {
  children: React.ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
  return (
    <div className="layout">
      <header>헤더</header>
      <main>{children}</main>
    </div>
  );
};

// 사용
<Layout>
  <h1>페이지 내용</h1>
</Layout>
```

- `React.ReactNode`는 JSX, 문자열, 숫자, null 등 렌더링 가능한 모든 것을 포함한다

## useState에 타입 지정하기

```tsx
// 단순 타입 — 초기값으로 자동 추론되므로 생략 가능
const [count, setCount] = useState(0);          // number로 자동 추론
const [name, setName] = useState("");            // string으로 자동 추론

// 객체나 배열 — 제네릭으로 타입을 직접 지정한다
interface User {
  id: number;
  name: string;
  email: string;
}

const [user, setUser] = useState<User | null>(null); // 초기값 null, 나중에 User
const [users, setUsers] = useState<User[]>([]);      // User 배열
```

- 초기값이 `null`이고 나중에 데이터가 들어오는 경우 `<User | null>`처럼 지정한다
- 배열의 경우 `<User[]>`로 지정하면, 배열 안의 각 항목이 User 타입임을 보장한다

## 이벤트 타입

```tsx
const SearchBar = () => {
  const [keyword, setKeyword] = useState("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setKeyword(e.target.value);
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log(keyword);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input value={keyword} onChange={handleChange} />
    </form>
  );
};
```

- 자주 쓰는 이벤트 타입:
    - `React.ChangeEvent<HTMLInputElement>` — input의 onChange
    - `React.FormEvent<HTMLFormElement>` — form의 onSubmit
    - `React.MouseEvent<HTMLButtonElement>` — button의 onClick
- 외울 필요 없다 — IDE에서 마우스를 올리면 타입이 표시된다
- 인라인으로 작성하면 타입이 자동 추론되므로 별도 지정이 불필요하다:

```tsx
// 인라인이면 타입 자동 추론 — 별도 지정 불필요
<input onChange={(e) => setKeyword(e.target.value)} />
```

## API 응답에 타입 지정하기

```tsx
interface Post {
  id: number;
  title: string;
  content: string;
  createdAt: string;
}

const PostList = () => {
  const [posts, setPosts] = useState<Post[]>([]);

  useEffect(() => {
    const fetchPosts = async () => {
      const res = await axios.get<Post[]>("/api/posts");
      setPosts(res.data); // res.data가 Post[] 타입으로 추론된다
    };
    fetchPosts();
  }, []);

  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>
          <h3>{post.title}</h3> {/* 자동완성으로 title, content 등이 뜬다 */}
          <p>{post.content}</p>
        </li>
      ))}
    </ul>
  );
};
```

---

## 전체 예시 — 유저 목록 컴포넌트

위에서 다룬 내용을 하나의 컴포넌트에 모아보면 이런 모습이다.

```tsx
import { useState, useEffect } from "react";
import axios from "axios";

interface User {
  id: number;
  name: string;
  email: string;
}

interface UserListProps {
  title: string;
  onDelete?: (id: number) => void;
}

const UserList = ({ title, onDelete }: UserListProps) => {
  const [users, setUsers] = useState<User[]>([]);
  const [keyword, setKeyword] = useState("");

  useEffect(() => {
    const fetchUsers = async () => {
      const res = await axios.get<User[]>("/api/users");
      setUsers(res.data);
    };
    fetchUsers();
  }, []);

  const filtered = users.filter((user) =>
    user.name.includes(keyword)
  );

  return (
    <div>
      <h2>{title}</h2>
      <input
        value={keyword}
        onChange={(e) => setKeyword(e.target.value)}
        placeholder="이름 검색"
      />
      <ul>
        {filtered.map((user) => (
          <li key={user.id}>
            {user.name} — {user.email}
            {onDelete && <button onClick={() => onDelete(user.id)}>삭제</button>}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default UserList;
```

- `interface` — User, Props 타입 정의
- `useState<User[]>` — 제네릭으로 배열 타입 지정
- `axios.get<User[]>` — API 응답 타입 지정
- `onDelete?: (id: number) => void` — 선택적 함수 Props
- `onChange` — 인라인이라 이벤트 타입 자동 추론