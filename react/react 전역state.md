## 전역 State의 필요성

- 지금까지 배운 State는 **컴포넌트 내부**에서만 사용할 수 있었다
- 부모 → 자식으로 Props를 통해 데이터를 전달할 수 있지만, 깊이가 깊어지면 **Prop Drilling** 문제가 발생한다
- 페이지가 다르면 부모-자식 관계가 아니므로, Props로 전달하는 것 자체가 불가능하다

### Prop Drilling

- 최상위 컴포넌트의 State를 깊은 자식에게 전달하려면, 중간 컴포넌트들이 사용하지도 않는 Props를 계속 전달해야 한다

```jsx
// App → Layout → Sidebar → UserInfo 로 user를 전달해야 하는 경우
const App = () => {
  const [user, setUser] = useState({ name: "홍길동" });
  return <Layout user={user} />;
};

const Layout = ({ user }) => {
  // Layout은 user를 사용하지 않지만 전달해야 한다
  return <Sidebar user={user} />;
};

const Sidebar = ({ user }) => {
  // Sidebar도 user를 사용하지 않지만 전달해야 한다
  return <UserInfo user={user} />;
};

const UserInfo = ({ user }) => {
  return <p>{user.name}</p>;
};
```

- 이런 구조는 컴포넌트가 많아질수록 유지보수가 어려워진다
- **전역 State**를 사용하면, 어떤 컴포넌트에서든 직접 데이터에 접근할 수 있다

---

## Zustand

- React에서 가장 인기 있는 전역 상태 관리 라이브러리이다
- Zustand전에 있기 있던 Redux보다 훨씬 간단하고, 보일러플레이트가 거의 없다
- 필요한 상태만 구독하므로 불필요한 리렌더링이 발생하지 않는다

### 설치

```bash
npm install zustand
```

## Store

- Store는 **상태(데이터)와 액션(함수)을 한 곳에 모아둔 전역 저장소**이다
- `useState`에서는 상태와 상태를 변경하는 함수가 컴포넌트 안에 있었다
    - 다른 컴포넌트에서 쓰려면 Props로 전달해야 한다.
- Store에서는 상태와 함수를 **컴포넌트 바깥에** 정의하고, 어떤 컴포넌트에서든 가져다 쓴다
    - 어떤 컴포넌트에서든 직접 가져다 쓸 수 있다
- 파일은 보통 `src/store/` 폴더에 만든다

---

## Store 만들기

- `create` 함수로 Store를 만든다
- Store에 **상태**와 상태를 변경하는 **함수(액션)**를 함께 정의한다

```jsx
// src/store/useCounterStore.js
import { create } from "zustand";

const useCounterStore = create((set) => ({
  // 상태 (데이터)
  count: 0,

  // 액션 (상태를 변경하는 함수)
  increase: () => set((state) => ({ count: state.count + 1 })),
  decrease: () => set((state) => ({ count: state.count - 1 })),
  reset: () => set({ count: 0 }),
}));

export default useCounterStore;
```

- `create`에 전달하는 함수가 Store의 초기 상태와 액션을 정의한다
- `set`은 상태를 변경하는 함수이다 (`useState`의 `setState`와 비슷한 역할)

### set 사용법

- `set`은 전달한 값만 **부분 업데이트**한다 (나머지 상태는 그대로 유지)
- 상태가 여러 개일 때 동작을 보면 명확하다
- set()을 보면 그냥 객체만 전달하는 경우와 화살표 함수를 통해 전달하는 방식 2개가 있음.
- 화살표 함수의 경우 축약형으로 작성되어 리턴 값만 보이는 것.
    - ({ age: state.age + 1}) = { return {age: state.age + 1} } 이랑 같다.
    - 즉 화살표 함수를 사용하면 그냥 값만 반환하는 것이 아니라 함수를 작성해서 더 복잡한 로직도 가능하다.

```jsx
const useProfileStore = create((set) => ({
  name: "홍길동",
  age: 25,
  email: "hong@example.com",

  changeName: (newName) => set({ name: newName }),
  // name만 변경, age와 email은 그대로 유지

  birthday: () => set((state) => ({ age: state.age + 1 })),
  // age만 변경, name과 email은 그대로 유지

  reset: () => set({ name: "", age: 0, email: "" }),
  // 여러 값을 한번에 변경
}));
```

```jsx
// changeName("김철수") 호출 시:
// 변경 전: { name: "홍길동", age: 25, email: "hong@example.com" }
// 변경 후: { name: "김철수", age: 25, email: "hong@example.com" }
//           ↑ 이것만 변경       ↑ 유지          ↑ 유지
```

| 방식 | 예시 | 설명 |
| --- | --- | --- |
| 객체 전달 | `set({ name: "김철수" })` | 고정값으로 변경 |
| 함수 전달 | `set((state) => ({ age: state.age + 1 }))` | 이전 상태를 참조하여 변경 |
- 이전 값을 기반으로 변경할 때는 **함수 전달** 방식을 사용한다 (`useState`와 동일한 원리)
- 이전 값과 관계없이 고정값으로 변경할 때는 **객체 전달** 방식을 사용한다

---

## 컴포넌트에서 사용하기

- Store에서 필요한 상태와 함수를 꺼내서 사용한다

```jsx
import useCounterStore from "../store/useCounterStore";

const Counter = () => {
  const count = useCounterStore((state) => state.count);
  const increase = useCounterStore((state) => state.increase);
  const decrease = useCounterStore((state) => state.decrease);
  const reset = useCounterStore((state) => state.reset);

  return (
    <div>
      <h2>카운트: {count}</h2>
      <button onClick={increase}>+1</button>
      <button onClick={decrease}>-1</button>
      <button onClick={reset}>초기화</button>
    </div>
  );
};

export default Counter;
```

- `useCounterStore((state) => state.count)` — Store에서 `count`만 가져온다
- **필요한 것만 가져오기 때문에**, 다른 상태가 바뀌어도 이 컴포넌트는 리렌더링되지 않는다

---

## 다른 컴포넌트에서도 같은 Store 사용

- 전역 State이므로, **어떤 컴포넌트에서든** 같은 Store에 접근할 수 있다
- Props로 전달할 필요가 없다

```jsx
// Header에서 count 표시
const Header = () => {
  const count = useCounterStore((state) => state.count);
  return <header>현재 카운트: {count}</header>;
};

// Footer에서 reset 버튼
const Footer = () => {
  const reset = useCounterStore((state) => state.reset);
  return <button onClick={reset}>카운트 초기화</button>;
};
```

- Header와 Footer는 부모-자식 관계가 아니어도 같은 `count`를 공유한다
- 어디서든 `increase()`를 호출하면, `count`를 사용하는 **모든 컴포넌트가 자동으로 업데이트**된다

---

## Store는 기능 단위로 분리한다

- 하나의 Store에 모든 상태를 넣지 않는다
- **관련 있는 상태끼리** 묶어서 Store를 나눈다

```
src/store/
├── useAuthStore.js      # 로그인, 유저 정보
├── useCartStore.js      # 장바구니 상품 목록
└── useThemeStore.js     # 다크모드 설정
```

- 로그인 관련 상태는 `useAuthStore`에, 장바구니 관련 상태는 `useCartStore`에 넣는다
- 서로 관련 없는 상태가 한 Store에 섞이면 관리가 어려워진다
- 하나의 컴포넌트에서 여러 Store를 동시에 사용할 수 있다

```jsx
const Header = () => {
  const user = useAuthStore((state) => state.user);
  const cartCount = useCartStore((state) => state.items.length);
  const isDark = useThemeStore((state) => state.isDark);

  // ...
};
```

---

## 전역 State는 언제 쓰는가?

- 핵심 기준: **2개 이상의 관련 없는 컴포넌트**에서 같은 데이터를 써야 할 때

| 사례 | 이유 |
| --- | --- |
| 로그인 정보 | Header, 마이페이지, 댓글 작성 등 앱 전체에서 "누가 로그인했는지" 알아야 한다 |
| 장바구니 | 상품 페이지에서 담고, Header에서 개수 표시하고, 장바구니 페이지에서 목록을 보여준다 |
| 다크모드 | 설정 페이지에서 변경하면 모든 컴포넌트의 스타일이 바뀌어야 한다 |
| 알림 | 어디서든 알림을 발생시키고, Header에서 알림 목록을 보여준다 |
- ex) 로그인 정보를 쓰는 곳
    - Header      →  "홍길동님 환영합니다" / 로그아웃 버튼
    - MyPage      →  내 정보 표시
    - CommentForm →  댓글 작성 시 작성자 정보
    - AdminPage   →  관리자 권한 체크

→ 이 4개 컴포넌트가 부모-자식이 아닌데 같은 데이터가 필요하다
→ Props로 전달하려면 Prop Drilling 발생
→ 전역 State가 필요한 상황

---

## useState vs Zustand 비교

| 구분 | useState | Zustand |
| --- | --- | --- |
| 범위 | 컴포넌트 내부 | 앱 전체 (전역) |
| 데이터 전달 | Props로 전달 | 어디서든 직접 접근 |
| 리렌더링 | State가 바뀌면 해당 컴포넌트 + 자식 전부 | 구독한 값이 바뀐 컴포넌트만 |
| 사용 시점 | 해당 컴포넌트에서만 쓰는 데이터 | 여러 컴포넌트에서 공유하는 데이터 |
- **useState**: 폼 입력값, 모달 열림/닫힘 등 해당 컴포넌트에서만 쓰는 데이터
- **Zustand**: 로그인 정보, 테마 설정, 장바구니 등 여러 곳에서 공유하는 데이터
- 둘 다 사용하는 것이 일반적이다 — 전부 전역으로 만들 필요는 없다