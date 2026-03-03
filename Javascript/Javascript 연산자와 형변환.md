## 타입 연산자

### typeof

- `typeof 데이터`: 데이터의 자료형 확인
    
    ```jsx
    const num = 123;
    const str = "Hello";
    const bool = true;
    const undef = undefined;
    console.log(typeof num); // number
    console.log(typeof str); // string
    console.log(typeof bool); // boolean
    console.log(typeof undef); // undefined
    
    ```
    

## 산술 연산자

### 기본 산술 연산자

- `+`: 더하기
- `-`: 빼기
- `*`: 곱하기
- `/`: 나누기

```jsx
const a = 7;
const b = 2;
console.log(a + b); // 9
console.log(a - b); // 5
console.log(a * b); // 14
console.log(a / b); // 3.5

```

### 나머지, 거듭제곱

- `%`: 나머지 (나눈 후 남은 값)
- `**`: 거듭제곱
- 파이썬과 다르게 `몫`에 대한 연산자는 존재하지 않는다.
    - 대신 `Math.floor()`를 사용한다.

```jsx
const num1 = 10;
const num2 = 3;
console.log(num1 % num2); // 1

const num3 = 7;
const num4 = 2;
console.log(num3 % num4); // 1

const base = 2;
const exponent = 3;
console.log(base ** exponent); // 8
console.log(exponent ** base); // 9

```

### 문자열 연결

- `+` 연산자로 문자열 연결
- 템플릿 리터럴을 활용하는것을 권장
- 문자열과 다른 자료형 `+` 연산 시, 결과는 문자열

```jsx
const str1 = "Hello";
const str2 = "World";
console.log(str1 + str2); // HelloWorld

```

**문자열과 숫자 연결**

```jsx
const prefix = "나이: ";
const age = 25;
console.log(prefix + age); // 나이: 25

```

## 비교 연산자

### 크기 비교

- `>`: 초과
- `<`: 미만
- `>=`: 이상
- `<=`: 이하
- 문자열: 사전순 비교

```jsx
const num1 = 10;
const num2 = 5;
console.log(num1 > num2); // true

const num3 = 3;
const num4 = 7;
console.log(num3 < num4); // true

const char1 = "a";
const char2 = "A";
console.log(char1 > char2); // true

```

- 파이썬과 다르게 다음 로직은 유효하지 않는다.
    
    ```jsx
    const x = 10;
    consle.log(1 < x < 20)
    ```
    

### 동등 비교

- `===`: 같음
- `!==`: 다름

**예시**

```jsx
const num1 = 5;
const num2 = 5;
console.log(num1 === num2); // true

const num3 = 5;
const num4 = 3;
console.log(num3 !== num4); // true

const str1 = "hello";
const str2 = "hello";
console.log(str1 === str2); // true

```

## 논리 연산자

- `&&` (AND): 모든 피연산자가 참일 때 참
- `||` (OR): 피연산자 중 하나라도 참일 때 참
- `!` (NOT): 피연산자의 불리언 값 반전

```jsx
const a = true;
const b = false;
console.log(a && a); // true
console.log(a || b); // true
console.log(!a); // false

```

## `==` 와 `===`

### `==`

- 값만 비교
- 자료형이 다르면 자료형 변환 후 비교
- 절대 사용하지 말 것

### `===`

- 값과 자료형 모두 비교
- 자료형이 다르면 비교 결과가 거짓

```jsx
const a = 1;
const b = 1;
console.log(a == b); // true
console.log(a === b); // true

const c = 1;
const d = "1";
console.log(c == d); // true
console.log(c === d); // false

```

---

# 형변환(Type Conversion)

- 데이터의 자료형을 다른 자료형으로 변환하는 과정
- 명시적 형변환과 암시적 형변환으로 구분

## 명시적 형변환

- 개발자가 직접 변환

### 문자열 형변환

- `String()` 함수 사용

```jsx
console.log(String(123)); // "123"
console.log(String(true)); // "true"
console.log(String(false)); // "false"
console.log(String(null)); // "null"
console.log(String(undefined)); // "undefined"

```

- `toString()` 메서드 사용

```jsx
console.log((123).toString()); // "123"
console.log(true.toString()); // "true"
console.log([1, 2, 3].toString()); // "1,2,3"
// null과 undefined는 메서드가 없어서 변환 불가

```

### 숫자 형변환

- `Number()` 함수 사용, 모든 문자가 숫자로 변환 가능하면 변환, 아니면 NaN
    - NaN : Not a Number란 뜻으로, 숫자가 아니지만 숫자로 취급되는 값이다.

```jsx
console.log(Number("123")); // 123
console.log(Number("123.45")); // 123.45
console.log(Number("123abc")); // NaN
console.log(Number("")); // 0
console.log(Number(" ")); // 0
console.log(Number(true)); // 1
console.log(Number(false)); // 0
console.log(Number(null)); // 0
console.log(Number(undefined)); // NaN

```

- `parseInt()` 함수 사용, 문자열의 앞부분 중 숫자로 변환 가능한 부분만 변환

```jsx
console.log(parseInt("123")); // 123
console.log(parseInt("123.45")); // 123
console.log(parseInt("123abc")); // 123

```

- `parseFloat()` 함수 사용, 문자열의 앞부분 중 실수로 변환 가능한 부분만 변환

```jsx
console.log(parseFloat("123")); // 123
console.log(parseFloat("123.45")); // 123.45
console.log(parseFloat("123abc")); // 123

```

### 불리언 형변환

- `Boolean()` 함수 사용

```jsx
console.log(Boolean(1)); // true
console.log(Boolean(0)); // false
console.log(Boolean("hello")); // true
console.log(Boolean("")); // false
console.log(Boolean(null)); // false
console.log(Boolean(undefined)); // false
console.log(Boolean(NaN)); // false

```

---

## 암시적 형변환

- JavaScript 엔진이 자동으로 변환
- 예상과 다르게 동작하는 일이 많기 때문에 사용하지 않는 것이 좋다.
    - ex) `'b'+'a'+ +'a'+'a'`

### 문자열 연결 시 형변환

```jsx
const a = 1;
const b = "2";
console.log(a + b); // "12"

```

### 산술 연산 시 형변환

```jsx
console.log("10" - 5); // 5 (문자열이 숫자로 변환)
console.log("10" * 2); // 20
console.log("10" / 2); // 5
console.log("10" % 3); // 1
console.log("abc" - 5); // NaN, 문자열이 숫자로 변환 불가

```