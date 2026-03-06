## 컴포넌트(Component)

- 재사용 가능한 사용자 인터페이스(UI) 블럭으로 하나의 페이지는 여러 개의 컴포넌트를 조합해서 만들어낸다
- 컴포넌트는 독립적인 파일을 생성하고, 함수를 정의해서 `요소(Element)` 객체를 반환해야 한다
- `Default Export ...`로 컴포넌트를 내보내고, `import ... from ...`로 컴포넌트를 가져와서 사용한다

### 컴포넌트 특징

- 재사용성 : 변수처럼 여러 위치에서 반복하여 사용한다
- 독립성 : 독립적으로 동작하며, 컴포넌트마다 별도의 데이터(상태)를 보유한다
- 계층 구조 : 다른 컴포넌트를 포함할 수 있다

### 컴포넌트 작성 규칙

- 파일명과 컴포넌트명은 파스칼 케이스(PascalCase)로 작성한다
- 하나의 파일에 하나의 컴포넌트만 정의한다
- 변수처럼 역할과 기능을 표현하는 이름을 사용한다
- 일관된 확장자(`.jsx`)를 사용한다
- 컴포넌트명이 소문자로 시작하면 HTML 태그로 인식되어 오류가 발생한다

**파스칼 케이스 예시**

```jsx
// 올바른 컴포넌트명 (파스칼 케이스)
function MyButton() { ... }
function UserProfile() { ... }
function TodoList() { ... }

// 잘못된 컴포넌트명 (소문자 시작 → HTML 태그로 인식)
function myButton() { ... }  // ❌
function userProfile() { ... }  // ❌
```

### 컴포넌트 작성 형태

- 컴포넌트는 함수 선언문, 화살표 함수 등 다양한 형태로 작성할 수 있다
- 실무에서는 **화살표 함수**를 가장 많이 사용한다

**1. 함수 선언문**

```jsx
export default function MyButton() {
  return <button>버튼</button>;
}
```

**2. 화살표 함수 + 별도 내보내기**

```jsx
const MyButton = () => {
  return <button>버튼</button>;
};

export default MyButton;
```

**3. 화살표 함수**

```jsx
const MyButton = () => <button>버튼</button>;

export default MyButton;
```

**4. rafce 스니펫**

- VSCode에서 `rafce`를 입력하면 자동으로 화살표 함수 컴포넌트가 생성된다
- **r**eact **a**rrow **f**unction **c**omponent **e**xport 의 약자

```jsx
// rafce 입력 후 자동 생성되는 코드
import React from "react";

const MyButton = () => {
  return <div>MyButton</div>;
};

export default MyButton;
```

- rafce로 생성된 코드에서 `import React from "react"`는 React 17 이후 생략 가능하다. 필요 없다면 삭제해도 된다.

---

## 컴포넌트 중첩(Nested Component)

- 컴포넌트 내부에 또 다른 컴포넌트를 포함해서 사용하는 방식

### 컴포넌트 생성 및 내보내기

- `src/components` 폴더에 `jsx` 확장자 파일을 생성한다
- 파일명과 컴포넌트명은 파스칼 케이스(PascalCase)로 작성한다
- 요소를 반환하는 함수를 작성하고 내보낸다

**기본 구조**

```jsx
const ComponentName = () => {
  return <div>컴포넌트 내용</div>;
};

export default ComponentName;

```

### 컴포넌트 불러오기 및 사용하기

- `import` 문법을 사용하여 컴포넌트를 불러온다
- 컴포넌트 사용 형태는 두 가지가 있다
    - `<컴포넌트명 />` : 자식(children)이 없을 때 사용한다 (Self-closing)
    - `<컴포넌트명>내용</컴포넌트명>` : 자식을 전달할 때 사용한다

```jsx
import ComponentName from "./components/ComponentName";

function App() {
  return (
    <div>
      <ComponentName />
      <ComponentName></ComponentName>
    </div>
  );
}
```

**컴포넌트 생성 및 내보내기**

```jsx
// components/MyList.jsx

const MyList = () => {
  return (
    <ul>
      <li>1. 리액트 프로젝트 생성</li>
      <li>2. 터미널 경로 이동</li>
      <li>3. 의존성 설치</li>
      <li>4. 프로젝트 서버 실행</li>
    </ul>
  );
};

export default MyList;

```

```jsx
// components/MyButton.jsx

const MyButton = () => {
  return <button>버튼</button>;
};

export default MyButton;
```

**컴포넌트 불러오기 및 사용하기**

```jsx
// App.jsx

// 컴포넌트 불러오기
import MyButton from "./components/MyButton";
import MyList from "./components/MyList";

function App() {
  return (
    <div>
      {/* 컴포넌트 사용 */}
      <MyList />
      <MyButton />
    </div>
  );
}

export default App;
```

## Props 전달하고 받기

### 전달하기

- 자식 컴포넌트 요소 속성(key=value) 형태로 Props를 전달한다
- `<컴포넌트명 PropsKey={PropsValue} ... />`

**기본 구조**

```jsx
import ChildComponent from "./components/ChildComponent";

const ParentComponent = () => {
  return (
    <div>
      <ChildComponent name="철수" age={25} job="개발자" />
    </div>
  );
};

export default ParentComponent;
```

### 받기

- Props 객체는 컴포넌트 함수의 첫 번째 매개변수에 저장된다
`function ChildComponent(props) { ... }`
- `props.속성명` 형태로 전달받은 데이터에 접근한다

**기본 구조**

```jsx
const ChildComponent = (props) => {
  return (
    <div>
      <p>{props.name}</p>
      <p>{props.age}</p>
      <p>{props.job}</p>
    </div>
  );
};

export default ChildComponent;
```

### Props 필요성

**Props 미사용 컴포넌트**

- 동일한 구조라도 다른 데이터를 사용하려면 새로운 컴포넌트를 생성해야 한다

```jsx
// App.jsx

// 예시를 위해 하나의 파일에 여러 컴포넌트를 생성
const UserProfileA = () => {
  return <div>Hello! 철수</div>;
};

const UserProfileB = () => {
  return <div>Hello! 영희</div>;
};

const UserProfileC = () => {
  return <div>Hello! 길동</div>;
};

function App() {
  return (
    <div>
      <UserProfileA /> {/* Hello! 철수 */}
      <UserProfileB /> {/* Hello! 영희 */}
      <UserProfileC /> {/* Hello! 길동 */}
    </div>
  );
}
export default App;
```

**Props 사용 컴포넌트**

- 하나의 컴포넌트에 다른 Props를 전달하여 다른 화면을 표현한다

```jsx
// App.jsx

const UserProfile = (props) => {
  return <div>Hello! {props.name}</div>;
};

function App() {
  return (
    <div>
      {/* <컴포넌트명 PropsKey={Value} /> */}
      <UserProfile name="철수" />
      <UserProfile name="영희" />
      <UserProfile name="길동" />
    </div>
  );
}
export default App;
```

---

## Props 구조 분해 할당

- `props.속성명` 대신, 매개변수에서 바로 구조 분해 할당으로 꺼내서 사용할 수 있다
- 실무에서는 구조 분해 할당을 더 많이 사용한다

**props 객체로 받기**

```jsx
const UserProfile = (props) => {
  return (
    <div>
      <h2>{props.name}</h2>
      <p>나이: {props.age}</p>
    </div>
  );
};
```

**구조 분해 할당으로 받기**

```jsx
const UserProfile = ({ name, age }) => {
  return (
    <div>
      <h2>{name}</h2>
      <p>나이: {age}</p>
    </div>
  );
};
```

### Props 기본값

- Props가 전달되지 않았을 때 사용할 기본값을 설정할 수 있다
- 구조 분해 할당에서 `=` 연산자로 기본값을 지정한다

```jsx
const UserProfile = ({ name = "익명", age = 0 }) => {
  return (
    <div>
      <h2>{name}</h2>
      <p>나이: {age}</p>
    </div>
  );
};
```

```jsx
// App.jsx

function App() {
  return (
    <div>
      <UserProfile name="철수" age={25} /> {/* 철수, 25 */}
      <UserProfile name="영희" />           {/* 영희, 0 (age 기본값) */}
      <UserProfile />                       {/* 익명, 0 (모두 기본값) */}
    </div>
  );
}
```

---

## Props를 직접 수정하면 안된다

- 자식 컴포넌트는 부모 컴포넌트에게 받은 Props를 절대 직접 수정하면 안된다
- Props는 **읽기 전용(Read-Only)** 데이터이다

**잘못된 코드**

```jsx
const UserProfile = (props) => {
  props.name = "다른 이름"; // Props 객체 직접 수정 → 에러 발생
  return <div>{props.name}</div>;
};

const UserProfile = ({ name }) => {
  name = "다른 이름"; // Props를 직접 수정 → 금지
  return <div>{name}</div>;
};

```

**올바른 코드**

```jsx
const UserProfile = ({ name }) => {
  const displayName = name + "님"; // 새로운 변수를 만들어서 사용
  return <div>{displayName}</div>;
};
```

## 다양한 타입의 Props 전달하기

- 문자열, 숫자, 객체 등 다양한 타입의 데이터를 Props로 전달할 수 있다

### 문자열 전달하기

- 문자열 데이터는 따옴표 `""`로 감싸서 전달한다

```jsx
import Profile from "./Profile";

const ProfileContainer = () => {
  return (
    <div>
      <Profile name="현우" />
      <Profile name="수진" />
    </div>
  );
};

export default ProfileContainer;
```

```jsx
const Profile = (props) => {
  return <div>저는 {props.name}입니다.</div>;
};

export default Profile;
```

### 숫자형 전달하기

- 숫자 데이터는 중괄호 `{}`로 감싸서 전달한다
- 따옴표 `""`로 감싸면 문자열로 전달된다

```jsx
import Profile from "./Profile";

const ProfileContainer = () => {
  return (
    <div>
      <Profile name="현우" age={22} />
      <Profile name="수진" age="21" />
    </div>
  );
};

export default ProfileContainer;
```

```jsx
const Profile = (props) => {
  return (
    <div>
      <p>
        저는 {props.name}이고, {props.age}세 입니다.
      </p>
      <p>타입: {typeof props.age}</p>
      {/* 현우 → 타입: number */}
      {/* 수진 → 타입: string */}
    </div>
  );
};

export default Profile;
```

### 변수 전달하기

- 변수는 중괄호 `{}`로 감싸서 전달한다

```jsx
const ProfileContainer = () => {
  const name = "현우";
  const age = 22;
  return <Profile name={name} age={age} />;
};

export default ProfileContainer;
```

```jsx
const Profile = (props) => {
  return (
    <div>
      저는 {props.name}이고, {props.age}세 입니다.
    </div>
  );
};

export default Profile;
```

### 객체 전달하기

- 객체 데이터는 중괄호 `{}`로 감싸서 전달한다

```jsx
import Profile from "./Profile";

const ProfileContainer = () => {
  return (
    <div>
      <Profile
        user={{
          name: "현우",
          age: 22,
        }}
      />
    </div>
  );
};

export default ProfileContainer;
```

```jsx
const Profile = (props) => {
  return (
    <div>
      저는 {props.user.name}이고, {props.user.age}세 입니다.
    </div>
  );
};

export default Profile;
```

### Spread 연산자로 전달하기

- `...` 연산자를 사용하면 객체의 속성을 개별 Props로 펼쳐서 전달할 수 있다

```jsx
import Profile from "./Profile";

const ProfileContainer = () => {
  const user = {
    name: "현우",
    age: 22,
  };

  // <Profile name="현우" age={22} /> 와 동일
  return <Profile {...user} />;
};

export default ProfileContainer;
```

```jsx
const Profile = (props) => {
  return (
    <div>
      저는 {props.name}이고, {props.age}세 입니다.
    </div>
  );
};

export default Profile;
```

## 구조 분해 할당 활용

- Props는 객체이므로 구조 분해 할당을 활용할 수 있다
    - 구조 분해 할당: 객체의 속성을 변수로 분해하여 할당하는 방법

```jsx
import Profile from "./Profile";

const ProfileContainer = () => {
  return (
    <div>
      <Profile name="현우" age={22} />
      <Profile name="수진" age={21} />
    </div>
  );
};

export default ProfileContainer;
```

```jsx
// const { name, age } = props;
const Profile = ({ name, age }) => {
  return (
    <div>
      저는 {name}이고, {age}세 입니다.
    </div>
  );
};

export default Profile;
```

### 객체 데이터의 Props 구조 분해할당

```jsx
import Profile from "./Profile";

const ProfileContainer = () => {
  const user = {
    name: "현우",
    age: 22,
  };

  return (
    <div>
      <Profile user={user} />
    </div>
  );
};

export default ProfileContainer;
```

```jsx
const Profile = ({ user }) => {
  return (
    <div>
      저는 {user.name}이고, {user.age}세 입니다.
    </div>
  );
};

export default Profile;
```