## Not Found 페이지 (path: "*")

- 사용자가 **존재하지 않는 경로**로 접속했을 때 안내 페이지를 보여주는 방법이다
- `path: "*"`은 **위에 정의된 어떤 경로에도 매칭되지 않을 때** 적용된다
- 관례상 `children` 배열의 **가장 마지막**에 위치시킨다

### NotFound 컴포넌트 만들기

```jsx
// src/pages/NotFound.jsx
import { Link } from "react-router-dom";

const NotFound = () => {
  return (
    <div>
      <h1>404 - 페이지를 찾을 수 없습니다</h1>
      <p>요청하신 페이지가 존재하지 않습니다.</p>
      <Link to="/">홈으로 돌아가기</Link>
    </div>
  );
};

export default NotFound;
```

### 라우터에 적용하기

```jsx
// src/router/index.jsx
import { createBrowserRouter } from "react-router-dom";
import Layout from "../layouts/Layout";
import Home from "../pages/Home";
import About from "../pages/About";
import NotFound from "../pages/NotFound";

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
        // 위 경로에 매칭되지 않는 모든 경로를 처리
        path: "*",
        element: <NotFound />,
      },
    ],
  },
]);

export default router;
```

- `/about` → About 컴포넌트 표시
- `/asdfg` → NotFound 컴포넌트 표시
- `path: "*"`은 관례상 `children` 배열의 **마지막에 위치**시키는 것이 좋다

---

## errorElement (에러 처리)

- 라우트에서 에러가 발생했을 때 보여줄 **에러 페이지**를 설정한다
- 컴포넌트 렌더링 중 에러가 나거나, 존재하지 않는 경로에 접속했을 때 표시된다

```jsx
// src/pages/ErrorPage.jsx
import { useRouteError, Link } from "react-router-dom";

const ErrorPage = () => {
  const error = useRouteError();

  return (
    <div>
      <h1>오류가 발생했습니다</h1>
      <p>{error.statusText || error.message}</p>
      <Link to="/">홈으로 돌아가기</Link>
    </div>
  );
};

export default ErrorPage;
```

```jsx
// src/router/index.jsx
import { createBrowserRouter } from "react-router-dom";
import Layout from "../layouts/Layout";
import Home from "../pages/Home";
import About from "../pages/About";
import ErrorPage from "../pages/ErrorPage";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    errorElement: <ErrorPage />,
    children: [
      {
        index: true,
        element: <Home />,
      },
      {
        path: "about",
        element: <About />,
      },
    ],
  },
]);

export default router;
```

- `errorElement`를 최상위 라우트에 넣으면, **하위 라우트에서 발생한 모든 에러**를 잡아준다
- `useRouteError()`로 에러 정보를 가져올 수 있다

| 에러 종류 | 예시 |
| --- | --- |
| 존재하지 않는 경로 | `/asdfg` 접속 (404) |
| 컴포넌트 렌더링 에러 | 컴포넌트 안에서 `undefined.map()` 등 런타임 에러 발생 |
| loader/action 에러 | 데이터 로딩 함수에서 에러 발생 또는 `throw new Response()` |

---

### path: "*" vs errorElement 비교

|  | `path: "*"` | `errorElement` |
| --- | --- | --- |
| 처리 범위 | 존재하지 않는 경로만 | 경로 에러 + 렌더링 에러 모두 |
| 에러 정보 | 접근 불가 | `useRouteError()`로 접근 가능 |
| 위치 | `children` 배열의 마지막 | 라우트 객체의 속성 |
- `path: "*"`은 **404 전용**이고, `errorElement`는 **모든 에러를 포괄**한다
- 둘 다 사용할 수도 있다: 404는 `path: "*"`으로, 나머지 에러는 `errorElement`로 처리
- 존재하지 않는 경로에 대해서는 **`path: "*"`이 우선**한다
`path: "*"`은 "매칭되는 라우트"이므로 에러가 아니다. `errorElement`가 404를 처리하는 것은 `path: "*"`이 **없을 때**만이다