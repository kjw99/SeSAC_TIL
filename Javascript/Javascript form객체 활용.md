## **FormData 객체 활용**

- 폼 내부의 입력 요소 데이터를 쉽게 추출할 수 있게 돕는 객체

```html
<!DOCTYPE html>
<html>
  <body>
    <form id="my-form">
      <label>
        이름:
        <input type="text" name="name" required />
      </label>
      <label>
        이메일:
        <input type="email" name="email" required />
      </label>
      <button type="submit">제출</button>
    </form>

    <script>
      const form = document.querySelector("#my-form");

      form.addEventListener("submit", function (event) {
        event.preventDefault();

        // FormData 생성 (이벤트가 발생한 폼 전달)
        const formData = new FormData(event.currentTarget);

        // get 메서드를 통해 name 속성값으로 데이터 추출
        console.log(formData.get("name")); // name 입력 값
        console.log(formData.get("email")); // email 입력 값
        
        // 모든 데이터를 객체 형태로 한 번에 변환
        const data = Object.fromEntries(formData.entries());
        console.log(data); // { name: "...", email: "..." }
      });
    </script>
  </body>
</html>
```

## 데이터 유효성 검사(validation)

- 사용자가 입력 요소에 작성한 값의 유효성을 검사하는 과정
    - 이메일, 비밀번호, 전화번호 등
- HTML의 기본 유효성 검사(required, pattern, min, max 등)
- 조건문과 DOM 조작을 통한 추가 유효성 검사

### HTML 태그의 기본 유효성 검사

- `type`: 입력 타입
- `min`: 최소 값
- `max`: 최대 값
- `minlength`: 최소 길이
- `maxlength`: 최대 길이
- `required`: 필수 입력 항목

**HTML 태그의 기본 유효성 검사**

```html
<!DOCTYPE html>
<html>
  <body>
    <form id="my-form">
      <label>
        이름:
        <input type="text" name="name" minlength="2" maxlength="10" required />
      </label>
      <button type="submit">제출</button>
    </form>
  </body>
</html>

```

### JavaScript의 유효성 검사

- 두 값을 비교하거나 복잡한 유효성 검사는 JavaScript를 사용하여 수행
- 에러 메세지를 표시하기 위해 DOM 조작 사용

**JavaScript의 유효성 검사**

```html
<!DOCTYPE html>
<html>
  <body>
    <form id="my-form">
      <label>
        비밀번호:
        <input type="password" name="password" required />
      </label>
      <label>
        비밀번호 확인:
        <input type="password" name="password-confirm" required />
      </label>
      <button type="submit">제출</button>
    </form>
    <script>
      const form = document.querySelector("#my-form");

      form.addEventListener("submit", function (event) {
        const formData = new FormData(event.currentTarget);
        
        const password = formData.get("password");
        const passwordConfirm = formData.get("password-confirm");

        if (password !== passwordConfirm) {
          alert("비밀번호가 일치하지 않습니다.");

          // 비밀번호가 다르면 제출 이벤트 중지
          event.preventDefault();
        } else {
          alert("비밀번호가 일치합니다.");
        }
      });
    </script>
  </body>
</html>
```

## 실시간 입력 처리

- `input` 이벤트: 사용자가 입력 요소의 값을 변경할 때마다 발생
- `change` 이벤트: 사용자가 입력 요소 값 변경 후, 포커스를 이동하거나 Enter 키를 입력하면 발생
- 두 이벤트를 사용하여 사용자 입력에 실시간으로 반응하고 데이터 유효성 검사

### `input` 이벤트와 `change` 이벤트

- `input`
    - 사용자가 입력 요소 값을 변경할 때마다 발생
    - 사용자 동작의 실시간 감지에 사용
    - 지원 태그: `<input>`, `<textarea>`, `<select>`
    - `checkbox`, `radio` 타입 미지원
- `change`
    - 사용자가 입력 완료 후, 포커스를 이동하거나 Enter 키를 입력하면 발생
    - 실시간 감지가 필요한 경우 부적합

**`input`과 `change` 이벤트 실시간 처리**

```html
<!DOCTYPE html>
<html lang="en">
  <body>
    <label for="text-input">텍스트 입력:</label>
    <input type="text" id="text-input" />
    <div class="output">
      <p>input 이벤트 : <span id="input-output"></span></p>
      <p>change 이벤트 : <span id="change-output"></span></p>
    </div>

    <script>
      const textInput = document.querySelector("#text-input");
      const inputOutput = document.querySelector("#input-output");
      const changeOutput = document.querySelector("#change-output");

      // input 이벤트: 입력 시마다 발생
      textInput.addEventListener("input", () => {
        inputOutput.textContent = textInput.value;
      });

      // change 이벤트: 입력이 완료된 후(포커스가 벗어나면) 발생
      textInput.addEventListener("change", () => {
        changeOutput.textContent = textInput.value;
      });
    </script>
  </body>
</html>
```