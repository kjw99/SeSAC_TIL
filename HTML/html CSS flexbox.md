# CSS 플렉스 박스 레이아웃

## 플렉스 박스(Flexbox)

- 웹 페이지의 유연한 레이아웃 구현
- 내부 요소 간 공간 분배와 정렬의 효율적 제어
- **플렉스 컨테이너(Flex Container)** 와 **플렉스 아이템(Flex Items)** 으로 구성

### 플렉스 박스 구성 요소

- **플렉스 컨테이너(Flex Container)**
    - 플렉스 레이아웃이 적용되는 **`부모 요소`**
    - 내부 요소를 플렉스 아이템으로 변환하는 영역
- **플렉스 아이템(Flex Items)**
    - 플렉스 컨테이너 내부의 **`자식 요소`**
    - 플렉스 박스 레이아웃에 따라 배치되는 대상

## 플렉스 컨테이너(Flex Container) 주요 속성

- `display: flex;` 속성이 적용된 요소는 플렉스 컨테이너
- 내부 요소(아이템)들의 배치 방식 정의
- **주 축(main-axis)** 과 **교차 축(cross-axis)** 기반으로 내부 요소 배치

### flex-direction

- 플렉스 아이템의 배치 방향
- `row` (기본값): 왼쪽에서 오른쪽으로 수평 배치 (주 축: 가로)
- `row-reverse`: 오른쪽에서 왼쪽으로 수평 배치 (주 축: 가로)
- `column`: 위에서 아래로 수직 배치 (주 축: 세로)
- `column-reverse`: 아래에서 위로 수직 배치 (주 축: 세로)
    
    ```html
    <div class="flex-container">
      <div class="flex-item">아이템 1</div>
      <div class="flex-item">아이템 2</div>
      <div class="flex-item">아이템 3</div>
    </div>
    
    ```
    
    ```css
    .flex-container {
      display: flex;
      flex-direction: row;
      border: 2px solid #333;
      padding: 10px;
    }
    
    .flex-item {
      padding: 20px;
      background-color: lightblue;
      margin: 5px;
    }
    
    ```
    

### justify-content

- **주 축(main-axis)** 기준 플렉스 아이템 정렬
- `flex-start`: 아이템을 시작점에 정렬
- `flex-end`: 아이템을 끝점에서 정렬
- `center`: 아이템을 가운데 정렬
- `space-between`: 아이템 사이에 동일한 간격, 양 끝에 여백 없음
- `space-around`: 아이템 주위에 동일한 간격, 양 끝에 동일한 여백 존재
    
    ```html
    <div class="flex-container">
      <div class="flex-item">아이템 1</div>
      <div class="flex-item">아이템 2</div>
      <div class="flex-item">아이템 3</div>
    </div>
    
    ```
    
    ```css
    .flex-container {
      display: flex;
      justify-content: center; /* 플렉스 아이템을 주 축에서 가운데 정렬 */
      border: 2px solid #333;
      padding: 10px;
    }
    
    .flex-item {
      padding: 20px;
      background-color: lightcoral;
      margin: 5px;
    }
    
    ```
    

### align-items

- **교차 축(cross-axis)** 기준 플렉스 아이템 정렬
- `stretch` (기본값): 아이템이 컨테이너 높이에 맞춰 늘어남
- `flex-start`: 교차 축의 시작점에서 정렬
- `flex-end`: 교차 축의 끝점에서 정렬
- `center`: 교차 축의 중앙에서 정렬
- `baseline`: 텍스트 기준선에 맞춰 정렬
    
    ```html
    <div class="flex-container">
      <div class="flex-item">아이템 1</div>
      <div class="flex-item">아이템 2</div>
      <div class="flex-item">아이템 3</div>
    </div>
    
    ```
    
    ```css
    .flex-container {
      display: flex;
      height: 200px; /* 교차 축 정렬을 확인하기 위한 높이 설정 */
      align-items: center; /* 플렉스 아이템을 교차 축에서 가운데 정렬 */
      border: 2px solid #333;
      padding: 10px;
    }
    
    .flex-item {
      padding: 20px;
      background-color: lightgreen;
      margin: 5px;
    }
    
    ```
    

### flex-wrap

- 플렉스 아이템의 줄 바꿈 처리
- `nowrap` (기본값): 줄바꿈 없음
- `wrap`: 여러 줄로 나눠 배치
- `wrap-reverse`: 역순으로 줄바꿈
    
    ```html
    <div class="flex-container">
      <div class="flex-item">아이템 1</div>
      <div class="flex-item">아이템 2</div>
      <div class="flex-item">아이템 3</div>
      <div class="flex-item">아이템 4</div>
      <div class="flex-item">아이템 5</div>
    </div>
    
    ```
    
    ```css
    .flex-container {
      display: flex;
      width: 400px; /* 컨테이너 너비 제한 */
      flex-wrap: wrap; /* 플렉스 아이템을 여러 줄로 나눠 배치 */
      border: 2px solid #333;
      padding: 10px;
    }
    
    .flex-item {
      width: 150px;
      padding: 20px;
      background-color: lightyellow;
      margin: 5px;
    }
    
    ```
    

### align-content

- `flex-wrap: wrap` 설정 시, **여러 줄**의 교차 축 정렬 방식
- 아이템들이 한 줄에 들어가지 않을 때 작동
- `align-items`는 한 줄 내에서의 아이템 정렬, `align-content`는 여러 줄 사이의 간격과 정렬을 다룸
- `stretch` (기본값): 아이템의 높이가 늘어나 교차 축을 가득 채움
- `flex-start`: 교차 축의 시작점으로 모든 줄을 정렬
- `flex-end`: 교차 축의 끝점으로 모든 줄을 정렬
- `center`: 교차 축의 중앙으로 모든 줄을 정렬
- `space-between`: 첫 줄은 시작점, 마지막 줄은 끝점에 정렬하고 나머지 줄은 균등한 간격으로 배치
- `space-around`: 모든 줄 주위에 균등한 간격으로 배치
    
    ```html
    <div class="flex-container">
      <div class="flex-item">1</div>
      <div class="flex-item">2</div>
      <div class="flex-item">3</div>
      <div class="flex-item">4</div>
      <div class="flex-item">5</div>
      <div class="flex-item">6</div>
    </div>
    
    ```
    
    ```css
    .flex-container {
      display: flex;
      flex-wrap: wrap; /* 여러 줄로 배치 */
      height: 300px; /* align-content 확인을 위한 높이 설정 */
      align-content: center; /* 여러 줄을 교차 축의 중앙에 정렬 */
      border: 2px solid #333;
      padding: 10px;
    }
    
    .flex-item {
      width: 100px;
      padding: 20px;
      background-color: lightgoldenrodyellow;
      margin: 5px;
    }
    
    ```
    

### gap

- 플렉스 아이템 간의 간격 조절
- `margin` 속성과 달리 아이템 사이의 간격만 조절
    
    ```html
    <div class="flex-container">
      <div class="flex-item">아이템 1</div>
      <div class="flex-item">아이템 2</div>
      <div class="flex-item">아이템 3</div>
    </div>
    
    ```
    
    ```css
    .flex-container {
      display: flex;
      gap: 3rem;
    }
    
    .flex-item {
      padding: 20px;
      background-color: lightcoral;
    }
    
    ```
    

---

## 플렉스 아이템(Flex Item) 주요 속성

- 플렉스 컨테이너의 자식 요소. 주어진 공간에 따라 크기를 유연하게 조정

### `align-self`

- 아이템별 교차 축 정렬 방식 지정
- 기본값은 `auto`, 속성에 값을 지정하면 컨테이너(부모 요소)의 `align-items` 속성을 덮어씀
- `flex-start`: 아이템을 교차 축의 **시작점**에 정렬
- `flex-end`: 아이템을 교차 축의 **끝점**에 정렬
- `center`: 아이템을 교차 축의 **가운데**에 정렬
- `baseline`: 아이템을 텍스트의 **기준선**에 맞춰 정렬
    
    ```html
    <div class="flex-container">
      <div class="flex-item">아이템 1</div>
      <div class="flex-item item-special">특별한 아이템</div>
      <div class="flex-item">아이템 3</div>
    </div>
    
    ```
    
    ```css
    .flex-container {
      display: flex;
      height: 200px;
      align-items: flex-start;
      border: 2px solid #333;
      padding: 10px;
    }
    
    .flex-item {
      padding: 20px;
      background-color: lightpink;
      margin: 5px;
    }
    
    .item-special {
      align-self: center; /* 이 아이템만 가운데 정렬 */
      background-color: orange;
    }
    
    ```
    

### flex-basis

- 플렉스 아이템의 **기본 크기**
- 주 축이 가로일 때는 너비, 세로일 때는 높이
    
    ```html
    <div class="flex-container">
      <div class="flex-item">기본 너비 200px</div>
      <div class="flex-item">기본 너비 200px</div>
      <div class="flex-item">기본 너비 200px</div>
    </div>
    
    ```
    
    ```css
    .flex-container {
      display: flex;
      flex-direction: row; /* 가로 배치 */
      border: 2px solid #333;
      padding: 10px;
    }
    
    .flex-item {
      flex-basis: 200px; /* 기본 너비를 200px로 설정 */
      padding: 20px;
      background-color: lightsteelblue;
      margin: 5px;
    }
    
    ```
    

### flex-grow

- 컨테이너 내 **남은 공간**에 대한 아이템의 차지 비율
- 기본값은 `0`, 값이 클수록 더 많은 공간을 차지
    
    ```html
    <div class="flex-container">
      <div class="flex-item">기본 아이템</div>
      <div class="flex-item item-grow">확장되는 아이템</div>
      <div class="flex-item">기본 아이템</div>
    </div>
    
    ```
    
    ```css
    .flex-container {
      display: flex;
      width: 600px;
      border: 2px solid #333;
      padding: 10px;
    }
    
    .flex-item {
      padding: 20px;
      background-color: lightgray;
      margin: 5px;
    }
    
    .item-grow {
      flex-grow: 2; /* 다른 아이템보다 2배 더 많은 공간을 차지 */
      background-color: lightseagreen;
    }
    
    ```
    

### flex-shrink

- 공간 부족 시 아이템의 축소 비율
- 기본값은 `1`, 0으로 설정 시 아이템 축소 안 됨
    
    ```html
    <div class="flex-container">
      <div class="flex-item">줄어드는 아이템</div>
      <div class="flex-item item-no-shrink">줄어들지 않는 아이템</div>
      <div class="flex-item">줄어드는 아이템</div>
    </div>
    
    ```
    
    ```css
    .flex-container {
      display: flex;
      width: 300px; /* 좁은 컨테이너로 shrink 효과 확인 */
      border: 2px solid #333;
      padding: 10px;
    }
    
    .flex-item {
      width: 150px;
      padding: 20px;
      background-color: lightcyan;
      margin: 5px;
      flex-shrink: 1; /* 공간이 부족할 때 줄어드는 정도 */
    }
    
    .item-no-shrink {
      flex-shrink: 0; /* 줄어들지 않음 */
      background-color: lightcoral;
    }
    
    ```
    

---

### flex (축약 속성)

- `flex-grow`, `flex-shrink`, `flex-basis`를 한 번에 지정하는 축약 속성
- `flex: <grow> <shrink> <basis>;` 순서로 값을 지정
- 가장 흔하게 사용되며, 이 속성을 이해하는 것이 중요

**주요 사용 예시**

- `flex: 1;`
    - `flex: 1 1 0;` 와 동일
    - 아이템이 컨테이너의 남은 공간을 균등하게 나눠 가짐 (가장 많이 사용되는 형태)
- `flex: auto;`
    - `flex: 1 1 auto;` 와 동일
    - 아이템의 `width`나 `height` 등 콘텐츠 크기를 기준으로 공간을 분배
- `flex: none;`
    - `flex: 0 0 auto;` 와 동일
    - 아이템의 크기가 고정되어 늘어나거나 줄어들지 않음
    
    ```html
    <div class="flex-container">
      <div class="flex-item item-1">flex: 1;</div>
      <div class="flex-item item-2">flex: 2;</div>
      <div class="flex-item item-3">flex: 1;</div>
    </div>
    
    ```
    
    ```css
    .flex-container {
      display: flex;
      width: 800px;
      border: 2px solid #333;
    }
    
    .flex-item {
      padding: 20px;
      color: white;
      text-align: center;
    }
    
    .item-1 {
      flex: 1; /* 1/4 공간 차지 */
      background-color: #60a5fa;
    }
    .item-2 {
      flex: 2; /* 2/4 공간 차지 */
      background-color: #f87171;
    }
    .item-3 {
      flex: 1; /* 1/4 공간 차지 */
      background-color: #34d399;
    }
    
    ```
    

## 연습하기

[Flexbox Froggy](https://flexboxfroggy.com/#ko)