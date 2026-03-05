# Promise

- 비동기 작업의 결과를 담는 객체
    - 쉽게 말해, "나중에 결과를 알려줄게"라는 **약속**
- 서버 요청, 파일 읽기 등 시간이 걸리는 작업의 결과를 다룰 때 사용

## Promise의 3가지 상태

- 대기(Pending)   → 작업이 아직 진행 중
- 이행(Fulfilled) → 작업이 성공적으로 완료됨
- 거부(Rejected)  → 작업이 실패함

---

## Promise 생성

- `new Promise()`로 생성
- `resolve`: 작업 성공 시 호출하는 함수
- `reject`: 작업 실패 시 호출하는 함수

```jsx
const promise = new Promise((resolve, reject) => {
  // 비동기 작업 수행
  // 성공하면 resolve(결과)
  // 실패하면 reject(에러)
});
```

**예시: 성공하는 Promise**

```jsx
const promise = new Promise((resolve, reject) => {
  resolve("성공!");
});

console.log(promise); // Promise { '성공!' }
```

**예시: 실패하는 Promise**

```jsx
const promise = new Promise((resolve, reject) => {
  reject("실패!");
});

console.log(promise); // Promise { <rejected> '실패!' }
```

---

## Promise 결과 사용: `.then()`과 `.catch()`

- `.then()`: 작업이 **성공**했을 때 실행할 코드
- `.catch()`: 작업이 **실패**했을 때 실행할 코드

### `.then()` - 성공 처리

```jsx
const promise = new Promise((resolve, reject) => {
  resolve("성공 데이터");
});

promise.then((result) => {
  console.log(result); // "성공 데이터"
});
```

### `.catch()` - 실패 처리

```jsx
const promise = new Promise((resolve, reject) => {
  reject("에러 발생");
});

promise.catch((error) => {
  console.log(error); // "에러 발생"
});
```

### `.then()`과 `.catch()` 함께 사용

```jsx
const promise = new Promise((resolve, reject) => {
  resolve("성공!");
});

promise
  .then((result) => {
    console.log("성공:", result);
  })
  .catch((error) => {
    console.log("실패:", error);
  });
```

---

## 실용 예시: 시간이 걸리는 작업

- `setTimeout`을 사용하여 시간이 걸리는 작업을 시뮬레이션

```jsx
const order = new Promise((resolve, reject) => {
  console.log("주문 접수!");

  setTimeout(() => {
    resolve("치킨");
  }, 2000); // 2초 후 완료
});

console.log("다른 일 하는 중...");

order.then((food) => {
  console.log(`${food} 도착!`);
});
```

```
주문 접수!
다른 일 하는 중...
치킨 도착!        ← 2초 후 출력
```

---

## Promise를 반환하는 함수

- 함수가 Promise를 `return`하면, 함수 호출 결과에 `.then()`/`.catch()` 사용 가능
- 실무에서 가장 많이 사용하는 패턴

```jsx
function fetchFood(menu) {
  return new Promise((resolve, reject) => {
    if (menu === "치킨") {
      resolve("치킨 준비 완료!");
    } else {
      reject("해당 메뉴는 품절입니다.");
    }
  });
}
```

**성공하는 경우**

```jsx
fetchFood("치킨")
  .then((result) => {
    console.log(result);
  })
  .catch((error) => {
    console.log(error);
  });
```

```
치킨 준비 완료!
```

**실패하는 경우**

```jsx
fetchFood("피자")
  .then((result) => {
    console.log(result);
  })
  .catch((error) => {
    console.log(error);
  });
```

```
해당 메뉴는 품절입니다.
```

---

## `.then()` 체이닝

- `.then()` 안에서 값을 `return`하면 다음 `.then()`에서 받아서 사용 가능
- 여러 작업을 순서대로 연결할 때 사용

```jsx
function getNumber() {
  return new Promise((resolve, reject) => {
    resolve(1);
  });
}

getNumber()
  .then((num) => {
    console.log(num); // 1
    return num + 1;
  })
  .then((num) => {
    console.log(num); // 2
    return num + 1;
  })
  .then((num) => {
    console.log(num); // 3
  });
```

```
1
2
3
```

---

## Promise와 async/await

- `.then()`/`.catch()` 대신 `async/await`로 더 간결하게 작성 가능
- 같은 동작을 하지만 코드가 위에서 아래로 읽혀서 **더 직관적**

**`.then()` 방식**

```jsx
fetchFood("치킨")
  .then((result) => {
    console.log(result);
  })
  .catch((error) => {
    console.log(error);
  });
```

**`async/await` 방식 (같은 동작)**

```jsx
async function order() {
  try {
    const result = await fetchFood("치킨");
    console.log(result);
  } catch (error) {
    console.log(error);
  }
}

order();
```

- Axios 같은 라이브러리가 반환하는 것도 Promise
    - 그래서 `await axios.get()`처럼 사용할 수 있었던 것

---

## Promise.all()

- 여러 개의 비동기 작업을 **동시에** 실행하고, **모두 완료되면** 결과를 받음
- 배열로 Promise들을 전달하고, 결과도 배열로 받음

```jsx
Promise.all([promise1, promise2, promise3])
  .then((results) => {
    // results = [결과1, 결과2, 결과3]
  });
```

**예시**

```jsx
function getUser(id) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(`유저${id}`);
    }, 1000);
  });
}

Promise.all([getUser(1), getUser(2), getUser(3)])
  .then((users) => {
    console.log(users);
  });
```

```
["유저1", "유저2", "유저3"]   ← 1초 후 한꺼번에 출력
```

- 하나씩 순서대로 실행하면 3초 걸리지만, `Promise.all()`은 동시에 실행하므로 **1초**면 완료

### 하나라도 실패하면?

- `Promise.all()`은 하나라도 실패하면 **전체가 실패** 처리됨

```jsx
Promise.all([
  Promise.resolve("성공1"),
  Promise.reject("실패!"),
  Promise.resolve("성공3"),
])
  .then((results) => {
    console.log(results); // 실행되지 않음
  })
  .catch((error) => {
    console.log(error); // "실패!"
  });
```

```
실패!
```