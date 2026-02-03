# 간단한 게시판 구현

- `id`, `제목`, `내용`을 갖는 간단한 게시글을 구현해보자.
- 게시글 구현을 위해서는
    - 게시글의 정보를 담기 위한 변수
    - 게시글을 CRUD 하기 위한 기능
    
    이 필요하다.
    

---

## 준비

`mysite` 폴더를 생성한다.

### 게시글 클래스 정의

- 데이터의 기본 단위가 되는 클래스를 작성한다.

```python
# mysite/post.py

class Post:

    def __init__(self, id, title, content):
        self.id = id
        self.title = title
        self.content = content
```

### 게시판 로직 구성

- 게시글 객체들을 저장할 리스트를 생성한다.
- 각 게시글의 고유한 식별 번호를 위한 변수를 만든다.
- FastAPI의 본체인 main.py와 분리되었으므로, Endpoint를 연결할 Router를 생성한다.
- 현재 main.py는 app을 가지고 있음. 이 app이 fastapi 본체.
- APIRouter를 통해서 여러 파일에 라우터를 생성하고 나중에 main.py에서 다 합치게 된다.
    - router에 엔드 포인트(/post)를 하나 만들어서 저장해둠.

```python
# mysite/post_api.py

from fastapi import APIRouter
from .post import Post

router = APIRouter()

# 게시글 객체들을 저장하는 리스트
posts = []
post_id = 0

@router.get("/post")
def create():
    return "post에 대한 url임"
```

### Router 연결

- post_api의 router와 app을 연결해준다.
- post_api의 위치는 mysite 폴더 안에 있기 때문에 mysite.post_api 이렇게 경로를 지정.
- router를 여러 가지 쓸 테니 as로 이름 부여.
- include_router()를 사용해서 app과 router 연결.

```python
from fastapi import FastAPI
from mysite.post_api import router as post_router

app = FastAPI()

app.include_router(post_router)
```

---

## Create - 게시글 작성

- 특정 주소로 요청을 보낼 때 새로운 게시글 객체를 생성하고 리스트에 추가한다.

```python
# mysite/post_api.py 내부에 추가

@router.get("/posts/create")
def create_post():
    # 식별자 1 증가
		global post_id 
		post_id += 1

    # 새로운 게시글 객체 생성
    post = Post(post_id , "제목", "내용")

    # 리스트에 추가
    posts.append(post)

    return post
```

---

## Read - 전체 게시글 조회

- 현재 리스트에 저장된 모든 게시글 데이터를 반환한다.
- 데이터 확인을 위해 초기화 로직을 추가할 수 있다.

```python
# mysite/post_api.py 내부에 추가

# 초기 데이터 추가를 위한 구문
posts.append(Post(1, "기본 제목", "기본 내용"))
post_id = 1

@router.get("/posts")
def read_posts():
    # 게시글 리스트 전체를 반환
    return posts

```

---

## Read - 단일 게시글 조회

- 단일 게시글을 식별하기 위한 id가 필요하다.

### 경로 매개변수(path parameter)

- 주소 경로에 변수를 포함하여 데이터를 전달하는 방식이다.
- 중괄호를 사용하여 변수명을 지정한다.

```python
# 경로 매개변수 기본 사용 예시

@router.get("/articles/{id}")
def get_article(id: int):
    # 매개변수로 전달받은 id를 활용
    return f"글 번호: {id}"

```

### 단일 게시글 조회

- 리스트를 순회하며 요청받은 식별자와 일치하는 객체를 탐색한다.

```python
# mysite/post_api.py 내부에 추가

@router.get("/posts/{id}")
def read_post_by_id(id: int):
    # 리스트 내 객체들을 하나씩 검사
    for post in posts:
        # 객체의 식별자와 입력받은 식별자가 일치하는지 확인
        if post.id == id:
            return post
    return None

```

---

## Update - 게시글 수정

- 특정 식별자의 게시글을 찾아 내부 데이터를 변경한다.

```python
# mysite/post_api.py 내부에 추가

@router.get("/posts/{id}/update")
def update_post(id: int):
    for post in posts:
        if post.id == id:
            # 객체의 속성 값 변경
            post.title = "수정된 제목"
            post.content = "수정된 내용"
            return post
    return None

```

---

### 게시글 삭제

- 특정 식별자와 일치하는 게시글을 찾아 리스트에서 제거한다.

```python
# mysite/post_api.py 내부에 추가

@router.get("/posts/{id}/delete")
def delete_post(id: int):
    # 리스트를 순회하며 인덱스(i)와 내용(post)을 함께 추출
    for i, post in enumerate(posts):
        if post.id == id:
            # 해당 인덱스의 데이터를 삭제하고 루프 종료

            return posts.pop(i)

    return "삭제 실패"

```

---

## Restful한 게시판 구현

위에 작성한 API들의 URL들은 Restful하지 않다.

Restful한 API는 자원은 URL로 표현하고, 행위는 HTTP 메서드로 표현한다.

|  | **기존** | Restful |
| --- | --- | --- |
| create | /posts/create | posts           + POST method |
| read(전체) | /posts | /posts          + GET method |
| read(전체) | /posts/{id} | /posts/{id}   + GET method |
| update | /posts/{id}/update | /posts/{id}   + PUT method
/posts/{id}   + PATCH method |
| delete | /posts/{id}/delete | /posts/{id}   + DELETE method |

- 각각의 method에 맞는 데코레이터가 다음과 같이 존재한다.
    - GET (`@app.get`)
        - 서버의 자원을 조회할 때 사용한다.
        - 데이터가 URL의 path parameter나 query parameter를 통해 전달된다.
    - POST (`@app.post`)
        - 서버에 새로운 자원을 생성할 때 사용한다.
        - 데이터가 요청 본문에 포함되어 외부로 노출되지 않는다.
    - PUT (`@app.put`)
        - 존재하는 자원을 전체적으로 수정하거나 교체할 때 사용한다.
    - PATCH (`@app.patch`)
        - 자원의 특정 부분만 수정할 때 사용한다.
    - DELETE (`@app.delete`)
        - 특정 자원을 삭제할 때 사용한다.
    
- 변경 후 코드
    
    ```python
    # mysite/post_api.py
    
    from fastapi import APIRouter
    from .post import Post
    
    router = APIRouter()
    
    # 게시글 객체들을 저장하는 리스트
    posts = []
    post_id = 0
    
    # 초기 데이터 추가를 위한 구문
    posts.append(Post(1, "기본 제목", "기본 내용"))
    post_id = 1
    
    @router.post("/posts")
    def create_post():
        # 식별자 1 증가
        Post.last_id += 1
    
        # 새로운 게시글 객체 생성
        post = Post(Post.last_id, "제목", "내용")
    
        # 리스트에 추가
        posts.append(post)
    
        return post
    
    @router.get("/posts")
    def read_posts():
        # 게시글 리스트 전체를 반환
        return posts
    
    @router.get("/posts/{id}")
    def read_post_by_id(id: int):
        # 리스트 내 객체들을 하나씩 검사
        for post in posts:
            # 객체의 식별자와 입력받은 식별자가 일치하는지 확인
            if post.id == id:
                return post
        return None
    
    @router.put("/posts/{id}")
    def update_post(id: int):
        for post in posts:
            if post.id == id:
                # 객체의 속성 값 변경
                post.title = "수정된 제목"
                post.content = "수정된 내용"
                return post
        return None
    
    @router.delete("/posts/{id}")
    def delete_post(id: int):
        # 리스트를 순회하며 인덱스(i)와 내용(post)을 함께 추출
        for i, post in enumerate(posts):
            if post.id == id:
                # 해당 인덱스의 데이터를 삭제하고 루프 종료
                posts.pop(i)
                return "삭제 완료"
    
        return "삭제 실패"
    
    ```
    

fastapi는 swagger, docs 제공이 되서 docs로 확인도 가능. 

---

### **공통 URL 경로 설정**

여러 엔드포인트에서 공통적으로 사용하는 경로를 통합하여 관리한다. 

FastAPI에서는 APIRouter 인스턴스 생성 시 경로 접두사를 설정하여 코드 중복을 제거한다. 하위 메서드에서는 공통 경로를 제외한 나머지 경로만 정의한다.

tag를 통해 swagger를 그룹화할 수 있다.

```python
router = APIRouter(prefix="접두사", tags=["그룹화"])
```

- 변경 후 코드
    
    ```python
    from fastapi import APIRouter
    from .post import Post
    
    router = APIRouter(prefix="/posts", tags=["posts"])
    
    # 게시글 객체들을 저장하는 리스트
    posts = []
    post_id = 0
    
    @router.post("")
    def create():
        # 실습을 위한 용도.
        global post_id
        post_id += 1
    
        post = Post(post_id, "제목", "내용")
        posts.append(post)
        print(posts)
        return post
    
    # 게시글 조회
    posts.append(Post(1, "기본 제목", "기본 내용"))
    post_id = 1
    
    @router.get("")
    def read_posts():
        # 게시글 리스트 전체 반환
        return posts
    
    @router.get("/{id}")
    def read_post_by_id(id: int):
        for post in posts:
            if post.id == id:
                return post
        return None
    
    @router.put("/{id}")
    def update_post(id: int):
        for post in posts:
            if post.id == id:
                # 객체의 속성 값 변경
                post.title = "수정된 제목"
                post.content = "수정된 내용"
                return post
        return None
    
    @router.delete("/{id}")
    def delete_post(id: int):
        # 리스트를 순회하며 인덱스(i)와 내용(post)을 함께 추출
        for i, post in enumerate(posts):
            if post.id == id:
                # 해당 인덱스의 데이터를 삭제하고 루프 종료
    
                return posts.pop(i)
    
        return "삭제 실패"
    ```
    
### 데이터 모델

데이터 모델은 데이터가 어떻게 구성되어야 하는지를 정의한 데이터 설계도이다. 어떤 정보가 포함되어야 하고 각 정보가 어떤 타입(숫자, 문자 등)이어야 하는지 약속하여 데이터의 형식을 통일하는 역할을 한다.

### Pydantic

Pydantic은 파이썬의 타입 힌트를 이용하여 데이터를 검증하고 설정 관리를 수행하는 라이브러리이다. 
실행 시점에 데이터 형식을 강제하며, 정의된 모델과 일치하지 않는 데이터가 입력될 경우 정해진 규칙에 따라 오류를 발생시킨다.

- 데이터 검증(Validation)
    
    들어온 값이 숫자인지, 문자열인지, 필수 값이 빠지지는 않았는지 자동으로 체크한다.
    
- 직렬화(Serialization)
    
    파이썬 객체를 JSON 형태의 텍스트로, 또는 그 반대로 아주 쉽게 변환한다.
    

### BaseModel

- BaseModel은 Pydantic에서 데이터 모델을 생성하기 위해 상속받아야 하는 클래스이다.
- 이 클래스를 상속받아 정의된 클래스는 각 필드의 데이터 형식을 선언하며, 입력된 데이터를 해당 형식에 맞게 변환하거나 검증하는 기능을 갖게 된다.
- 해당 코드에서 height 부분의 값을 “키” 이런식으로 float 외의 값으로 넣으면 에러가 나옴.
- User 클래스가 BaseModel을 상속 받아서, typehinting이 강제성을 띄게 됨. 그래서 타입이 다르게 들어오면 에러가 나오게 되는 것.
- 유저가 잘못 된 데이터를 입력하는 것을 막기 위한 것.

```python
from pydantic import BaseModel

# BaseModel을 상속받은 데이터 모델 정의
class User(BaseModel):
    # 정수형 필드 선언
    id: int
    # 문자열 필드 선언
    name: str
    # 부동 소수점 필드 선언
    height: float

# 데이터 입력 및 객체 생성
user_data = {"id": "123", "name": "이름", "height": 175.5}
user = User(**user_data)

# 출력 결과 확인
print(user.id) # 문자열 "123"이 정수 123으로 자동 변환됨
print(type(user.id)) # 데이터 형식 확인

```

### 데이터 검증 및 타입 강제 메커니즘

Pydantic은 인스턴스 생성 시점에 각 필드에 할당된 데이터 형식을 확인한다. 선언된 형식과 호환되지 않는 데이터가 입력되면 검증 오류(ValidationError)를 발생시켜 프로그램의 안정성을 확보한다.

- 에러가 나오는데 안전하다? = 개발자가 상상할 수 있는 에러가 나오기 때문!

```python
from pydantic import ValidationError

class User(BaseModel):
    # 정수형 필드 선언
    id: int
    # 문자열 필드 선언
    name: str
    # 부동 소수점 필드 선언
    height: float

try:
    # height 필드에 정수로 변환 불가능한 문자열 입력
    invalid_data = {"id": "123", "name": "이름", "height": "키"}
    invalid_user = User(**invalid_data)
    print(invalid_user)
except ValidationError as e:
    # 오류 내용 출력
    print(e.json())
    # 데이터 형식이 일치하지 않음을 알리는 로그 확인 가능

```

### 기본값 설정 및 선택적 필드

필드 정의 시 등호를 사용하여 기본값을 지정할 수 있다. 
기본값이 설정된 필드는 데이터 입력 단계에서 생략이 가능하며, 파이썬의 `|` 연산자를 통해 데이터가 없는 상태(None)를 허용할 수도 있다.

```python
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    # 기본값 0 설정
    price: int = 0
    # None 허용 및 기본값 None 설정
    description: str | None = None

# 필수 필드인 name만 입력하여 생성
p1 = Product(name="노트북")
print(p1.price) # 0 출력
print(p1.description) # None 출력
```

### 중첩된 모델 구조

하나의 데이터 모델 내부에 다른 BaseModel 클래스를 필드 형식으로 정의할 수 있다. 이는 복잡한 계층 구조를 가진 데이터를 구조화하고 하위 객체까지 일괄적으로 검증하는 데 사용된다.

```python
from pydantic import BaseModel

class Address(BaseModel):
    city: str
    zip_code: str

class Company(BaseModel):
    name: str
    # Address 모델을 필드 형식으로 사용
    address: Address

# 중첩된 형태의 데이터 입력
company_info = {
    "name": "기술연구소",
    "address": {
        "city": "서울",
        "zip_code": "12345"
    }
}

company = Company(**company_info)
# 하위 객체의 속성에 접근
print(company.address.city)

```

모델들의 리스트를 필드로 가질 수 있다.

```python
from pydantic import BaseModel

class Comment(BaseModel):
    user_id: int
    text: str

class Post(BaseModel):
    title: str
    # Comment 모델의 리스트를 필드로 가짐
    comments: list[Comment]

# 중첩된 데이터 구조 생성
post_data = {
    "title": "공지사항",
    "comments": [
        {"user_id": 10, "text": "첫 번째 댓글"},
        {"user_id": 20, "text": "두 번째 댓글"}
    ]
}

post = Post(**post_data)
print(post.comments[0].text)
```

### **모델의 직렬화**

검증이 완료된 객체를 파이썬 딕셔너리나 JSON 문자열로 변환하는 기능을 제공한다. 이는 API 응답을 생성하거나 데이터를 저장할 때 활용된다.

```python
from pydantic import BaseModel

class Member(BaseModel):
    id: int
    name: str

member = Member(id=1, name="이순신")

# 딕셔너리로 변환
member_dict = member.model_dump()
print(member_dict)

# JSON 문자열로 변환
member_json = member.model_dump_json()
print(member_json)
```

# 상호작용 가능한 게시판 구현

위에 작성한 API들은 제목이 “제목”, 내용이 “내용”인 게시글만 생성이 가능하다.

사용자에게 입력받도록 수정해보자

### HTTP Request Body

- HTTP 요청의 본문(Body)에 들어있는 데이터이다
- POST, PUT, PATCH 요청에서 주로 사용된다
- 클라이언트가 서버로 데이터를 전송할 때 사용한다

- Request Body vs Query Parameter
    - Query Parameter
        - URL: `/articles?title=제목&content=내용`
        - 주로 GET 요청에서 사용
        - URL에 데이터가 노출됨
    - Request Body
        - URL: `/articles`
        - Body: `{"title": "제목", "content": "내용"}`
        - POST, PUT, PATCH에서 사용
        - URL에 데이터가 노출되지 않음

---

## 준비

`mysite2` 폴더를 생성한다.

### **게시글 데이터 모델 정의**

게시글 데이터를 검증하고 구조화하기 위해 pydantic 모델을 도입한다. 이를 통해 클라이언트가 전송하는 요청 본문 데이터를 객체로 자동 변환하고 유효성을 검사한다.

```python
# mysite2/post.py
from pydantic import BaseModel

# 게시글 생성을 위한 데이터 모델
class PostCreate(BaseModel):
    # 게시글 제목
    title: str
    # 게시글 내용
    content: str
    
    
# 게시글 클래스
class Post:
    def __init__(self, id, title, content):
        self.id = id
        self.title = title
        self.content = content

```

### 게시판 라우터 및 데이터 저장소 설정

게시글 객체들을 관리할 리스트와 식별자 생성 로직을 포함하는 라우터를 구성한다. 경로 접두사를 사용하여 공통 경로를 관리한다.

```python
# post_api.py
from fastapi import APIRouter
from .post import PostCreate, Post

# 경로 접두사 설정
router = APIRouter(prefix="/posts-pydantic")

# 게시글 저장소 역할을 수행하는 리스트
posts = []
# 고유 식별자 생성을 위한 카운터
post_id = 0
```

### Router 연결

post_api의 router와 app을 연결해준다.

```python
from fastapi import FastAPI
from mysite2.post_api import router as pydantic_router

app = FastAPI()

app.include_router(pydantic_router)
```

---

## 게시글 생성 및 요청 본문 처리

클라이언트가 요청 본문에 담아 보낸 데이터를 PostCreate 모델로 수신한다. 함수 매개변수에 모델 타입을 명시하면 FastAPI가 자동으로 JSON 데이터를 파싱한다.

```python
# post_api.py 내부에 추가

@router.post("")
def create_post(post_data: PostCreate):
    global post_id
    post_id += 1

    # 모델 데이터를 기반으로 저장용 데이터 생성
    new_post = Post(post_id, post_data.title, post_data.content)

    
    # 저장소에 추가
    posts.append(new_post)

    return new_post
```

---

## 전체 및 단일 게시글 조회

저장소에 보관된 게시글 데이터를 조회한다. 단일 조회 시에는 경로 매개변수를 통해 특정 식별자를 전달받아 검색을 수행한다.

```python
# post_api.py 내부에 추가

@router.get("")
def read_posts():
    # 저장된 모든 게시글 반환
    return posts

@router.get("/{id}")
def read_post(id: int):
    # 식별자가 일치하는 데이터를 리스트에서 탐색
    for post in posts:
        if post.id == id:
            return post
    return {"message": "데이터를 찾을 수 없습니다."}
```

---

## 게시글 수정 및 데이터 검증

PUT 메서드를 사용하여 특정 식별자의 데이터를 교체한다. 수정할 정보 역시 PostCreate 모델을 거쳐 유효성이 검증된 후 반영된다.

```python
# post_api.py 내부에 추가

@router.put("/{id}")
def update_post(id: int, updated_post: PostCreate):
    for post in posts:
        if post.id == id:
            # 전달받은 객체의 필드값으로 기존 데이터 갱신
            post.title = updated_post.title
            post.content = updated_post.content
            return post
    return {"message": "수정할 대상이 없습니다."}
```

---

## 게시글 삭제

DELETE 메서드와 경로 매개변수를 결합하여 특정 자원을 저장소에서 제거한다.

```python
# post_api.py 내부에 추가

@router.delete("/{id}")
def delete_post(id: int):
    for index, post in enumerate(posts):
        if post.id == id:
            # 해당 인덱스의 요소를 추출하여 제거
            return posts.pop(index)
    return {"message": "삭제할 대상이 없습니다."}
```