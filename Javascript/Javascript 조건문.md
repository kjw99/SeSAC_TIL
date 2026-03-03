## 조건문

## if ~ else if ~ else

- 조건식이 참일 때 코드 실행
- 여러 조건식이 필요할 때 사용
- 실행 코드 블록은 중괄호 `{}`로 구분

```jsx
if (조건식) {
  // 조건식이 참일 때 실행
} else if (조건식) {
  // 조건식이 참일 때 실행
} else {
  // 모든 조건식이 거짓일 때 실행
}

```

### `if`

- 조건식의 평가 결과가 참(true)이면 코드 실행
- 단일 조건에 따라 코드 실행 여부를 결정할 때 사용

```jsx
let x = 5;

if (x >= 5) {
  // 조건식이 참일 때 실행
  console.log(`${x}는 5이상 이다.`);
}

console.log("조건식 결과와 상관없이 실행된다.");

```

### `else if`

- 여러 조건 중 하나를 만족할 때 코드 실행
- `if`문 또는 이전 `else if`문의 조건식이 거짓(false)이고, 현재 조건식이 참(true)이면 코드 실행
- 조건식을 위에서 아래로 평가하며, 참(false)인 조건식 발견 시 나머지 조건은 평가하지 않음

```jsx
let x = 4;

if (x >= 5) {
  console.log(`${x}는 5이상 이다.`);
} else if (x >= 3) {
  // x >= 3 조건식이 참이므로, 아래 코드가 실행
  // 이후의 else if 문은 미평가
  console.log(`${x}는 3이상 이다.`);
} else if (x >= 1) {
  console.log(`${x}는 1이상 이다.`);
}

```

### `else`

- 모든 `if`, `else if` 조건식이 거짓(false)이면 코드 실행

**if ~ else문 예시**

```jsx
let x = 1;
if (x > 0) {
  console.log(`${x}는 양수`);
} else {
  console.log(`${x}는 0 또는 음수`);
}

```

**if ~ else if ~ else문 예시**

```jsx
let x = 1;

if (x >= 5) {
  console.log(`${x}는 5이상 이다.`);
} else if (x >= 3) {
  console.log(`${x}는 3이상 이다.`);
} else {
  // 모든 조건식이 거짓이므로 실행
  console.log(`${x}는 3미만 이다.`);
}

```

### 중첩 조건문

- 조건문 내부에 다른 조건문 작성
- 복잡한 조건을 처리할 때 사용

```jsx
let age = 25;
let isStudent = true;

if (age >= 20) {
  if (isStudent === true) {
    console.log("성인 학생입니다.");
  } else {
    console.log("성인입니다.");
  }
} else {
  if (isStudent === true) {
    console.log("미성년 학생입니다.");
  } else {
    console.log("미성년입니다.");
  }
}

```

## 삼항 연산자

- 조건식의 평가 결과에 따라 값을 반환하는 간단한 조건 처리

```jsx
{ 조건식 } ? { 참일 때 데이터 } : { 거짓일 때 데이터 };
```

**짝수 홀수 판별**

```jsx
let x = 7;

let result = x % 2 === 0 ? "짝수" : "홀수";

console.log(`${x}는 ${result}입니다.`);

```

## `switch`문

- 표현식의 평가 결과를 `case`의 값과 비교하여 일치하는 코드 블록 실행
- `break`: 다음 `case` 실행 방지, 생략하면 다음의 모든 `case` 실행
- `default`: 일치하는 `case`가 없을 때 실행
- 활용도가 낮으므로, 존재만 인지

**switch문 기본 구조**

```jsx
switch (표현식) {
  case 값1:
    // 코드
    break;
  case 값2:
    // 코드
    break;
  default:
  // 기본 코드
}

```

**예시**

```jsx
let day = "월";
let dayName = "";

switch (day) {
  case "월":
    dayName = "월요일";
    break;
  case "화":
    dayName = "화요일";
    break;
  case "수":
    dayName = "수요일";
    break;
  default:
    dayName = "주말 또는 잘못된 요일";
}

console.log(dayName); // "월요일"

```

### block scope

- if문은 `{} - block` 으로 이루어져있기 때문에 if문 안에서의 변수는 밖에서 사용하지 못한다.
    
    ```jsx
    if (true){
      const num = 10;
    }
    
    // console.log(num) // 사용 불가
    ```
    
- if문 안에서 변수의 값을 변경해야 하면 미리 let으로 선언해줘야 한다.
    
    ```jsx
    let num;
    
    if (true){
      num = 10;
    }
    
    console.log(num);
    ```