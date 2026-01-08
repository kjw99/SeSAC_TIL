# 각종 기본적인 문법
* print()
* 출력문. 기본은 줄넘김이 되어 있고 속성을 통해 추가적인 설정이 가능함.
* print(val, sep = "", end = "")
* sep는 print(값1, 값2) 이렇게 print에서 값을 여러개 한 번에 출력할 때 각 값 사이에 띄어쓰기나 다른 값이나 원하는 것을 설정.
* end는 print()가 끝날 때 줄넘김 이외에 다른걸 하고 싶을 때 설정
```
print("a", "b")
print("c", "d")
# a b
# c d

print("a", "b", sep="/", end=" ")
print("c", "d", sep="/", end=" ")
#a/b c/d
```
* 이런식으로 나오게 됨.
---
* 변수 사용법
```
value = "asd"
num1 = 1
num2 = 3
print(value)
print(num1 + num2)
```
---
* 각종 자료형
* 숫자형 : 정수, 실수와 같은 숫자. +, - 등 연산 가능
* 문자열 : 텍스트 형태. 큰 따옴표 또는 작은 따옴표로 감싸서 사용.
* 불리언(boolean) : True, False 값만 있는 자료형
* 리스트(List) : 다수의 데이터 저장에 사용. 각 데이터마다 index를 통해 접근 가능. arr = [1, 2] 이런 식으로 []를 통해 정의.
* 딕셔너리(dictionary) : key : value 형태로 이루어진 자료형. dic = {'key' : value } 이런 식으로 정의.
* 리스트와 배열 모두 데이터로 다양한 형태를 넣을 수 있고, 리스트 안에 리스트, 리스트 안에 딕셔너리, 딕셔너리 안에 리스트, 딕셔너리 등 복잡하게 넣는 것도 가능!
---
* 반복문 for, while
* 반복문을 통해 문자열 "abc" 를 a, b, c 이렇게 하나 하나 빼서 사용 가능
```
names = ['a', 'b', 'c']
for name in names:
	print(name)
	
for num in range(10): # 0 ~ 9 출력
	print(num)
	
print(list(range(3, 11, 2))) # 3 5 7 9
```
* 위 코드처럼 기본적으로 for OO in OO: 이렇게 시작하고 들여쓰기를 통해 for 문에서 실행할 코드를 입력함.
* 데이터들을 하나씩 가져와서 반복할 수도 있고, range() 함수를 통해 0 ~ n까지 반복할 수도 있다.
* range(start, end, step) 함수는 인자를 3개 받을 수 있는데, 1개만 쓰면 0부터 n까지가 된다.
* range() 함수는 연속된 정수의 수열을 생성해주는 함수.
* len() 함수는 문자열 길이를 반환하는 함수인데, 이걸 같이 사용하면 문자열 길이만큼 반복하는 식으로 구현 가능.
- while 반복문 설명
    - 계속 조건식을 체크하면서 실행하니까 조건식에 변수를 사용. 실행문에선 조건이 false로 바뀔 수 있도록 종료 시기를 정해두며 사용하기.
    - i < len(배열) 뭐 이런식으로.. len은 해당 요소의 길이. 배열은 배열 길이, 문자열은 문자열 등 다 가능
    
    ```python
    while 조건식:
    	실행문
    
    while True:
    	실행문
    	if 조건:
    		break
    ```
* break는 해당 반복을 종료한다는 뜻. continue는 다음 반복 사이클로 넘어가라는 뜻.
---
- list 잘라서 새로운 list 만들기
    - 인덱스를 활용한 list 사용법
    - 인덱스 생략 = 전체
    - 앞의 생략 = 처음부터
    - 뒤의 생략 = 끝까지
    - [:5] 이런 경우는 a부터 e까지.
    - [-1] 이런 경우는 뒤에서 1칸. 즉 e가 나옴
    
    ```python
    lst = ['a', 'b', 'c', 'd', 'e']
    print(lst[2:5]) # c d e 출력
    print(lst[::2]) # a c e 출력. 처음부터 2칸씩 띄어서 라는 뜻.
    print(lst[::-1]) # e d c b a 출력. -1 이면 반대로.
    ```
- in 연산자
    - list에 값이 들어있는지 확인할 수 있는 연산자.
    
    ```python
    print(1 in [1, 2, 3]) # true
    print(10 in [1, 2, 3]) # false
    ```
- 함수, 메서드 설명
    - list의 함수들
    - append(값) : 리스트에 값 추가.
    - pop() : 리스트 뒷 부분 제거. 변수에 저장 가능. 인덱스 지정해서 특정 위치 값 제거 가능
    
    ```python
    lst = ['a', 'b', 'c', 'd', 'e']
    lst.append('g')
    print(lst) # a b c d e g
    lst.pop() # a b c d e
    lst.pop(2) # a b d e
    ```
- 리스트 컴프리헨션
    - 리스트를 간편하게 만드는 방법. (규칙에 따라서)
    - 빈 리스트에 for문을 사용해서 값 추가하는 방식
    - lst = [num for num in range(1, 7)] 이렇게 해서 만들기도 가능.
        - num은 append에서 사용한 변수명. for 조건에 따라 배열 값 생성.
    - lst = [num for num in range(1, 20) if num % 2 == 0] 이렇게 하면 for문과 if문을 사용해 만든 것과 동일하게 생성.
        - 앞의 num 부분에 num * 2 + 1 이런식으로 변주를 주는 것도 가능.
    
    ```python
    lst = []
    
    #for num in range(1, 7):
    #    lst.append(num)
    
    lst = [num for num in range(1, 7)] # 위랑 아래랑 같은 동작
    
    lst = [num for num in range(1, 20) if num % 2 == 0] # 이런식으로 for문 if문 같이도 가능
    
    print(lst)
    
    ```
- insert() 원하는 위치에 값 넣기.
    - insert(index, 값) : 원하는 index 위치에 값을 넣는다.
    
    ```python
    numbers = [1, 2, 3, 4]
    numbers.insert(1, 5)
    
    print(numbers) # 1 5 2 3 4
    ```
- extend() 리스트 끝부분에 새로운 리스트를 이어 붙임. 리스트 합칠 때 사용
    - append랑 차이점은 extend는 기존 리스트의 뒤에 추가한다면 append는 리스트 자체를 통째로 붙인다는 점.
    
    ```python
    numbers = [1, 2, 3, 4]
    
    numbers.extend([7, 8, 9]) # 1 2 3 4 7 8 9
    #numbers.append([7, 8, 9]) # 1 2 3 4 [7 8 9]
    
    print(numbers)
    ```
- remove() 리스트에서 해당 원소 삭제. 중복 시 가장 앞에 원소 삭제.

```python
numbers = [1, 2, 1, 2]
numbers.remove(2)

print(numbers) # 1 1 2
```
- count() : 리스트에서 특정 요소의 개수를 반환. count(2)는 리스트에 2라는 값이 몇개 있는지 반환
- index() : 리스트에서 해당 요소가 몇 번 인덱스에 있는지 반환. 같은 값이 여러개 있으면 가장 앞에 있는 인덱스 반환함
- sort() : 리스트 정렬. 속성으로 reverse=True 지정하면 역 정렬
- reverse() : 리스트 뒤집기
- 리스트 연산
    - 덧셈 : a = [1, 2] b = [3, 4] 일때 a + b 하면 1 2 3 4 가 된다.
    - 곱셈 : a = [1, 2] b = a * 3 ⇒ 1 2 1 2 1 2 이렇게 됨.