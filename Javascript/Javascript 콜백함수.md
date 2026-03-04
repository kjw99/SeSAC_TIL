## 일급 객체(First-Class Object)

- **변수에 할당, 인자로 전달, 함수의 반환값으로 사용되는 객체**
- JavaScript의 함수는 일급 객체이므로 아래 특징을 가짐
    - 변수에 할당
    - 인자로 전달
    - 함수의 반환값

### 변수에 할당

```jsx
const sayHello = (name) => {
  return `안녕하세요, ${name}님!`;
};

console.log(sayHello("철수")); // "안녕하세요, 철수님!"

```

### 함수의 인자로 전달

```jsx
function applyOperation(func, number) {
  return func(number);
}

const double = (x) => x * 2;
const square = (x) => x * x;

console.log(applyOperation(double, 5)); // 10
console.log(applyOperation(square, 5)); // 25

```

### 함수의 반환값으로 사용

```jsx
function createMultiplier(multiplier) {
  return (number) => {
    return number * multiplier;
  };
}

const double = createMultiplier(2);
const triple = createMultiplier(3);

console.log(double(5)); // 2 * 5 = 10
console.log(triple(5)); // 3 * 5 = 15

```

---

## 콜백 함수(Callback Function)

- **다른 함수의 인자로 전달(일급 객체 특성)** 되어 다른 함수에서 실행되는 함수
- 콜백 함수를 인자로 받는 함수는 **고차 함수(Higher-Order Function)**

```jsx
// 콜백 함수
function callbackFunction() {}

// 고차 함수
function highOrderFunction(callback) {
  callback();
}

highOrderFunction(callbackFunction);

```

**화살표 함수를 활용한 간략화**

```jsx
highOrderFunction((callback) => {
  // 적용할 로직
});

```

## 콜백 함수의 필요성

### 코드의 재사용성과 유연성

- 인자로 전달되는 콜백 함수에 따라 다른 동작을 수행하여 코드 재사용성 향상
- 하나의 함수에 여러 콜백 함수를 전달하여 유연성 향상

**콜백 함수를 사용하지 않은 경우**

```jsx
const add = (x, y) => {
  console.log(`작업 시작`);
  const result = x + y;
  console.log(`작업 완료`);
  console.log(`결과: ${result}`);
};

const multiply = (x, y) => {
  console.log(`작업 시작`);
  const result = x * y;
  console.log(`작업 완료`);
  console.log(`결과: ${result}`);
};

const subtract = (x, y) => {
  console.log(`작업 시작`);
  const result = x - y;
  console.log(`작업 완료`);
  console.log(`결과: ${result}`);
};

add(5, 3);
multiply(5, 3);
subtract(5, 3);

```

**콜백 함수를 사용한 경우**

```jsx
// 콜백 함수
const add = (x, y) => x + y;

// 콜백 함수
const multiply = (x, y) => x * y;

// 콜백 함수
const subtract = (x, y) => x - y;

// 고차 함수
function performAction(a, b, callback) {
  console.log(`작업 시작`);
  const result = callback(a, b);
  console.log(`작업 완료`);
  console.log(`결과: ${result}`);
}

performAction(5, 3, add);
performAction(5, 3, multiply);
performAction(5, 3, subtract);

```

```
작업 시작
작업 완료
결과: 8
작업 시작
작업 완료
결과: 15
작업 시작
작업 완료
결과: 2

```