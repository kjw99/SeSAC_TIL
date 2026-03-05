## ECMAScript

- JavaScript 공식 표준 문법, 줄여서 ES라고 함
- 2015년(ECMAScript2015, ES6)부터 매년 새로운 문법이 업데이트됨
- 많은 문법이 추가된 ES6을 모던 자바스크립트의 시작점이 됨
    - `let` `const` `arrow function` `template literal` 등

## 단축 프로퍼티(property value shorthand)

- 변수명과 객체의 속성명이 같으면 `{key:value}` 대신 `{변수명}`으로 축약하는 문법
- 코드의 가독성을 향상시킨다

```jsx
const variableName = "variableValue";

const obj = {
  variableName,
};

console.log(obj); // { variableName: 'variableValue' }

```

**예시**

```jsx
// 변수 선언
const name = "jun";
const age = 25;

// 객체 생성
const person1 = {
  name: name,
  age: age,
};

// 단축 프로퍼티 사용
const person2 = {
  name, // name: name과 동일
  age, // age: age와 동일
};

console.log(person1); // { name: 'jun', age: 25 }
console.log(person2); // { name: 'jun', age: 25 }

```

---

## 계산된 속성명(Computed Property Names)

- `[key(이름)]` 연산자
- 객체의 속성명을 변수를 활용해 동적으로 생성할 수 있음

**기본 구조**

```jsx
const key = "name";
const value = "jun";

const obj = {
  [key]: value,
};

console.log(obj); // { name: 'jun' }

```

---

## 펼침 연산자(Spread Operator)

- `...` 연산자
- 배열의 원소 또는 객체의 속성을 마치 펼쳐서 새로운 배열 또는 객체를 생성하는 연산자

**기본 구조**

```jsx
const newArray = [...array]; // 배열의 원소를 펼쳐서 새로운 배열 생성
const newObject = { ...object }; // 객체의 속성을 펼쳐서 새로운 객체 생성

```

### 배열의 펼침 연산자

- 배열 원소를 그대로 복사하여 새로운 배열 생성
- 다른 배열과 결합하는 방법

**배열 복사**

```jsx
let arr1 = [1, 2, 3];
let arr2 = [...arr1];

console.log(arr2); // [1, 2, 3]

```

**다른 배열과 결합**

```jsx
let arr1 = [1, 2, 3];
let arr2 = [...arr1, 4, 5, 6];

console.log(arr2); // [1, 2, 3, 4, 5, 6]

```

### 객체의 펼침 연산자

- 객체 속성을 그대로 복사하여 새로운 객체 생성
- 다른 객체와 결합하는 방법

**객체 복사**

```jsx
let obj1 = { name: "홍길동", age: 25 };
let obj2 = { ...obj1 };

console.log(obj2); // { name: '홍길동', age: 25 }

```

**다른 객체와 결합**

```jsx
let obj1 = { name: "홍길동", age: 25 };
let obj2 = { ...obj1, age: 20 }; // 기존 속성의 값 변경
let obj3 = { ...obj1, job: "개발자" }; // 새로운 속성(key-value) 추가

console.log(obj2); // { name: '홍길동', age: 20}
console.log(obj3); // { name: '홍길동', age: 25, job: '개발자' }

```

### 할당문과 펼침 연산자 비교

- 할당문은 주소를 복사하고, 펼침 연산자는 값을 복사

```jsx
const arr1 = [1, 2, 3];
const arr2 = arr1; // 배열의 주소를 복사
const arr3 = [...arr1]; // 배열의 원소를 펼쳐서 새로운 배열 생성

arr1.push(4);
arr2.push(5);
arr3.push(6);

console.log(arr1); // [1, 2, 3, 4, 5]
console.log(arr2); // [1, 2, 3, 4, 5]
console.log(arr3); // [1, 2, 3, 6]

```

---

## 구조 분해 할당(Destructuring Assignment)

- 배열이나 객체의 값을 개별 변수로 분해하여 할당하는 문법

**기본 구조**

```jsx
const [variable1, variable2] = array; // 배열의 원소를 각 위치의 변수에 할당
const { key1, key2 } = object; // 객체의 속성을 각 이름의 변수에 할당

```

### 배열의 구조 분해 할당

**배열 원소를 각 위치의 변수에 할당**

```jsx
const fruits = ["사과", "바나나", "딸기"];

// 배열의 원소를 각 위치의 변수에 할당
const [first, second, third] = fruits;

console.log(first); // '사과'
console.log(second); // '바나나'
console.log(third); // '딸기'

```

### 객체의 구조 분해 할당

**객체 속성과 동일한 이름의 변수에 할당**

```jsx
const person = {
  name: "홍길동",
  age: 30,
  job: "개발자",
};

// 변수의 순서와 관계없이 객체의 속성과 동일한 이름의 변수로 할당
const { name, job, age } = person;

console.log(name); // '홍길동'
console.log(age); // 30
console.log(job); // '개발자'

```

---

## 옵셔널 체이닝

- `?.` 연산자
- 배열의 원소와 객체의 속성, 메서드에 안전하게 접근하는 문법
- 존재하지 않는 데이터(원소, 속성, 메서드)에 접근 시 오류를 일으키는 대신 `undefined` 을 반환한다
- API 응답 데이터 구조가 고정적이지 않을 때 유용하다
- 객체에 대해서 없는 key에 접근하면 undefined가 나오는데, undefined에 대해 key에 접근하면 에러가 나옴.
    - obj.gender 값이 undefined인데, obj.gender.detail 이런식으로 접근하면 에러가 나온다는 것.
- 근데, 비동기 작업으로 나중에 값이 들어오는 경우도 많음! 특히 리액트. 그래서 옵셔널 체이닝을 사용해서 값이 있으면 가져오고, 없으면 undefined를 받도록 설정하는 것.
    - obj.gender.detail = 에러. / obj.gender?.detail = undefined
    - obj.gender 는 undefined 라고 가정.

**기본 구조**

```jsx
object?.property;
object?.method();

```

### 객체에서의 옵셔널 체이닝

```jsx
const user = {
  name: "홍길동",
  address: {
    city: "서울",
  },
};

console.log(user?.name); // 홍길동
console.log(user?.address?.city); // 서울

// 존재하지 않는 속성 접근
console.log(user?.phone?.number); // undefined

```

### 배열에서의 옵셔널 체이닝

```jsx
const users = [{ name: "철수" }, { name: "영희" }];

console.log(users?.[0]?.name); // 철수
console.log(users?.[1]?.name); // 영희

// 존재하지 않는 인덱스 접근
console.log(users?.[2]?.name); // undefined

```

### 메서드 호출 옵셔널 체이닝

```jsx
const user = {
  greet() {
    return "안녕하세요!";
  },
};

console.log(user.greet?.()); // 안녕하세요!

// 존재하지 않는 메서드 호출
console.log(user.sayHello?.()); // undefined

```

---

## Nullish 병합 연산자

- `??` 연산자
- 접근하려는 값이 `null` 또는 `undefined`일 때 기본값(default value)을 적용한다
- 옵셔널 체이닝과 결합하여 API 호출 시 응답 데이터에 특정 속성이 없을 때 기본값을 적용한다

**기본 구조**

```jsx
const value1 = null;
const defaultValue = "defaultValue";

let variable = value1 ?? defaultValue;

console.log(variable); // 'defaultValue'

```

**에시**

```jsx
let username = null;
let defaultName = "익명";

let userAge;
let defaultAge = 20;

let userJob = "프로그래머";
let defaultJob = "취준생";

let name = username ?? defaultName; // username은 null이므로 기본값 적용
let age = userAge ?? defaultAge; // userAge는 undefined이므로 기본값 적용
let job = userJob ?? defaultJob; // userJob은 "프로그래머"이므로 기본값 적용 X

console.log(name); // 익명
console.log(age); // 20
console.log(job); // 프로그래머

```

**옵셔널 체이닝과 결합**

```jsx
const user = {
  name: "홍길동",
  address: {
    city: "대구",
  },
};

const city = user?.address?.city ?? "서울";
const country = user?.address?.country ?? "한국";

console.log(city); // 대구
console.log(country); // 한국

```

---

## JS에서의 Truthy / Falsy

- 불리언(Boolean) 문맥(if문의 조건문 등)에서 다음 값들은 false로 처리된다.
    
    
    | **값** | **설명** |
    | --- | --- |
    | **false** | 불리언 false |
    | **0** | 숫자 0 (양수, 음수 0 포함) |
    | **0n** | BigInt의 0 |
    | **""** | 빈 문자열 (작은따옴표, 백틱 포함) |
    | **null** | 아무것도 없음 |
    | **undefined** | 정의되지 않음 |
    | **NaN** | Not a Number (숫자가 아님) |
    | **document.all** | (특수 사례) 과거 브라우저 하위 호환용 |
- python에서 `[]`(빈 리스트), `{}` (빈 딕셔너리) 등이 False로 처리되는 것과는 달리,
JS에서는 true로 처리된다.