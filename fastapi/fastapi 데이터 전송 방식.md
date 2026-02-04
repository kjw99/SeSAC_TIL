## Query Parameter 활용

URL 뒤에 `?key=value` 형태로 전달되는 쿼리 파라미터를 활용할 수 있다.

path parameter에 명시되지 않은 함수의 입력값이 query parameter로 활용된다.

```python
@router.get("/url")
def func(key1: int, key2: str = None):
    # url?key1=value1&key2=value2로 요청이 오면 해당 값을 활용할 수 있다.
    pass
```

- query parameter를 활용한 간단한 검색기능
    - 코드를 위에서 아래로 읽어옴. 그래서 위에서 get 방식으로 {id}를 받는 게시글 조회 같은 경우에 /search 를 입력할 때 “이 search가 id값으로 입력한 건가??” 이런 식으로 구분을 못할 수가 있다.
        - 구현했던 코드는 id는 반드시 int여야 해! 라는 방식으로 구현해서 id 부분이 search 기능으로 보낼 데이터를 받으면 에러를 발생시킴.
    - 이 문제는 /search를 url로 쓰는 기능이 /{id} 이런 url을 쓰는 기능 밑에 구현되어 있기 때문에 발생한 문제.
    - 검색 기능을 위로 올려주면 문제 없이 동작함.
    - 애초에 이런 문제를 방지하려면 이렇게 기능들의 순서를 잘 조정하거나 경로 자체를 겹치지 않도록 설정해야 한다고 함.

```python
# post_api.py 수정

@router.get("/search")
def search_posts(keyword: str = None): # 기본값 None인 쿼리 파라미터
    if keyword:
        # 제목에 키워드가 포함된 글만 골라내기
        return [p for p in posts if keyword in p.title]
    return posts
```

### 클라이언트 → 서버로의 데이터 전달 방식

- Path Parameters (경로 매개변수)
    
    URL 경로의 일부로 데이터를 전달한다.주로 특정 리소스를 식별할 때(ID 등) 사용한다.
    
    ```python
    @router.get("/posts/{post_id}")
    def read_post_by_id(post_id: int):
        # /posts/1 형태의 요청에서 1을 post_id로 받음
        return {"post_id": post_id}
    ```
    

- Query Parameters (쿼리 매개변수)
    
    URL 뒤에 `?`로 시작하여 `key=value` 형태로 전달한다. 주로 **정렬, 필터링, 검색** 등 선택적인 옵션을 부여할 때 사용한다.
    
    ```python
    @router.get("/posts")
    def read_posts(limit: int = 10, skip: int = 0):
        # /posts?limit=5&skip=2 형태의 요청 처리
        return {"limit": limit, "skip": skip}
    ```
    

- Request Body (요청 본문)
    
    데이터를 JSON 형태로 본문에 담아 전달한다. 주로 데이터를 생성(POST)하거나 수정(PUT)할 때, 복잡하고 양이 많은 데이터를 보낼 때 사용한다.
    
    ```python
    from pydantic import BaseModel
    
    class PostCreate(BaseModel):
        title: str
        content: str
    
    @router.post("/posts")
    def create_post(post: PostCreate):
        # 클라이언트가 보낸 JSON 데이터를 Post 모델 객체로 받음
        return post
    ```
    

---

## Response Model (응답 모델)

- 서버가 클라이언트에게 데이터를 돌려줄 때 사용하는 필터이다.
- 동일한 데이터 모델이라도 상황(로그인, 타인 프로필 조회 등)에 따라 보여줄 정보를 다르게 설정할 수 있으며, 비밀번호, 주민번호 같은 민감한 정보를 제외하고 내보낼 수 있다.
- DB 구조가 바뀌어도 클라이언트가 받는 데이터 형식은 유지할 수 있다.
- 요청 모델(PostCreate)과 더불어 DTO(data transfer object)라고 불린다.

```python
# post.py

class PostDetailResponse(BaseModel):
    id: int
    title: str
    content: str

class PostListResponse(BaseModel):
    id: int
    title: str

```

- 각 응답에 맞는 Response Model을 사용할 수 있다.
- reponse_model에다가 list[PostListResponse] 를 입력함. 이러면 return 값인 posts를 list 형태로 반환하고, list의 값을 PostListResponse 형태인 객체들로 반환되도록 한다는 것. [ {} {} ] 이런 느낌.

```python
# post_api.py 수정

@router.get("", response_model=list[PostListResponse])
def read_posts():
    # 저장된 모든 게시글 반환
    return posts

@router.get("/{id}", response_model=PostDetailResponse)
def read_post(id: int):
    # 식별자가 일치하는 데이터를 리스트에서 탐색
    for post in posts:
        if post.id == id:
            return post
    return {"message": "데이터를 찾을 수 없습니다."}
```