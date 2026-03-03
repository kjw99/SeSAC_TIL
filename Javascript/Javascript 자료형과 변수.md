## 원시 자료형

- 가장 기본적인 데이터 타입
- 불변성 - 생성 후 값 변경 불가

### 문자열(String)

```jsx
console.log("안녕하세요"); // 큰 따옴표
console.log('반갑습니다'); // 작은 따옴표
console.log(`좋은 하루 되세요`); // 백틱
```

### 숫자형(Number)

- 정수와 실수 포함

```jsx
console.log(25); // 양수
console.log(19.99); // 실수
console.log(0); // 영
console.log(-10); // 음수

```

- `BigInt`
    
    Number가 다룰 수 있는 최대치 이상의 정수를 다룰 때 사용한다.
    

### 불리언(Boolean)

- python은 `True` 로 대문자로 시작하지만, JS는 `true`로 소문자이다.

```jsx
console.log(true); // 참
console.log(false); // 거짓

```

### undefined

- 값이 정의되지 않았음을 시스템이 알려주는 상태

```jsx
console.log(undefined); // undefined 값 출력
console.log(typeof undefined); // undefined

```

### null

- 값이 없음을 의도적으로 명시할 때 사용하는 값

```jsx
console.log(null); // null 값 출력
console.log(typeof null); // object

```

### Symbol

- 중복되지 않는 유일무이한 식별자를 생성
- 우리가 직접 다룰 일은 거의 없다.

## 변수

python과 달리, JS에서는 `let`, `const`라는 키워드를 통해 선언한다. 한번 선언한 변수는 재선언이 불가능하다.

### let

- `let` 으로 선언한 변수는 데이터 변경이 가능하다
- 즉, 재할당이 가능하다.

```jsx
let score = 80;
console.log(score); // 80

score = 90; // 변수에 데이터 재할당
console.log(score); // 90
```

### const

- `const`로 선언한 변수는 상수로, 데이터 재할당이 불가능하다.

```jsx
const PI = 3.14;
console.log(PI); // 3.14

PI = 3.15; // 오류 발생: 값을 바꿀 수 없음
```

### block scope

- let과 const는 중괄호 { }로 감싸진 영역(블록) 안에서만 유효하다.

```jsx
{
  let num = 10
  console.log(num)
}

// console.log(num) // 실행되지 않는다.
```

### let vs const 선택 기준

- 데이터 재할당이 필요하면: `let`
- 데이터가 변경되면 안 되면: `const`
- `const`를 기본적으로 사용하고, 변경이 필요한 경우에만 `let`을 사용한다.

### var

- 레거시 선언 키워드로, 사용하지 않는다.

## 변수 이름 짓기

### 기본 규칙

- 영어, 숫자, `_`, `$` 만 사용 가능
- 숫자로 시작 불가능
- 대소문자 구분
- 예약어 사용 불가능 (let, const, if 등)
- 예약어: 프로그래밍 언어에서 이미 사용 중인 단어로, 개발자 사용 불가

### 변수 이름 짓기

- 카멜 케이스 사용
    - 첫 단어는 소문자, 다음 단어부터 대문자로 시작
    - 자바스크립트의 관례
    - 예시: `userName`, `userId`, `totalPrice`, `isLoggedIn`

```jsx
let userName = "김철수";
let userId = 1;
let totalPrice = 15000;
let isLoggedIn = true;

```

### 템플릿 리터럴(Template Literal)

- 백틱과 `${ }` 기호를 사용해 문자열 안에 변수와 표현식을 삽입하는 방법
    - 표현식: 데이터를 생성하는 코드 조각(수식, 함수 호출 등)

```jsx
// ${변수명}

age = 99;
message = `${age}살`;
console.log(message); // 99살

```

### 참고) 호이스팅

- 변수와 함수 선언이 그들이 포함된 스코프의 최상단으로 끌어올려진 것처럼 동작하는 JavaScript 엔진의 특성이다.
    - `var`로 선언된 변수는 선언 전 접근이 가능하지만, 값은 **`undefined`**이다.
- 코드의 가독성을 해치고 예상치 못하게 실행될 수 있기 때문에 활용하지 않는 것이 좋다.
    - `let`, `const`로 선언하면 호이스팅이 발생하지 않는다.

```jsx
console.log(name); // undefined (호이스팅 발생)

var name = '철수';

console.log(name); // 철수
```

```jsx
console.log(name); // ReferenceError (실행이 안됨)

let name = '철수';

console.log(name);
```

- 레거시 코드 이해 및 면접 대비용으로 키워드는 알아두는게 좋다.