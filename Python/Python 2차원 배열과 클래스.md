## 2차원 배열

- 2차원 배열은 이렇게 생겼다!
- mat[0]의 값은 [1, 2, 3, 4]
- mat[1]의 값은 [5, 6, 7, 8]
- mat[0][0] 의 뜻은 mat[0]에 있는 [1, 2, 3, 4] 리스트 중 [0]위치에 있는 1을 가져온다는 뜻!

```python
mat = [
    [1, 2, 3, 4],
    [5, 6, 7, 8]
]

print(mat[0][1]) # 2
```

- n * m의 2차원 배열이고, 값은 1 ~ n * m 까지 채우는 코드를 작성해보자.
- 처음엔 for문 2개를 써서 했지만, 규칙성을 찾아서 range를 활용하면 for문 1개만 있어도 됨.
- 더 압축하면 아예 1줄도 가능하다.

## 클래스

- python scope 에 대하여..
- 함수 내부에서 외부의 값에 접근이 가능함. 근데, 변경은 불가능.
    - 함수 내부에서 외부의 변수를 새롭게 지정하려고 하면 그냥 함수 내부에서 같은 이름의 변수를 새롭게 생성한 것.
    
    ```python
    def func():
        a = 5
        print(a) # 5
    a = 3
    func()
    print(a) # 3
    ```
    
- 근데 list 같은 경우는 좀 다르게 동작함. 주소값을 통해 접근하는 경우 함수 내부에서 접근해서 값을 바꾸는 방식이라 밖에서도 값이 바뀐 것이 유지됨.

```python
def func():
    lst[0] = 100
    print(lst) # 100 2 3
lst = [1, 2, 3]
func()
print(lst) # 100 2 3
```

- 위 예시는 lst의 0번 인덱스에 접근하고 값을 바꿔서 저렇게 바뀌는 것.
- 만약 lst 자체를 다시 설정하려고 하면 밖에는 영향이 없음.
    - 아래의 경우는 lst 자체를 다시 생성한 것이기 때문.

```python
def func():
    lst = [100, 2, 3]
    print(lst) # 100 2 3
lst = [1, 2, 3]
func()
print(lst) # 1 2 3
```

- 클래스 정의 및 인스턴스 생성
    - class 키워드로 선언.
    - 클래스란, 데이터와 데이터를 처리하는 메서드를 하나의 단위로 묶어 관리하는 사용자 정의 데이터 형식.
    - 클래스를 호출하여 메모리에 실제 객체를 생성하는 과정을 인스턴스화라고 하며 생성된 객체를 인스턴스라고 함.
    
    ```python
    class Person:
    	name = "홍길동"
    	age = 13
    
    p1 = Person()
    ```
    
    - 생성자 사용
    - 밑줄(_)은 각각 2개씩임. self는 java의 this처럼 사용. p1에 Person 클래스를 사용해서 객체를 만들면, self는 p1을 가리킬 것이고 p2에 쓰면 p2를 가리킨다
    - self는 반드시 필요! 입력을 받지는 않음.
    - 생성자를 통해 변수를 유동적으로 사용 가능.
        - 딱히 매개변수 없이 직접 초기 값 지정하는 것도 가능. 매개변수의 이름과 클래스의 변수이름이 같을 필요는 없음. name = name << 이거 서로 달라도 됨.
    - 클래스 안에 함수 만들어서 사용도 가능. 여기서도 self 써서 각 객체마다 다르게 사용 가능.
        - self 없으면 밖에서 호출이 안됨.
    - 모든 인스턴스가 공유하는 변수 생성 가능. 다른 함수나 생성자와 조합해서 값 변경도 가능.
    
    ```python
    class Person:
        # 클래스 변수
        # 모든 인스턴스들이 공유하는 변수
        city = "seoul"
        population = 0
    
        def __init__(self, name, age):
            # self : 아직 생성되지 않은 instance를 의미.
            # 인스턴스 변수
            self.name = name
            self.age = age
            Person.population += 1
        
        # Person이라는 인간 종이 하는 행동이 아니라
        # 개개인의 인간이 하는 행동 -> instance
        def hello(self):
            print(f"hi, {self.name}")
    
    p1 = Person("홍길동", 12)
    p2 = Person("김길동", 7)
    
    print(p1.name) # 홍길동
    print(p2.name) # 김길동
    p1.hello() # hi, 홍길동
    p2.hello() # hi, 김길동
    print(p1.population) #2
    print(p2.population) #2
    print(Person.population) # 2
    ```
    
- 매직 메서드
    - 메서드 이름 앞 뒤에 __(_ 2개)가 붙어있는 형식을 가짐.
    - 클래스 내부에 정의되어 특정 상황에서 파이썬 인터프리터에 의해 자동으로 호출됨.
    
    ```python
    class Person:
        def __init__(self, name, hobbies):
            self.name = name
            self.hobbies = hobbies
    
        def __str__(self):
            # 객체를 출력하거나 문자열로 변환할 때 반환할 값 정의
            return f"이름: {self.name}"
    
        def __len__(self):
            # len 함수 호출 시 반환할 정수 값 정의
            return len(self.hobbies)
    
    p = Person("세종대왕", ["독서", "음악", "연구"])
    # __str__ 호출 결과 출력
    print(p)
    # __len__ 호출 결과 출력
    print(len(p))
    
    ```
    
    - 원래는 len() 하면 오류가 나오는데, 매직 메서드를 통해 정의해두면 사용이 가능(len 함수를 쓰는 것 처럼 보이지만 결과는 우리가 원하는 결과로 나오게 하는 것).
    - == 이나 <, > 같은 것도 가능.
    
    ```python
    class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age
    
        def __eq__(self, other):
            # == 연산자 사용 시 실행되는 비교 논리
            return self.age == other.age
    
        def __lt__(self, other):
            # < 연산자 사용 시 실행되는 비교 논리
            return self.age < other.age
    
    p1 = Person("사용자A", 20)
    p2 = Person("사용자B", 25)
    
    # 재정의된 비교 연산 수행 및 결과 확인
    print(p1 == p2)
    print(p1 < p2)
    ```
    
    - **del** 메서드는 객체의 참조 횟수가 0이 되어 메모리에서 해제되기 직전에 호출되는 특수 메서드이다.
    - 파일 닫기나 네트워크 접속 종료와 같은 정리 작업을 수행할 때 사용한다.
    
    ```python
    class Person:
        def __init__(self, name):
            self.name = name
            print(f"{self.name} 객체가 생성되었습니다.")
    
        def __del__(self):
            # 객체가 메모리에서 해제될 때 실행되는 로직
            print(f"{self.name} 객체가 메모리에서 해제됩니다.")
    
    p = Person("이순신")
    # 명시적으로 참조를 제거하여 소멸자 호출 유도
    del p
    
    ```
    
- 데코레이터
    - 함수나 메서드의 소스 코드를 직접 수정하지 않고 기능을 추가하거나 변경하기 위해 사용하는 고차 함수
    - @ 기호를 사용. 정의된 기능을 대상 코드의 상단에 배치.
    - 기본 구조
        - 데코레이터는 함수를 매개변수로 전달 받아 내부에 새로운 함수를 정의한 뒤 이를 반환하는 구조.
        - 클래스 내부의 메서드에 적용할 경우 첫 번째 매개변수로 인스턴스 자신인 self를 전달받는 구조를 반영해야 한다.
    
    ```python
    def trace_log(func):
        # 대상 메서드를 감싸는 내부 함수 정의
        def wrapper(self, *args, **kwargs):
            # 메서드 실행 전 공통 로직 수행
            print(f"실행 기록: {func.__name__} 메서드가 호출되었습니다.")
            # 실제 메서드 실행 및 결과 저장
            result = func(self, *args, **kwargs)
            return result
        return wrapper
    
    class Person:
        def __init__(self, name):
            self.name = name
    
        @trace_log
        def walk(self):
            # 데코레이터가 적용되어 실행 시 로그가 먼저 출력됨
            print(f"{self.name}이 걷고 있습니다.")
    
    p = Person("홍길동")
    p.walk()
    ```
    
- 고차 함수
    - 고차 함수는 함수를 인자로 받거나 함수를 반환하는 함수를 정의함.
    - 함수를 매개변수로 전달받는 고차 함수
        - 특정 동작을 수행하는 함수를 인자로 받아 내부에서 실행함으로써 로직의 중복을 제거하고 확장성을 확보한다.
    - 아래의 execute_activity() 함수를 보면, person과 특정 함수를 매개변수로 받음.
    - 아래에서는 매개변수로 Person형인 p와 run, sleep 함수를 보냄.
    - run, sleep 실행 결과를 result에 저장하고 반환해서 활동기록 시작 - 종료 - run or sleep 출력 이런 흐름이 된 것.
    
    ```python
    class Person:
        def __init__(self, name):
            self.name = name
    
    def execute_activity(person, activity_func):
        # 함수를 매개변수로 받아 내부에서 실행하는 고차 함수
        print("활동 기록을 시작합니다.")
        # 전달받은 함수를 실행하고 결과 반환
        result = activity_func(person)
        print("활동 기록이 종료되었습니다.")
        return result
    
    def run(person):
        return f"{person.name}이 달립니다."
    
    def sleep(person):
        return f"{person.name}이 잠을 잡니다."
    
    p = Person("이몽룡")
    
    # 고차 함수에 서로 다른 함수를 인자로 전달
    print(execute_activity(p, run))
    print(execute_activity(p, sleep))
    ```
    
- 일급 객체
    - 파이썬의 객체들은 다 일급 객체.
    - 일급 객체는 다음 세 가지 조건을 충족하는 객체를 의미.
        - 변수나 데이터 구조에 할당할 수 있어야 한다.
        - 함수의 매개변수로 전달할 수 있어야 한다.
        - 함수의 반환값으로 사용할 수 있어야 한다.
    - 파이썬에서 함수는 일급 객체로 취급됨. 그래서 정수나 문자열과 동일하게 취급이 가능.
    - 변수 할당 및 데이터 구조 저장
        - 함수를 변수에 할당하여 호출하거나 리스트, 딕셔너리 등의 데이터 구조에 저장하여 관리할 수 있다.
        - 아래 코드를 보면, Person 클래스에 있는 speak 함수를 action 변수에 저장해둠.
        - 이후 action()을 통해 저장된 메서드가 호출됨. 여기서 중요한 점은 ()를 붙였다는 점. 그냥 action으로 호출하면 정상적인 값이 안 나옴.
        - 리스트로 저장할 때도 마찬가지. a에서도 ()를 붙인 것을 확인.
    
    ```python
    class Person:
        def __init__(self, name):
            self.name = name
    
        def speak(self):
            return f"{self.name}이 말을 합니다."
    
        def eat(self):
            return f"{self.name}이 식사를 합니다."
    
    p = Person("홍길동")
    
    # 메서드를 변수에 할당
    action = p.speak
    # 변수를 통해 메서드 호출
    print(action())
    
    # 메서드를 리스트에 저장하여 관리
    actions = [p.speak, p.eat]
    for a in actions:
        # 리스트 요소를 순회하며 실행
        print(a())
    
    ```
    
- 클래스 속성 관리
    - 데코레이터는 함수나 메서드의 동작을 수정하거나 확장하기 위해 사용하는 특수 구문이다.
    - 클래스 내부에서 속성 접근 제어와 메서드의 성격을 규정하는 데 사용된다.
    - property 접근자
        - 메서드를 호출할 때 변수처럼 접근할 수 있도록 해줌.
        - 내부 데이터를 직접 노출하지 않고 가공된 값을 반환하거나 읽기 전용 속성을 만들 때 사용
        - 아래처럼 원래 full_name()으로 해야하는데, @property 추가하면 full_name 만 해도 됨.
        
        ```python
        class Person:
            def __init__(self, first_name, last_name):
                self.first_name = first_name
                self.last_name = last_name
        
            @property
            def full_name(self):
                # 인스턴스 변수들을 조합하여 새로운 값을 반환
                return f"{self.first_name} {self.last_name}"
        
        p = Person("길동", "홍")
        # 메서드지만 괄호 없이 변수처럼 접근하여 결과 확인
        print(p.full_name)
        ```
        
    - setter 설정자
        - setter 데코레이터 인스턴스 변수에 값을 할당할 때 실행되는 로직을 정의함.
        - 데이터 할당 전 유효성 검사를 수행하여 부적절한 데이터가 저장되는 것을 방지한다.
        - _변수명 : 변수명 앞에 _ 를 쓰면, 외부에 노출하지 않겠다는 뜻.
        - p.age = 25 이런식으로 변수에 값 넣듯 가능한 이유는 setter를 설정해 뒀기 때문. setter 없으면 이렇게 못함!
        
        ```python
        class Person:
            def __init__(self, age):
                self._age = age
        
            @property
            def age(self):
                # 내부 변수 _age의 값을 반환
                return self._age
        
            @age.setter
            def age(self, value):
                # 나이가 음수인 경우 할당을 거부하는 유효성 검사 로직
                if value < 0:
                    print("나이는 음수일 수 없습니다.")
                else:
                    self._age = value
        
        p = Person(20)
        # setter 메서드가 호출되어 유효성 검사 수행
        p.age = -5
        p.age = 25
        print(p.age)
        ```
        
    - 클래스 메서드
        - classmethod 데코레이터는 인스턴스가 아닌 클래스 자체를 첫 번째 매개변수로 전달받는다.
        - 클래스 변수에 접근하거나 클래스 상태를 변경하는 로직을 구현할 때 사용한다.
        - get_population() 매개변수에 cls가 있는데, 클래스 자체를 cls라는 이름의 매개변수로 집어넣었다는 뜻. cls가 아니라 다른거여도 상관 없다.
        - 이를 활용해서 Person 클래스의 population 변수에 접근한 것.
        
        ```python
        class Person:
            population = 0
        
            def __init__(self, name):
                self.name = name
                Person.population += 1
        
            @classmethod
            def get_population(cls):
                # 매개변수 cls를 통해 클래스 변수 population에 접근
                return cls.population
        
        p1 = Person("사용자1")
        p2 = Person("사용자2")
        # 클래스 이름으로 직접 메서드 호출
        print(Person.get_population())
        ```
        
    - 정적 메서드
        - staticmethod 데코레이터는 인스턴스나 클래스에 대한 참조 없이 동작하는 메서드를 정의한다.
        - 클래스의 네임스페이스 안에 포함되어 있으나 클래스 내부 상태와 무관한 독립적인 기능을 수행한다.
        - 정적 메서드를 지정해놔서 print에서 인스턴스 생성 없이 바로 접근 가능.
        
        ```python
        class Person:
            def __init__(self, name):
                self.name = name
        
            @staticmethod
            def is_adult(age):
                # 인스턴스나 클래스 변수 사용 없이 독립적인 논리 연산 수행
                return age >= 19
        
        # 인스턴스 생성 없이 클래스 이름을 통해 호출 가능
        print(Person.is_adult(20)) # True
        print(Person.is_adult(15)) # False
        ```
        
- 파이썬 클래스 상속
    - 이미 정의된 클래스의 모든 속성과 메서드를 새로운 클래스가 물려받아 기능을 확장하거나 재사용하는 메커니즘
    - 단일 상속
        - 하나의 자식 클래스가 하나의 부모 클래스로부터 기능을 물려받는 구조.
        - 자식 클래스는 부모 클래스에 정의된 인스턴스와 변수를 자신의 것처럼 사용 가능.
            - 자식 클래스가 가지고 있는 경우 자식 클래스의 것을 사용. (메서드 오버라이딩)
        - 아래 코드에선 Person가 부모 역할, Student가 자식 역할. 상속을 받으려면 클래스 선언할 때 ( ) 안에 부모 클래스 명을 쓴다.
        
        ```python
        class Person:
            def __init__(self, name):
                # 인스턴스 변수 name 초기화
                self.name = name
        
            def walk(self):
                # 걷기 동작을 수행하는 메서드
                print(f"{self.name}이 걷습니다.")
        
        class Student(Person):
            # Person 클래스를 상속받음
            def study(self):
                # 자식 클래스 전용 메서드 정의
                print(f"{self.name}이 학습을 수행합니다.")
        
        # Student 인스턴스 생성
        s = Student("김철수")
        # 부모로부터 상속받은 메서드 호출
        s.walk()
        # 자식 클래스 고유 메서드 호출
        s.study()
        
        ```
        
    - 메서드 오버라이딩 예시
        - 부모 클래스에 정의된 메서드를 자식 클래스에서 다시 정의해서 동작을 변경하는 것.
        
        ```python
        class Person:
            def greet(self):
                # 부모 클래스의 기본 인사 동작
                print("안녕하세요.")
        
        class Employee(Person):
            def greet(self):
                # 부모의 greet 메서드를 직업 환경에 맞게 재정의
                print("안녕하십니까, 업무를 시작합니다.")
        
        # 각 클래스의 인스턴스 생성
        p = Person()
        e = Employee()
        
        # 오버라이딩에 의해 서로 다른 결과 출력
        p.greet()
        e.greet()
        ```
        
    - super 함수를 사용한 기능 확장
        - super()는 자식 클래스에서 부모 클래스의 메서드나 생성자 호출할 때 사용.
        - 부모 클래스의 로직을 유지하며 자식 클래스에서 필요한 기능을 추가할 때 사용.
        
        ```python
        class Person:
            def __init__(self, name):
                self.name = name
        
            def introduce(self):
                print(f"제 이름은 {self.name}입니다.")
        
        class Developer(Person):
            def __init__(self, name, language):
                # 부모 클래스의 생성자를 호출하여 name 초기화 로직 재사용
                super().__init__(name)
                self.language = language
        
            def introduce(self):
                # 부모 클래스의 introduce 실행 후 추가 내용 출력
                super().introduce()
                print(f"주력 언어는 {self.language}입니다.")
        
        dev = Developer("이영희", "Python")
        dev.introduce()
        ```
        
    - 다중 상속
        - 하나 이상의 부모 클래스에게 동시에 기능을 상속받는 것
        - 클래스 선언할 때 ()에서 ,(콤마)를 통해 구분하여 명시함.
        
        ```python
        class Person:
            def speak(self):
                print("사람이 말을 합니다.")
        
        class Job:
            def work(self):
                print("업무를 수행합니다.")
        
        class Professional(Person, Job):
            # Person과 Job 클래스 모두를 상속받음
            pass
        
        prof = Professional()
        # 두 부모 클래스의 모든 메서드 사용 가능
        prof.speak()
        prof.work()
        ```
        
    - 다중 상속의 메서드 결정 순서
        - 다중 상속의 경우 메서드의 이름이 같은 경우가 많은데, 이럴 때 메서드를 검색하고 실행하는 우선순위를 의미함.
        
        ```python
        class A:
            def action(self):
                print("A의 동작")
        
        class B(A):
            def action(self):
                print("B의 동작")
        
        class C(A):
            def action(self):
                print("C의 동작")
        
        class D(B, C):
            # 다중 상속 구조
            pass
        
        d = D()
        # MRO 순서에 따라 B의 action이 호출됨
        d.action()
        # 검색 순서 출력 (D -> B -> C -> A -> object)
        print(D.mro())
        ```
        
- 클래스 다형성
    - 다형성은 상속 관계에 있는 여러 클래스들이 동일한 이름의 메서드를 공유하면서도 각자의 목적에 맞게 서로 다른 동작을 수행하는 성질.
    - 동일한 인터페이스를 통해 다양한 형태의 객체를 일관된 방식으로 제어할 수 있게 하여 코드의 유연성을 확보한다.
    - 메서드 오버라이딩을 통한 다형성 구현
        - 부모 클래스에 정의된 공통 메서드를 자식 클래스에서 재정의함으로써 다형성을 구현한다.
        - 호출하는 측에서는 객체의 구체적인 형식을 확인하지 않고 공통 메서드만 호출하여 결과를 도출한다.
        
        ```python
        class Person:
            def __init__(self, name):
                self.name = name
        
            def perform_role(self):
                # 자식 클래스에서 재정의할 공통 메서드 정의
                pass
        
        class Student(Person):
            def perform_role(self):
                # Student 클래스의 특성에 맞게 메서드 재정의
                return f"학생 {self.name}은 학습을 수행합니다."
        
        class Teacher(Person):
            def perform_role(self):
                # Teacher 클래스의 특성에 맞게 메서드 재정의
                return f"교사 {self.name}은 강의를 수행합니다."
        
        # 서로 다른 자식 클래스의 인스턴스들을 하나의 리스트로 관리
        people = [Student("김철수"), Teacher("이영희"), Student("박지민")]
        
        for person in people:
            # 각 인스턴스의 실제 형식에 따라 재정의된 메서드가 동적으로 호출됨
            print(person.perform_role())
        ```
        
    - 추상 클래스와 다형성
        - 추상 클래스를 사용하여 하위 클래스가 반드시 구현해야 할 메서드 규격을 강제함으로써 다형성의 구조적 무결성을 보장한다.
        
        ```python
        from abc import ABC, abstractmethod
        
        class Person(ABC):
            @abstractmethod
            def work(self):
                # 자식 클래스에서 반드시 구현해야 하는 추상 메서드
                pass
        
        class Student(Person):
            def work(self):
                # 추상 메서드 구체화
                print("학습을 진행합니다.")
        
        class Teacher(Person):
            def work(self):
                # 추상 메서드 구체화
                print("강의를 진행합니다.")
        
        s = Student()
        t = Teacher()
        s.work()
        t.work()
        ```
        
- 클래스 Composition
    - has a 관계
    - Composition을 활용한 기능 확장
        - Composition은 부분-전체 관계를 형성하여 객체의 복합적인 기능을 구성한다.
        - 하위 클래스에 기능을 직접 상속하는 방식 대신, 필요한 기능을 가진 객체를 속성으로 포함시켜 런타임에 동작을 결정하거나 변경할 수 있는 유연성을 제공한다.
        - 클래스 내에 다른 클래스의 인스턴스를 만들고 활용하는 느낌.
        - 필요한 경우 인스턴스 값을 변경해서 사용할 수도 있음. (아래 10000 짜리)
        
        ```python
        class Engine:
            def __init__(self, horsepower):
                self.horsepower = horsepower
        
            def start(self):
                # 엔진 시동 로직 구현
                return f"{self.horsepower}마력 엔진이 가동됩니다."
        
        class Car:
            def __init__(self, model, horsepower):
                self.model = model
                # 외부 클래스의 인스턴스를 내부 속성으로 포함 (합성)
                self.engine = Engine(horsepower)
        
            def drive(self):
                # 포함된 객체의 기능을 활용하여 상위 기능을 수행
                engine_status = self.engine.start()
                return f"{self.model} 모델이 {engine_status} 주행을 시작합니다."
        
        # Car 객체가 생성될 때 Engine 객체의 생명 주기가 결정됨
        my_car = Car("전기차", 300)
        my_engine = Engine(10000)
        my_car.engine = my_engine
        print(my_car.drive())
        ```
        
    - composition에서의 동적 교체
        - 포함되는 객체를 외부에서 주입받는 방식으로 설계하면, 코드의 수정 없이도 내부 부품 객체를 동적으로 교체하여 기능을 변경할 수 있다.
        
        ```python
        class Logger:
            def log(self, message):
                # 기본 로그 출력 방식 정의
                print(f"[시스템 로그]: {message}")
        
        class AdvancedLogger:
            def log(self, message):
                # 확장된 로그 출력 방식 정의
                print(f"--- [상세 분석 로그] --- \\n시간: 2024-05-20 \\n내용: {message}")
        
        class Service:
            def __init__(self, logger):
                # 실행 시점에 사용할 로거 객체를 외부에서 주입받음
                self.logger = logger
        
            def perform_action(self):
                # 주입된 객체에 따라 서로 다른 로그 출력 동작 수행
                self.logger.log("작업이 완료되었습니다.")
        
        # 서로 다른 기능을 가진 객체를 각각 주입하여 동작 확인
        standard_service = Service(Logger())
        advanced_service = Service(AdvancedLogger())
        
        standard_service.perform_action()
        advanced_service.perform_action()
        ```
        