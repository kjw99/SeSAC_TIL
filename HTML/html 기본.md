## 프론트엔드

- 프론트엔드(Frontend)는 사용자가 웹 브라우저를 통해 상호작용하는 웹 애플리케이션의 클라이언트 사이드 부분을 의미한다.
- 주로 사용자 경험(UX)과 사용자 인터페이스(UI)를 개발하는 데 초점을 맞추며, 웹사이트의 디자인, 레이아웃, 그리고 동작 방식을 구현한다.
- HTML, CSS, JavaScript로 구현한다.
    - HTML : 화면의 내용 및 구조를 나타낸다.
    - CSS : 화면의 구도 및 스타일을 지정한다.
    - JavaScript : 화면에 동적인 요소를 추가하여 사용자와 상호작용할 수 있도록 한다.
## HTML(Hyper Text Markup Language)

### 하이퍼 텍스트(Hyper Text)

- 다른 문서 또는 웹 페이지로 연결하는 텍스트
- [구글 페이지](https://www.google.com/)에서 `Gmail` 링크를 클릭해서 페이지를 이동하는 것이 하이퍼 텍스트의 대표적인 예시

### 마크업 언어(Markup Language)

- 태그(tag) 를 사용하여 문서를 구조화하고, 내용을 표현하는 언어
- Gmail은 `<a>` 태그로 정의된 텍스트이며, 클릭하면 다른 페이지로 이동한다
    
    ```html
    <a href="https://mail.google.com/">Gmail</a>
    ```
    

---

## 요소(Element)

- 웹 페이지의 **구조와 컨텐츠를 만드는 기본 단위**
- HTML 문서는 수 많은 요소들로 구성되고, 각 요소는 특정 기능과 의미를 가진다

### 요소의 구조

```html
<태그 속성="값">내용</태그>
```

- **태그** : 요소의 기능을 나타내고, 시작 태그 `<>` 와 종료 태그 `</>` 로 구성된다.
    - `<a href="https://google.com">google.com</a>` 에서 `<a>` `</a>` 부분이 태그
- **속성** : 요소의 추가 특성을 나타내고, 시작 태그 내부에 작성한다.
    - `<a href="https://google.com">google.com</a>` 에서 `href` 부분이 속성
- **내용** : 화면에 표시할 텍스트 또는 또 다른 요소를 작성한다.
    - `<a href="https://google.com">google.com</a>` 에서 `google.com` 부분이 내용

## 태그(Tags)

- **요소의 기능과 역할을 결정**
- 태그는 시작 태그 `<>` 와 종료 태그 `</>` 로 구성된다
- 하지만, 종료 태그가 없는 태그도 존재한다

### 텍스트 관련 태그

- `<h1>` ~ `<h6>` : 제목을 표시하고, 숫자가 작을수록 크기가 크다
- `<p>` : 단락(Paragraph)을 나타낸다
- `<a>` : 하이퍼링크를 나타낸다. `href` 속성으로 링크 대상을 지정한다
- `<br>` : 줄바꿈을 삽입하는 태그로 종료 태그가 없다. 줄바꿈을 삽입하는 태그이다

```html
<!-- 제목 태그 -->
<h1>이것은 h1 제목이다.</h1>
<h2>이것은 h2 제목이다.</h2>
<h3>이것은 h3 제목이다.</h3>
<h4>이것은 h4 제목이다.</h4>
<h5>이것은 h5 제목이다.</h5>
<h6>이것은 h6 제목이다.</h6>

<!-- 단락 태그 -->
<p>이것은 단락(p) 태그로 작성된 문장이다. 문단을 표현할 때 사용된다.</p>

<!-- 하이퍼링크 태그 -->
<p>다음은 <a href="https://example.com">Example.com</a> 사이트로의 링크이다.</p>

<!-- 줄바꿈 태그 -->
<p>이 텍스트는 줄바꿈을 할 것이다.<br />여기서 줄이 바뀌었다.</p>
```

### 이미지 및 멀티미디어 태그

- `<img>` : 문서에 이미지 파일을 삽입한다. `src` 속성으로 이미지 파일 경로를 지정한다.
- `<audio>` : 문서에 오디오 파일을 삽입한다. `src` 속성으로 오디오 파일 경로를 지정한다.
- `<video>` : 문서에 비디오 파일을 삽입한다. `src` 속성으로 비디오 파일 경로를 지정한다.

```html
<img src="https://example.com/image.png" alt="이미지 설명" />
<audio src="https://example.com/audio.mp3" controls />
<video src="https://example.com/video.mp4" controls />
```

---

## 속성(Attribute)

- 요소에 추가적인 정보와 기능을 제공한다
- 속성은 속성 이름과 값으로 구성된다. `속성명="값"` 형태로 작성한다

### id 속성

- 요소에 **고유한 식별자를 부여**
- 문서 내에서 id의 값들은 중복되면 안된다
- `id="id명"` 형태로 작성한다

### class 속성

- 여러개의 **요소를 그룹화**하기 위해 사용
- 하나의 요소에 여러개의 클래스를 지정하거나, 하나의 클래스를 여러개의 요소에 지정할 수 있다
- 여러개의 클래스를 지정할 때 공백을 통해 클래스를 구분한다
- `class="class-1 class-2"` 형태로 작성한다

### style 속성

- 요소에 인라인 스타일을 지정한다. 인라인 스타일은 요소에 직접 스타일을 적용하는 방식이다
- `style="속성1: 값; 속성2: 값; 속성3: 값;"` 형태로 작성한다

### 그외 속성

- `src` : 이미지, 비디오 등 파일의 경로를 지정한다.
- `href` : a 태그의 고유 속성으로 클릭했을 때 이동할 주소를 지정한다.

## 요소 중첩

- 요소 내부에 또 다른 요소를 중첩해서 사용할 수 있다
- 웹 페이지의 복잡한 구조를 표현하기 위한 중요한 개념

### 기본 구조

```html
<div>
  <h1>h1 태그</h1>
  <div>
    <h3>h3 태그</h3>
    <div>
      <p>p 태그</p>
      <p>p 태그</p>
      <p>p 태그</p>
    </div>
  </div>
</div>

```

### 중첩 예시

```html
<div>
  <h3>오늘의 할 일</h3>
  <div>
    <p>복습하기</p>
    <p>기한 : 22시까지</p>
  </div>
  <div>
    <p>예습하기</p>
    <p>기한 : 23시까지</p>
  </div>
</div>

```

## HTML 주석

- 실제 **웹 페이지에 표시되지 않는 문서 내 개발자를 위한 설명문**
- 문서 내에서 설명을 추가하거나 문서 일부를 비활성화 하는데 사용된다

### 주석 작성 방법

- `<!-- 주석 내용 -->` 형태로 작성한다.

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>

  <body>
    <!-- 이 콘텐츠는 주석이기 때문에 웹 페이지에 표시되지 않는다.-->
  </body>
</html>

```

### 주석 작성 주의사항

- 주석 내부에 또 다른 주석은 사용할 수 없다
- 주석을 너무 길게 작성하지 않는다. 너무 긴 주석은 가독성을 떨어뜨린다
- 주석에 중요한 정보를 포함하면 안된다. 주석은 웹 페이지에 표시되지는 않지만 개발자 도구를 통해 주석은 볼 수 있다. 주석에 비밀번호를 작성하면 개발자 도구를 통해 비밀번호를 확인할 수 있다

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>

  <body>
    <!--
        <!-- 주석안에 주석을 사용할 수 없다. -->
    -->
  </body>
</html>

```

## HTML 문서 구조

- 웹 페이지를 표현하는 HTML 문서의 기본적인 구조

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>

  <body></body>
</html>

```

### `<!DOCTYPE html>`

- 문서의 형식이 html 임을 나타낸다

### `<html></html>`

- html 문서 전체를 감싸는 루트 요소이다

### `<head></head>`

- 메타데이터, 스타일 시트, 스크립트 등 문서를 정의하는 정보를 포함하는 영역
- 메타데이터 : 페이지의 제목, 작성자, 날짜 등을 정의하는 정보

### `<body></body>`

- **웹 페이지의 컨텐츠**가 들어가는 영역

---

## 브라우저 개발자 도구

- 웹 페이지의 HTML 문서, 스타일, 네트워크 등을 분석할 수 있는 도구
- 브라우저 개발자 도구는 일반적으로 사용하는 브라우저에 내장되어 있다
- 키보드의 **F12 키** 또는 **Ctrl + Shift + I** 키를 누르면 열 수 있다

### 요소(Elements) 메뉴

- HTML 문서 구조와 CSS 스타일을 실시간으로 분석하고 수정할 수 있다
- 왼쪽 상단의 **검사 요소 선택** 버튼을 활용해서 특정 요소를 선택할 수 있다
### 콘솔(Console) 메뉴

- 자바스크립트 코드를 실행하고 결과를 확인할 수 있다
- 오류와 경고를 확인해서 버그를 추적하고 해결할 수 있다

## 기능에 따른 분류

- HTML 태그는 웹 페이지에서 수행하는 역할에 따라 다음과 같이 분류할 수 있다

### 구조 정의 태그

- 문서의 전체 구조와 메타데이터를 정의하는 태그
- `<html>` : HTML 문서의 루트 요소
- `<head>` : 문서의 메타데이터 영역
- `<body>` : 문서의 본문 내용 영역

```html
<!DOCTYPE html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <title>웹 페이지 제목</title>
  </head>
  <body>
    <!-- 본문 내용 -->
  </body>
</html>

```

### 콘텐츠 표시 태그

- 텍스트 콘텐츠를 화면에 표시하는 태그
- `<h1>` ~ `<h6>` : 제목 태그
- `<p>` : 단락 태그
- `<span>` : 단순 인라인 레벨 컨테이너
- `<ul>` : 순서 없는 목록 (Unordered List)
- `<ol>` : 순서 있는 목록 (Ordered List)
- `<li>` : 목록의 각 항목 (List Item)

```html
<h1>메인 제목</h1>
<h2>부제목</h2>
<p>이것은 단락입니다. <span>강조된 텍스트</span>가 포함되어 있습니다.</p>

<ul>
  <li>항목 1</li>
  <li>항목 2</li>
  <li>항목 3</li>
</ul>

<ol>
  <li>첫 번째</li>
  <li>두 번째</li>
  <li>세 번째</li>
</ol>
```

### 레이아웃 태그

- 문서의 레이아웃과 구조를 정의하는 태그
- `<div>` : 단순 블록 레벨 컨테이너
- `<header>` : 머리말 영역
- `<nav>` : 내비게이션 링크 그룹
- `<main>` : 주요 콘텐츠 영역
- `<aside>` : 본문과 간접적으로 관련된 콘텐츠 (사이드바 등)
- `<section>` : 문서내 그룹화된 콘텐츠
- `<article>` : 독립적인 콘텐츠 영역
- `<footer>` : 바닥글 영역

```html
<div>
  <header>
    <h1>사이트 제목</h1>
  </header>
  <main>
	  <section>
	    <article>
	      <h2>기사 제목</h2>
	      <p>기사 내용...</p>
	    </article>
	  </section>
  </main>
  <footer>
    <p>저작권 정보</p>
  </footer>
</div>

```

### 멀티미디어 콘텐츠 태그

- 이미지, 오디오, 비디오 등 멀티미디어 콘텐츠를 삽입하는 태그
- `<img>` : 이미지 삽입
- `<audio>` : 오디오 파일 삽입
- `<video>` : 비디오 파일 삽입

```html
<img src="image.jpg" alt="대체 텍스트" />
<audio src="music.mp3" controls></audio>
<video src="video.mp4" controls></video>

```

### 상호작용 태그

- 사용자와 웹 페이지 간의 상호작용을 가능하게 하는 태그
- `<form>` : 폼 컨테이너
- `<input>` : 입력 필드
- `<select>` : 드롭다운 목록
- `<button>` : 버튼

```html
<form>
  <input type="text" placeholder="이름을 입력하세요" />
  <select>
    <option value="option1">옵션 1</option>
    <option value="option2">옵션 2</option>
  </select>
  <button type="submit">제출</button>
</form>

```

---

## display 속성에 따른 분류

### block 태그

- 문서의 구조를 구성하는 태그
- 부모 요소의 전체 너비를 차지한다
- 너비와 높이를 지정할 수 있다
- `<div>`, `<p>`, `<h1>` ~ `<h6>`, `<ul>`, `<ol>`, `<li>`

```html
<div style="background-color: lightblue;">첫 번째 div</div>
<div style="background-color: lightgreen;">두 번째 div</div>
<p>단락 태그도 block 태그입니다.</p>

```

### inline 태그

- 문서의 콘텐츠를 감싸는 태그
- 콘텐츠 크기만큼의 너비를 차지한다
- 너비와 높이를 지정할 수 없다
- 텍스트나 다른 inline 요소를 감싸는 데 사용된다. 예를 들어 `<span>` 태그는 텍스트를 감싸는 용도
- `<span>`, `<a>`, `<strong>`

```html
<p>
  이 문장에는 <span style="color: red;">빨간 텍스트</span>와
  <a href="#">링크</a>가 포함되어 있습니다.
</p>

```

---

## 의미론적 태그와 비의미론적 태그

### 의미론적 태그(Semantic Tags)

- 태그 이름을 통해 콘텐츠의 의미와 역할을 명확하게 전달하는 태그
- **의미론적 태그의 장점**
    - 문서의 구조와 내용을 명확히 정의
    - 웹 접근성 향상
    - 검색 엔진 최적화(SEO)
- **주요 의미론적 태그**
    - `<p>`, `<h#>`
    - `<header>` : 문서나 섹션의 머리말
    - `<nav>` : 내비게이션 링크 그룹
    - `<main>` : 문서의 주요 콘텐츠
    - `<article>` : 독립적이고 완전한 콘텐츠 블록
    - `<section>` : 문서의 논리적 구역
    - `<aside>` : 본문과 간접적으로 관련된 콘텐츠
    - `<footer>` : 문서나 섹션의 바닥글
    - `<strong>` : 중요한 텍스트 (굵게 표시)
    - `<em>` : 강조된 텍스트 (기울임 표시)

```html
<article>
  <header>
    <h1>블로그 포스트 제목</h1>
    <p>작성일: 2024년 1월 1일</p>
  </header>
  <section>
    <p>블로그 포스트 내용...</p>
  </section>
  <footer>
    <p>작성자: 홍길동</p>
  </footer>
</article>

```

### 비의미론적 태그(Non-semantic Tags)

- 태그 이름이 콘텐츠의 의미를 전달하지 않는 태그
- 웹 페이지를 구조화하는 데 사용된다
- **주요 비의미론적 태그**
    - `<div>`, `<span>`, `<b>`, `<i>`

## `<a>` 하이퍼링크 태그

- 다른 페이지나 특정 위치로 이동하는 링크를 만드는 태그
- `href` : 이동할 주소를 지정한다
- `target` : 링크를 열 방식을 지정한다
    - `_self` : 현재 탭에서 열기 (기본값)
    - `_blank` : 새 탭에서 열기

```html
<!-- 외부 링크 (새 탭에서 열기) -->
<a href="https://www.google.com" target="_blank">구글로 이동</a>

<!-- 내부 링크 (같은 사이트 내 이동) -->
<a href="/about">소개 페이지</a>

<!-- 페이지 내 특정 위치로 이동 (id 활용) -->
<a href="#section1">섹션 1로 이동</a>

<h2 id="section1">섹션 1</h2>
<p>이 위치로 스크롤된다.</p>
```

---

## `<img>` 이미지 태그

- 문서에 이미지를 삽입하는 태그. 종료 태그가 없다
- `src` : 이미지 파일 경로
- `alt` : 이미지를 표시할 수 없을 때 보여줄 대체 텍스트. 웹 접근성과 SEO에 중요하다
- `width`, `height` : 이미지의 너비와 높이를 지정한다

```html
<!-- 기본 사용 -->
<img src="photo.jpg" alt="풍경 사진" />

<!-- 크기 지정 -->
<img src="photo.jpg" alt="풍경 사진" width="400" height="300" />
```

---

## `<audio>` / `<video>` 멀티미디어 태그

- 오디오, 비디오 파일을 삽입하는 태그
- 공통 속성
    - `src` : 파일 경로
    - `controls` : 재생, 일시정지, 볼륨 등 컨트롤 버튼을 표시한다
    - `autoplay` : 페이지 로드 시 자동 재생한다
    - `loop` : 반복 재생한다
- `<video>` 전용 속성
    - `poster` : 비디오 로드 전 표시할 썸네일 이미지를 지정한다
    - `width`, `height` : 비디오 플레이어의 크기를 지정한다

```html
<!-- 오디오 -->
<audio src="music.mp3" controls></audio>
<audio src="https://interactive-examples.mdn.mozilla.net/media/cc0-audio/t-rex-roar.mp3" controls></audio>

<!-- 비디오 (썸네일 포함) -->
<video src="video.mp4" controls poster="thumbnail.jpg" width="640"></video>

<!-- 자동 반복 재생 -->
<video src="background.mp4" autoplay loop></video>
<video src="https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4" autoplay loop></video>

```

---

## `<ul>` / `<ol>` / `<li>` 목록 태그

- `<ul>` : 순서 없는 목록 (Unordered List). 항목 앞에 점(●)이 표시된다
- `<ol>` : 순서 있는 목록 (Ordered List). 항목 앞에 번호가 표시된다
- `<li>` : 목록의 각 항목 (List Item). 반드시 `<ul>` 또는 `<ol>` 안에서 사용한다

```html
<!-- 순서 없는 목록 -->
<ul>
  <li>사과</li>
  <li>바나나</li>
  <li>포도</li>
</ul>

<!-- 순서 있는 목록 -->
<ol>
  <li>HTML 배우기</li>
  <li>CSS 배우기</li>
  <li>JavaScript 배우기</li>
</ol>
```

### 목록 중첩

- 목록 안에 또 다른 목록을 넣을 수 있다
- `<li>` 내부에 `<ul>` 또는 `<ol>`을 작성한다

```html
<ul>
  <li>프론트엔드
    <ul>
      <li>HTML</li>
      <li>CSS</li>
      <li>JavaScript</li>
    </ul>
  </li>
  <li>백엔드
    <ul>
      <li>Python</li>
      <li>Java</li>
    </ul>
  </li>
</ul>
```

---

## `<table>` 테이블 태그

- 데이터를 행과 열로 구성된 표 형태로 표시하는 태그
- `<table>` : 표 전체를 감싸는 컨테이너
- `<thead>` : 표의 머리글 영역
- `<tbody>` : 표의 본문 영역
- `<tr>` : 하나의 행 (Table Row)
- `<th>` : 머리글 셀 (Table Header). 기본적으로 굵게, 가운데 정렬된다
- `<td>` : 데이터 셀 (Table Data)

```html
<table>
  <thead>
    <tr>
      <th>이름</th>
      <th>나이</th>
      <th>직업</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>홍길동</td>
      <td>25</td>
      <td>개발자</td>
    </tr>
    <tr>
      <td>김철수</td>
      <td>30</td>
      <td>디자이너</td>
    </tr>
  </tbody>
</table>
```

---

## `<div>` 태그 활용

- `<div>`는 그 자체로는 의미가 없는 블록 레벨 컨테이너이다
- 여러 요소를 **그룹화**하거나 **스타일을 적용**할 때 사용한다

### 요소 그룹화

- 관련된 요소들을 하나로 묶어서 관리할 때 사용한다

```html
<div>
  <h3>공지사항</h3>
  <p>내일은 휴무입니다.</p>
  <p>다음 주 회의는 월요일입니다.</p>
</div>
```

### 스타일 적용 (class / id 활용)

- `class`나 `id`를 지정하여 CSS 스타일을 적용하는 단위로 활용한다

```html
<div class="card">
  <img src="product.jpg" alt="상품 이미지" />
  <h3>상품명</h3>
  <p>10,000원</p>
</div>

<div class="card">
  <img src="product2.jpg" alt="상품 이미지" />
  <h3>상품명 2</h3>
  <p>20,000원</p>
</div>
```

### 레이아웃 구성

- 페이지의 영역을 나누는 용도로 사용한다
- 단, 의미가 명확한 경우에는 시맨틱 태그(`<header>`, `<main>` 등)를 우선 사용한다

```html
<div class="container">
  <div class="sidebar">사이드바</div>
  <div class="content">메인 콘텐츠</div>
</div>
```

### `<div>` vs 시맨틱 태그

- 시맨틱 태그로 표현할 수 있으면 시맨틱 태그를 쓴다
- 단순히 스타일링이나 그룹화 목적일 때 `<div>`를 쓴다

```html
<!-- 좋은 예 : 의미에 맞는 시맨틱 태그 사용 -->
<header>
  <h1>사이트 제목</h1>
</header>

<!-- 나쁜 예 : 시맨틱 태그를 쓸 수 있는데 div 사용 -->
<div class="header">
  <h1>사이트 제목</h1>
</div>
```

---

## 자주 사용하는 태그들

| **태그** | **설명** | **용도** |
| --- | --- | --- |
| `<html>` | HTML 문서의 루트 요소 | 전체 HTML 문서를 감싸는 최상위 요소 |
| `<head>` | 문서의 메타데이터 영역 | 제목, 스타일, 스크립트 등 문서 정보 포함 |
| `<title>` | 문서의 제목 | 브라우저 탭에 표시되는 페이지 제목 |
| `<body>` | 문서의 본문 영역 | 사용자에게 보여지는 실제 콘텐츠 영역 |
| `<h1>~<h6>` | 제목 태그 | 문서의 제목과 부제목을 나타냄 (h1이 가장 큰 제목) |
| `<p>` | 문단 태그 | 텍스트의 문단을 구분 |
| `<div>` | 블록 레벨 컨테이너 | 콘텐츠를 그룹화하는 범용 컨테이너 |
| `<span>` | 인라인 컨테이너 | 텍스트의 일부분을 그룹화 |
| `<ul>` | 순서 없는 목록 | 불릿 포인트로 표시되는 목록 |
| `<ol>` | 순서 있는 목록 | 숫자나 문자로 순서가 매겨진 목록 |
| `<li>` | 목록 항목 | ul, ol 내부의 각 항목 |
| `<a>` | 하이퍼링크 태그 | 다른 페이지나 파일 등으로 연결 |
| `<img>` | 이미지 삽입 태그 | 웹 페이지에 이미지를 표시 |
| `<br>` | 줄바꿈 태그 | 텍스트에서 강제 줄바꿈 |
| `<hr>` | 수평선 태그 | 콘텐츠를 구분하는 수평선 |
| `<header>` | 헤더 영역 | 페이지나 섹션 상단의 로고, 메뉴 등을 포함 |
| `<nav>` | 네비게이션 | 페이지 이동을 위한 메뉴 링크 영역 |
| `<main>` | 메인 콘텐츠 | 문서의 핵심적인 주요 내용을 정의 |
| `<article>` | 독립적 콘텐츠 | 뉴스, 블로그 등 독립적으로 배포 가능한 영역 |
| `<section>` | 섹션 구분 | 문서의 주제별 영역을 논리적으로 구분 |
| `<aside>` | 사이드바 | 본문 옆의 부수적인 정보나 링크를 표시 |
| `<footer>` | 푸터 영역 | 페이지 하단의 저작권 정보, 연락처 등을 포함 |

## 폼(Form) 태그

- 사용자로부터 정보를 입력받고 웹 서버로 전송하는 태그

### 폼 태그 역할

- 사용자에게 정보를 입력받는다
    - 회원가입 폼
    - 로그인 폼
    - 검색 폼
    - 글 작성 폼
    - 결제 폼
- 입력된 정보를 웹 서버로 전송한다
- 여러 개의 입력(input) 요소를 하나로 묶어준다

### 기본 구조

```html
<form action="정보를 보낼 주소" method="보내는 방식">
  <!-- 입력 요소들 -->
</form>
```

- `action` : 입력된 정보를 보낼 주소(URL)
- `method` : 정보를 보내는 방식
    - GET
    - POST

---

## 입력(input) 태그

- 사용자가 정보를 입력할 수 있는 필드를 만드는 태그

### 기본 구조

```html
<input type="입력_종류" name="입력_이름" value="기본값" />
```

- `type` : 입력 종류
- `name` : 입력 이름 (서버로 전송할 때 사용)
- `value` : 입력 필드에 미리 작성할 기본 값
- `placeholder` : 입력 필드의 안내 문구
- `required` : 필수 입력 필드로 설정

---

## 입력 태그 종류

### 글자 입력 태그

- `text` : 일반 글자 입력
- `password` : 비밀번호 입력
- `email` : 이메일 입력
- `number` : 숫자 입력
- `tel` : 전화번호 입력
- `url` : 주소 입력

```html
<!-- 일반 글자 입력 -->
<input type="text" name="username" placeholder="사용자명을 입력하세요" />

<!-- 비밀번호 입력 (입력한 글자가 마스킹 처리됨) -->
<input type="password" name="password" placeholder="비밀번호를 입력하세요" />

<!-- 이메일 입력 (이메일 형식인지 자동으로 확인) -->
<input type="email" name="email" placeholder="이메일을 입력하세요" />

<!-- 숫자 입력 -->
<input type="number" name="age" min="1" max="100" />
```

### 선택 입력 태그

- `checkbox` : 여러 개 선택 가능
- `radio` : 하나만 선택 가능

```html
<!-- 체크박스 (여러 개 선택 가능) -->
<input type="checkbox" id="hobby1" name="hobbies" value="reading" />

<input type="checkbox" id="hobby2" name="hobbies" value="music" />

<!-- 라디오 버튼 (하나만 선택 가능) -->
<input type="radio" id="male" name="gender" value="male" />

<input type="radio" id="female" name="gender" value="female" />
```

### 기타 입력 태그

- `file` : 파일 선택
- `hidden` : 화면에 보이지 않는 입력
- `date` : 날짜 선택
- `time` : 시간 선택

```html
<!-- 파일 선택 -->
<input type="file" name="profile_image" accept="image/*" />

<!-- 숨겨진 입력창 (화면에 보이지 않음) -->
<input type="hidden" name="user_id" value="12345" />

<!-- 날짜 선택 -->
<input type="date" name="birth_date" />

<!-- 시간 선택 -->
<input type="time" name="meeting_time" />
```

## 기타 입력태그

- `<input>` 태그가 아닌 `<form>` 관련 태그

### 긴 글 입력(textarea) 태그

- 여러 줄의 긴 글을 입력받을 때 사용하는 태그

```html
<label for="message">메시지:</label>
<textarea
  id="message"
  name="message"
  rows="5"
  cols="50"
  placeholder="메시지를 입력하세요"
></textarea>
```

- `rows` : 보여줄 줄 개수
- `cols` : 보여줄 글자 개수
- `placeholder` : 입력 필드의 안내 문구

### 선택 목록(select) 태그

- 여러 선택지 중에서 하나를 고를 수 있는 드롭다운 목록을 만드는 태그

```html
<label for="country">국가 선택:</label>
<select id="country" name="country">
  <option value="">국가를 선택하세요</option>
  <option value="kr">대한민국</option>
  <option value="us">미국</option>
  <option value="jp">일본</option>
  <option value="cn">중국</option>
</select>
```

- `multiple` : 여러 개 선택 가능한 목록을 만든다

### 버튼(button) 태그

- 폼을 제출(submit)하는 버튼을 만드는 태그

```html
<!-- 폼 제출 버튼 -->
<button type="submit">제출</button>

<!-- 폼 초기화 버튼 (모든 입력을 지움) -->
<button type="reset">초기화</button>
```

---

## 라벨(label) 태그

- 입력 필드를 설명하는 태그

### 기본 구조

```html
<label for="username">사용자명:</label>
<input type="text" id="username" name="username" />
```

- `for` : 라벨과 연결할 입력 필드의 `id` 속성을 작성한다