# 쿼리 스트링 (Query String)

- URL 뒤에 `?`를 붙여서 **추가 정보를 전달**하는 방식이다
- `key=value` 형태이며, 여러 개는 `&`로 연결한다

```
/posts?page=2
/posts?page=2&limit=10
/search?keyword=react
/products?category=shoes&sort=price
```

- 동적 라우팅(`:id`)은 **어떤 데이터인지** 식별할 때 사용한다 → `/posts/3`
- 쿼리 스트링은 **옵션이나 조건**을 전달할 때 사용한다 → `/posts?page=2`

|  | URL 파라미터 | 쿼리 스트링 |
| --- | --- | --- |
| 형태 | `/posts/:id` | `/posts?page=2` |
| 용도 | 특정 데이터 식별 | 검색, 필터, 정렬, 페이지네이션 |
| Hook | `useParams` | `useSearchParams` |
| 필수 여부 | 필수 (없으면 라우트 매칭 안 됨) | 선택 (없어도 페이지 접근 가능)
단, 강제하도록 할 수는 있음. |

## useSearchParams

- `useSearchParams`는 쿼리 스트링을 **읽고 쓸 수 있는** Hook이다
- `useState`와 비슷한 형태로 `[searchParams, setSearchParams]`를 반환한다

```jsx
import { useSearchParams } from "react-router-dom";

const ProductList = () => {
  const [searchParams, setSearchParams] = useSearchParams();

  // 쿼리 스트링 읽기
  const page = searchParams.get("page"); // "2" (문자열) 또는 null

  return <p>현재 페이지: {page}</p>;
};
```

- `searchParams.get("key")`로 값을 가져온다
- 해당 키가 없으면 `null`을 반환한다
- 값은 항상 **문자열**이다 (숫자가 필요하면 `Number()`로 변환)

### searchParams 주요 메서드

| 메서드 | 설명 | 예시 (URL: `?page=2&sort=title`) |
| --- | --- | --- |
| `get("key")` | 값 가져오기 | `searchParams.get("page")` → `"2"` |
| `get("key")` | 없는 키 | `searchParams.get("name")` → `null` |
| `has("key")` | 키 존재 여부 | `searchParams.has("sort")` → `true` |
| `toString()` | 전체 쿼리 스트링 | `searchParams.toString()` → `"page=2&sort=title"` |

### 쿼리 스트링 변경하기

- `setSearchParams`로 쿼리 스트링을 변경하면 **URL이 바뀌고 컴포넌트가 리렌더링**된다
- 객체를 전달하면 기존 쿼리 스트링을 **전체 교체**한다

```jsx
import { useSearchParams } from "react-router-dom";

const ProductList = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const page = Number(searchParams.get("page")) || 1;

  const goToNextPage = () => {
    setSearchParams({ page: page + 1 });
  };

  const goToPrevPage = () => {
    setSearchParams({ page: page - 1 });
  };

  return (
    <div>
      <p>현재 페이지: {page}</p>
      <button onClick={goToPrevPage} disabled={page <= 1}>
        이전
      </button>
      <button onClick={goToNextPage}>다음</button>
    </div>
  );
};
```

- `Number(searchParams.get("page")) || 1` : 값이 없거나 숫자가 아니면 기본값 1을 사용한다
- "다음" 버튼을 클릭하면 URL이 `/posts?page=2` → `/posts?page=3`으로 변경된다

### 주의: setSearchParams는 전체 교체

```jsx
// 현재 URL: /posts?page=2&sort=title

setSearchParams({ page: 3 });
// 결과: /posts?page=3  (sort가 사라진다!)

setSearchParams({ page: 3, sort: "title" });
// 결과: /posts?page=3&sort=title  (둘 다 유지)
```

- 기존 쿼리 스트링을 유지하면서 일부만 바꾸려면 **모든 값을 함께 전달**해야 한다

---

## useLocation

- `useLocation`은 **현재 URL의 정보**를 가져오는 Hook이다
- 현재 어떤 경로에 있는지, 쿼리 스트링이 무엇인지 등을 확인할 수 있다

```jsx
import { useLocation } from "react-router-dom";

const MyPage = () => {
  const location = useLocation();

  console.log(location);
  // {
  //   pathname: "/posts",
  //   search: "?page=2",
  //   hash: "",
  //   key: "default"
  // }

  return <p>현재 경로: {location.pathname}</p>;
};
```

### location 객체의 주요 속성

| 속성 | 설명 | 예시 (URL: `/posts?page=2`) |
| --- | --- | --- |
| `pathname` | 현재 경로 | `"/posts"` |
| `search` | 쿼리 스트링 (`?` 포함) | `"?page=2"` |