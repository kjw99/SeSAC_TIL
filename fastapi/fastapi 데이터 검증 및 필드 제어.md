## 간단한 Validation

pydantic이 데이터의 형식을 강제하지만, 현재 코드에서는 다음과 같이 빈 문자열이 올수도 있다.

![image.png](attachment:fb96f4c6-de59-4190-a383-359ba316439e:image.png)

### Validation

데이터의 유효성을 검사하는 과정이며, 잘못된 데이터가 시스템에 유입되는 것을 방지한다.

```python
# post_api.py 

from fastapi import APIRouter, HTTPException, status

@router.post("")
def create_post(post_data: PostCreate):
    global post_id
    post_id += 1

    if post_data.title == "":
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "title을 입력하세요")

    if post_data.content == "":
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "content를 입력하세요")

    # 모델 데이터를 기반으로 저장용 데이터 생성
    new_post = Post(post_id, post_data.title, post_data.content)

    # 저장소에 추가
    posts.append(new_post)

    return new_post
```

- 수정 로직의 경우에도 같은 로직이 필요하다.
    
    ```python
    # post_api.py 
    
    @router.put("/{id}")
    def update_post(id: int, updated_post: PostCreate):
    
        if updated_post.title == "":
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "title을 입력하세요")
    
        if updated_post.content == "":
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "content를 입력하세요")
    
        for post in posts:
            if post.id == id:
                # 전달받은 객체의 필드값으로 기존 데이터 갱신
                post.title = updated_post.title
                post.content = updated_post.content
                return post
                
        raise HTTPException(status_code=404, detail="수정할 대상이 없습니다.")
    
    ```
    

- 간단한 validation의 경우 pydantic에서 추가적인 작업을 통해 처리할 수 있다.

# **데이터 검증 및 필드 제어**

## Annotated

타입 힌트 시스템을 확장하여 타입에 임의의 메타데이터를 결합한다.

`Annotated[T, x]` 의 문법으로 활용하며 `T`는 실제 정적 타입, `x`는 메타데이터이다.

---

## Path & Query (매개변수 선언 도구)

Path는 경로 파라미터, Query는 쿼리 파라미터의 메타데이터를 정의할 때 사용하며 데이터를 추출하고 제약 조건을 적용한다.

메타데이터 = 데이터를 위한 데이터

- `from typing import Annotated` < import 필요. Path, Query도 쓰려면 같이 import 하자.

```python
변수명 : Annotated[타입, 도구(**옵션)] = 기본값
```

의 형태를 가지며, 기본값이 `...`인 경우 필수 매개변수가 된다.

선택적인 매개변수를 위해서는 다음과 같은 형식을 활용한다.

```python
변수명 : Annotated[타입 | None, 도구(**옵션)] = None
```

### **주요 옵션**

- alias
    
    URL이나 JSON 키 값으로 사용될 별칭이다. 파이썬 변수명으로 불가능한 이름(예: user-name)을 처리할 때 사용한다.
    
- min_length / max_length
    
    문자열의 최소/최대 길이를 제한한다.
    
- ge / gt / le / lt
    
    숫자의 수치 범위(크기)를 제한한다.
    
- pattern
    
    정규 표현식을 사용하여 문자열의 특정 형식을 강제한다.
    
- title / description
    
    자동 생성되는 Swagger UI 문서에 표시될 이름과 상세 설명이다.
    

```python
@router.get("/items/{item_id}")
def get_items(
    # 1. Path: 정수형, 1 이상, 설명 추가
    item_id: Annotated[int, Path(ge=1, description="아이템 고유 번호")],
    
    # 2. Query: 필수값(...), 최소 2자, 최대 10자, 별칭 사용
    # URL: ?search-keyword=apple
    q: Annotated[str, Query(min_length=2, max_length=10, alias="search-keyword")] = ...,
    
    # 3. Query: 선택값(None), 기본값 1, 최대 100
    size: Annotated[int, Query(le=100)] = 1
):
    return {"item_id": item_id, "keyword": q, "size": size}
```

## Pydantic Field

모델 클래스 내부에서 필드별 검증, 직렬화, 문서화 설정을 정의한다. Query, Path와 유사한 검증 옵션을 공유한다.

Field의 첫 매개변수 자리에 `...`을 명시하면 필수로 입력받아야 한다.

```python
from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    # 1. 필수값, 별칭(prod_name), 길이 제한, 예시 데이터
    name: str = Field(
        ..., 
        alias="prod_name", 
        min_length=2, 
        max_length=100,
        examples=["유기농 귀리 우유 1L"]
    )
    
    # 2. 숫자 범위 제한 (가격: 0원 이상, 1,000,000원 이하)
    price: int = Field(
        ...,
        ge=0,
        le=1000000,
        description="상품의 판매 가격 (원 단위)",
        examples=[15000]
    )
    
    # 3. 기본값 설정 및 문서용 설명 (상태 코드)
    # gt(Greater Than): 0보다 커야 함 (최소 수량 1개)
    stock: int = Field(
        default=10,
        gt=0,
        description="현재 재고 수량"
    )

    # 4. 문자열 패턴 제한 (예: 상품 코드 형식 PRD-0000)
    category: str = Field(
        default="ETC",
        max_length=20,
        description="상품 카테고리 (FOOD, TECH, LIFE 등)"
    )
```

---

## Pydantic field_validator

특정 필드에 대해 사용자 정의 로직을 실행하는 데코레이터이다. 기본 타입 검증이 완료된 후 호출되는 'after' 모드가 기본값이다.
반드시 classmethod여야 하며, 검증을 통과한 값(또는 가공된 값)을 반드시 return 해야 한다. 실패 시 ValueError 등을 발생시켜 422 에러를 유도한다.

### 주요 인자

- **v**
    
    현재 검증하고 있는 해당 필드의 값이다.
    
- **info**
    
    검증 맥락을 담고 있다. info.data를 통해 **이미 검증이 완료된 다른 필드**의 값에 접근할 수 있어, 필드 간 비교 검증 시 필수적으로 사용된다.
    

- 단일 필드 검증
    
    비즈니스 로직에 따라 특정 문자열 포함 여부나 형식을 검증한다.
    
    ```python
    from pydantic import BaseModel, field_validator
    
    class TransferCreate(BaseModel):
        amount: int
        account_number: str
    
        @field_validator('amount')
        @classmethod
        def validate_amount_unit(cls, v: int) -> int:
            if v % 100 != 0:
                raise ValueError("이체 금액은 100원 단위로 입력해야 합니다.")
            return v
    
        @field_validator('account_number')
        @classmethod
        def validate_account_format(cls, v: str) -> str:
            if "-" not in v:
                raise ValueError("계좌번호는 하이픈(-)을 포함해야 합니다.")
            return v
    ```
    

- 필드 간 비교 검증
    
    비밀번호 확인이나 이메일 중복 확인처럼 두 필드의 값이 일치해야 하는 경우에 사용한다.
    
    ```python
    from pydantic import BaseModel, field_validator, ValidationInfo
    
    class Signup(BaseModel):
        email: str
        confirm_email: str
    
        @field_validator('confirm_email')
        @classmethod
        def check_emails_match(cls, v: str, info: ValidationInfo) -> str:
            # info.data를 통해 먼저 검증된 'email' 필드 값에 접근
            if 'email' in info.data and v != info.data['email']:
                raise ValueError("이메일이 일치하지 않는다.")
            return v
    ```
    

---

## Response Model

- 기존 방식
    
    리턴 타입과 response model이 정확히 같지 않아도 동작한다.
    
    ```python
    @router.get("/posts", response_model=list[PostResponse])
    def get_posts():
        # FastAPI는 리턴 타입 힌트를 보고 자동으로 response_model을 설정한다.
        return post_service.get_all_posts()
    
    ```
    

- 리턴 타입 힌트 활용
    
    함수의 파라미터에 대한 타입 힌트와 같은 방식으로 리턴 타입 힌트를 활용하면 response_model과 같은 기능을 한다.
    
    리턴 타입과 response model이 정확히 같아야 한다.
    

```python
@router.get("/posts")
def get_posts() -> list[PostResponse]:
    # FastAPI는 리턴 타입 힌트를 보고 자동으로 response_model을 설정한다.
    return post_service.get_all_posts()
```