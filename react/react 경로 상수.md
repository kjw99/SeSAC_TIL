## 경로 상수 (Path Constants)

- 여러 컴포넌트에서 경로 문자열을 직접 작성하면 오타가 발생하기 쉽다
- 경로가 변경되면 **여러 파일을 일일이 수정**해야 한다
- 경로를 **상수 객체로 관리**하면 한 곳에서 수정하여 전체에 반영할 수 있다

### 경로 상수 정의

```jsx
// src/constants/paths.js
const PATHS = {
  HOME: "/",
  ABOUT: "/about",
  DUMMY: {
    INDEX: "/dummy",
    POSTS: "/dummy/posts",
    PRODUCTS: "/dummy/products",
    getPostDetailPath: (postId) => `/dummy/posts/${postId}`,
  },
};

export default PATHS;
```

- 정적 경로는 **문자열 상수**로 정의한다
- 동적 경로(파라미터 포함)는 **함수로 만들어** 실제 값을 넣어 사용한다

### 컴포넌트에서 사용

```jsx
import { Link, useNavigate } from "react-router-dom";
import PATHS from "../constants/paths";

const Navigation = () => {
  const navigate = useNavigate();

  return (
    <nav>
      {/* 정적 경로 */}
      <Link to={PATHS.HOME}>홈</Link>
      <Link to={PATHS.DUMMY.POSTS}>게시글 목록</Link>

      {/* 동적 경로 - 함수로 실제 값 전달 */}
      <Link to={PATHS.DUMMY.getPostDetailPath(1)}>1번 게시글</Link>

      {/* useNavigate에서도 동일하게 사용 */}
      <button onClick={() => navigate(PATHS.DUMMY.PRODUCTS)}>
        상품 페이지
      </button>
    </nav>
  );
};
```