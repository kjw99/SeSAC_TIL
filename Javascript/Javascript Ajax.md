## AJAX란?

- **Asynchronous JavaScript and XML**의 약자
- 페이지 **새로고침 없이** 서버와 데이터를 주고받는 기술
- 현재 대부분의 웹사이트가 이 방식으로 동작

### AJAX가 없던 시절

1. 사용자가 버튼 클릭
2. 서버에 요청
3. 서버가 새로운 HTML 페이지 전체를 응답
4. 브라우저가 페이지 전체를 새로고침 ← 화면이 깜빡임

### AJAX를 사용하면

1. 사용자가 버튼 클릭
2. JavaScript가 서버에 요청 (AJAX)
3. 서버가 데이터(JSON)만 응답
4. JavaScript가 받은 데이터로 필요한 부분만 변경 ← 화면 깜빡임 없음

- 우리가 사용하는 **Axios**가 바로 이 AJAX 요청을 보내는 라이브러리
- Axios 외에도 `fetch`, `XMLHttpRequest` 등을 통해 AJAX를 구현할 수 있다.

---

## CDN

- **Content Delivery Network** - 라이브러리 파일을 인터넷에서 바로 가져오는 방식
- npm 설치 없이 `<script>` 태그 한 줄로 라이브러리 사용 가능

### npm 설치 vs CDN

| 방식 | 사용법 | 적합한 환경 |
| --- | --- | --- |
| npm 설치 | `npm install axios` → `import axios from "axios"` | Vite, React 등 번들러 사용 시 |
| CDN | `<script src="CDN주소"></script>` | HTML + JS 파일만 사용할 때 |

### CDN 사용법

```html
<!-- HTML의 <head> 또는 <body>에 추가 -->
<script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
```

- 이 한 줄만 추가하면 JS 파일에서 `axios`를 바로 사용할 수 있음
- `import` 없이 전역에서 `axios.get()`, `axios.post()` 등 사용 가능

---

# 실습

- DOM 조작 / 이벤트 / Axios를 활용해 버튼을 클릭하면 TMDB의 data를 화면에 그려주는 기능을 구현해보자.

## 프로젝트 셋업

### HTML 기본 구조

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>TMDB 영화 검색</title>
  <!-- Axios CDN -->
  <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
  <style>
    .movie-list {
      display: flex;
      flex-wrap: wrap;
      gap: 20px;
    }
    .movie-card {
      width: 200px;
      text-align: center;
    }
    .movie-card img {
      width: 100%;
      border-radius: 8px;
    }
  </style>
</head>
<body>
  <h1>TMDB 영화</h1>
  <button id="load-btn">영화 불러오기</button>
  <div id="movie-list" class="movie-list"></div>

  <script src="now_playing.js"></script>
</body>
</html>
```

- Axios를 CDN으로 불러옴 (설치 없이 `<script>` 태그로 사용)
- `#load-btn`: 클릭하면 API 요청을 보낼 버튼
- `#movie-list`: 영화 카드들이 들어갈 빈 컨테이너

---

## 버튼 클릭 시 API 요청 보내기

```jsx
// now_playing.js

const API_KEY = "";
const BASE_URL = "https://api.themoviedb.org/3";

const button = document.querySelector("#load-btn");
const loadMovies = async function () {
  const config = {
    params: {
      language: "ko-KR",
      page: 1,
    },
    headers: {
      Authorization: `Bearer ${API_KEY}`,
    },
  };
  const response = await axios.get(`${BASE_URL}/movie/now_playing`, config);

  console.log(response.data);
};
button.addEventListener("click", loadMovies);

```

- 버튼 클릭 → `addEventListener`로 이벤트 감지
- 콜백 함수에 `async`를 붙여서 내부에서 `await` 사용
- `params` 옵션으로 쿼리 파라미터 전달

## 받은 데이터를 DOM에 그리기

```jsx
// now_playing.js

const API_KEY = "";
const BASE_URL = "https://api.themoviedb.org/3";
const IMAGE_URL = "https://image.tmdb.org/t/p/w500";

const button = document.querySelector("#load-btn");
const movieList = document.querySelector("#movie-list");

const loadMovies = async function () {
  const config = {
    params: {
      language: "ko-KR",
      page: 1,
    },
    headers: {
      Authorization: `Bearer ${API_KEY}`,
    },
  };
  const response = await axios.get(`${BASE_URL}/movie/now_playing`, config);

  const movies = response.data.results;

  // 기존 내용 비우기
  movieList.innerHTML = "";

  for (let movie of movies) {
    // 카드 div 생성
    const card = document.createElement("div");
    card.className = "movie-card";

    // 포스터 이미지
    const img = document.createElement("img");
    img.src = `${IMAGE_URL}${movie.poster_path}`;
    img.alt = movie.title;

    // 제목
    const title = document.createElement("h3");
    title.textContent = movie.title;

    // 평점
    const rating = document.createElement("p");
    rating.textContent = `평점: ${movie.vote_average}`;

    // 카드에 요소들 추가
    card.appendChild(img);
    card.appendChild(title);
    card.appendChild(rating);

    // 화면에 추가
    movieList.appendChild(card);
  }
};

button.addEventListener("click", loadMovies);

```

### 전체 흐름 정리

1. 버튼 클릭
2. 이벤트 핸들러 실행
3. axios.get()으로 TMDB API에 요청
4. await로 응답 기다림
5. response.data.results에서 영화 배열 꺼냄
6. for문으로 영화 하나하나 DOM 요소 생성
7. appendChild로 화면에 추가

---

## 에러 처리 추가

- API 키가 잘못되거나 네트워크 오류가 발생할 수 있음
- `try/catch`로 에러 상황 처리

```jsx
const loadMovies = async function () {
  try {
    const config = {
      params: {
        language: "ko-KR",
        page: 1,
      },
      headers: {
        Authorization: `Bearer ${API_KEY}`,
      },
    };
    const response = await axios.get(`${BASE_URL}/movie/now_playing`, config);

    const movies = response.data.results;
    movieList.innerHTML = "";

    for (let movie of movies) {
      const card = document.createElement("div");
      card.className = "movie-card";

      const img = document.createElement("img");
      img.src = `${IMAGE_URL}${movie.poster_path}`;
      img.alt = movie.title;

      const title = document.createElement("h3");
      title.textContent = movie.title;

      const rating = document.createElement("p");
      rating.textContent = `평점: ${movie.vote_average}`;

      card.appendChild(img);
      card.appendChild(title);
      card.appendChild(rating);
      movieList.appendChild(card);
    }
  } catch (error) {
    movieList.innerHTML = "<p>영화를 불러오는 데 실패했습니다.</p>";
    console.log("에러 발생:", error.message);
  }
};

```

- `catch` 블록에서 사용자에게 에러 메시지를 보여줌
- 콘솔에도 에러 내용을 출력하여 디버깅에 활용

---

## 버튼 없이 페이지 진입 시 자동 실행

- 실제 서비스는 페이지에 들어오면 **자동으로** 데이터를 보여줌
- 버튼과 이벤트 리스너를 없애고, **async 함수를 만들어 바로 호출**하면 됨

### 변경 전 (버튼 클릭)

```jsx
button.addEventListener("click", loadMovies); // 버튼을 클릭해야 실행
```

### 변경 후 (페이지 진입 시 자동 실행)

```jsx
loadMovies(); // 바로 호출
```

- `<script>`가 `</body>` 바로 위에 있으면, 실행 시점에 이미 DOM이 준비된 상태
- 그래서 별도의 이벤트 없이 **함수를 선언하고 바로 호출**하면 됨

### HTML 변경

```html
<!-- 변경 전 -->
<button id="load-btn">영화 불러오기</button>
<div id="movie-list" class="movie-list"></div>

<!-- 변경 후: 버튼 제거 -->
<div id="movie-list" class="movie-list"></div>
```

### 전체 코드

```jsx
const API_KEY = "";
const BASE_URL = "https://api.themoviedb.org/3";
const IMAGE_URL = "https://image.tmdb.org/t/p/w500";

const button = document.querySelector("#load-btn");
const movieList = document.querySelector("#movie-list");

const loadMovies = async function () {
  try {
    const config = {
      params: {
        language: "ko-KR",
        page: 1,
      },
      headers: {
        Authorization: `Bearer ${API_KEY}`,
      },
    };
    const response = await axios.get(`${BASE_URL}/movie/now_playing`, config);

    const movies = response.data.results;

    // 기존 내용 비우기
    movieList.innerHTML = "";

    for (let movie of movies) {
      // 카드 div 생성
      const card = document.createElement("div");
      card.className = "movie-card";

      // 포스터 이미지
      const img = document.createElement("img");
      img.src = `${IMAGE_URL}${movie.poster_path}`;
      img.alt = movie.title;

      // 제목
      const title = document.createElement("h3");
      title.textContent = movie.title;

      // 평점
      const rating = document.createElement("p");
      rating.textContent = `평점: ${movie.vote_average}`;

      // 카드에 요소들 추가
      card.appendChild(img);
      card.appendChild(title);
      card.appendChild(rating);

      // 화면에 추가
      movieList.appendChild(card);
    }
  } catch (error) {
    movieList.innerHTML = "<p>영화를 불러오는 데 실패했습니다.</p>";
    console.log("에러 발생:", error.message);
  }
};

// button.addEventListener("click", loadMovies);
loadMovies();

```

---

## 영화 검색 기능 만들기

- 인기 영화 대신 **사용자가 입력한 키워드**로 검색
- `<form>` 태그를 사용하면 **버튼 클릭**뿐만 아니라 **Enter 키**로도 검색 가능

### form 태그와 submit 이벤트

- `<form>`은 사용자 입력을 묶어주는 태그
- `<form>` 안에서 버튼을 클릭하거나 Enter를 누르면 **`submit` 이벤트**가 발생
- `submit`의 기본 동작은 **페이지 새로고침** → `preventDefault()`로 막아야 함

```jsx
form.addEventListener("submit", function (event) {
  event.preventDefault(); // 페이지 새로고침 방지
  // 검색 로직
});
```

### HTML 추가

```html
<form id="search-form">
  <input type="text" id="search-input" placeholder="영화 제목을 입력하세요" />
  <button type="submit">검색</button>
</form>

<script src="search.js"></script>
```

### JavaScript 작성

```jsx
// search.js
const searchForm = document.querySelector("#search-form");
const searchInput = document.querySelector("#search-input");

// 검색 함수 정의
async function searchMovies(event) {
  // form의 기본 동작(페이지 새로고침) 방지
  event.preventDefault();

  // 입력값 가져오기 (앞뒤 공백 제거)
  const keyword = searchInput.value.trim();

  // 빈 검색어 체크
  if (keyword === "") {
    alert("검색어를 입력해주세요!");
    return;
  }

  try {
    // API 요청 설정 
    const config = {
      params: {
        language: "ko-KR",
        query: keyword,
      },
      headers: {
        Authorization: `Bearer ${API_KEY}`,
      },
    };

    // TMDB 검색 API 요청
    const response = await axios.get(`${BASE_URL}/search/movie`, config);

    const movies = response.data.results;

    // 기존 내용 비우기
    movieList.innerHTML = "";

    // 검색 결과가 없는 경우
    if (movies.length === 0) {
      movieList.innerHTML = "<p>검색 결과가 없습니다.</p>";
      return;
    }

    // 영화 카드 생성 및 화면에 추가
    for (let movie of movies) {
      const card = document.createElement("div");
      card.className = "movie-card";

      const img = document.createElement("img");
      img.src = `${IMAGE_URL}${movie.poster_path}`;
      img.alt = movie.title;

      const title = document.createElement("h3");
      title.textContent = movie.title;

      const rating = document.createElement("p");
      rating.textContent = `평점: ${movie.vote_average}`;

      card.appendChild(img);
      card.appendChild(title);
      card.appendChild(rating);
      movieList.appendChild(card);
    }
  } catch (error) {
    // 에러 발생 시 사용자에게 메시지 표시
    movieList.innerHTML = "<p>검색 중 오류가 발생했습니다.</p>";
    console.log("에러 발생:", error.message);
  }
}

// form에 submit 이벤트 등록 (버튼 클릭 + Enter 키 모두 동작)
searchForm.addEventListener("submit", searchMovies);

```