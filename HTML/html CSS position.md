# CSS 포지션 속성

## 포지션(Position)

- 요소가 웹 페이지에서 어디에 위치할지 결정하는 속성
- 다른 요소 또는 부모 요소와의 관계를 통해 배치된다

[position - CSS | MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/position)

## 포지션 속성 종류

### static

- 기본값, 요소를 문서의 일반적인 흐름(위 -> 아래)에 따라 배치

```html
<div class="parent-box">
  <div class="box1">박스 1</div>
  <div class="box2">박스 2</div>
</div>

```

```css
.parent-box {
  width: 300px;
  background-color: lightgray;
}

.box1 {
  width: 100px;
  height: 100px;
  background-color: lightcoral;
  /* position: static은 기본값이므로 명시할 필요 없음 */
}

.box2 {
  width: 100px;
  height: 100px;
  background-color: lightgreen;
  /* 별도의 위치 지정이 없으므로 기본값인 static이 적용됨 */
}

```

### relative

- 요소를 문서 흐름 내에서 상대적으로 배치
- 원래 자리에서 지정한 좌표(`top`, `right`, `bottom`, `left`)만큼 이동
- 자리는 그대로 유지되며 주변 요소에 영향을 주지 않는다
- 이를 통해 요소의 위치를 미세하게 조정할 수 있다

```html
<div class="parent-box">
  <div class="box1 position-relative">박스 1</div>
  <div class="box2">박스 2</div>
</div>

```

```css
.parent-box {
  width: 300px;
  background-color: lightgray;
}

.position-relative {
  position: relative;
  top: 50px;
  left: 30px;
  /* 원래 위치에서 상대적(top, left)으로 이동 */
}

.box1 {
  width: 100px;
  height: 100px;
  background-color: lightcoral;
}

.box2 {
  width: 100px;
  height: 100px;
  background-color: lightgreen;
}

```

### absolute

- 요소를 조상 요소 중 포지션이 `relative`인 요소를 기준으로 배치
- 해당 요소는 문서의 일반적인 흐름에서 벗어나고, 다른 요소와 겹쳐진다
- 배치 기준점이 없는 경우, 뷰포트를 기준으로 배치

```html
<div class="parent-box">
  <div class="box1">박스 1</div>
  <div class="box2">박스 2</div>
</div>

```

```css
.parent-box {
  width: 300px;
  height: 200px;
  margin: 50px;
  background-color: lightgray;
  border: 2px solid black;
  /* 부모에 relative 적용 */
  position: relative;
}

.box1 {
  width: 100px;
  height: 100px;
  background-color: lightcoral;
  position: absolute;
  /* 부모 위치에서 상대적으로 이동 */
  top: 50px;
  left: 30px;
}

.box2 {
  width: 100px;
  height: 100px;
  background-color: lightgreen;
}

```

### fixed

- 요소를 뷰포트에 고정해서 배치
- 스크롤을 해도 요소는 고정된 위치에 남아 있으며, 문서의 흐름에 영향을 받지 않는다
- 주로 상단 고정 메뉴나 스크롤에 따라 고정된 광고 배너 등에 사용
    
    ```html
    <div class="header">고정된 헤더</div>
    <div class="content">컨텐츠</div>
    
    ```
    
    ```css
    .header {
      width: 100%;
      background-color: steelblue;
      color: white;
      text-align: center;
      /* 상단에서 5vh 위치에 고정됨 */
      position: fixed;
      top: 5vh;
    }
    
    .content {
      /* 고정된 헤더 아래의 내용이 겹치지 않도록 여백 추가 */
      background-color: lightgray;
      height: 1500px;
      /* 스크롤을 위해 긴 내용 추가 */
    }
    
    ```
    

### sticky

- `relative`와 `fixed`의 혼합된 형태로, 스크롤 위치에 따라 요소의 배치가 달라진다
- 처음에는 `relative`처럼 동작하다가, 특정 위치부터 `fixed`처럼 동작한다
- 주로 스크롤 중에 헤더나 사이드바를 고정할 때 사용

```html
<div class="head"></div>
<div class="header">스크롤하면 고정되는 헤더</div>
<div class="content">컨텐츠</div>

```

```css
.head {
  height: 500px;
  width: 100%;
  background-color: green;
}

.header {
  width: 100%;
  background-color: lightcoral;
  color: white;
  text-align: center;
  position: sticky;
  /* 스크롤 시 일정 위치에 고정됨 */
  top: 50px;
  /* top 값에 따라 고정되는 위치가 결정됨 */
}

.content {
  background-color: lightgray;
  height: 1500px;
}

```