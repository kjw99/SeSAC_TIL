# CSS 속성

## 텍스트 관련 속성

### color

- 텍스트의 색상 지정
    
    ```css
    p {
      color: blue;
    }
    
    h1 {
      color: #ff5733;
    }
    
    span {
      color: rgb(255, 99, 71);
    }
    
    ```
    

### font-size

- 텍스트의 크기 지정
    
    ```css
    p {
      font-size: 16px;
    }
    
    h1 {
      font-size: 2em;
    }
    
    span {
      font-size: 150%;
    }
    
    ```
    

### font-weight

- 텍스트의 두께(굵기) 지정
- 단어 값으로는 `normal`, `bold`, `bolder`, `lighter`가 있다
- 숫자값(100~900)도 사용 가능하다
    
    ```css
    p {
      font-weight: normal;
    }
    
    h1 {
      font-weight: bold;
    }
    
    span {
      font-weight: 700;
    }
    
    ```
    

### text-align

- 텍스트의 정렬 방식 지정
- block 요소에만 적용된다.
- 값으로는 `left`, `center`, `right`, `justify`가 있다
    
    ```css
    p {
      text-align: left;
    }
    
    h1 {
      text-align: center;
    }
    
    div {
      text-align: right;
    }
    
    ```
    

---

## 너비와 높이

### width

- 요소의 너비 지정
- 값으로는 `auto`, `px`, `%`, `em`, `rem`, `vw`, `vh` 등이 있다
    
    ```css
    div {
      width: 100px; /* 요소의 너비를 100픽셀로 설정 */
    }
    
    ```
    

### height

- 요소의 높이 지정
- 값으로는 `auto`, `px`, `%`, `em`, `rem`, `vw`, `vh` 등이 있다
    
    ```css
    div {
      height: 200px; /* 요소의 높이를 200픽셀로 설정 */
    }
    
    ```
    

### min-width 와 max-width

- 요소의 최소 너비와 최대 너비 지정
- 값으로는 `auto`, `px`, `%`, `em`, `rem`, `vw`, `vh` 등이 있다
    
    ```css
    div {
      min-width: 300px; /* 요소의 최소 너비를 300픽셀로 설정 */
    }
    
    div {
      max-width: 500px; /* 요소의 최대 너비를 500픽셀로 설정 */
    }
    
    ```
    

### min-height 와 max-height

- 요소의 최소 높이와 최대 높이 지정
- 값으로는 `auto`, `px`, `%`, `em`, `rem`, `vw`, `vh` 등이 있다
    
    ```css
    div {
      min-height: 100px; /* 요소의 최소 높이를 100픽셀로 설정 */
    }
    
    div {
      max-height: 400px; /* 요소의 최대 높이를 400픽셀로 제한 */
    }
    
    ```
    

### 상대 크기

- 너비와 높이를 상대적 크기로 지정
- 값으로는 `auto`, `px`, `%`, `em`, `rem`, `vw`, `vh` 등이 있다
    
    ```css
    div {
      width: 50vw; /* 뷰포트 너비의 50% */
    }
    
    div {
      height: 100vh; /* 뷰포트 높이의 100%, 즉 화면 전체 높이 */
    }
    
    div {
      width: 80%; /* 부모 요소 너비의 80% */
      height: 60%; /* 부모 요소 높이의 60% */
    }
    
    ```
    

---

## 배경 관련 속성

### background-color

- 요소의 배경 색상 지정
    
    ```css
    div {
      background-color: lightblue;
    }
    
    p {
      background-color: #ffebcd;
    }
    
    h1 {
      background-color: rgba(255, 99, 71, 0.5);
    }
    
    ```
    

### background-image

- 요소의 배경에 이미지 설정
    
    ```css
    div {
      background-image: url("background.jpg");
    }
    
    p {
      background-image: url("<https://example.com/image.png>");
    }
    
    h1 {
      background-image: linear-gradient(to right, red, yellow);
    }
    
    ```
    

### background-repeat

- 배경 이미지의 반복 방식 지정
- 값으로는 `repeat`, `no-repeat`, `repeat-x`, `repeat-y`가 있다
    
    ```css
    div {
      background-repeat: no-repeat; /* 배경 이미지를 반복하지 않음 */
    }
    
    p {
      background-repeat: repeat-x; /* 배경 이미지를 가로로 반복 */
    }
    
    h1 {
      background-repeat: repeat-y; /* 배경 이미지를 세로로 반복 */
    }
    
    ```
    

---

## 기타 속성

### opacity

- 요소의 투명도 설정
- 값은 0(완전 투명)에서 1(완전 불투명)까지 설정할 수 있다
    
    ```css
    div {
      opacity: 0.5; /* 요소의 투명도를 50%로 설정 */
    }
    
    p {
      opacity: 0.7; /* 요소의 투명도를 70%로 설정 */
    }
    
    img {
      opacity: 0.3; /* 요소의 투명도를 30%로 설정 */
    }
    
    ```
    

### cursor

- 요소 위에 마우스를 올렸을 때 커서 모양 지정
- 값으로는 `pointer`, `default`, `text`, `move`, `not-allowed`, `help`, `wait`, `crosshair`, 등이 있다
    
    ```css
    a {
      cursor: pointer; /* 마우스를 올렸을 때 포인터 모양으로 변경 */
    }
    
    p {
      cursor: text; /* 마우스를 올렸을 때 텍스트 모양으로 변경 */
    }
    
    div {
      cursor: move; /* 마우스를 올렸을 때 이동 모양으로 변경 */
    }
    
    ```
    

### visibility

- 요소의 가시성 설정
- 값으로는 `visible`, `hidden`, `collapse`가 있다
- 웹 페이지내에서 차지하는 공간은 유지한다.
    
    ```css
    div {
      visibility: hidden; /* 요소를 숨김 */
    }
    
    p {
      visibility: visible; /* 요소를 보임 */
    }
    
    h1 {
      visibility: collapse; /* 요소를 숨김 */
    }
    
    ```