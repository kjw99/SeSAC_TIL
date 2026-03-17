## 라우터 모듈화 (Modular Router)

- 프로젝트가 커지면 **하나의 라우터 파일에 모든 경로**가 몰리게 된다
- 레이아웃 단위로 라우트 배열을 **별도 파일로 분리**하여 관리한다
- 최종 라우터 파일에서 분리된 라우트들을 **합쳐서** 사용한다

### 분리 전 라우터 예시

```jsx
// src/router/index.js
import { createBrowserRouter } from "react-router-dom";
import RootLayout from "../layouts/RootLayout";
import DummyLayout from "../layouts/DummyLayout";
import Home from "../pages/RootPages/Home";
import About from "../pages/RootPages/About";
import DummyHome from "../pages/DummyPages/DummyHome";
import Posts from "../pages/DummyPages/Posts";
import PostDetail from "../pages/DummyPages/PostDetail";
import Products from "../pages/DummyPages/Products";

const router = createBrowserRouter([
  {
    path: "/",
    element: <RootLayout />,
    children: [
      { index: true, element: <Home /> },
      { path: "about", element: <About /> },
    ],
  },
  {
    path: "/dummy",
    element: <DummyLayout />,
    children: [
      { index: true, element: <DummyHome /> },
      { path: "posts", element: <Posts /> },
      { path: "posts/:postId", element: <PostDetail /> },
      { path: "products", element: <Products /> },
    ],
  },
]);

export default router;
```

- 레이아웃이 늘어날수록 **import와 라우트 설정이 한 파일에 계속 쌓인다**
- 레이아웃 단위로 파일을 분리하면 관리하기 쉬워진다

### 디렉토리 구조

```
📁 src/
├── 📁 router/
│   ├── 🚦 index.js            ← 라우터 합치는 파일
│   └── 📁 routes/
│       ├── 🚦 rootRoutes.js   ← Root 레이아웃 라우트
│       └── 🚦 dummyRoutes.js  ← Dummy 레이아웃 라우트
└── ⚛️ main.jsx
```

### 라우트 파일 분리

```jsx
// src/router/routes/rootRoutes.js
import RootLayout from "../../layouts/RootLayout";
import Home from "../../pages/RootPages/Home";
import About from "../../pages/RootPages/About";

const rootRoutes = [
  {
    path: "/",
    element: <RootLayout />,
    children: [
      { index: true, element: <Home /> },
      { path: "about", element: <About /> },
    ],
  },
];

export default rootRoutes;
```

```jsx
// src/router/routes/dummyRoutes.js
import DummyLayout from "../../layouts/DummyLayout";
import DummyHome from "../../pages/DummyPages/DummyHome";
import Posts from "../../pages/DummyPages/Posts";
import PostDetail from "../../pages/DummyPages/PostDetail";
import Products from "../../pages/DummyPages/Products";

const dummyRoutes = [
  {
    path: "/dummy",
    element: <DummyLayout />,
    children: [
      { index: true, element: <DummyHome /> },
      { path: "posts", element: <Posts /> },
      { path: "posts/:postId", element: <PostDetail /> },
      { path: "products", element: <Products /> },
    ],
  },
];

export default dummyRoutes;
```

### 라우터 합치기

```jsx
// src/router/index.js
import { createBrowserRouter } from "react-router-dom";
import rootRoutes from "./routes/rootRoutes";
import dummyRoutes from "./routes/dummyRoutes";

// 스프레드 연산자로 라우트 배열을 합친다
const router = createBrowserRouter([...rootRoutes, ...dummyRoutes]);

export default router;
```

- 각 라우트 파일은 **배열을 내보낸다**
- 최종 라우터에서 `...` (스프레드 연산자)로 합친다
- 새로운 레이아웃이 추가되면 **새 라우트 파일만 만들어서 합치면** 된다