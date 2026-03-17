# 동적 라우팅 (Dynamic Route)

- 게시글 목록에서 게시글을 클릭하면 **해당 게시글의 상세 페이지**로 이동하는 것이 일반적이다
- 게시글이 100개라면 라우트를 100개 만들 수는 없다
- URL에 변하는 값(파라미터)을 넣어서 하나의 라우트로 처리한다

```
/posts/1    →  1번 게시글 상세 페이지
/posts/2    →  2번 게시글 상세 페이지
/posts/100  →  100번 게시글 상세 페이지
```

---

## URL 파라미터와 useParams

- 라우트의 `path`에 `:파라미터이름`을 넣으면 **동적 경로**가 된다
- `useParams` Hook으로 URL에서 파라미터 값을 가져올 수 있다

### useParams 사용법

```jsx
import { useParams } from "react-router-dom";

// 라우트 path가 "posts/:id" 일 때
// URL이 /posts/3 이면

const { id } = useParams(); // id = "3" (문자열)
```

- `useParams()`는 URL 파라미터를 **객체**로 반환한다
- 구조 분해 할당으로 필요한 파라미터를 꺼낸다
- 값은 항상 **문자열**이다 (숫자가 필요하면 `Number()`로 변환)

```jsx
const { id } = useParams(); // id = "3" (문자열)

// ❌ 문자열이므로 === 비교 시 주의
id === 3    // false ("3" !== 3)

// ✅ 숫자로 변환 후 비교
Number(id) === 3  // true
```

### 라우터 설정

```jsx
// src/router/index.jsx
import { createBrowserRouter } from "react-router-dom";
import Layout from "../layouts/Layout";
import Home from "../pages/Home";
import PostList from "../pages/PostList";
import PostDetail from "../pages/PostDetail";

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
        path: "posts",
        element: <PostList />,
      },
      {
        path: "posts/:id",
        element: <PostDetail />,
      },
    ],
  },
]);

export default router;
```

- `posts/:id`에서 `:id`가 URL 파라미터이다
- `/posts/3`으로 접속하면 `id`의 값은 `"3"`이 된다

### 목록 페이지

```jsx
// src/pages/PostList.jsx
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axios from "axios";

const PostList = () => {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    const fetchPosts = async () => {
      const response = await axios.get(
        "https://jsonplaceholder.typicode.com/posts"
      );
      setPosts(response.data.slice(0, 10));
    };

    fetchPosts();
  }, []);

  return (
    <div>
      <h1>게시글 목록</h1>
      <ul>
        {posts.map((post) => (
          <li key={post.id}>
            <Link to={`/posts/${post.id}`}>{post.title}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default PostList;
```

- `Link`의 `to`에 템플릿 리터럴로 각 게시글의 id를 넣어 동적 경로를 만든다
- 클릭하면 `/posts/1`, `/posts/2` 등으로 이동한다

### 상세 페이지

```jsx
// src/pages/PostDetail.jsx
import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";

const PostDetail = () => {
  const { id } = useParams();
  const [post, setPost] = useState(null);

  useEffect(() => {
    const fetchPost = async () => {
      const response = await axios.get(
        `https://jsonplaceholder.typicode.com/posts/${id}`
      );
      setPost(response.data);
    };

    fetchPost();
  }, [id]);

  return (
    <div>
      <h1>{post?.title}</h1>
      <p>{post?.body}</p>
      <Link to="/posts">← 목록으로</Link>
    </div>
  );
};

export default PostDetail;
```

- `useParams()`는 URL 파라미터를 **객체**로 반환한다
- `const { id } = useParams()`로 `:id` 값을 가져온다
- `useEffect`의 의존성 배열에 `id`를 넣어, URL이 바뀌면 API를 다시 호출한다