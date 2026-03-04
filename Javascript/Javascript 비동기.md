## 스레드, 동기적 처리, 비동기적 처리

### 스레드(Thread)

- 프로그램의 작업 처리 단위
- JavaScript는 싱글 스레드 구조로, 한 번에 하나의 작업만 처리

### 동기적 처리(Synchronous)

- 하나의 작업이 끝날 때까지 다음 작업을 시작하지 않는 방식
- 순차적 처리
- 앞의 작업이 길어지면 전체 프로그램 정지

### 비동기적 처리(Asynchronous)

- 시간이 오래 걸리는 작업을 백그라운드에서 처리하며 다른 작업을 계속 진행하는 방식
- 동시 처리
- 프로그램 정지 없음

### 블록킹(Blocking)과 논블록킹(Non-Blocking)

- 블록킹: 하나의 작업이 끝날 때까지 다음 작업을 시작하지 않는 방식, 동기적 처리
- 논블록킹: 하나의 작업이 끝날 때까지 기다리지 않고 다음 작업을 시작하는 방식, 비동기적 처리

### 문제 상황

**동기적 처리 문제**

```jsx
console.log("작업 1 시작");

// 5초 동안 아무것도 하지 않는 코드
let start = Date.now();
while (Date.now() - start < 5000) {
  // 5초 대기
}

console.log("작업 1 완료");
console.log("작업 2 시작");

```

**위 코드의 문제점**

- 5초 동안 프로그램 완전 정지
- 웹 서비스의 경우, 사용자 행동에 무반응

### 문제 해결

**비동기적 처리로 문제 해결**

```jsx
console.log("작업 1 시작");

// setTimeout() : 특정 시간 후 콜백 함수를 실행하는 비동기 처리 API
setTimeout(() => {
  console.log("작업 1 완료");
}, 5000);

// setTimeout() 실행과 상관없이 바로 실행된다
console.log("작업 2 시작");

```

---

## JavaScript 비동기 처리 API

- 웹 브라우저(Node.js) 제공 비동기 처리 함수
- 비동기 처리 API는 콜백 함수를 필수 인자로 받음

### `setTimeout()`

- 지정된 시간 후 콜백 함수를 실행

**기본 구조**

```jsx
setTimeout(callback, delay);

```

- `callback`: 지연 후 실행할 코드
- `delay`: 실행 지연 시간 (밀리초)

**예시**

```jsx
console.log(1);

setTimeout(() => {
  console.log(2);
}, 2000);

console.log(3);

// 실행 결과: 1, 3, 2
```

**실행 과정**

1. `printMessage(1)`: 함수 즉시 실행
2. `setTimeout`: `printMessage(2)`를 5초 후 실행하도록 등록
3. `printMessage(3)`: 함수 즉시 실행
4. 5초 후 `printMessage(2)` 실행

### `setInterval()`

- 지정된 시간마다 콜백 함수를 반복 실행

**기본 구조**

```jsx
const intervalId = setInterval(callback, delay);

clearInterval(intervalId);

```

- `callback`: 반복 실행할 코드
- `delay`: 반복 실행 간격 (밀리초)
- `intervalId`: `setInterval()`에서 반환된 아이디
- `clearInterval`: 반복 실행 중지

**예시**

```jsx
function printMessage(number) {
  console.log(number);
}

let count = 0;

const intervalId = setInterval(() => {
  printMessage(count);
  count++;
  if (count === 3) {
    clearInterval(intervalId);
  }
}, 1000);

```

**실행 과정**

1. `setInterval`: `printMessage(count)`를 1초마다 실행하도록 등록
2. 1초 후 `printMessage(0)`: 실행
3. 2초 후 `printMessage(1)` 실행
4. 3초 후 `printMessage(2)` 실행
5. 3초 후 `clearInterval` 실행

---

## JavaScript 비동기 처리 구성 요소와 메커니즘

### Web APIs

- 웹 브라우저 또는 Node.js 환경이 제공하는 비동기 기능(setTimeout, fetch 등) 처리
- JavaScript 코드 실행 환경과 분리된 멀티 스레드 환경

콜백 큐, 이벤트 루프, 콜 스택 이런 것들이 면접에서 중요. 잘 알아두고 면접을 보자.

### 콜백 큐 (Callback Queue)

- 비동기 처리 완료 후 실행될 콜백 함수 대기 장소
- 이벤트 루프에서 비동기 작업이 끝나면 콜백 큐로 이동함.

### 이벤트 루프 (Event Loop)

- 콜 스택의 상태를 지속적으로 확인하여, 비어있을 경우 콜백 큐의 함수를 콜 스택으로 이동

### 콜 스택 (Call Stack)

- 현재 실행 중인 함수가 쌓이는 곳
- JavaScript 코드 실행 영역
- **싱글 스레드 환경**
- setTimeout() 같은 비동기 작업이 시간이 3000이 아니라 0초 라고 해도 일단 이벤트 루프로 보냄.
그래서 0초로 설정해도 동기1, 동기2가 실행된 후 실행된다.

### 예시

```jsx
const first = () => {
  console.log('동기 작업 1');
};

const second = () => {
  setTimeout(() => {
    console.log('비동기 작업 1');
  }, 3000);
};

const third = () => {
  setTimeout(() => {
    console.log('비동기 작업 2');
  }, 1000);
};

const fourth = () => {
  console.log('동기 작업 2');
};

first();
second();
third();
fourth();
```

- 실행 결과
    
    ```bash
    동기 작업 1
    동기 작업 2
    비동기 작업 2
    비동기 작업 1
    ```