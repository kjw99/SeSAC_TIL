## axios

- 외부 서버와 데이터를 주고받기 위한 HTTP 통신 라이브러리
    - 웹 브라우저에서 다른 서버의 데이터를 가져오거나 보낼 때 사용
- 비동기 방식으로 동작하여 서버 응답을 기다리는 동안 다른 작업 수행 가능

### 설치

```bash
npm install axios

```

**package.json 추가 작성**

```json
{
  "type": "module"
}

```

### 기본 구조

**async/await 방식**

```jsx
import axios from "axios";

const getPosts = async (url) =>{
  try{
    const response = await axios.get(url)
    console.log(response.data)
  } catch (error){
    console.error(error.message)
  }
  
}

getPosts(`https://jsonplaceholder.typicode.com/posts/1`);

```

---

### JavaScript의 async / await

- Python의 `async`/`await`와 같은 개념
- `async`: 함수 앞에 붙여서 비동기 함수로 선언
- `await`: 비동기 작업의 결과가 올 때까지 기다림

```python
# Python
async def get_data():
    result = await fetch_data()
    print(result)
```

```jsx
// JavaScript
async function getData() {
  const result = await fetchData();
  console.log(result);
}
```

---

## Axios 응답 객체

- Axios 요청의 결과로 받는 객체
- 다양한 정보를 포함하고 있음

```jsx
async function getUsers() {
  const response = await axios.get(
    "https://jsonplaceholder.typicode.com/users"
  );

  console.log(response.data); // 서버가 보내준 실제 데이터
  console.log(response.status); // HTTP 상태 코드 (200, 404 등)
}

getUsers();
```

### 에러 처리

- 서버 요청은 **항상 성공하지 않음** (네트워크 오류, 서버 오류 등)
- `try/catch`를 사용하여 에러 상황을 처리

```jsx
import axios from "axios";

async function getUser() {
  try {
    const response = await axios.get(
      "https://jsonplaceholder.typicode.com/users/1"
    );
    console.log(response.data);
  } catch (error) {
    console.error("에러 발생:", error.message);
  }
}

getUser();
```

---

### Query Params (쿼리 파라미터)

- URL 뒤에 `?key=value` 형태로 붙는 검색/필터 조건
- `params` 옵션을 사용하면 자동으로 URL에 붙여줌

```jsx
// params 없이 직접 작성
axios.get("https://example.com/posts?userId=1&page=2");

// params 옵션 사용 (같은 결과)
const config = {
  params: {
    userId: 1,
    page: 2,
  },
};

axios.get("<https://example.com/posts>", config);
```

**예시**

```jsx
import axios from "axios";

async function getUserPosts(userId) {
  const config = {
    params: {
      userId: userId,
    },
  };

  const response = await axios.get(
    "https://jsonplaceholder.typicode.com/posts",
    config
  );
  console.log(response.data);
}

getUserPosts(1); // userId가 1인 게시글만 가져옴
```

### Headers (헤더)

- 서버에 **추가 정보**를 전달할 때 사용
- 주로 인증 토큰(로그인 정보)을 보낼 때 사용

**예시: GET 요청에 헤더 추가**

```jsx
import axios from "axios";

async function getProtectedData() {
  const config = {
    headers: {
      Authorization: "Bearer abc123token",
    },
  };

  const response = await axios.get("https://example.com/api/data", config);
  console.log(response.data);
}
```

**예시: POST 요청에 헤더 추가**

- POST는 두 번째 인자가 `보낼 데이터`, 세 번째 인자가 `옵션(headers 등)`

```jsx
import axios from "axios";

async function createPost() {
  const newPost = {
    title: "새 게시글",
    body: "내용입니다.",
  };

  const config = {
    headers: {
      Authorization: "Bearer abc123token",
    },
  };

  const response = await axios.post(
    "https://example.com/api/posts",
    newPost,
    config
  );
  console.log(response.data);
}
```

### params와 headers 함께 사용

```jsx
const config = {
  params: {
    page: 1,
  },
  headers: {
    Authorization: "Bearer abc123token",
  },
};

axios.get("https://example.com/api/posts", config);
```