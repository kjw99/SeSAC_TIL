- 딕셔너리 (Dict)
    - 키와 벨류의 쌍을 순서 없이 저장하는 컨테이너 자료형
    - key : value 형태
    - 키를 통해 데이터 접근. 리스트는 순서로 접근
    - key 부분은 기본 자료형과 변경 불가한 컨테이너만 허용.
    - value 부분은 전부 가능.
    - key는 중복이 불가. 나중에 넣은 키와 값으로 덮어씌움.
    
    ```python
    student ={"이름" : 10}
    
    empty = {}
    print(f"빈 딕셔너리: {empty}")
    
    students = {"kyle": 10, "alex": 20}
    print(f"쌍의 갯수: {len(students)}") # 2
    ```
    
    - 딕셔너리[키] = 밸류 형식 사용.
    
    ```python
    students = {}
    
    students["kyle"] = 10  # 삽입
    print(students) # {'kyle': 10}
    
    students["kyle"] = 20  # 수정
    print(students) # {'kyle': 20}
    ```
    
    - 조회 및 삭제
    - 조회는 딕셔너리명[’키값’] 형태로 하면 value 값이 나옴.
    - 삭제는 키값을 사용해서 삭제하면 된다.
    
    ```python
    students = {"kyle": 10}
    
    # 조회
    print(students["kyle"]) # 키에 대한 값이 없으면 에러!
    print(students.get("kyle")) # 키에 대한 값이 없으면 None. 두 번째 인자로 기본값 지정 가능.

    try:
        print(students["alex"]) # 존재하지 않는 키 조회 시 에러
    except KeyError as e:
        print(f"KeyError: {e}")
    
    # 삭제
    del students["kyle"]
    print(f"삭제 후: {students}")
    ```
    
    - 딕셔너리 멤버십 연산
    - 해당 딕셔너리에 키값이 있는지 확인.
    
    ```python
    students = {"kyle": 10, "alex": 20}
    
    print("kyle" in students)      # True
    print("justin" in students)    # False
    print("justin" not in students) # True
    ```
    
    - 딕셔너리 메서드
        - keys(), values(), items()
        - 각각 딕셔너리의 키값을 가져오고, 밸류값을 가져오고, 둘 다 가져오는 메서드
        
        ```python
        students = {"kyle": 10, "alex": 20}
        
        print(students.keys()) # dict_keys(['kyle', 'alex'])
        print(students.values()) # dict_values([10, 20])
        print(students.items()) # dict_items([('kyle', 10), ('alex', 20)])
        
        print("\n--- 반복문 활용 ---")
        # 키 반복 (기본값)
        for name in students:
            print(f"Key: {name}") 
            # Key: kyle
            # Key: alex
        
        # 밸류 반복
        for age in students.values():
            print(f"Value: {age}")
            # Value: 10
            # Value: 20
        
        # 키와 밸류 동시 반복
        for name, age in students.items():
            print(f"{name}의 나이는 {age}")
            # kyle의 나이는 10
            # alex의 나이는 20
        ```
        
        - get(”key”) : key에 대칭되는 밸류값을 가져옴. 없으면 None 또는 지정된 기본값 반환
        
        ```python
        students = {"kyle": 10}
        
        print(students.get("kyle")) # 10
        print(students.get("justin"))      # None (없어서 None)
        print(students.get("justin", 0))   # 0 (없으면 0으로 기본값 지정)
        ```
        
        - pop(’key’) : 해당 key와 value를 제거하고 value 반환.
        
        ```python
        students = {"kyle": 10}
        
        value = students.pop("kyle")
        
        print(f"꺼낸 값: {value}, 남은 딕셔너리: {students}") 
        # 꺼낸 값: 10, 남은 딕셔너리: {}
        
        # 키가 없는 경우 기본값 반환 설정 가능
        print(students.pop("justin", 0)) # 0
        ```
        
        - 반복문을 사용한 메서드 활용 방법
        
        ```python
        person = {
        	"name" : "홍길동",
        	'age' : 16
        }
        print(person['name']) # 홍길동
        
        # 반복문을 통해 person에 있는 key 값을 하나씩 가져오고 key 값을 사용해서 value 값 저장
        for key in person:
        	value = person[key]
        	print(key, value) 
        	# name 홍길동
        	# age 16
        
        # keys() 메서드를 이용해서 key 값을 가져오고 반복문을 통해 하나씩 사용.
        for key in person.keys():
        	value = person[key]
        	print(key, value)
        	# name 홍길동
        	# age 16
        
        print(person.keys()) # dict_keys(['name', 'age'])
        
        # values()를 사용해서 value 값만 가져오고 출력
        for value in person.values():
        	print(value)
        	# 홍길동
        	# 16
        
        # items()를 사용해서 key, value 값을 가져오고 출력
        for key, value in person.items():
        	print(key, value)
        	# name 홍길동
        	# age 16
        
        ```
        
    -
## 딕셔너리 sum(), set 사용
- python에는 sum() 함수가 있다..
- 딕셔너리의 값들을 sum()에 넣으면 반복문 없이 한번에 합치기가 가능.
- 그냥 for문으로 출력해도 되지만, format을 사용해서 출력하는 것도 가능. 변수명을 알아보기 쉽게 직관적으로 작성하자.

```python
scores = {
    "Alice": 85,
    "Bob": 92,
    "Charlie": 78,
    "David": 95,
    "Eve": 88
}

for name in scores:
    score = scores[name]
    print(f"{name} : {score}")

templates = "이름 : {name} / 점수 : {score}"

for name in scores:
    score = scores[name]
    print(templates.format(name = name, score = score))
```

- set을 통해 교집합, 차집합, 합집합 등 사용해서 데이터 뽑기도 가능.

```python
# 코드를 여기에 작성하세요
scores = {
    "Alice": 85,
    "Bob": 92,
    "Charlie": 78,
    "David": 95,
    "Eve": 88
}

top_student = []

for key in scores:
    if scores[key] >= 90:
        top_student.append(key)

print(top_student)

good_list = []
for name, score in scores.items():
    if score >= 90:
        good_list.append(name)

print(good_list)

# 차집합을 통해 90점 미만인 사람들 출력
print(set(scores.keys()) - set(good_list))
```

- pass의 기준인 80점이 변경될 수도 있음. 변수로 설정해서 관리하자.
- pass와 fail 외에 다른 값을 추가하거나 변경할 수도 있음. 그렇기에 status 변수를 생성하고 해당 변수에 상태를 저장해두고 마지막에 변경하자.
- 복잡한 코드일수록 이런 방식으로 코드를 더 친절하게 작성해야 좋음.

```python
# 코드를 여기에 작성하세요
scores = {
    "Alice": 85,
    "Bob": 92,
    "Charlie": 78,
    "David": 95,
    "Eve": 88
}

scores_pass_fail = {}
good_score = 80

for name in scores:
    status = None

    if scores[name] >= good_score:
        status = 'Pass'
    else:
        status = 'Fail'
    
    scores_pass_fail[name] = status

for name in scores_pass_fail:
    value = scores_pass_fail[name]
    print(f"{name} : {value}")

```

- 딕셔너리의 삽입은 얼핏 보면 배열에 삽입하는 것과 비슷해서 혼동이 올 수가 있음.
- 배열의 경우엔 0번방, 1번방에 값을 넣는다. 라는 느낌이면, 딕셔너리의 경우 a번 방에 값을 넣는다. name값의 방에 status를 넣는다. 이런식으로 생각하자.
- 아래의 경우 { name : status } 이런식으로 될 것.

```python
scores_pass_fail = {}
scores_pass_fail[name] = status
```