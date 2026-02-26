## CSS(Cascading Style Sheets)

- 웹 페이지의 **스타일을 정의**하는 스타일 시트 언어

### HTML과 CSS

- **HTML** : 웹 페이지의 구조와 내용을 정의
- **CSS** : 웹 페이지의 스타일을 정의
    
    ```html
    <!-- HTML만 사용한 경우 -->
    <!-- 웹 페이지의 구조와 내용을 정의 -->
    <h1>웹사이트 제목</h1>
    <p>이것은 기본 텍스트입니다.</p>
    
    <!-- CSS를 적용한 경우 -->
    <!-- 웹 페이지의 디자인과 스타일을 정의 -->
    <h1 style="color: blue; font-size: 32px;">웹사이트 제목</h1>
    <p style="color: gray; font-size: 16px;">
      이것은 스타일이 적용된 텍스트입니다.
    </p>
    ```
    

---

## CSS 기본 구조

- **선택자**, **속성**, **값**으로 구성된다

```css
선택자 {
  속성: 값;
}
```

### 선택자(Selector)

- 스타일을 적용할 HTML 요소를 선택한다

```css
/* h1 태그를 선택 */
h1 {
}

/* class가 "title"인 요소를 선택 */
.title {
}

/* id가 "header"인 요소를 선택 */
#header {
}
```

### 속성(Property)과 값(Value)

- 속성 : 스타일(글자 색, 크기, 너비, 높이 등)의 종류
- 값 : 스타일의 구체적인 값

```css
p {
  color: red; /* 빨간색 */
  font-size: 16px; /* 16픽셀 크기 */
  background-color: yellow; /* 노란색 배경 */
}
```

### CSS 작성 규칙

- 속성과 값은 `:` 으로 구분한다
- 각 선언은 `;` 으로 끝낸다
- 선언들은 `{}` 로 감싼다

---

## CSS 적용 방법

### 인라인 스타일(Inline Style)

- HTML 요소의 `style` 속성에 직접 CSS를 작성하는 방법
- 해당 요소에만 스타일이 적용된다
    
    ```html
    <p style="color: blue; font-size: 20px;">
      이 텍스트는 파란색이며, 크기는 20px입니다.
    </p>
    ```
    

### 내부 스타일 시트(Internal Style Sheet)

- HTML 문서의 `<head>` 내부에 `<style>` 태그를 사용하여 CSS 코드를 작성하는 방법
    
    ```html
    <!DOCTYPE html>
    <html lang="ko">
      <head>
        <style>
          h1 {
            color: blue;
            text-align: center;
          }
    
          p {
            color: gray;
            font-size: 16px;
          }
        </style>
      </head>
      <body>
        <h1>웹사이트 제목</h1>
        <p>이것은 스타일이 적용된 문단입니다.</p>
      </body>
    </html>
    
    ```
    

### 외부 스타일 시트(External Style Sheet)

- 외부 CSS 파일을 만들어 HTML 문서에 연결하는 방법
1. 외부 CSS 파일 작성
    
    ```css
    /* styles.css 파일 */
    h1 {
      color: blue;
      text-align: center;
    }
    
    p {
      color: gray;
      font-size: 16px;
      line-height: 1.5;
    }
    
    .highlight {
      background-color: yellow;
      padding: 5px;
    }
    
    ```
    
2. HTML 문서에서 외부 CSS 불러오기
    
    ```html
    <!DOCTYPE html>
    <html lang="ko">
      <head>
        <link rel="stylesheet" href="styles.css" />
      </head>
      <body>
        <h1>웹사이트 제목</h1>
        <p>이것은 외부 CSS가 적용된 문단입니다.</p>
        <p class="highlight">이것은 강조된 문단입니다.</p>
      </body>
    </html>
    
    ```
    

---

## 브라우저 개발자 도구

- 웹 브라우저의 개발자 도구를 사용하여 CSS를 확인하고 수정할 수 있다

### 개발자 도구 열기

- **Windows/Linux** : `F12` 키 또는 `Ctrl + Shift + I`
- **Mac** : `Cmd + Option + I`
- **마우스** : 웹 페이지에서 우클릭 → "검사" 또는 "요소 검사"

### 주요 기능

**Elements(요소) 메뉴**

- HTML 구조를 확인할 수 있다
- 요소를 선택하여 해당 요소의 CSS를 확인할 수 있다

**Styles(스타일) 패널**

- 선택된 요소에 적용된 CSS 규칙을 확인할 수 있다
- 실시간으로 CSS 값을 수정하여 결과를 미리 볼 수 있다
- 체크박스를 해제하여 특정 스타일을 임시로 비활성화할 수 있다

**Computed(계산된 스타일) 패널**

- 요소에 최종적으로 적용된 모든 CSS 값을 확인할 수 있다
- 상속받은 스타일과 직접 적용된 스타일을 구분하여 볼 수 있다

## CSS 우선순위

- 요소에 2개 이상의 스타일이 적용될 때 우선순위에 따라 적용되는 스타일을 결정한다.
- 선택자의 범위가 좁을수록 우선순위가 높아진다.

### 우선순위

- **!important**: CSS 속성을 **강제로 우선시**하는 키워드. 최대한 사용하지 않는 것이 좋다.
    
    ```css
    p {
      color: blue !important;
    }
    
    ```
    
- **요소 인라인 스타일** : 요소에 직접 적용된 스타일
    
    ```html
    <p style="color: red;">p 태그 요소</p>
    
    ```
    
- **id 선택자**: 요소에 고유한 식별자를 부여하여 스타일을 적용하는 방법
    
    ```html
    <p id="bold">bold 아이디 요소</p>
    
    ```
    
    ```css
    #bold {
      color: red;
    }
    
    ```
    
- **class 선택자**: 요소에 공통적인 특성을 부여하여 스타일을 적용하는 방법
    
    ```html
    <p class="italic">italic 클래스 요소</p>
    
    ```
    
    ```css
    .italic {
      color: blue;
    }
    
    ```
    
- **tag 선택자**: 요소의 타입을 기반으로 스타일을 적용하는 방법
    
    ```html
    <p>p 태그 요소</p>
    
    ```
    
    ```css
    p {
      color: blue;
    }
    
    ```
    
- **나중에 작성된 스타일 코드**: 우선 순위가 같은 경우 나중에 작성된 스타일이 우선순위가 높다.
    
    ```css
    span {
      color: blue;
    }
    
    span {
      color: red;
    }
    
    ```
    

## 예시 코드

```html
<head>
  <style>
    p {
      color: gray;
    }
    p {
      color: red;
    }

    .my-class {
      color: blue;
    }

    #my-id {
      color: green;
    }

    .force-style {
      color: black !important;
    }
  </style>
</head>
<body>

  <p>1. 그냥 태그 (Red - gray를 덮어씀)</p>

  <p class="my-class">2. class있는 태그 (Blue)</p>

  <p id="my-id" class="my-class">3. class, id있는 태그 (Green)</p>

  <p id="my-id" class="my-class" style="color: orange;">
    4. class, id, 인라인 태그 (Orange)
  </p>

  <p id="my-id" class="my-class force-style" style="color: orange;">
    5. class, id, 인라인, !important 태그 (Black)
  </p>

</body>
```
    

## CSS 상속

- 부모 요소에 지정된 스타일 속성이 자식 요소에게 전달되는 작동 방식
- 상속되는 속성과 상속되지 않는 속성으로 구분할 수 있다

### 상속되는 속성 목록

text와 관련된 속성들은 대부분 상속된다.

- `color`: 글자 색상
- `font-family`: 글꼴 종류
- `font-size`: 글자 크기
- `line-height`: 줄 간격
- `text-align`: 텍스트 정렬
- `visibility`: 요소의 가시성
    
    ```html
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <style>
          div {
            color: green;
            font-size: 30px;
          }
        </style>
      </head>
    
      <body>
        <div>
          <p>p 태그 요소</p>
          <span>span 태그 요소</span>
        </div>
      </body>
    </html>
    
    ```
    

### 상속되지 않는 속성 목록

- `margin`: 외부 여백
- `padding`: 내부 여백
- `border`: 테두리
- `width`, `height`: 크기
- `background`: 배경

