실습을 진행하기 전, `index.css`와 `App.css`의 내용은 전부 지워준다.

## Module CSS

- 컴포넌트마다 개별 css 파일을 생성하는 방식
- 컴포넌트 간 CSS 클래스 이름 충돌을 막는 기술

### Module 적용하기

**`1. App.module.css` 파일 생성 및 CSS 코드 작성**

- `컴포넌트명.module.css` 형태로 작성
- 컴포넌트에서 사용할 CSS 코드 작성

```css
/* App.module.css */
.container {
  text-align: center;
  margin-top: 4rem;
}
.title {
  font-size: 2rem;
  font-weight: bold;
  color: blue;
}
```

**2. `**App**.jsx` 파일에서 Module CSS 불러오기 및 적용하기**

- `import` 문법을 사용하여 CSS 모듈을 불러오고, `styles` 객체로 사용
- `className` 속성에 `styles.클래스명` 형태로 적용

```jsx
import styles from "./App.module.css";

function App() {
  return (
    <>
      <div className={styles.container}>
        <h1 className={styles.title}>Hello World</h1>
      </div>
    </>
  );
}

export default App;
```

### 여러 클래스 적용하기

- 템플릿 리터럴을 사용하여 여러 클래스를 동시에 적용

```jsx
<div className={`${styles.container} ${styles.active}`}>
  여러 클래스 적용
</div>
```

### 케밥 케이스 클래스명 접근

- CSS 클래스명에 (하이픈)이 포함된 경우 대괄호 표기법 사용

```css
/* App.module.css */
.font-title {
  font-size: 2rem;
}
```

```jsx
// App.jsx
<h1 className={styles["font-title"]}>Hello</h1>
```

---

## Tailwind CSS

- Tailwind CSS를 프로젝트에 설치하여 유틸리티 클래스로 스타일링

### 유틸리티 클래스

- 하나의 클래스에 하나의 스타일 속성만 가진 클래스

**유틸리티 클래스 `.w-40`**

```css
/* 순수 css 표현 */
.w-40 {
  width: 10rem;
}
```

### Tailwind CSS 설치

- Tailwind CSS 버전 4.0 이상 기준

**1. tailwindcss 설치**

- 터미널의 현재 위치가 프로젝트 루트 폴더인지 확인 후 설치
    - 프로젝트 루트 폴더: `package.json` 파일이 있는 폴더

```bash
npm install tailwindcss @tailwindcss/vite
```

**2. `package.json`에서 설치 확인**

- 설치 후 `package.json`의 `dependencies`에 `tailwindcss`, `@tailwindcss/vite`가 추가되었는지 확인

### Vite 설정 파일 `vite.config.js` 수정

```jsx
// vite.config.js

import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// 1. tailwindcss 플러그인 불러오기
import tailwindcss from "@tailwindcss/vite";

// https://vite.dev/config>
export default defineConfig({

// 2. tailwindcss() 플러그인(plugin) 추가
  plugins: [react(), tailwindcss()],
});
```

### `src/index.css` 파일 수정

- tailwindcss 불러오기

```css
@import "tailwindcss";
```

### Tailwind CSS 적용 확인

```jsx
function App() {
  return (
    <>
      <div className={styles.container}>
        <h1 className={styles.title}>Hello World</h1>
      </div>
      <h1 className="text-3xl font-bold text-red-500">Hello World</h1>
    </>
  );
}

export default App;
```

---

## 자주 사용하는 Tailwind 유틸리티 클래스

### 텍스트 (Typography)

| 클래스 | CSS 속성 | 설명 |
| --- | --- | --- |
| `text-xs` | `font-size: 0.75rem` | 아주 작은 텍스트 |
| `text-sm` | `font-size: 0.875rem` | 작은 텍스트 |
| `text-base` | `font-size: 1rem` | 기본 텍스트 |
| `text-lg` | `font-size: 1.125rem` | 큰 텍스트 |
| `text-xl` | `font-size: 1.25rem` | 더 큰 텍스트 |
| `text-2xl` | `font-size: 1.5rem` | 2배 큰 텍스트 |
| `text-3xl` | `font-size: 1.875rem` | 3배 큰 텍스트 |
| `font-thin` | `font-weight: 100` | 아주 얇은 굵기 |
| `font-normal` | `font-weight: 400` | 기본 굵기 |
| `font-bold` | `font-weight: 700` | 굵은 굵기 |
| `text-center` | `text-align: center` | 가운데 정렬 |
| `text-left` | `text-align: left` | 왼쪽 정렬 |
| `text-right` | `text-align: right` | 오른쪽 정렬 |

### 색상 (Colors)

| 클래스 | 설명 |
| --- | --- |
| `text-red-500` | 빨간색 텍스트 |
| `text-blue-500` | 파란색 텍스트 |
| `text-green-500` | 초록색 텍스트 |
| `text-gray-500` | 회색 텍스트 |
| `text-white` | 흰색 텍스트 |
| `text-black` | 검은색 텍스트 |
| `bg-red-500` | 빨간색 배경 |
| `bg-blue-500` | 파란색 배경 |
| `bg-green-500` | 초록색 배경 |
| `bg-gray-100` | 연한 회색 배경 |
| `bg-gray-500` | 회색 배경 |
| `bg-white` | 흰색 배경 |
- 색상 뒤의 숫자는 명도 단계 (50~950, 숫자가 클수록 진함)

### 여백 (Spacing)

| 클래스 | CSS 속성 | 설명 |
| --- | --- | --- |
| `p-4` | `padding: 1rem` | 전체 안쪽 여백 |
| `px-4` | `padding-left/right: 1rem` | 좌우 안쪽 여백 |
| `py-4` | `padding-top/bottom: 1rem` | 상하 안쪽 여백 |
| `pt-4` | `padding-top: 1rem` | 위 안쪽 여백 |
| `pb-4` | `padding-bottom: 1rem` | 아래 안쪽 여백 |
| `m-4` | `margin: 1rem` | 전체 바깥 여백 |
| `mx-auto` | `margin-left/right: auto` | 가로 가운데 배치 |
| `my-4` | `margin-top/bottom: 1rem` | 상하 바깥 여백 |
| `mt-4` | `margin-top: 1rem` | 위 바깥 여백 |
| `mb-4` | `margin-bottom: 1rem` | 아래 바깥 여백 |
| `gap-4` | `gap: 1rem` | Flex/Grid 자식 간 간격 |
- 숫자 기준: `1` = 0.25rem, `2` = 0.5rem, `4` = 1rem, `8` = 2rem, `16` = 4rem

### 크기 (Sizing)

| 클래스 | CSS 속성 | 설명 |
| --- | --- | --- |
| `w-full` | `width: 100%` | 부모 너비만큼 |
| `w-screen` | `width: 100vw` | 화면 전체 너비 |
| `w-1/2` | `width: 50%` | 부모의 절반 |
| `w-40` | `width: 10rem` | 고정 너비 |
| `h-full` | `height: 100%` | 부모 높이만큼 |
| `h-screen` | `height: 100vh` | 화면 전체 높이 |
| `h-40` | `height: 10rem` | 고정 높이 |
| `min-h-screen` | `min-height: 100vh` | 최소 화면 높이 |
| `max-w-md` | `max-width: 28rem` | 최대 너비 제한 |
| `max-w-lg` | `max-width: 32rem` | 최대 너비 제한 |

### Flexbox

| 클래스 | CSS 속성 | 설명 |
| --- | --- | --- |
| `flex` | `display: flex` | Flex 컨테이너 |
| `flex-col` | `flex-direction: column` | 세로 방향 배치 |
| `flex-row` | `flex-direction: row` | 가로 방향 배치 (기본값) |
| `justify-center` | `justify-content: center` | 주축 가운데 정렬 |
| `justify-between` | `justify-content: space-between` | 주축 양쪽 정렬 |
| `justify-around` | `justify-content: space-around` | 주축 균등 정렬 |
| `items-center` | `align-items: center` | 교차축 가운데 정렬 |
| `items-start` | `align-items: flex-start` | 교차축 시작 정렬 |
| `items-end` | `align-items: flex-end` | 교차축 끝 정렬 |
| `flex-wrap` | `flex-wrap: wrap` | 줄바꿈 허용 |
| `flex-1` | `flex: 1 1 0%` | 남은 공간 채우기 |

### 테두리 (Border)

| 클래스 | CSS 속성 | 설명 |
| --- | --- | --- |
| `border` | `border-width: 1px` | 기본 테두리 |
| `border-2` | `border-width: 2px` | 2px 테두리 |
| `border-gray-300` | `border-color: ...` | 회색 테두리 색상 |
| `rounded` | `border-radius: 0.25rem` | 약간 둥근 모서리 |
| `rounded-lg` | `border-radius: 0.5rem` | 둥근 모서리 |
| `rounded-full` | `border-radius: 9999px` | 완전한 원형 모서리 |

### 그림자 및 효과 (Effects)

| 클래스 | 설명 |
| --- | --- |
| `shadow` | 기본 그림자 |
| `shadow-md` | 중간 그림자 |
| `shadow-lg` | 큰 그림자 |
| `opacity-50` | 투명도 50% |
| `cursor-pointer` | 마우스 포인터 모양 |

### 반응형 (Responsive)

- 화면 크기에 따라 다른 스타일을 적용할 수 있음
- 클래스 앞에 접두사를 붙여 사용

| 접두사 | 최소 너비 | 설명 |
| --- | --- | --- |
| `sm:` | 640px | 작은 화면 |
| `md:` | 768px | 중간 화면 |
| `lg:` | 1024px | 큰 화면 |
| `xl:` | 1280px | 아주 큰 화면 |

```jsx
{/* 기본: 세로 배치, md(768px) 이상: 가로 배치 */}
<div className="flex flex-col md:flex-row">
  <div>1</div>
  <div>2</div>
</div>
```

### 상태 (States)

- 마우스 오버, 포커스 등 상태에 따른 스타일 적용

| 접두사 | 설명 |
| --- | --- |
| `hover:` | 마우스를 올렸을 때 |
| `focus:` | 포커스 되었을 때 |
| `active:` | 클릭 중일 때 |

```jsx
<button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
  버튼
</button>
```