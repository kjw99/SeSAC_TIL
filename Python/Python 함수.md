## 함수 (function)
- 재료(매개변수)를 줘서 기능을 실행시키고 결과물(반환값, 리턴값)을 받는다.
- print()의 경우!
    - 기능 : 개발자에게 보여준다
    - 입력값 : () 사이에 들어가는 것들
    - 반환값 : 없음!
- sum(), max(), min() 이런 것도 다 마찬가지. ( ) 안에 리스트를 넣으면 값 더해서 반환하고, 최대 최소 반환하고..
- 함수 생성 방법

```python
def 함수이름(매개변수, 파라미터): # 선언
	함수 기능
	return 결과물

함수이름(인자) # 호출
```

- def를 통해 함수 선언. 이후 함수명을 사용해 호출하며 사용.
- 매개변수, return 값은 없어도 됨. 없다는 것을 None 이라 표현함.
    - a = print(b) 이런식으로 리턴값이 없는 함수를 변수에 저장하려고 하면 None 값이 나옴.
    - return 생략하면 None를 return 하는 것과 같음.
- 매개변수 외에 기본값도 같이 넣어서 사용 가능. dfe addnum(a, b, c=100)
- pass = 문법적으로 빈 공간을 채우기 위한 키워드.
- list는 .sort()를 통해 정렬이 가능.
- set(), list() 를 통해 각각 set, list 형 변환 가능.
- 한 줄로 작성한 코드와 여러 줄로 작성한 코드 중에서 더 좋은 건 한 줄 짜리 코드다.
    - 성능면에서도 그렇고..
    - 단, 이 경우에는 아래에서 함수를 사용하기 때문에 좋은 코드라고 하는 것.
    - 만약 맨 아래 print 부분에 한 줄 코드로 출력하는 것은 나쁜 코드!
    - 사용자 입장에서는 코드가 어떻게 동작하는지 읽어야 하는 과정은 없는 것이 좋다. 사용자 입장에서는 함수만 호출하면 함수명을 통해 기능을 직관적으로 파악할 수 있음.
    - 반면, 한 줄이면 된다고 그냥 함수도 없이 그대로 써버리면 해석해야 한다는 이론.
    - 결국 함수란 것은 사용자 입장에서는 알 필요가 없는 기능적인 부분을 굳이 보여주지 않고 기능만 사용할 수 있도록 하기 위한 것이기도 하다.

```python
def filter_long_names(names):
    # 이렇게 작성하는 것도 좋다.
    # return [name for name in names if len(name) >= 3]
    result_names = []
    for name in names:
        if len(name) >= 3:
            result_names.append(name)
    
    return result_names

# 테스트
name_list = ["김철수", "이영희", "박씨", "최도날드"]
print(filter_long_names(name_list)) # 결과: ["김철수", "이영희", "최도날드"]

```

- 코드를 작성할 때 각 로직을 따로 작성하고 재활용 가능한 경우 함수로 뺀 다음 구현하는 것이 더 좋음. checkout_price에서는 할인율을 계산하지 않고 그냥 값만 계산한다. discount_rate에서 할인율을 계산한다. 이런식으로 각 로직마다 분리하는 것이 좋은 코드.
- 딕셔너리에서 .get()함수의 2번째 인자는 기본값 설정.

```python
def calculate_discount_rate(membership_grade):

    discount_rate_dict ={
        "GOLD" : 0.1,
        "VIP" : 0.15
    }
    discount_rate = discount_rate_dict.get(membership_grade, 0) #dict.get(key, default_value)
    
    return discount_rate

def calculate_checkout_price(cart_items, membership_grade):
    # cart_items는 {'price': 정수, 'quantity': 정수} 형태의 딕셔너리 리스트입니다.
    
    last_price = 0
    discount_rate = calculate_discount_rate(membership_grade)

    for cart_item in cart_items:
        price = cart_item["price"]
        quantity = cart_item["quantity"]
        last_price += price * quantity
    
    last_price = last_price * (1 - discount_rate)

    if last_price < 50000:
        last_price += 3000
    
    return int(last_price)

my_cart = [{"price": 25000, "quantity": 1}, {"price": 15000, "quantity": 2}]
print(calculate_checkout_price(my_cart, "GOLD")) # 결과: 52500
```
* 보통 python에서 중복 제거가 필요하면 set()을 많이 쓴다고 함.
* 이후 정렬까지 필요하면 sorted() 함수 사용하기. 반환값이 list 형태로 나옴.
* 그래서 list를 중복 제거 및 정렬하고 싶으면 set으로 바꾸고, sorted() 함수를 쓰면 된다.