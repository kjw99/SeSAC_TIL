- 문자열이란?
    - 0개 이상의 문자를 순서 있게 저장하는 컨테이너 자료형
    - 작은 따옴표 또는 큰 따옴표를 사용해서 생성.
    - len()를 통해 문자열 길이 확인 가능.
- 문자열 연산. 덧셈과 곱셈을 활용해서 문자열 연산이 가능함.

```python
a = "asd"
b = "dfg"
c = a + b
print(c) # asddfg

hello = "안녕"
print(hello * 3) # 안녕안녕안녕
```

- 인덱스 활용.
    - 문자열[인덱스] 방식으로 접근 가능
    - 인덱스를 활용해서 특정 위치의 문자를 수정하는 것은 불가능. ex) word[1] = ‘k’ 안됨!
        - 그래서 덧셈이나 슬라이싱을 통해 수정된 것처럼 사용해야 한다.

```python
word = "python"
# word[1] = 'k' # error!
print(word[1]) # y
print(word[-1]) # n
```

- 문자열 포매팅
    - + 활용 방법, f-string 방법, .format 방법이 있음.
    - f-string의 경우는 알고리즘 및 기타 다양한 상황에 사용.
    - .format은 예전 문법이지만 prompting에 자주 사용

```python
subject = "user content"
print(subject + "가 뭘까")
print(f"{subject}가 뭘까")

# .format 활용한 문자열 포매팅
sentence = "{subject}에 대해서 자세히 알려줘".format(subject = 'user input')
print(sentence)
```

- split
    - 구분자를 기준으로 문자열 나눠서 리스트로 반환.
    
    ```python
    sentence = "hello$python$!"
    print(sentence.split("$")) # ['hello', 'python', '!']
    ```