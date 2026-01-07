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
* 딕셔너리(dictionary) : 