## 함수

- 특정 작업 수행을 위해 미리 정의된 **코드 블록**
- **입력(parameter)** 을 받아 특정 작업을 수행하고 **결과(return value)** 를 반환
    - 결과가 없는 함수도 존재
- 코드 **재사용성** 향상, 중복 감소, 유지보수 용이

### 함수 정의(Define)

```jsx
function 함수이름(매개변수) {
  // 함수가 수행할 작업을 정의하는 코드 블록
  return 반환값;
}

```

- **함수 이름**: 함수 식별 및 호출에 사용
- **매개변수(Parameter)**: 함수에 전달될 입력값을 담는 변수
- **Body**: 함수가 수행할 실제 코드를 포함하는 블록
- **`return`**: 함수 실행 결과를 반환하는 키워드
- **반환값(Return Value)**: 함수가 호출된 곳으로 돌려주는 값

### 함수 호출(Call)

- 함수 실행
- 함수 이름과 괄호 `함수명()` 를 사용
- 함수 호출 시, 매개변수에 전달될 값은 인자(Argument)

**함수 호출**

```jsx
function greet(name) {
  return `안녕하세요, ${name}님!`;
}

console.log(greet("철수")); // 안녕하세요, 철수님!

```

### 매개변수

- 인자를 적게 전달했을 때 - 자동으로 undefined가 할당된다.
- 인자를 더 많이 전달했을 때 - 초과된 인자가 무시되며, 프로그램이 정상적으로 실행된다.

- 기본 매개변수 (Default Parameters)
    - 함수 호출 시 인자를 전달하지 않았을 때 사용할 기본값을 설정한다.
    - 인자가 `undefined`일 경우에만 기본값이 적용된다.

```jsx
function greet(name = "방문자"){
  return `안녕하세요, ${name}님!`;
};

console.log(greet("철수")); // 안녕하세요, 철수님!
console.log(greet());      // 안녕하세요, 방문자님!
```

- 나머지 매개변수 (Rest Parameters)
    - 매개변수 이름 앞에 마침표 세 개 `...`를 붙여 정의한다.
    - 함수에 전달된 **남은 인자들을 하나의 배열**로 모아준다.
    - 나머지 매개변수는 항상 매개변수의 **마지막**에 위치한다.

```jsx
function sumAll(...numbers){
  // numbers는 [1, 2, 3, 4]와 같은 배열 형태가 됨
  let total = 0;
  for (let num of numbers) {
    total += num;
  }
  return total;
};

console.log(sumAll(1, 2));          // 3
console.log(sumAll(1, 2, 3, 4, 5)); // 15
```

---

## 함수 정의 방식 종류

### 함수 선언식(Function Declaration)

- `function` 키워드로 함수 선언
- 가장 기본적인 함수의 형태
- 호이스팅(Hoisting)의 영향으로 **선언 이전에 호출** 가능

```jsx
// 선언 이전에 호출
console.log(add(2, 3)); // 5

// 함수 정의
function add(a, b) {
  return a + b;
}

```

### 함수 표현식(Function Expression)

- 이름이 없는 `function` 함수를 변수에 할당하는 방식
- 호이스팅 미발생

```jsx
const multiply = function (a, b) {
  return a * b;
};

console.log(multiply(2, 3)); // 6

```

### 화살표 함수(Arrow Function)

- `function` 키워드 대신 화살표(`=>`)를 사용해 함수를 간결하게 정의
- 이름이 없는 함수를 **변수에 할당**하는 방식
- 호이스팅 미발생

```jsx
const add = (a, b) => {
  return a + b;
};

console.log(add(5, 7)); // 12

```

- 중괄호 `{}`와 `return` 키워드 생략 가능

**`{}` 와 `return` 키워드 생략**

```jsx
const multiply = (a, b) => a * b;

console.log(multiply(5, 7)); // 35

```

### 함수 정의 방식 비교

```jsx
// 함수 선언식
function add(a, b) {
  return a + b;
}

// 함수 표현식
const addExpression = function (a, b) {
  return a + b;
};

// 화살표 함수
const addArrow = (a, b) => {
  return a + b;
};

console.log(add(2, 3)); // 5
console.log(addExpression(2, 3)); // 5
console.log(addArrow(2, 3)); // 5

```

### 어떤 방식을 써야 하는지

- 대부분의 경우 `화살표 함수`를 사용한다.