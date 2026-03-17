## useRef

- React에서 **DOM 요소에 직접 접근**하거나, **리렌더링 없이 값을 저장**할 때 사용하는 Hook
- `useState`와 달리 값이 바뀌어도 **화면이 다시 그려지지 않음**
- `useRef`의 값은 `.current`로 접근함

**useRef를 쓰는 상황**

- DOM 요소에 직접 접근할 때 (포커스, 스크롤, 크기 측정, 동영상/오디오 제어)
- 리렌더링 없이 값을 유지하고 싶을 때 (이전 state 기억, 타이머 ID 저장, 내부 카운트)

```jsx
import { useState, useRef } from "react";

const Counter = () => {
  const [render, setRender] = useState(false);
  let count = 0; // 리렌더링될 때마다 0으로 초기화됨
  const countRef = useRef(0); // 리렌더링되어도 값이 유지됨

  const handleLetClick = () => {
    count += 1;
    console.log("let:", count);
  };

  const handleRefClick = () => {
    countRef.current += 1;
    console.log("useRef:", countRef.current);
  };

  return (
    <div>
      <button onClick={handleLetClick}>let 증가</button>
      <button onClick={handleRefClick}>useRef 증가</button>
      <button onClick={() => setRender(!render)}>리렌더링</button>
    </div>
  );
};

export default Counter
```

### useState vs useRef vs 일반 변수

- React 컴포넌트는 리렌더링될 때마다 **함수가 다시 실행**됨
- 일반 변수(`let`)는 리렌더링될 때마다 **초기값으로 돌아감**
- `useRef`는 리렌더링되어도 **값이 유지됨**

|  | `useState` | `useRef` | 일반 변수 (`let`) |
| --- | --- | --- | --- |
| 값이 바뀌면 | 리렌더링 O | 리렌더링 X | 리렌더링 X |
| 리렌더링 시 값 | 유지됨 | 유지됨 | 초기화됨 |
| 용도 | 화면에 표시되는 데이터 | DOM 접근, 내부 값 저장 | 사용하지 않음 |

---

## DOM 요소에 접근하기

- `useRef`로 만든 ref를 JSX 요소의 `ref` 속성에 연결하면 해당 DOM 요소에 직접 접근할 수 있음
- JavaScript의 `document.querySelector()`와 비슷한 역할

### 페이지 열릴 때 input에 자동 포커스

```jsx
import { useRef, useEffect } from "react";

const SearchPage = () => {
  const inputRef = useRef(null);

  useEffect(() => {
    inputRef.current.focus();
  }, []);

  return <input ref={inputRef} placeholder="검색어를 입력하세요" />;
};

export default SearchPage;
```

- `useRef(null)`로 ref 객체를 생성
- `ref={inputRef}`로 input 요소에 연결
- `inputRef.current`로 실제 DOM 요소에 접근
- `useEffect`에서 컴포넌트가 렌더링된 후 `.focus()` 호출

### 스크롤 이동

- 특정 영역으로 스크롤을 이동시킬 때 사용

```jsx
import { useRef } from "react";

const ScrollPage = () => {
  const bottomRef = useRef(null);

  const scrollToBottom = () => {
    bottomRef.current.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <div>
      <button onClick={scrollToBottom}>맨 아래로 이동</button>
      <div style={{ height: "200vh" }} />
      <div ref={bottomRef}>여기가 맨 아래입니다</div>
    </div>
  );
};

export default ScrollPage;
```

## SPA에서의 페이지 이동

- React는 SPA이므로 **하나의 HTML 페이지**에서 모든 화면을 처리한다
    
    → 페이지 이동이 불가능하다.
    
- 하지만 사용자 입장에서는 여전히 **페이지 이동**이 필요하다

### URL이 바뀌지 않으면 생기는 문제

- 사용자가 **특정 페이지를 즐겨찾기**할 수 없다
- 친구에게 **링크를 공유**할 수 없다 (항상 첫 페이지로 이동됨)
- **뒤로 가기 버튼**이 작동하지 않는다
- 즉, URL이 바뀌지 않으면 **웹의 기본적인 사용성이 깨진다**

### 라우팅

- URL에 따라 다른 화면(컴포넌트)을 보여주는 것
- React만으로는 URL에 따라 다른 화면을 보여주는 기능이 없다
- `react-router-dom` 라이브러리를 사용하여 URL 기반 라우팅을 구현한다

---

# react-router-dom

### 설치

```bash
npm install react-router-dom@6
```

- 이 수업에서는 **v6 기준**으로 진행한다

---

## 기본 라우팅 설정

- `createBrowserRouter`로 라우트(경로-컴포넌트 매핑)를 정의한다
- `RouterProvider`로 라우터를 앱에 연결한다

### 페이지 컴포넌트 만들기

- router에서 관리하는 페이지는 `page` 디렉토리에, 재사용이 가능한 컴포넌트는 `components`에 분리하여 활용한다.
- 먼저 각 경로에 보여줄 페이지 컴포넌트를 만든다

```jsx
// src/pages/Home.jsx
const Home = () => {
  return <h1>홈 페이지</h1>;
};

export default Home;
```

```jsx
// src/pages/About.jsx
const About = () => {
  return <h1>소개 페이지</h1>;
};

export default About;
```

```jsx
// src/pages/Contact.jsx
const Contact = () => {
  return <h1>연락처 페이지</h1>;
};

export default Contact;
```

### 라우터 설정하기

- `path`: URL 경로
- `element`: 해당 경로에서 보여줄 컴포넌트

```jsx
// src/router/index.jsx
import { createBrowserRouter } from "react-router-dom";
import Home from "../pages/Home";
import About from "../pages/About";
import Contact from "../pages/Contact";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
  },
  {
    path: "/about",
    element: <About />,
  },
  {
    path: "/contact",
    element: <Contact />,
  },
]);

export default router;
```

```jsx
// src/App.jsx
import { RouterProvider } from "react-router-dom";
import router from "./router";

const App = () => {
  return <RouterProvider router={router} />;
};

export default App;
```

- 브라우저에서 `http://localhost:5173/about`으로 접속하면 About 컴포넌트가 표시된다

---

## Link 컴포넌트

- HTML의 `<a>` 태그를 사용하면 페이지가 **완전히 새로고침**된다
- `<Link>` 컴포넌트를 사용하면 **새로고침 없이** 페이지를 이동할 수 있다

```jsx
// src/pages/Home.jsx
import { Link } from "react-router-dom";

const Home = () => {
  return (
    <div>
      <h1>홈 페이지</h1>
      {/* ❌ a 태그 - 페이지 전체가 새로고침된다 */}
      <a href="/about">소개 (a 태그)</a>

      {/* ✅ Link - 새로고침 없이 이동한다 */}
      <Link to="/about">소개 (Link)</Link>
      <Link to="/contact">연락처 (Link)</Link>
    </div>
  );
};

export default Home;
```

---

## 절대 경로와 상대 경로

- `Link`의 `to`나 라우트의 `path`에서 **`/`로 시작하면 절대 경로**, **`/` 없이 시작하면 상대 경로**이다
- 절대 경로는 항상 **루트(`/`)부터** 시작하는 전체 경로이다
- 상대 경로는 **현재 위치를 기준으로** 경로를 계산한다

```jsx
// 현재 URL: /settings/profile

// 절대 경로 - 항상 같은 곳으로 이동
<Link to="/about">소개</Link>        // → /about
<Link to="/settings">설정</Link>     // → /settings

// 상대 경로 - 현재 위치 기준
<Link to="account">계정</Link>       // → /settings/account
<Link to="..">상위로</Link>          // → /settings
```

|  | 절대 경로 | 상대 경로 |
| --- | --- | --- |
| 형태 | `/`로 시작 | `/` 없이 시작 |
| 기준 | 항상 루트(`/`)부터 | 현재 라우트 위치 기준 |
| 예시 | `to="/about"` | `to="about"` |
| `..` | - | 부모 라우트로 이동 |
- 단순한 구조에서는 **절대 경로**가 직관적이고 헷갈리지 않는다
- 중첩 라우팅에서는 **상대 경로**가 유용하다 (부모 경로가 바뀌어도 자식이 영향을 받지 않음)
## 레이아웃 (Layout)

- 웹사이트에서 **헤더, 네비게이션, 푸터**는 모든 페이지에서 동일하게 표시된다
- 매 페이지 컴포넌트마다 헤더와 푸터를 넣으면 **코드가 중복**된다
- 레이아웃 컴포넌트를 만들어 **공통 UI는 한 곳에**, 페이지별 내용만 교체하는 구조를 만든다

### Outlet

- `Outlet`은 **자식 라우트의 컴포넌트가 렌더링되는 자리**이다
- 레이아웃 안에서 `<Outlet />`을 넣으면, URL에 따라 해당 위치에 페이지 컴포넌트가 표시된다
    
    ![image.png](attachment:d9019643-352f-4b55-9853-b27c970e8f7b:image.png)
    

|  | `children` (props) | `<Outlet />` |
| --- | --- | --- |
| 결정 방식 | 부모 컴포넌트가 직접 자식을 전달 | **URL에 따라** 자동으로 결정 |
| 용도 | 범용 컴포넌트 (카드, 버튼 등) | 라우팅 기반 레이아웃 |

### 레이아웃 컴포넌트 만들기

```jsx
// src/layouts/Layout.jsx
import { Outlet, Link } from "react-router-dom";

const Layout = () => {
  return (
    <div>
      <header>
        <nav>
          <Link to="/">홈</Link>
          <Link to="/about">소개</Link>
          <Link to="/contact">연락처</Link>
        </nav>
      </header>

      <main>
        <Outlet />
      </main>

      <footer>
        <p>© 2099 My Website</p>
      </footer>
    </div>
  );
};

export default Layout;
```

### 라우터에 레이아웃 적용하기

- 레이아웃 라우트의 `children` 배열에 페이지 라우트를 넣는다
- 자식 라우트의 컴포넌트가 레이아웃의 `<Outlet />` 위치에 렌더링된다

```jsx
// src/router/index.jsx
import { createBrowserRouter } from "react-router-dom";
import Layout from "../layouts/Layout";
import Home from "../pages/Home";
import About from "../pages/About";
import Contact from "../pages/Contact";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      {
        index: true,
        element: <Home />,
      },
      {
        path: "about",
        element: <About />,
      },
      {
        path: "contact",
        element: <Contact />,
      },
    ],
  },
]);

export default router;
```

- `index: true`: 부모 경로(`/`)에 접속했을 때 보여줄 기본 자식 라우트
- 자식 라우트의 `path`에는 `/`를 붙이지 않는다 (부모 경로에 이어붙여짐)
    - 부모: `"/"` + 자식: `"about"` → 최종 경로: `"/about"`

---

## NavLink

- `NavLink`는 `Link`와 동일하게 동작하지만, **현재 페이지에 해당하는 링크에 자동으로 `active` 클래스**가 추가된다
- 현재 어떤 페이지에 있는지 시각적으로 표시할 때 사용한다

```jsx
// src/layouts/Layout.jsx
import { Outlet, NavLink } from "react-router-dom";
import "./Layout.css";

const Layout = () => {
  return (
    <div>
      <header>
        <nav>
          <NavLink to="/">홈</NavLink>
          <NavLink to="/about">소개</NavLink>
          <NavLink to="/contact">연락처</NavLink>
        </nav>
      </header>

      <main>
        <Outlet />
      </main>
    </div>
  );
};

export default Layout;
```

```css
/* src/layouts/Layout.css */
nav {
  display: flex;
  gap: 16px;
}

nav a {
  text-decoration: none;
  color: gray;
}

nav a.active {
  color: black;
  font-weight: bold;
}
```

- `/about` 페이지에 있으면 "소개" 링크에 `active` 클래스가 자동으로 추가된다
- CSS에서 `.active` 스타일을 지정하면 현재 페이지 링크가 강조된다

### end 속성

- `to="/"`인 NavLink는 **모든 경로가 `/`로 시작**하기 때문에 항상 `active`가 된다
- `end` 속성을 넣으면 **정확히 해당 경로일 때만** `active`가 적용된다

```jsx
{/* ❌ /about에서도 "홈"이 active 상태가 된다 */}
<NavLink to="/">홈</NavLink>

{/* ✅ 정확히 / 일 때만 active */}
<NavLink to="/" end>홈</NavLink>
```

---

## useNavigate

- `Link`는 사용자가 **클릭해서** 이동하는 것이다
- `useNavigate`는 **코드에서** 페이지를 이동시킬 때 사용한다
- 주로 다음과 같은 상황에서 사용한다:
    - 폼 제출 후 다른 페이지로 이동
    - 로그인 성공 후 홈으로 이동
    - 특정 조건에 따라 페이지 이동

```jsx
import { useNavigate } from "react-router-dom";

const LoginPage = () => {
  const navigate = useNavigate();

  const handleLogin = () => {
    // 로그인 처리...
    alert("로그인 성공!");
    navigate("/"); // 홈으로 이동
  };

  return (
    <div>
      <h1>로그인</h1>
      <button onClick={handleLogin}>로그인</button>
    </div>
  );
};

export default LoginPage;
```

### navigate의 옵션

| 사용법 | 설명 |
| --- | --- |
| `navigate("/about")` | `/about` 페이지로 이동 |
| `navigate(-1)` | 뒤로 가기 (브라우저 뒤로가기와 동일) |
| `navigate(1)` | 앞으로 가기 |
| `navigate("/", { replace: true })` | `/`으로 이동 후 현재 페이지를 히스토리에서 교체 (뒤로가기로 돌아올 수 없음) |

---

## Navigate 컴포넌트 (리다이렉트)

- `useNavigate`는 **함수 안에서** 페이지를 이동시킨다 (이벤트 핸들러, useEffect 등)
- `<Navigate />`는 **렌더링 시** 자동으로 페이지를 이동시키는 **컴포넌트**이다
- 주로 **조건에 따라 다른 페이지로 보내야 할 때** 사용한다

```jsx
import { Navigate } from "react-router-dom";

const MyPage = () => {
  const isLoggedIn = false;

  if (!isLoggedIn) {
    return <Navigate to="/login" replace />;
  }

  return <h1>마이 페이지</h1>;
};

export default MyPage;
```

- `replace`를 넣으면 히스토리가 교체되어, 뒤로가기를 눌러도 이 페이지로 돌아오지 않는다
- `replace`가 없으면 뒤로가기로 다시 돌아올 수 있다 (그러면 또 리다이렉트되어 무한 루프처럼 느껴질 수 있다)

### useNavigate vs Navigate 비교

|  | `useNavigate` | `<Navigate />` |
| --- | --- | --- |
| 종류 | Hook (함수) | 컴포넌트 |
| 사용 위치 | 이벤트 핸들러, useEffect 안 | JSX 안 (렌더링 시) |
| 사용 예시 | 버튼 클릭 후 이동, 폼 제출 후 이동 | 조건부 리다이렉트 |

```jsx
// useNavigate: 이벤트에서 이동
const handleClick = () => {
  navigate("/home");
};

// Navigate: 렌더링 시 자동 이동
if (!isLoggedIn) {
  return <Navigate to="/login" replace />;
}
```