## 중첩 라우팅 (Nested Routes)

- 지금까지 Layout + children으로 **1단계 중첩**을 사용했다
- 실제 웹사이트에서는 **여러 단계로 중첩**되는 경우가 많다

```
/settings              →  설정 메인 페이지
/settings/profile      →  프로필 설정
/settings/account      →  계정 설정
```

- `/settings` 안에서 공통 UI(사이드바 등)를 유지하면서, 오른쪽 영역만 바꾸는 구조이다
- 이미 배운 `Outlet`과 `children`을 **한 단계 더 깊게** 적용하는 것이다

### 구조 이해

![image.png](attachment:0be9f26f-d76b-4f1a-b26b-0f0052d62141:image.png)

- 최상위 Layout의 `<Outlet />`에 Settings 페이지가 들어간다
- Settings 안의 `<Outlet />`에 Profile, Account 등이 들어간다

---

## 라우터 설정

```jsx
// src/router/index.jsx
import { createBrowserRouter } from "react-router-dom";
import Layout from "../layouts/Layout";
import Home from "../pages/Home";
import Settings from "../pages/Settings";
import Profile from "../pages/settings/Profile";
import Account from "../pages/settings/Account";

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
        path: "settings",
        element: <Settings />,
        children: [
          {
            index: true,
            element: <Profile />,
          },
          {
            path: "profile",
            element: <Profile />,
          },
          {
            path: "account",
            element: <Account />,
          },
        ],
      },
    ],
  },
]);

export default router;
```

- `settings` 라우트 안에 `children`을 또 넣어서 **2단계 중첩**을 만든다
- `settings`의 `index: true`는 `/settings` 접속 시 기본으로 보여줄 페이지이다
- 최종 경로: `/settings/profile`, `/settings/account`

---

## 페이지 컴포넌트

```jsx
// src/pages/Settings.jsx
import { Outlet, NavLink } from "react-router-dom";

const Settings = () => {
  return (
    <div className="flex gap-8">
      <nav className="flex flex-col gap-2">
        <NavLink to="/settings/profile">프로필 설정</NavLink>
        <NavLink to="/settings/account">계정 설정</NavLink>
      </nav>
      <div className="flex-1">
        <Outlet />
      </div>
    </div>
  );
};

export default Settings;
```

- Settings 컴포넌트 안에 `<Outlet />`을 넣어서 자식 라우트가 렌더링될 자리를 만든다
- 사이드바 네비게이션은 고정되고, 오른쪽 영역만 바뀐다

```jsx
// src/pages/settings/Profile.jsx
const Profile = () => {
  return (
    <div>
      <h2>프로필 설정</h2>
      <p>이름, 프로필 사진 등을 변경할 수 있습니다.</p>
    </div>
  );
};

export default Profile;
```

```jsx
// src/pages/settings/Account.jsx
const Account = () => {
  return (
    <div>
      <h2>계정 설정</h2>
      <p>비밀번호 변경, 계정 삭제 등을 할 수 있습니다.</p>
    </div>
  );
};

export default Account;
```