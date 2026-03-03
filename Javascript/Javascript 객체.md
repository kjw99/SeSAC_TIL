# 객체(Object)

- 이름(key)과 값(value)의 집합을 저장하는 자료형
- 이름과 값의 쌍을 속성(property)이라고 부름

## 객체 기본 조작

### 객체 생성

- 중괄호 `{}`를 사용해 생성
- 이름(key)과 값(value)은 콜론 `:`으로 구분
- 속성(property)은 쉼표 `,`로 구분

```jsx
let object = {
  key: value,
  key2: value2,
};

```

**예시**

```jsx
let person = {
  name: "홍길동",
  age: 30,
  job: "개발자",
};

console.log(person); // { name: '홍길동', age: 30, job: '개발자' }

```

### 객체 속성 접근

- 마침표 `.`
- 대괄호 `[]`
- 키에 변수를 사용하거나 공백이나 특수문자가 포함된 경우 대괄호 `[]` 사용

```jsx
let person = {
  name: "홍길동",
  age: 30,
  job: "개발자",
};

console.log(person.name); // 홍길동
console.log(person["job"]); // 개발자

```

### 객체 속성 수정

- 마침표 `.` 또는 대괄호 `[]`를 사용해 수정할 속성에 접근하여 값 재할당

```jsx
let person = {
  name: "홍길동",
  age: 30,
  job: "개발자",
};

person.age = 40;
person["job"] = "프로그래머";

console.log(person); // { name: '홍길동', age: 40, job: '프로그래머' }

```

### 객체 속성 추가

- 마침표 `.` 또는 대괄호 `[]`를 사용해 속성 추가

```jsx
let person = {
  name: "홍길동",
  age: 30,
  job: "개발자",
};

person.address = "서울";
person["nationality"] = "한국";

console.log(person); // { name: '홍길동', age: 30, job: '개발자', address: '서울', nationality: '한국' }

```

### 객체 메서드

- 객체에 데이터를 추가하거나 제거하는 등의 작업을 수행하는 도구

**`Object.keys()`**

- 객체의 모든 이름(key)을 배열로 반환

```jsx
let person = {
  name: "홍길동",
  age: 30,
  job: "개발자",
};

console.log(Object.keys(person)); // [ 'name', 'age', 'job' ]

```

**`Object.values()`**

- 객체의 모든 값(value)을 배열로 반환

```jsx
let person = {
  name: "홍길동",
  age: 30,
  job: "개발자",
};

console.log(Object.values(person)); // [ '홍길동', 30, '개발자' ]

```

**`Object.entries()`**

- 객체의 모든 [이름(key), 값(value)] 쌍을 배열로 반환

```jsx
let person = {
  name: "홍길동",
  age: 30,
  job: "개발자",
};

```

```jsx
console.log(Object.entries(person));
// [ ['name', '홍길동'], ['age', 30], ['job', '개발자'] ]

```

**`객체.hasOwnProperty(속성명)`**

- 객체의 특정 속성이 있는지 확인

```jsx
let person = {
  name: "홍길동",
  age: 30,
  job: "개발자",
};

console.log(person.hasOwnProperty("name")); // true
console.log(person.hasOwnProperty("address")); // false

```

### 객체 속성 제거 연산자

**`delete 객체.속성명`**

- 객체의 이름(key)에 해당하는 속성 제거

```jsx
let person = {
  name: "홍길동",
  age: 30,
  job: "개발자",
};

delete person.job;

console.log(person); // { name: '홍길동', age: 30}

```

---

## `for...in` 반복문

- 객체(Object)의 모든 이름(key)을 순회

**기본 구조**

```jsx
for (let key in 객체) {
  // 객체의 이름(key)을 순회
}

```

**객체의 이름(key) 순회**

```jsx
const person = { name: "홍길동", age: 30, city: "서울" };

for (let key in person) {
  console.log(`${key}`);
}

```

```
name
age
city

```

**객체의 이름(key)과 값(value) 순회**

```jsx
const person = { name: "홍길동", age: 30, city: "서울" };

for (let key in person) {
  let value = person[key];
  console.log(`${key}: ${value}`);
}

```

```
name: 홍길동
age: 30
city: 서울

```

## `forEach` 메서드

- 객체를 배열로 변환한 후 각 요소를 순회

```jsx
Object.keys(객체).forEach(function(key) {
  // 객체의 이름(key)을 순회
});
```

**객체의 이름(key) 순회**

```jsx
const person = { name: "홍길동", age: 30, city: "서울" };

Object.keys(person).forEach(key => {
  console.log(`${key}`);
});
```

```
name
age
city
```

**객체의 값(value) 순회**

```jsx
const person = { name: "홍길동", age: 30, city: "서울" };

Object.values(person).forEach(value => {
  console.log(`${value}`);
});
```

```
홍길동
30
서울
```

**객체의 이름(key)과 값(value) 순회**

```jsx
const person = { name: "홍길동", age: 30, city: "서울" };

Object.entries(person).forEach(([key, value]) => {
  console.log(`${key}: ${value}`);
});
```

```
name: 홍길동
age: 30
city: 서울
```

---

## 메서드(Method)

- 객체의 속성으로 할당된 함수
- 해당 객체의 동작을 정의
- 하나의 객체는 여러 메서드를 가질 수 있음

### 메서드 구조

```jsx
const 객체 = {
  메서드: function () {
    // 객체의 동작을 정의하는 코드 블록
  },
};

```

**예시**

```jsx
const person = {
  name: "철수",
  greet: function () {
    console.log("안녕하세요. 반갑습니다.");
  },
};

person.greet(); // 안녕하세요. 반갑습니다.

```

**축약형 메서드**

```jsx
const person = {
  name: "철수",
  greet() {
    console.log("안녕하세요. 반갑습니다.");
  },
};

person.greet(); // 안녕하세요. 반갑습니다.

```

---

## JSON(JavaScript Object Notation)

- 데이터 교환용 경량의 텍스트 형식
- JavaScript의 객체 형식과 유사

### JSON 변환

**`JSON.stringify()`**

- JavaScript 객체를 JSON 문자열로 변환

```jsx
const person = { name: "홍길동", age: 30, job: "개발자" };
const jsonString = JSON.stringify(person);
console.log(jsonString); // {"name":"홍길동","age":30,"job":"개발자"}

```

**`JSON.parse()`**

- JSON 문자열을 JavaScript 객체로 변환

```jsx
const jsonString = '{"name":"홍길동","age":30,"job":"개발자"}';
const person = JSON.parse(jsonString);
console.log(person); // { name: '홍길동', age: 30, job: '개발자' }

```