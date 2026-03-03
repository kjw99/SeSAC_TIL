# 집합(Set)

- 중복되지 않는 값(value)들의 집합
- 데이터 중복 저장을 허용하지 않음

## 집합 기본 조작

### 집합 생성

**`new Set()`**

- 집합 생성자 함수에 배열을 인자로 전달하여 생성

**예시**

```jsx
let array = [1, 2, 2, 3];
let set = new Set(array);
console.log(set); // Set { 1, 2, 3 }

```

### 집합 크기

**`size`**

- 집합의 원소 개수를 반환

```jsx
let set = new Set([1, 2, 2, 3]);
console.log(set.size); // 3

```

### 집합 메서드

**`add(x)`**

- 집합에 새로운 데이터 추가

```jsx
let set = new Set([1, 2, 2, 3]);

set.add(4);
set.add(3);
console.log(set); // Set(4) { 1, 2, 3, 4 }

```

**`has(x)`**

- 집합에 특정 데이터 존재 여부 확인

```jsx
let set = new Set([1, 2, 2, 3]);

console.log(set.has(2)); // true
console.log(set.has(4)); // false

```

**`delete(x)`**

- 집합에서 특정 데이터 제거

```jsx
let set = new Set([1, 2, 2, 3]);

set.delete(2);
console.log(set); // Set(2) { 1, 3 }

set.delete(2); // 오류 미발생

```

**`clear()`**

- 집합의 모든 원소 제거

```jsx
let set = new Set([1, 2, 2, 3]);
set.clear();
console.log(set); // Set(0) {}

```

# 맵(Map)

- 키(key)와 값(value)의 쌍으로 이루어진 컬렉션
- 일반 객체와 달리 키에 다양한 자료형(객체, 함수 등)을 사용할 수 있음
- 데이터가 삽입된 순서대로 순회함

## 맵 기본 조작

### 맵 생성

**`new Map()`**

- `[키, 값]` 형태의 배열을 인자로 전달하여 생성

```jsx
let array = [['name', '홍길동'], ['age', 30]];
let map = new Map(array);
console.log(map); // Map(2) { 'name' => '홍길동', 'age' => 30 }
```

### 맵 크기

**`size`**

- 맵에 저장된 요소의 개수를 반환

```jsx
let map = new Map([['a', 1], ['b', 2]]);
console.log(map.size); // 2
```

### 맵 메서드

**`set(key, value)`**

- 맵에 새로운 키와 값을 추가하거나 기존 값을 수정

```jsx
let map = new Map();

map.set('id', 1);
map.set('id', 2); // 기존 값 수정
map.set(true, 'bool'); // 불리언을 키로 사용
console.log(map); // Map(2) { 'id' => 2, true => 'bool' }
```

**`get(key)`**

- 특정 키에 해당하는 값을 반환 (키가 없으면 `undefined` 반환)

```jsx
let map = new Map([['name', '홍길동']]);

console.log(map.get('name')); // 홍길동
console.log(map.get('age')); // undefined
```

**`has(key)`**

- 맵에 특정 키가 존재하는지 여부 확인

```jsx
let map = new Map([['a', 1]]);

console.log(map.has('a')); // true
console.log(map.has('b')); // false
```

**`delete(key)`**

- 맵에서 특정 키와 그에 해당하는 값을 제거

```jsx
let map = new Map([['a', 1], ['b', 2]]);

map.delete('a');
console.log(map); // Map(1) { 'b' => 2 }

map.delete('a'); // 오류 미발생
```

**`clear()`**

- 맵의 모든 요소 제거

```jsx
let map = new Map([['a', 1], ['b', 2]]);
map.clear();
console.log(map); // Map(0) {}
```

### Object 대신 Map을 써야 하는 경우

대부분의 경우 Object를 사용해도 무방하지만, 다음과 같은 경우에는 Map을 쓴다.

- 키(Key)가 문자열이 아닐 때
    - ID가 숫자(Number)이거나, 객체(Object) 자체를 키로 써야 할 때
- 데이터의 추가·삭제가 매우 빈번할 때
    - 수천 개의 데이터를 실시간으로 넣고 빼는 작업이 반복된다면, 엔진 차원에서 최적화된 Map이 성능상 훨씬 유리하다
- 삽입 순서가 절대적으로 중요할 때
    - 데이터를 넣은 순서 그대로 화면에 렌더링해야 한다면, 순서를 완벽히 보장하는 Map을 쓰는 것이 안전하다.