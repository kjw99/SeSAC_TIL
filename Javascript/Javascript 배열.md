## 배열(Array)

- 0개 이상의 데이터를 순서에 따라 저장하는 자료형
    - 배열에 저장된 데이터를 `원소(요소)` 라고 부름
- 데이터 추가/제거가 자유로움
- 자료형 구분 없이 데이터 저장 가능

## 배열 기본 조작

### 배열 생성

- 대괄호 `[]`를 사용해 생성
- 배열의 원소는 쉼표 `,`로 구분

**빈 배열 생성**

```jsx
let emptyArray = [];
console.log(emptyArray); // []

```

**원소가 있는 배열 생성**

```jsx
let array = [1, 2, 3, "4"];
console.log(array); // [1, 2, 3, '4']

```

### 인덱스(위치 번호)

- 배열 내부 원소의 위치를 나타내는 0부터 시작하는 번호
- 인덱스 범위: 0 ~ (배열 원소 개수 - 1)

```jsx
let array = [1, 2, 3, 4];
/*
인덱스: 원소
0: 1
1: 2
2: 3
3: 4
*/

```

### 배열 원소 접근

- 대괄호 `[]`와 인덱스로 배열 원소에 접근

```jsx
let array = [1, 2, 3];
console.log(array[0]); // 1
console.log(array[1]); // 2
console.log(array[2]); // 3

// 인덱스 범위를 벗어난 경우 undefined 반환
console.log(array[3]); // undefined

```

### 배열 원소 수정

- 대괄호 `[]`와 인덱스로 접근하여 원소 데이터 재할당

```jsx
let array = [1, 2, 3];
array[0] = 10;
console.log(array); // [10, 2, 3]

```

---

## 배열 속성과 메서드

- 배열에 데이터를 추가하거나 제거하는 등의 작업을 수행하는 도구

**`.length`**

- 배열의 원소 개수를 반환

```jsx
let array = [1, 2, 3];
const length = array.length;
console.log(length); // 3

```

**`push(x)`**

- 배열의 끝에 데이터 추가

```jsx
let numbers = [1, 2, "3"];
numbers.push(4);
console.log(numbers); // [ 1, 2, "3", 4 ]

```

**`pop()`**

- 배열의 마지막 원소를 제거하고, 제거한 원소 반환(return)
    - 반환(return): 메서드가 생성하는 데이터

```jsx
let numbers = [1, 2, "3"];
console.log(numbers); // [1, 2, "3"]

let pop_number = numbers.pop();
console.log(numbers); // [1, 2]
console.log(pop_number); // "3"

```

**`slice(start, end)`**

- 배열의 일부를 잘라 새로운 배열 생성
- 원본 배열 유지

```jsx
let numbers = [1, 2, "3"];
let slice_numbers = numbers.slice(0, 2);

console.log(numbers); // [1, 2, "3"]
console.log(slice_numbers); // [ 1, 2 ]

```

---

## 배열 반복

### `for` 반복문 활용

```jsx
for (let i = 0; i < 배열.length; i++) {
  // 배열[i]를 사용하여 배열의 원소에 접근
}

```

**예시**

```jsx
let array = [1, 2, 3, 4, 5];

for (let i = 0; i < array.length; i++) {
  console.log(array[i]);
}

```

```
1
2
3
4
5

```

### `for...of` 반복문

- 반복 가능한(Iterable) 자료형 값을 순회
- 반복 가능한 자료형: 배열, 문자열 등

```jsx
for (let value of 반복_가능한_자료형) {
  // 값을 순회
}

```

**배열 반복**

```jsx
const array = [1, 2, 3, 4, 5];

for (let number of array) {
  console.log(`숫자: ${number}`);
}

```

```
숫자: 1
숫자: 2
숫자: 3
숫자: 4
숫자: 5

```

**문자열 반복**

```jsx
const string = "Hello";

for (let char of string) {
  console.log(`문자: ${char}`);
}

```

```
H
e
l
l
o

```

### `forEach` 메서드

- 배열의 모든 원소를 순회하며, 각 원소에 대해 설정한 함수를 실행
- `for`문이나 `for...of`문보다 간결하게 배열 데이터를 처리할 때 사용

기본 문법

- 화살표 함수와 함께 사용하는 것이 일반적임
- 첫 번째 인자는 **현재 원소의 값**, 두 번째 인자는 **현재 원소의 인덱스**를 의미 (인덱스는 생략 가능)

```jsx
배열.forEach((값, 인덱스) => {
  // 실행할 코드
});
```

### 값만 사용

```jsx
const fruits = ["사과", "바나나", "포도"];

fruits.forEach((fruit) => {
  console.log(`과일: ${fruit}`);
});
```

```
과일: 사과
과일: 바나나
과일: 포도
```

### 값과 인덱스 함께 사용

```jsx
const colors = ["Red", "Green", "Blue"];

colors.forEach((color, index) => {
  console.log(`${index}번 색상: ${color}`);
});
```

```
0번 색상: Red
1번 색상: Green
2번 색상: Blue
```