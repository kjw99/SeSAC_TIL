## React

[React](https://ko.react.dev/)

- 레고 블럭들을 조합해서 레고 구조물을 만들듯이, 리액트는 컴포넌트(Component)라는 블럭을 조립해서 사용자 인터페이스(UI)를 만드는 JavaScript 라이브러리
- SPA와 Virtual DOM을 통해 성능을 최적화하고 사용자 경험(UX)을 향상시켰다

### 왜 React를 사용할까?

- **컴포넌트 기반**: UI를 독립적인 조각으로 나눠서 재사용할 수 있다
- **거대한 생태계**: 수많은 라이브러리, 도구, 커뮤니티가 존재해 문제 해결이 쉽다
- **높은 수요**: 많은 기업에서 React를 사용하고 있어 취업 시장에서 유리하다

---

## SPA (Single Page Application)

- 하나의 HTML 파일(`index.html`)로 구성된 웹 애플리케이션
- 페이지 새로고침 없이 데이터 갱신과 화면 전환이 이루어지는 방식

### SPA vs MPA (Multi Page Application)

| 구분 | SPA | MPA |
| --- | --- | --- |
| 페이지 | 하나의 HTML 파일 | 여러 개의 HTML 파일 |
| 화면전환 | 새로고침 없이 부분 업데이트 | 페이지 전체를 새로 불러옴 |
| 속도 | 초기 로딩 느림, 이후 빠름 | 매 페이지 로딩마다 시간 소요 |
| 예시 | Gmail, YouTube, Instagram | 네이버 뉴스, 위키백과 |

### SPA 장점

- 빠른 화면 전환: 필요한 데이터만 받아와서 부분적으로 업데이트하므로 빠르다
- 앱과 유사한 경험: 새로고침이 없어 모바일 앱처럼 자연스러운 사용감을 제공한다

### SPA 단점

- 초기 로딩 속도: 처음에 모든 JavaScript를 불러와야 하므로 첫 화면 표시가 느릴 수 있다
- SEO 불리: 하나의 HTML 파일이므로 검색 엔진이 페이지 내용을 파악하기 어렵다

---

## Virtual DOM (가상 DOM)

- 기존 DOM의 비효율적인 렌더링 방식을 개선하기 위해 만들어진 렌더링의 중간 계층
- **성능 최적화의 핵심이자 리액트가 많은 개발자들을 끌어들인 요소**

### 실제 DOM 직접 조작의 문제점

- DOM을 변경할 때마다 브라우저는 **레이아웃 계산 → 화면 그리기** 과정을 반복한다
- 변경이 10번 일어나면 이 과정도 10번 반복되어 성능이 저하된다
- 즉, 변경 하나하나마다 화면 전체를 다시 계산하는 것이 핵심 문제

### Virtual DOM 원리

1. **데이터** 변경: 사용자의 행동으로 데이터가 변경
2. 가상 DOM 생성: 실제 화면이 아닌 메모리 상에 가상 DOM을 생성
3. 기존 가상 DOM과 비교: 새로 생성한 가상 DOM과 기존 가상 DOM을 비교하여 정확히 어떤 부분이 변경됐는지 확인
4. 실제 DOM 반영: 변경된 부분을 실제 DOM에 한 번에 반영

### Virtual DOM 장점

- 개발 편의성: 개발자는 오로지 **데이터** 변경만 신경쓰면 된다
- 성능 향상: 변경사항을 한 번에 반영하여 실제 DOM 조작 비용을 줄인다

### Virtual DOM 단점

- 메모리 사용량 증가: 가상 DOM을 생성하고 비교하는 과정에서 메모리 사용량이 증가한다
- 추상화: DOM 조작 과정을 직접 제어하지 않기에 내부 동작을 파악하기 어렵다

## Vite 기반 React 프로젝트 생성

**1. 터미널 명령어 입력**

```bash
# npm create vite@latest {프로젝트 이름} -- --template react
npm create vite@latest my-react-app -- --template react
```

**2. 설치 진행 동의 메세지 출력 확인**

```bash
Need to install the following packages:
create-vite@...
Ok to proceed? (y)
```

### 개발 서버 실행

**1. 개발 서버 실행 명령어 입력**

프로젝트 루트(package.json이 위치한)에 위치한 것을 확인한다.

```bash
npm run dev
```

**2. 개발 서버 실행 시 출력되는 메시지 확인**

```bash
➜  Local:   <http://localhost:5173/>
➜  Network: use --host to expose
➜  press h + enter to show help
```

**3. 브라우저로 http://localhost:5173/ 접속**

### 프로덕션 파일 빌드

- 프로덕션 환경에서 사용할 정적 파일(html, css, js)을 빌드하는 작업

**1. 프로덕션 파일 빌드 명령어 입력**

```bash
npm run build
```

---

## Vite

[Vite](https://ko.vite.dev/)

- 차세대 프론트엔드 빌드 도구로, 기존 React 개발 환경(CRA)의 느린 개발 서버와 빌드 속도 문제를 해결한다
- Vite는 개발 서버와 프로덕션 환경을 위한 빌드 기능을 제공한다
- React 뿐만 아니라 Vue, Svelte, Lit 등의 다양한 프레임워크를 지원한다

### 네이티브 ES 모듈 기반 개발 서버

- 기존 개발 서버(Webpack)는 모든 파일을 하나로 번들링한 후 브라우저에 제공하여, 프로젝트가 커질수록 시작이 느려진다
    - 번들링: 여러 모듈을 하나 또는 소수의 파일로 묶는 기술
- Vite는 번들링 없이 브라우저의 네이티브 ES 모듈(`import/export`)을 활용하여 필요한 모듈만 제공한다
- esbuild를 이용한 사전 번들링(Pre-bundling)으로 외부 의존성(`node_modules`)을 빠르게 처리한다
    - esbuild는 Go 언어로 작성되어 기존 번들러 대비 10~100배 빠르다
- HMR(Hot Module Replacement)을 통해 수정된 모듈만 교체하여 전체 페이지 새로고침 없이 변경 사항을 즉시 반영한다

### Rollup 기반 프로덕션 파일 빌드

- 프로덕션 환경에서는 수많은 모듈을 개별 요청하면 네트워크 비용이 크기 때문에 번들링이 필요하다
- Rollup 라이브러리로 코드를 효율적으로 묶고, 트리 쉐이킹(Tree Shaking)으로 사용되지 않는 코드를 제거한다
    - 트리 쉐이킹: 실제 사용되는 코드만 남기고 나머지를 제거하는 최적화 기술
- 개발자는 최적화된 정적 파일(static files)을 제공받는다
    - HTML, CSS, JavaScript 파일

---

## React 프로젝트 기본 구조

```
📁 프로젝트명/
  ├── 📁 public/
  │   └── 🎨 vite.svg
  ├── 📁 src/
  │   ├── 📁 assets/
  │   ├── ⚛️ App.jsx
  │   ├── 🎨 App.css
  │   ├── ⚛️ main.jsx
  │   └── 🎨 index.css
  ├── 📝 .gitignore
  ├── 📝 .eslintrc.json
  ├── 📝 index.html
  ├── 📝 package.json
  ├── 📝 README.md
  └── 📝 vite.config.js
```

### public 폴더

- 빌드 과정에서 압축되거나 변형되지 않는 파일을 저장하는 폴더

### src 폴더

- 리액트 애플리케이션 소스 코드가 저장된 핵심 폴더

**main.jsx**

- 리액트의 진입점(시작점)
- `createRoot(document.getElementById("root")).render(<App />);` 코드로 `App` 컴포넌트를 렌더링한다

**App.jsx**

- 리액트의 최상위 메인 컴포넌트
- 다른 모든 컴포넌트를 감싸는 부모 컴포넌트

**index.css**

- 리액트의 전체 스타일을 정의하는 파일

**assets 폴더**

- 컴포넌트에 직접적으로 사용되는 정적 파일을 저장하는 폴더
- 이미지, 폰트, 미디어 파일 등을 저장한다
- public 폴더에 저장된 파일과 다르게 빌드 과정에서 번들러에 의해 처리된다

### .eslintrc.json

- 코드 스타일과 문법을 검사하는 **ESLint** 설정 파일
- 코드 품질을 향상시키고, 협업 시 일관된 코드 스타일 유지를 도와준다

### vite.config.js 파일

- 프로젝트 관리 도구인 `Vite`의 설정 파일
- 기능 확장을 위한 플러그인(Plugin), 서버의 포트(Port), 프록시(Proxy) 서버, 빌드 설정 등을 정의한다

### package.json 파일

- 프로젝트의 의존성(Dependency)과 스크립트(Script)를 관리하는 파일
- 패키지 설치, 실행 명령어, 빌드 명령어 등을 정의한다

### package-lock.json 파일

- 프로젝트의 의존성의 정확한 버전과 구조를 관리하는 파일
- package.json 파일은 버전을 범위로 지정하지만, package-lock.json 파일은 정확한 버전과 구조를 관리한다

### [README.md](http://readme.md/) 파일

- 프로젝트에 대한 설명을 작성하는 파일
- 프로젝트의 목적, 사용 방법, 의존성(Dependency) 등을 작성한다