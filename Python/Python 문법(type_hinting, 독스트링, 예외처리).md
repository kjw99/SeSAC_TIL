## 파이썬 type_hinting

- type_hinting
- type_hinting(형식 힌트)는 코드의 변수, 함수 매개변수, 반환값에 기대되는 데이터 형식을 명시적으로 선언하는 기능. 강제성은 없으나 정적 분석 도구와 개발 환경의 지원으로 코드의 안전성을 높임
- 변수 이름 뒤에 콜론 자료형으로 명시.
    - count: int = 10 이렇게.
- 합집합 형식 힌트
    - 하나의 변수가 여러 데이터 형식을 가질 수 있을 경우 | ( or 기호 )를 사용해서 명시함.
        - user_id: int | str
- 클래스 인스턴스 형식 지정
    - 정의된 클래스 이름도 형식 힌트로 사용 가능. user: User

## 독스트링

- 모듈, 함수, 클래스 또는 메서드 정의의 첫 번째 문장으로 작성되는 문자열
- 코드의 의도, 사용법, 매개변수 및 반환값 등을 설명하여 코드의 가독성과 유지보수성을 높이며, 주석과 달리, 파이썬 런타임에서 객체의 doc속성으로 저장되어 접근이 가능함.
- 3개의 큰 따옴표를 사용해서 표현. “”” 문자열 “””
    - Args : 매개변수에 대한 내용
    - Returns : 반환값에 대한 내용

```python
    """원공의 반지름을 입력받아 면적을 계산하여 반환함.

    Args:
        radius (float): 원의 반지름.
    Returns:
        float: 계산된 원의 면적.
    """
```

- 이걸 사용해서 AI에게 다양한 권한을 줘서 일을 시킬 수 있다고 함.
- https://google.github.io/styleguide/pyguide.html#383-functions-and-methods
    - 코딩 규칙에 대한 내용
    - 다양한 규칙이 있음!

## 예외처리

- 예외 : 프로그램 실행 중 발생하는 논리적인 오류

```python
try:
	# 예외 발생 가능성이 있는 코드
except:
	# 예외 발생 시 실행되는 코드
```

- 프로그램은 실행했을 때 직접 끄는 것이 아니라면 절대 꺼져선 안됨!
- 근데 에러가 나면 프로그램이 꺼진다. 그래서 예외 처리를 해줘야 하는 것.
- try 문에 있는 코드를 실행했는데, 에러가 나오면 프로그램이 꺼지는 것이 아니라 except 문의 코드로 이동한다!
- 특정 에러만 처리하기
    - 이런식으로 예외의 종류를 명시해서 해당 오류만 처리할 수도 있음.

```python
try:
    numbers = [1, 2, 3]
    # 인덱스 범위 초과 예외 발생
    print(numbers[5])
except IndexError:
    # 특정 예외가 발생했을 때 실행되는 블록
    print("인덱스 범위를 초과하였습니다.")
```

- 다중 예외 처리 : except를 여러개 써서 각각 다른 종류의 에러 처리도 가능.

```python
try:
    value = int("abc")
    result = 10 / 0
except ValueError:
    # 데이터 형변환 오류 시 실행
    print("형변환에 실패하였습니다.")
except ZeroDivisionError:
    # 0으로 나누기 오류 시 실행
    print("0으로 나눌 수 없습니다.")
```

- 예외 객체 참조. 에러가 나오면 해당 에러를 확인하기 위해 사용
    - as 키워드를 통해 e라는 변수에 error의 내용을 저장하고 확인.

```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    # 예외 객체를 e 변수에 할당
    print(e) # 시스템에서 전달하는 예외 메시지 출력
```

- 예외 발생 여부에 따른 추가 제어
    - else, finally를 통해 추가적인 제어 가능.
    - else는 정상적인 상황인 경우 실행.
    - finally는 에러가 나건 말건 반드시 실행.

```python
def divide_data(input_value):
    try:
        # 정수 형변환 및 나눗셈 연산
        number = int(input_value)
        calculation = 100 / number
    except ValueError:
        # 유효하지 않은 숫자 형식 입력 시 처리
        print("숫자 형태의 문자가 아닙니다.")
    except ZeroDivisionError:
        # 0 입력으로 인한 연산 불가 시 처리
        print("0으로 나눌 수 없습니다.")
    else:
        # 예외 없이 연산이 성공한 경우 결과 출력
        print(f"연산 결과는 {calculation} 입니다.")
    finally:
        # 성공 및 실패 여부와 무관하게 작업 종료 상태 출력
        print("데이터 처리를 완료했습니다.")

# 정상 실행 예시
divide_data("20")

# 예외 발생 예시
divide_data("0")
```

- 예외 강제 발생
    - raise 키워드를 통해 의도적으로 예외를 발생 시킬 수 있다. 이를 통해 프로그램의 흐름을 중단하거나 제어함.(필요한 경우에)
    - 나이의 경우 음수가 들어가선 안되니까 에러를 발생 시켜서 예외 처리를 하는 것.
    - 또한, 에러는 가장 바깥쪽에 있는 메인 로직에서 처리하는게 자연스러움. 그래서 특정 기능에서 발생한 에러를 통해 일부로 새로운 에러를 발생시키고, 메인 로직에서 처리하는 식으로 사용하기도 함.

```python
def check_age(age):
    if age < 0:
        # ValueError를 인위적으로 발생시킴
        raise ValueError("나이는 음수일 수 없습니다.")
    return age

try:
    check_age(-5)
except ValueError as e:
    # raise에 의해 발생한 예외를 처리
    print(e)
```

- 사용자 정의 예외
    - 기존 예외 클래스를 상속받아서 새로운 예외 클래스를 정의하여 사용할 수 있음.

```python
class MyCustomError(Exception):
    # 기본 Exception 클래스를 상속받아 사용자 정의 예외 생성
    def __init__(self, message):
        self.message = message

try:
    # 사용자 정의 예외 발생
    raise MyCustomError("사용자 정의 오류가 발생했습니다.")
except MyCustomError as e:
    # 생성한 예외 클래스에 대한 처리
    print(e.message)
```