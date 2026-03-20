## Custom Hooks

- 반복되는 로직을 `use`로 시작하는 함수로 분리하는 것이다
- 예를 들어, 여러 컴포넌트에서 "API 호출 → 로딩 → 에러 처리"를 반복한다면, `useFetch`라는 Custom Hook으로 묶을 수 있다
- 코드 재사용의 핵심이며, 면접에서도 자주 물어보는 주제이다
- 검색 키워드: `React Custom Hook 만들기`

```jsx
// Custom Hook 정의
const useFetch = (url) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await axios.get(url);
        setData(res.data);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [url]);

  return { data, loading, error };
};

// 사용하는 쪽 — 한 줄로 API 호출 로직을 재사용한다
const App = () => {
  const { data, loading, error } = useFetch("https://api.example.com/posts");

  if (loading) return <p>로딩 중...</p>;
  if (error) return <p>에러 발생</p>;

  return <ul>{data.map((post) => <li key={post.id}>{post.title}</li>)}</ul>;
};
```

---

## useMemo / useCallback

- 불필요한 재계산이나 함수 재생성을 막아주는 성능 최적화 Hook이다
- `useMemo` — 계산 결과를 캐싱한다 (값이 바뀔 때만 다시 계산)
- `useCallback` — 함수를 캐싱한다 (의존성이 바뀔 때만 다시 생성)
- 면접에서 "리렌더링 최적화"와 함께 단골로 나오는 주제이다

```jsx
// useMemo — 무거운 계산 결과를 캐싱한다
const App = () => {
  const [count, setCount] = useState(0);
  const [text, setText] = useState("");

  // ❌ text만 바뀌어도 매번 다시 계산된다
  const total = items.reduce((sum, item) => sum + item.price, 0);

  // ✅ items가 바뀔 때만 다시 계산한다
  const total = useMemo(() => {
    return items.reduce((sum, item) => sum + item.price, 0);
  }, [items]);

  return (
    <div>
      <p>합계: {total}</p>
      <input value={text} onChange={(e) => setText(e.target.value)} />
    </div>
  );
};
```

```jsx
// useCallback — 함수를 캐싱한다
const App = () => {
  const [count, setCount] = useState(0);

  // ❌ 리렌더링마다 새 함수가 만들어진다
  const handleClick = () => setCount(count + 1);

  // ✅ count가 바뀔 때만 새 함수를 만든다
  const handleClick = useCallback(() => {
    setCount(count + 1);
  }, [count]);

  // 자식 컴포넌트에 함수를 넘길 때 효과가 있다
  return <ChildButton onClick={handleClick} />;
};
```

> **참고: React Compiler (React 19+)**
> 
> 
> React 19부터 도입된 React Compiler가 빌드 시점에 자동으로 memoization을 적용해준다.
> 따라서 `useMemo`, `useCallback`, `React.memo`를 직접 작성할 필요가 점점 없어지고 있다.
> 다만 면접에서는 여전히 이 Hook들의 개념과 동작 원리를 물어보므로, 원리는 알아둘 것.
> 검색 키워드: `React Compiler 자동 memoization`
> 

---

## TanStack Query (React Query)

- 서버에서 데이터를 가져오고 캐싱하는 것을 전문적으로 다루는 라이브러리이다
- `useEffect` + `useState`로 직접 API 호출, 로딩, 에러를 관리하는 코드를 대폭 줄여준다
- 자동 캐싱, 자동 재요청, 로딩/에러 상태 관리를 한 번에 해결한다
- 채용 공고에서 자주 등장하며, 실무에서 거의 표준처럼 쓰이는 라이브러리이다

```jsx
// ❌ 직접 관리 — useEffect + useState 3개를 매번 작성해야 한다
const App = () => {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const res = await axios.get("/api/posts");
        setPosts(res.data);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };
    fetchPosts();
  }, []);

  if (loading) return <p>로딩 중...</p>;
  if (error) return <p>에러 발생</p>;

  return <ul>{posts.map((p) => <li key={p.id}>{p.title}</li>)}</ul>;
};
```

```jsx
// ✅ TanStack Query — 위 코드와 동일한 동작 + 캐싱, 자동 재요청까지 포함
const App = () => {
  const { data: posts, isLoading, error } = useQuery({
    queryKey: ["posts"],
    queryFn: () => axios.get("/api/posts").then((res) => res.data),
  });

  if (isLoading) return <p>로딩 중...</p>;
  if (error) return <p>에러 발생</p>;

  return <ul>{posts.map((p) => <li key={p.id}>{p.title}</li>)}</ul>;
};
```

---

## Suspense / React.lazy

- 컴포넌트를 필요할 때 불러오는(코드 스플리팅) 기능이다
- 앱이 커지면 처음 로딩할 때 모든 코드를 한 번에 불러오면 느려진다
- `React.lazy`로 특정 페이지/컴포넌트를 나중에 불러오고, `Suspense`로 로딩 중 화면을 보여준다

---

## Next.js

- React 기반의 풀스택 프레임워크이다
- SSR(서버 사이드 렌더링), SSG(정적 사이트 생성) 등 다양한 렌더링 방식을 지원한다
- 파일 기반 라우팅, API 라우트, 이미지 최적화 등 실무에 필요한 기능이 내장되어 있다
- React 채용 공고에서 가장 많이 요구하는 프레임워크이다

---

## 테스트 (Vitest + React Testing Library)

- 작성한 컴포넌트와 로직이 의도대로 동작하는지 자동으로 검증하는 방법이다
- Vitest — Vite 기반의 빠른 테스트 러너이다 (Jest 대체)
- React Testing Library — 컴포넌트를 사용자 관점에서 테스트한다 (버튼 클릭, 텍스트 확인 등)
- 면접에서 테스트 경험을 물어보는 회사가 많으며, 협업 시 코드 품질을 보장하는 핵심 도구이다

---

## UI 라이브러리 (shadcn/ui, MUI 등)

- 버튼, 모달, 드롭다운 같은 UI 컴포넌트를 직접 만들지 않고 가져다 쓰는 방법이다
- shadcn/ui — Tailwind CSS 기반, 복사해서 커스터마이징하는 방식이다 (최근 가장 인기)
- MUI (Material UI) — 구글 디자인 시스템 기반, 오래된 만큼 레퍼런스가 풍부하다
- 실무에서는 거의 100% UI 라이브러리를 사용하므로, 하나쯤은 익숙해지면 좋다