## 박스 모델(Box Model)

- 브라우저가 요소의 너비와 높이를 계산할 때 사용하는 기준
    
    ![출처 : https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_box_model](https://prod-files-secure.s3.us-west-2.amazonaws.com/f2678325-6f7b-4a25-b188-86c42030d6d5/462ac5b5-efac-4363-b147-63c126197556/image.png)
    
    출처 : https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_box_model
    

### 박스 모델 구성요소

- **콘텐츠(Content)**: 텍스트나 이미지가 들어가는 실제 내용
- **패딩(Padding)**: 콘텐츠와 테두리 사이의 공간으로, 요소 내부의 여백
- **테두리(Border)**: 요소의 가장자리를 둘러싸는 테두리로, 두께, 스타일, 색상을 설정할 수 있다.
- **마진(Margin)**: 요소 바깥의 공간으로, 다른 요소들과의 간격

### 콘텐츠(Content)

- 요소의 실제 내용을 담는 영역
- `width` 와 `height` 속성으로 크기가 제어된다

### 패딩(Padding)

- 콘텐츠와 테두리 사이의 내부 여백
- `padding` 속성을 사용해 상/하/좌/우 내부 여백을 설정할 수 있다
    
    ```html
    <div class="padding-box">패딩 박스</div>
    
    ```
    
    ```css
    .padding-box {
      width: 200px;
      height: 100px;
      color: white;
      background-color: lightgreen;
      padding: 100px 20px 30px 40px;
      /* 상, 우, 하, 좌  패딩 */
    }
    
    ```
    

### 테두리(Border)

- 요소의 가장자리를 둘러싸는 선으로, 두께, 스타일, 색상을 설정할 수 있다.
- `border` 속성을 사용해 테두리의 크기와 스타일을 제어할 수 있다
    
    ```html
    <div class="border-box"></div>
    
    ```
    
    ```css
    .border-box {
      width: 200px;
      height: 100px;
      background-color: lightyellow;
      border: 5px dotted darkblue;
      /* 테두리 두께, 스타일, 색상 */
    }
    
    ```
    

### 마진(Margin)

- 요소의 바깥쪽 공간으로, 다른 요소와의 간격을 설정한다.
- `margin` 속성을 사용해 요소 간의 상/하/좌/우 간격을 설정할 수 있다
    
    ```html
    <div class="margin-box"></div>
    <div class="margin-box"></div>
    <div class="margin-box"></div>
    <div class="margin-box"></div>
    
    ```
    
    ```css
    .margin-box {
      width: 200px;
      height: 100px;
      background-color: lightpink;
      margin: 10px 5px 50px 50px;
      /* 상, 우, 하, 좌 각각의 마진 */
    }
    
    ```
    

### Margin 중첩(Margin Collapse)

- 두 요소의 마진이 겹쳐질 때 더 큰 값이 적용된다
    
    ```html
    <div>
      <div class="box box-d"></div>
      <div class="box box-e"></div>
      <div class="box box-f"></div>
    </div>
    
    ```
    
    ```css
    .box {
      height: 80px;
    }
    
    .box-d {
      background-color: lightgreen;
      margin: 20px 0; /* 상하 20px 마진 */
    }
    
    .box-e {
      background-color: lightblue;
      margin: 40px 0; /* 상하 40px 마진 */
    }
    
    .box-f {
      background-color: lightpink;
      margin: 60px 0; /* 상하 60px 마진 */
    }
    
    ```
    

### Margin과 Padding 비교

- Margin은 다른 요소와의 여백을 설정
- Padding은 요소 내부의 여백을 설정
    
    ```html
    <div>
      <div class="box margin"></div>
      <div class="box padding"></div>
    </div>
    
    ```
    
    ```css
    .box {
      background-color: white;
      border: 3px solid lightcoral;
      border-radius: 8px;
      height: 120px;
    }
    
    .margin {
      margin: 100px;
      /* 경계선 바깥쪽에 100px 여백 */
    }
    
    .padding {
      padding: 100px;
      /* 경계선 안쪽에 100px 여백 */
    }
    
    ```
    

---

## box-sizing

- 요소의 크기를 계산할 때, 패딩과 테두리를 포함할지 여부를 결정하는 속성

### `content-box` (기본값)

- 콘텐츠 영역으로만 너비와 높이를 계산한다.

### `border-box` (선호)

- 패딩과 테두리를 포함한 영역을 너비와 높이를 계산한다
- `content-box` 보다 직관적이기 때문에 선호된다

```html
<div class="content-box">box-sizing: content-box</div>
<div class="border-box">box-sizing: border-box</div>

```

```css
.content-box {
  width: 200px;
  height: 100px;
  padding: 20px;
  border: 5px solid black;
  background-color: lightblue;
  box-sizing: content-box;
  /* 기본값: 패딩과 테두리 제외한 크기 */
  margin-bottom: 20px;
}

.border-box {
  width: 200px;
  height: 100px;
  padding: 20px;
  border: 5px solid black;
  background-color: lightgreen;
  box-sizing: border-box;
  /* 패딩과 테두리 포함한 크기 */
}

```