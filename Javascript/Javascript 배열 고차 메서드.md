## 배열 고차 메서드(Array Higher Order Method)

- 배열 내부의 각 원소에 콜백 함수를 순차적으로 적용하는 메서드

### `forEach()`

- 기본적인 배열의 반복 작업에 사용
- 콜백 함수의 반환값(return)이 없음(undefined)
- 모든 배열 고차 메서드의 기본 형태
- 활용도 높음

```jsx
array.forEach((element, index, array) => {
  // 적용할 로직
});

```

- `element` : 배열 내부의 각 원소
- `index` : 배열 내부의 각 원소의 인덱스
- `array` : 원본 배열

**for 반복문 비교**

```jsx
for (let i = 0; i < array.length; i++) {
  // 적용할 로직
}

```

**예시**

```jsx
let todos = ["숙제하기", "운동하기", "독서하기"];

todos.forEach((todo, index) => {
  console.log(`${index + 1}. ${todo}`);
});

```

### `map()`

- 콜백 함수의 반환값을 원소로 모아서 새로운 배열 생성
- 데이터의 변환, UI 렌더링에 사용
- 활용도 높음. **아주 중요!**

```jsx
const newArray = array.map((element, index, array) => {
  // 적용할 로직
  return 반환값;
});

```

- `element` : 배열 내부의 각 원소
- `index` : 배열 내부의 각 원소의 인덱스
- `array` : 원본 배열

**for 반복문 비교**

```jsx
let newArray = [];
for (let i = 0; i < array.length; i++) {
  newArray.push(callbackFunction(array[i], i, array));
}

```

**예시**

```jsx
let todos = ["숙제하기", "운동하기", "독서하기"];

let completedTodos = todos.map((todo) => {
  return `${todo} 완료`;
});
let urgentTodos = todos.map((todo) => {
  return `긴급: ${todo}`;
});

console.log(todos); // ["숙제하기", "운동하기", "독서하기"] (원본 유지)
console.log(completedTodos); // ["숙제하기 완료", "운동하기 완료", "독서하기 완료"]
console.log(urgentTodos); // ["긴급: 숙제하기", "긴급: 운동하기", "긴급: 독서하기"]

```

### `filter()`

- 콜백 함수의 반환값이 `true`인 원소만 모아 새로운 배열 생성
- 데이터의 필터링(검색)에 사용
- 활용도 높음

```jsx
const newArray = array.filter((element, index, array) => {
  if (조건) {
    return true;
  } else {
    return false;
  }
});

```

- `element` : 배열 내부의 각 원소
- `index` : 배열 내부의 각 원소의 인덱스
- `array` : 원본 배열

**for 반복문 비교**

```jsx
let newArray = [];
for (let i = 0; i < array.length; i++) {
  if (조건) {
    newArray.push(array[i]);
  }
}

```

**예시**

```jsx
let todos = [
  { task: "숙제하기", priority: "high", completed: false },
  { task: "운동하기", priority: "medium", completed: true },
  { task: "독서하기", priority: "high", completed: false },
  { task: "청소하기", priority: "low", completed: false },
];

let highPriorityTodos = todos.filter((todo) => {
  if (todo.priority === "high") {
    return true;
  }
});

let incompleteTodos = todos.filter((todo) => {
  if (todo.completed === false) {
    return true;
  }
});

console.log(highPriorityTodos); // 우선순위가 높은 할 일들
console.log(incompleteTodos); // 완료되지 않은 할 일들

```

### `find()`

- 콜백 함수의 반환값이 `true`인 첫 번째 원소 반환
- `true`를 반환하는 원소가 없으면 `undefined` 반환
- 특정 데이터 검색에 사용
- 활용도 높음

```jsx
const newArray = array.find((element, index, array) => {
  // 적용할 로직
  if (조건) {
    return true;
  }
});

```

- `element` : 배열 내부의 각 원소
- `index` : 배열 내부의 각 원소의 인덱스
- `array` : 원본 배열

**예시**

```jsx
let todos = [
  { id: 1, task: "숙제하기", priority: "medium" },
  { id: 2, task: "운동하기", priority: "high" },
  { id: 3, task: "독서하기", priority: "low" },
];

let highPriorityTodo = todos.find((todo) => {
  if (todo.priority === "high") {
    return true;
  }
});
let urgentTodo = todos.find((todo) => {
  if (todo.priority === "urgent") {
    return true;
  }
});

console.log(highPriorityTodo); // { id: 2, task: "운동하기", priority: "high" }
console.log(urgentTodo); // undefined

```

### `reduce()`

- 배열의 원소를 순차적으로 누적하여 하나의 값으로 반환
- 활용도 중간

```jsx
const newArray = array.reduce((acc, element, index, array) => {
  // 적용할 로직
  return 반환값;
});

```

- `acc` : 누적값
- `element` : 배열 내부의 각 원소
- `index` : 배열 내부의 각 원소 인덱스
- `array` : 원본 배열

**예시**

```jsx
let todos = [
  { task: "숙제하기", timeSpent: 2 },
  { task: "운동하기", timeSpent: 1 },
  { task: "독서하기", timeSpent: 3 },
  { task: "청소하기", timeSpent: 1 },
];

let totalTime = todos.reduce((acc, todo) => {
  console.log(`누적 시간: ${acc}, 현재 작업 시간: ${todo.timeSpent}`);
  return acc + todo.timeSpent;
}, 0); // 초기값 0

console.log(`총 소요 시간: ${totalTime}시간`);

```

```
누적 시간: 0, 현재 작업 시간: 2
누적 시간: 2, 현재 작업 시간: 1
누적 시간: 3, 현재 작업 시간: 3
누적 시간: 6, 현재 작업 시간: 1
총 소요 시간: 7시간

```

### `sort()`

- 배열의 원소를 정렬
- 배열의 첫 원소부터 끝 원소까지 순차적으로 두 개씩 비교
- 원본 배열 변경
- 활용도 중간

```jsx
const newArray = array.sort((a, b) => {
  // 정렬 기준
  // a가 b보다 앞에 오게 하려면 음수 반환
  // a가 b보다 뒤에 오게 하려면 양수 반환
  // a가 b보다 같게 하려면 0 반환
});

```

**예시**

```jsx
let numbers = [1, 5, 2, 7, 3];

// 오름차순 정렬
numbers.sort((a, b) => {
  if (a < b) {
    // a가 작기 때문에 앞에 오게 하려면 음수 반환
    return -1;
  } else if (a > b) {
    // a가 크기 때문에 뒤에 오게 하려면 양수 반환
    return 1;
  } else {
    return 0;
  }
});

console.log(numbers); // [1, 2, 3, 5, 7]

// 내림차순 정렬
numbers.sort((a, b) => {
  if (a < b) {
    // a가 작기 때문에 뒤에 오게 하려면 양수 반환
    return 1;
  } else if (a > b) {
    // a가 크기 때문에 앞에 오게 하려면 음수 반환
    return -1;
  } else {
    return 0;
  }
});

console.log(numbers); // [7, 5, 3, 2, 1]

// 간단한 오름차순 정렬
numbers.sort((a, b) => {
  // a가 b보다 작으면 음수를 반환하기에 a가 앞에 배치
  // a가 b보다 크면 양수를 반환하기에 a가 뒤에 배치
  return a - b;
});

console.log(numbers); // [1, 2, 3, 5, 7]

// 간단한 내림차순 정렬
numbers.sort((a, b) => {
  // a가 b보다 작으면 양수를 반환하기에 a가 뒤에 배치
  // a가 b보다 크면 음수를 반환하기에 a가 앞에 배치
  return b - a;
});

console.log(numbers); // [7, 5, 3, 2, 1]

```

### `some()`

- 배열의 원소 중 하나라도 콜백 함수의 반환값이 `true` 인지 확인
- 하나라도 `true`를 반환하면 고차 메서드는 `true` 반환
- 모든 원소가 `false`를 반환하면 고차 메서드는 `false` 반환
- 활용도 중간

```jsx
const newArray = array.some((element, index, array) => {
  // 적용할 로직
  if (조건) {
    return true;
  }
});

```

- `element` : 배열 내부의 각 원소
- `index` : 배열 내부의 각 원소의 인덱스
- `array` : 원본 배열

### `every()`

- 배열의 모든 원소가 콜백 함수의 반환값이 `true` 인지 확인
- 모든 원소가 `true`를 반환하면 고차 메서드는 `true` 반환
- 하나라도 `false`를 반환하면 고차 메서드는 `false` 반환
- 활용도 중간

```jsx
const newArray = array.every((element, index, array) => {
  // 적용할 로직
  if (조건) {
    return true;
  }
});

```

- `element` : 배열 내부의 각 원소
- `index` : 배열 내부의 각 원소의 인덱스
- `array` : 원본 배열

### `findIndex()`

- 콜백 함수의 반환값이 `true`인 첫 번째 원소의 인덱스 반환
- `true`를 반환하는 원소가 없으면 `-1` 반환
- 활용도 낮음

```jsx
const newArray = array.findIndex((element, index, array) => {
  // 적용할 로직
  if (조건) {
    return true;
  }
});

```

- `element` : 배열 내부의 각 원소
- `index` : 배열 내부의 각 원소의 인덱스
- `array` : 원본 배열

## 정리표

| 메서드 | 기능 | 반환값 | 활용도 | 원본 배열 변경 |
| --- | --- | --- | --- | --- |
| `forEach()` | 각 원소에 콜백 함수 적용 | `undefined` | 높음 | ❌ |
| `map()` | 각 원소를 변환하여 새 배열 생성 | 새로운 배열 | 높음 | ❌ |
| `filter()` | 조건에 맞는 원소만 필터링 | 새로운 배열 | 높음 | ❌ |
| `find()` | 조건에 맞는 첫 번째 원소 찾기 | 원소 또는 `undefined` | 높음 | ❌ |
| `reduce()` | 모든 원소를 하나의 값으로 축약 | 단일 값 | 중간 | ❌ |
| `sort()` | 원소를 정렬 | 정렬된 배열 | 중간 | ✅ |
| `some()` | 하나라도 조건에 맞는 원소 있는지 확인 | `true` 또는 `false` | 낮음 | ❌ |
| `every()` | 모든 원소가 조건에 맞는지 확인 | `true` 또는 `false` | 낮음 | ❌ |
| `findIndex()` | 조건에 맞는 첫 번째 원소의 인덱스 | 인덱스 또는 `-1` | 낮음 | ❌ |