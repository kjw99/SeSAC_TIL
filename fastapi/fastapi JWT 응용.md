# 게시글에 작성자(User) 연결하기

작성자가 있는 게시글 작성을 위해 다음과 같은 API를 만든다.

| Method | Path | 설명 | 인증 |
| --- | --- | --- | --- |
| POST | `/posts2` | 게시글 작성 | 필요 |
| GET | `/posts2` | 전체 목록 조회 | 불필요 |
| GET | `/posts2/{id}` | 상세 조회 | 불필요 |
| GET | `/posts2/user/{user_id}` | 특정 유저의 글 조회 | 불필요 |
| PUT | `/posts2/{id}` | 게시글 수정 | 필요 (본인만) |
| DELETE | `/posts2/{id}` | 게시글 삭제 | 필요 (본인만) |
| GET | `/me/posts` | 내가 쓴 글 조회 | 필요 |

---

## Post2 모델 정의

기존의 post모델은 relation, schema등 복잡하므로 새로운 모델을 만들어서 진행한다.

```python
# mysite4/models/post2.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey
from database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User

class Post2(Base):
    __tablename__ = "posts2"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # User 외래키: 작성자 정보
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    # User와의 관계 설정 (N:1)
    user: Mapped["User"] = relationship(back_populates="posts2")
```

### User 모델에 역방향 relationship 추가

```python
# mysite4/models/user.py (기존 코드에 추가)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .post2 import Post2
    
class User(Base):
    # ... 기존 필드들 ...

    # User가 작성한 Post2 목록 (1:N)
    posts2: Mapped[list["Post2"]] = relationship(back_populates="user")
```

### models/**init**.py에 등록

```python
# mysite4/models/__init__.py
from .post import Post
from .post2 import Post2  # 추가
from .comment import Comment
from .tag import Tag
from .post_tag import PostTag
from mysite4.models.user import User
from database import Base

__all__ = ["Base", "Post", "Post2", "Comment", "Tag", "PostTag", "User"]
```

---

### 스키마 작성

```python
# mysite4/schemas/post2.py
from pydantic import BaseModel, ConfigDict
from mysite4.schemas.user import UserResponse

class Post2Create(BaseModel):
    title: str
    content: str

class Post2ListResponse(BaseModel):
    id: int
    title: str
    user: UserResponse

    model_config = ConfigDict(from_attributes=True)

class Post2DetailResponse(BaseModel):
    id: int
    title: str
    content: str
    user: UserResponse

    model_config = ConfigDict(from_attributes=True)

```

---

## 게시글 작성 (Create)

### Repository

```python
# mysite4/repositories/post2_repository.py

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from mysite4.models.post2 import Post2
from mysite4.schemas.post2 import Post2Create

class Post2Repository:
    def save(self, db: Session, new_post: Post2):
        db.add(new_post)
        return new_post

post2_repository = Post2Repository()
```

### Service

```python
# mysite4/services/post2_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from mysite4.repositories.post2_repository import post2_repository
from mysite4.models.post2 import Post2
from mysite4.schemas.post2 import Post2Create
from mysite4.models.user import User

class Post2Service:
    def create_post(self, db: Session, data: Post2Create, current_user: User):
        # 로그인한 유저의 ID를 자동으로 설정한다.
        new_post = Post2(title=data.title, content=data.content, user=current_user)

        post2_repository.save(db, new_post)
        db.commit()
        db.refresh(new_post)
        return new_post

post2_service = Post2Service()
```

- db.begin()을 쓰지 않는 이유

`get_current_user`가 토큰에서 유저를 조회할 때 이미 DB 트랜잭션이 시작된다.
이 상태에서 `with db.begin()`을 쓰면 **"A transaction is already begun"** 에러가 발생한다.
따라서 이미 시작된 트랜잭션에서는 `db.commit()`으로 수동 커밋해야 한다.

```python
# (X) get_current_user 이후에는 사용 불가
with db.begin():
    post2_repository.save(db, new_post)

# (O) 이미 시작된 트랜잭션에서는 수동 commit
post2_repository.save(db, new_post)
db.commit()
```

db.commit()을 service에서 직접 명시하지 않기 위한 다른 우회적인 로직들도 존재한다.

### Router

`Depends(get_current_user)`를 통해 로그인 토큰에서 유저 정보를 자동으로 추출한다.
클라이언트는 "누가 쓴 글인지" 신경 쓸 필요가 없다.

```python
# mysite4/routers/post2_router.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from mysite4.services.post2_service import post2_service
from mysite4.schemas.post2 import Post2Create, Post2DetailResponse, Post2ListResponse
from mysite4.dependencies import get_current_user
from mysite4.models.user import User

router = APIRouter(prefix="/posts2", tags=["posts2"])

@router.post("", response_model=Post2DetailResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    data: Post2Create,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # 로그인한 유저 자동 주입
):
    return post2_service.create_post(db, data, current_user)
```

### main.py에 라우터 등록

```python
# main.py
from mysite4.routers.post2_router import router as post2_router

app.include_router(post2_router)
```

---

## 게시글 조회 (Read)

### Repository

게시글과 user를 함께 가져오기 위해 joinedload를 활용한다.

```python
# mysite4/repositories/post2_repository.py
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from mysite4.models.post2 import Post2

class Post2Repository:
    # ... save() ...

    def find_all(self, db: Session):
        return db.scalars(
            select(Post2).options(joinedload(Post2.user))
        ).all()

    def find_by_id(self, db: Session, id: int):
        return db.scalars(
            select(Post2).options(joinedload(Post2.user)).where(Post2.id == id)
        ).first()
```

### Service에 조회 메서드 추가

```python
# mysite4/services/post2_service.py (추가)

    def read_posts(self, db: Session):
        return post2_repository.find_all(db)

    def read_post_by_id(self, db: Session, id: int):
        post = post2_repository.find_by_id(db, id)
        if not post:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, "존재하지 않는 게시글입니다."
            )
        return post
```

### Router에 조회 엔드포인트 추가

```python
# mysite4/routers/post2_router.py (추가)

@router.get("", response_model=list[Post2ListResponse])
def read_posts(db: Session = Depends(get_db)):
    return post2_service.read_posts(db)

@router.get("/{id}", response_model=Post2DetailResponse)
def read_post(id: int, db: Session = Depends(get_db)):
    return post2_service.read_post_by_id(db, id)
```

---

## 게시글 수정/삭제 (Update/Delete)

### Repository

```python
# mysite4/repositories/post2_repository.py (추가)

    def update(self, db: Session, post: Post2, data: Post2Create):
        post.title = data.title
        post.content = data.content
        return post

    def delete(self, db: Session, post: Post2):
        db.delete(post)
```

### Service - Authorization 체크

- 작성자 본인만 수정/삭제 가능하도록 한다.

```python
# mysite4/services/post2_service.py (추가)

    def update_post(self, db: Session, id: int, data: Post2Create, current_user: User):
        post = self.read_post_by_id(db, id)

        # 작성자 본인만 수정 가능
        if post.user_id != current_user.id:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN, "본인의 게시글만 수정할 수 있습니다."
            )

        updated_post = post2_repository.update(db, post, data)
        db.commit()
        db.refresh(updated_post)
        return updated_post

    def delete_post(self, db: Session, id: int, current_user: User):
        post = self.read_post_by_id(db, id)

        # 작성자 본인만 삭제 가능
        if post.user_id != current_user.id:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN, "본인의 게시글만 삭제할 수 있습니다."
            )

        post2_repository.delete(db, post)
        db.commit()
```

- **인증(Authentication) vs 인가(Authorization):**

```python
# 인증: "누구인가?" → Depends(get_current_user)로 처리
current_user: User = Depends(get_current_user)

# 인가: "권한이 있는가?" → service에서 직접 체크
if post.user_id != current_user.id:
    raise HTTPException(403, "본인의 게시글만 수정할 수 있습니다.")
```

- **인증(Authentication)**: 로그인한 사용자인지 확인 → FastAPI의 `Depends`가 자동 처리
- **인가(Authorization)**: 해당 리소스에 권한이 있는지 확인 → 비즈니스 로직에서 직접 처리

### Router

```python
# mysite4/routers/post2_router.py (추가)

@router.put("/{id}", response_model=Post2DetailResponse)
def update_post(
    id: int,
    data: Post2Create,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # 본인 확인용
):
    return post2_service.update_post(db, id, data, current_user)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # 본인 확인용
):
    post2_service.delete_post(db, id, current_user)
```

---

## 내 글 조회 / 특정 유저의 글 조회

"내 정보"의 일부이므로 `/me/posts`가, “특정 유저 정보”의 일부이므로 `users/{user_id}/posts`가  REST 관점에서 자연스럽다.

### Repository

조회하는 데이터는 `posts`에 대한 데이터이기 때문에 post_repository에 정의한다.

```python
# mysite4/repositories/post2_repository.py (추가)

    def find_by_user_id(self, db: Session, user_id: int):
        """특정 유저가 작성한 게시글 목록 조회"""
        return db.scalars(
            select(Post2)
            .options(joinedload(Post2.user))
            .where(Post2.user_id == user_id)
        ).all()
```

### User Service 생성

- 이 때, `post2_repository`를 직접 호출하는 것이 아닌 `post2_service`를 통해 간접적으로 호출하는 것도 고려해야 한다.

```python
# mysite4/services/user_service.py
from sqlalchemy.orm import Session
from mysite4.repositories.post2_repository import post2_repository
from mysite4.models.user import User

class UserService:
    def read_my_posts(self, db: Session, current_user: User):
        """내가 작성한 게시글 목록 조회"""
        return post2_repository.find_by_user_id(db, current_user.id)

    def read_posts_by_user_id(self, db: Session, user_id: int):
        """특정 유저가 작성한 게시글 목록 조회"""
        return post2_repository.find_by_user_id(db, user_id)
        
user_service = UserService()
```

### User Router에 엔드포인트 추가

```python
# mysite4/routers/user_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from mysite4.schemas.user import UserResponse
from mysite4.schemas.post2 import Post2ListResponse
from mysite4.models.user import User
from mysite4.dependencies import get_current_user
from mysite4.services.user_service import user_service

router = APIRouter(tags=["Users"])

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/me/posts", response_model=list[Post2ListResponse])
def read_my_posts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """내가 작성한 게시글 목록 조회"""
    return user_service.read_posts_by_user_id(db, current_user.id)
    
    
@router.get("/users/{user_id}/posts", response_model=list[Post2ListResponse])
def read_posts_by_user(user_id: int, db: Session = Depends(get_db)):
    """특정 유저가 작성한 게시글 목록 조회"""
    return user_service.read_posts_by_user_id(db, user_id)

```