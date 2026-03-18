## Protected Route

- 로그인하지 않은 사용자가 **특정 페이지에 접근하지 못하도록** 막는 패턴이다
- 예: 마이페이지, 글쓰기 페이지는 로그인한 사용자만 접근 가능
- 로그인 여부를 확인하고, 로그인되지 않았으면 **로그인 페이지로 리다이렉트**한다

### 인증 스토어 만들기

- Zustand로 로그인 상태를 전역으로 관리한다

```jsx
// src/store/useUserStore.js
import { create } from "zustand";

const useUserStore = create((set) => ({
  isLoggedIn: false,
  login: () => set({ isLoggedIn: true }),
  logout: () => set({ isLoggedIn: false }),
}));

export default useUserStore;
```

### 로그인 페이지 / 마이 페이지

```jsx
// src/pages/LoginPage.jsx

import { Link, useNavigate } from "react-router-dom";
import useUserStore from "../store/useUserStore";

const LoginPage = () => {
  const navigate = useNavigate();
  const login = useUserStore((state) => state.login);

  const handleLogin = () => {
    // 로그인 처리...
    login()
    navigate("/"); // 홈으로 이동
  };

  return (
    <div>
      <h1>로그인</h1>
      <button className="button" onClick={handleLogin}>
        로그인
      </button>
      <Link to="/">홈으로!</Link>
    </div>
  );
};

export default LoginPage;

```

```jsx
// src/pages/MyPage.jsx
const MyPage = () => {
  return <h1>마이페이지 (로그인한 사용자만 볼 수 있음)</h1>;
};

export default MyPage;
```

### ProtectedRoute 컴포넌트 만들기

- `<Navigate />`를 활용하여 조건부 리다이렉트를 구현한다
- 로그인 상태이면 자식 컴포넌트를 그대로 보여주고, 아니면 로그인 페이지로 보낸다

```jsx
// src/components/ProtectedRoute.jsx
import { Navigate } from "react-router-dom";
import useUserStore from "../store/useUserStore";

const ProtectedRoute = ({ children }) => {
  const isLoggedIn = useUserStore((state) => state.isLoggedIn);

  if (!isLoggedIn) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

export default ProtectedRoute;
```

- `children`: 보호할 페이지 컴포넌트가 들어온다
- `isLoggedIn`이 `false`면 `/login`으로 리다이렉트된다
- Zustand 스토어에서 직접 가져오므로 **props 전달이 필요 없다**

### 라우터에 적용하기

```jsx
// src/router/index.jsx
import { createBrowserRouter } from "react-router-dom";
import Layout from "../layouts/Layout";
import Home from "../pages/Home";
import Login from "../pages/Login";
import MyPage from "../pages/MyPage";
import ProtectedRoute from "../components/ProtectedRoute";

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
        path: "login",
        element: <Login />,
      },
      {
        path: "mypage",
        element: (
          <ProtectedRoute>
            <MyPage />
          </ProtectedRoute>
        ),
      },
    ],
  },
]);

export default router;
```

### 동작 흐름

```
사용자가 /mypage 접속
    ↓
ProtectedRoute가 useUserStore에서 isLoggedIn 확인
    ↓
├── true  → MyPage 컴포넌트 표시
└── false → /login 으로 리다이렉트
```

---

## Outlet을 활용한 ProtectedRoute

- 보호할 페이지가 여러 개일 때, 각각 `<ProtectedRoute>`로 감싸면 코드가 반복된다
- `Outlet`을 활용하면 **보호된 영역을 라우트 구조로** 깔끔하게 관리할 수 있다

```jsx
// src/components/ProtectedRoute.jsx
import { Navigate, Outlet } from "react-router-dom";
import useUserStore from "../store/useUserStore";

const ProtectedRoute = () => {
  const isLoggedIn = useUserStore((state) => state.isLoggedIn);

  if (!isLoggedIn) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
};

export default ProtectedRoute;
```

```jsx
// src/router/index.jsx
import { createBrowserRouter } from "react-router-dom";
import Layout from "../layouts/Layout";
import Home from "../pages/Home";
import Login from "../pages/Login";
import MyPage from "../pages/MyPage";
import Settings from "../pages/Settings";
import ProtectedRoute from "../components/ProtectedRoute";

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
        path: "login",
        element: <Login />,
      },
      // 보호된 라우트 그룹
      {
        element: <ProtectedRoute />,
        children: [
          {
            path: "mypage",
            element: <MyPage />,
          },
          {
            path: "settings",
            element: <Settings />,
          },
        ],
      },
    ],
  },
]);

export default router;
```

- `ProtectedRoute`를 **부모 라우트**로 사용하고, 보호할 페이지들을 `children`에 넣는다
- `ProtectedRoute`에는 `path`가 없다 → URL 구조에 영향을 주지 않는 **레이아웃 라우트**이다
- `/mypage`와 `/settings` 모두 로그인 체크가 자동으로 적용된다