## 예외 처리(Exception Handling)

- 프로그램 실행 중 발생하는 오류를 처리하는 기술
- 예외(오류) 발생 시, 프로그램이 종료되지만 예외 처리를 통해 **프로그램 종료 대신 적절한 대처** 가능

### 기본 구조

- `try`: 오류 발생 가능성이 있는 코드 블록
- `catch`: 오류 발생 시 실행할 코드 블록

**try-catch**

```jsx
try {
  // 오류가 발생할 가능성이 있는 코드
} catch (error) {
  // 오류가 발생했을 때 실행되는 코드
}

```

- `finally`: 오류 발생 여부와 상관없이 실행할 코드 블록

**try-catch-finally**

```jsx
try {
  // 오류가 발생할 가능성이 있는 코드
} catch (error) {
  // 오류가 발생했을 때 실행되는 코드
} finally {
  // 오류 발생과 상관없이 무조건 실행되는 코드
}

```

---

## 예외 발생시키기(Throw Exception)

- `throw` 키워드로 개발자가 **예외를 강제로 발생**
- 사용자 정의 예외 생성 시 활용하며, 예외 객체 `Error`를 던짐(throw)

```jsx
function plusOne(num) {
  if (typeof num !== "number") {
    throw new Error("숫자가 아닙니다.");
  }
  console.log(num + 1);
}

try {
  plusOne("문자열"); // Error 발생
} catch (error) {
  console.error(error.name); // 에러의 종류(ReferenceError, TypeError, SyntaxError 등)
  console.error(error.message); // 에러 메세지
  console.error(error.stack); // 에러 스택 트레이스
}

```

## 모듈(Module)

- 특정 기능을 담당하는 독립적인 코드 단위
- 연관성 높은 코드를 파일로 나누어 관리하는 시스템

### 모듈 시스템의 필요성

- **코드 재사용**: 한 번 만든 모듈을 여러 곳에서 사용
- **유지보수 용이**: 특정 기능에 문제가 생기면 해당 모듈만 수정
- **협업 효율성**: 팀원들이 각자 다른 모듈을 개발

---

## 모듈 시스템의 역사

### 초기 JavaScript

- 모든 코드를 하나의 파일에 작성

**하나의 파일에 모든 코드 작성**

```jsx
// 모든 코드가 하나의 파일에 있었음
var userName = "홍길동";
var userAge = 25;

function greetUser() {
  console.log("안녕하세요, " + userName + "님!");
}

function calculateAge(birthYear) {
  return new Date().getFullYear() - birthYear;
}

```

### CommonJS (Node.js 환경)

- 2009년 Node.js와 함께 등장
- 서버 사이드 JavaScript를 위한 모듈 시스템
- `require()`와 `module.exports` 사용
- 브라우저에서는 사용 불가

**CommonJS 모듈**

```jsx
// math.js
function add(a, b) {
  return a + b;
}

module.exports = { add };

```

**CommonJS 모듈 사용**

```jsx
// main.js
const { add } = require("./math.js");

console.log(add(1, 2)); // 3

```

### ES 모듈 (표준 모듈 시스템)

- **현재 권장 방식**
- 2015년 ES6(ECMAScript 2015)에서 표준화
- `import`와 `export` 사용
- 브라우저와 Node.js 모두에서 사용 가능

**package.json 생성**

```bash
touch package.json

```

**package.json 작성**

```json
{
  "type": "module"
}

```

**`"type": "module"` 필요성**

- 모듈 시스템을 ES 모듈로 사용하겠다고 명시하는 설정

---

**ES 모듈**

```jsx
// math.js
function add(a, b) {
  return a + b;
}

export { add };

```

**ES 모듈 사용**

```jsx
// main.js
import { add } from "./math.js";

console.log(add(1, 2)); // 3

```

---

## ES 모듈 내보내기/불러오기

- `export`: 모듈에서 값 또는 함수를 내보낼 때 사용
- `import`: 다른 모듈에서 값 또는 함수를 가져올 때 사용

### Named Export (이름 있는 내보내기)

- 여러 값과 함수를 내보내기 가능
- 가져올 때 정확한 이름 사용
- `export` 키워드와 함께 중괄호 `{}` 사용

**모듈 내보내기**

```jsx
// math.js
const PI = 3.14159;
const E = 2.71828;

function add(a, b) {
  return a + b;
}

function subtract(a, b) {
  return a - b;
}

function multiply(a, b) {
  return a * b;
}

function divide(a, b) {
  if (b === 0) {
    throw new Error("0으로 나눌 수 없습니다");
  }
  return a / b;
}

export { PI, E, add, subtract, multiply, divide };

```

**일부 모듈만 불러오기**

- 트리 셰이킹(Tree Shaking): 사용하지 않는 코드를 제거하는 기술, 코드 최적화 기술

```jsx
// main.js
import { PI, add, multiply } from "./math.js";

const a = 1;
const b = 2;

console.log("원주율:", PI);
console.log(`a + b = ${add(a, b)}`);
console.log(`a * b = ${multiply(a, b)}`);

```

**별칭 `as` 키워드 사용**

- 불러온 함수에 별칭(별명) 부여

```jsx
// main.js
import { add as a, subtract as s, PI as p} from "./math.js";

console.log("2 + 3 =", a(2, 3)); // 2 + 3 = 5
console.log("5 - 2 =", s(5, 2)); // 5 - 2 = 3
console.log("원주율:", p); // 원주율: 3.14159

```

## **모든 내보내기 불러오기  키워드 사용**

```jsx
// main.js
import * as math from "./math.js";

const a = 1;
const b = 2;

console.log(math);
console.log("원주율:", math.PI);
console.log("자연상수:", math.E);
console.log(`a + b = ${math.add(a, b)}`);
console.log(`a - b = ${math.subtract(a, b)}`);
console.log(`a * b = ${math.multiply(a, b)}`);
console.log(`a / b = ${math.divide(a, b)}`);

```

---

### Default Export (기본 내보내기)

- 모듈 당 하나의 내보내기
- 가져올 때 아무 이름으로 가져오기 가능
- `export` 키워드와 `default` 키워드를 함께 사용, 중괄호 `{}` 없이 사용

**모듈 만들고 내보내기**

```jsx
// calculator.js

// 계산기 객체
const Calculator = {
  add: (a, b) => a + b,
  subtract: (a, b) => a - b,
  multiply: (a, b) => a * b,
  divide: (a, b) => {
    if (b === 0) {
      throw new Error("0으로 나눌 수 없습니다");
    }
    return a / b;
  },
};

export default Calculator;

```

**모듈 불러오기**

```jsx
// main.js
import Calculator from "./calculator.js";

const a = 1;
const b = 2;
console.log(Calculator.add(a, b));
console.log(Calculator.subtract(a, b));
console.log(Calculator.multiply(a, b));
console.log(Calculator.divide(a, b));

```

---

## NPM(Node Package Manager)

- JavaScript 패키지 관리 도구
- Node.js와 함께 자동 설치
- `package.json` 파일로 패키지 의존성 관리
    - 의존성: 특정 패키지를 사용하기 위해 필요한 다른 패키지

### 주요 명령어

**프로젝트 초기화**

```bash
npm init

# 또는 기본 세팅으로 초기화
npm init -y

```

**패키지 설치 방법**

```bash
# 프로젝트에 패키지 설치
npm install lodash

# 전역 패키지 설치
npm install -g lodash

# 개발 의존성 패키지 설치
# 개발 의존성 패키지 : 개발 환경에서만 사용되는 패키지
npm install --save-dev jest

```

**패키지 제거**

```bash
npm uninstall lodash

```

**패키지 업데이트**

```bash
npm update

```

**설치된 패키지 목록 확인**

```bash
npm list

```