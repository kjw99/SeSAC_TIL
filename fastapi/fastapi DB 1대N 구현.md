## 1:N 관계에서의 주요 개념

- 외래키 (ForeignKey)
    
    N(다) 쪽 테이블에 1(일) 쪽의 식별자를 저장하는 실제 컬럼이다.
    
- 관계 설정 (relationship)
    
    데이터베이스 컬럼은 아니지만, 파이썬 코드에서 객체 간에 서로를 즉시 참조할 수 있게 해주는 논리적 지름길이다.
    
- 영속성 전이 (Cascade)
    
    1(일) 쪽 데이터가 삭제될 때 연결된 N(다) 쪽 데이터를 어떻게 처리할지 정하는 규칙이다.
    

---

## 실습

Post와 1:N 관계를 가지는 Comment를 생성해보자.

댓글에 대한 생성, 수정, 삭제 로직을 작성하며, 댓글에 대한 조회는 게시글 상세 조회에 포함한다.

- Comment는 Post에 종속됨.
- 그래서 create의 경우 /post/{post_id}/comment 이런 형식의 url을 갖게 될 것이고,
update의 경우 /post/{post_id}/comment/{comment_id} 이런 형식의 url을 갖게 됨.
- 댓글 수정의 경우 /comment/{comment_id} 이런 형태여도 기능에는 문제가 없지만, 리소스의 계층을 식별할 수 있는 위의 url이 좀 더 좋은 url 형태이다.

---

### Comment 모델 정의

- `mapped_column`는 comments table의 실제 컬럼을 생성한다.
- `relationship`은 comments table에서가 아닌 python 코드에서의 편의를 위하여 사용한다.
    - 즉, `comment.post`로 댓글과 연관된 게시글에 접근할 수 있다.
    - `back_populates` 옵션을 통해서 `post.comments`로도 접근할 수 있도록 할 수 있으며, `Post` 모델에도 함께 명시해주어야 한다.
- 타입 힌트에 따옴표를 활용하고 `TYPE_CHECKING`에 명시하여 순환 참조 에러를 방지한다.
    - 타입 체크를 할 때 Post를 import 해온다는 것. # 2 부분을 위한 코드. 의미론 적인 부분?. 실행할 때는 필요 없는 부분임.

```python
# models/comment.py

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .post import Post

class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(String(200), nullable=False)

    # 1. 외래키 설정: posts 테이블의 id를 참조한다.
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False)

    # 2. 관계 설정: 댓글 객체에서 소속된 게시글 객체로 바로 접근한다.
    post: Mapped["Post"] = relationship("Post", back_populates="comments")
```

main.py에서 편하게 import를 하기 위해 `mysite4/models/__init__.py` 생성 후 Post, Comment를 import한다.

- `__init__.py`는 해당 폴더가 파이썬의 패키지임을 알리는 특별한 파일이다.
`models/__init__.py`에서 모든 모델을 미리 임포트해두면 main.py에서는 `from mysite4 import models` 한 줄만으로 모든 모델을 Base에 등록시킬 수 있다.

```python
# mysite4/models/__init__.py

from .post import Post
from .comment import Comment
from database import Base

__all__ = ["Base", "Post", "Comment"]

```

```python
# main.py

from database import engine
from mysite4 import models

# 기존 테이블 지우기
# models.Base.metadata.drop_all(bind=engine)

# 정의된 모델들을 기반으로 DB에 테이블을 생성한다.
models.Base.metadata.create_all(bind=engine)
```

### Post 모델 수정

comments는 posts 테이블의 컬럼에는 영향을 미치지 않지만

`relationship`을 통해 python에서 객체로 접근이 가능하도록 한다.

comments는 여러 개니까, list[”Comment”] 이렇게 표현.

back_populates의 값인 post와 comments는 서로 대칭.

comments에서는 post - comments, post에서는 comments - post 이런 식으로 되어 있음.

```python
# models/post.py 수정

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text
from database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .comment import Comment

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
```

- Post모델이 변경되었으므로 main.py에서의 다음 코드를 `Base.metadata.drop_all(bind=engine)`을 주석해제하여 테이블을 초기화한다.
    - 초기화 하면 다시 주석 처리해서 데이터 보관할 수 있도록 하자.
    
    ```python
    # 기존 테이블 지우기
    Base.metadata.drop_all(bind=engine)
    
    # 정의된 모델들을 기반으로 DB에 테이블을 생성한다.
    Base.metadata.create_all(bind=engine)
    ```
    

### 영속성 전이 (cascade)

부모 객체에 수행된 작업이 관계된 자식 객체에 어떻게 전달될지를 정의하는 설정이다.

- 주요 Cascade 옵션
    - save-update (기본값)
        
        부모 객체가 세션에 추가(add)되거나 업데이트될 때, 연결된 자식 객체들도 자동으로 세션에 포함된다.
        
    - delete
        
        부모 객체가 삭제될 때 연결된 자식 객체들도 함께 삭제된다.
        
    - delete-orphan
        
        부모와의 관계가 끊어진 자식 객체(고아 객체)를 자동으로 삭제한다. 게시글에서 특정 댓글을 리스트에서 제거(post.comments.remove(comment))할 때 DB에서도 해당 댓글을 지우고 싶다면 이 옵션이 필수적이다.
        
    - all
        
        save-update, merge, refresh-expire, expunge, delete를 모두 포함하는 단축 속성이다.
        
    - all, delete-orphan
        
        실무에서 가장 많이 사용하는 조합으로, 부모 삭제 시 자식 동반 삭제 및 관계 단절 시 고아 객체 삭제를 모두 수행한다.
        코드를 예시로 들면, Post를 지우면 Comment도 지워진다는 것.
        

---

## 스키마 정의

```python
# schemas/comment.py

from pydantic import BaseModel, ConfigDict

class CommentCreate(BaseModel):
    content: str

class CommentResponse(BaseModel):
    id: int
    content: str

    model_config = ConfigDict(from_attributes=True) 
```

게시글 상세조회 시 댓글에 대한 응답 스키마를 포함할 수 있도록 변경한다.
기본값으로 `[ ]`를 명시하여 댓글이 없는 경우에도 일관적인 응답을 보장할 수 있다.

```python
# schemas/post.py (상세 응답 수정)

from mysite4.schemas.comment import CommentResponse

class PostDetailResponse(BaseModel):
    id: int
    title: str
    content: str
    
    # 해당 게시글에 달린 댓글 목록을 포함한다.
    # SQLAlchemy의 relationship을 통해 자동으로 데이터를 매핑한다.
    comments: list[CommentResponse] = [] 

    model_config = ConfigDict(from_attributes=True)
```

---

## Repository 구현

```python
# repositories/comment_repository.py

from sqlalchemy.orm import Session
from mysite4.models.comment import Comment

class CommentRepository:
    def save(self, db: Session, new_comment: Comment):
        # 세션의 작업 목록에 새로운 댓글 객체를 추가한다.
        db.add(new_comment)
        return new_comment

    def find_by_id(self, db: Session, comment_id: int):
        return db.get(Comment, comment_id)

    def delete(self, db: Session, comment: Comment):
        db.delete(comment)

comment_repository = CommentRepository()
```

---

## Service 구현

```python
# services/comment_service.py

from sqlalchemy.orm import Session
from mysite4.repositories.comment_repository import comment_repository
from mysite4.services.post_service import post_service
from mysite4.models.comment import Comment
from mysite4.schemas.comment import CommentCreate
from fastapi import HTTPException

class CommentService:
    def create_comment(self, db: Session, post_id: int, data: CommentCreate):
        # 1. 경로로 받은 post_id가 실제 존재하는 게시글인지 검증
        post = post_service.read_post_by_id(db, post_id)

        # 2. 모델 인스턴스 생성 시 post를 직접 매핑
        new_comment = Comment(
            content=data.content,
            post=post
        )
        
        with db.begin():
            comment_repository.save(db, new_comment)
        
        db.refresh(new_comment)
        return new_comment
        
    def update_comment(self, db: Session, post_id: int, comment_id: int, content: str):
        with db.begin():
            comment = comment_repository.find_by_id(db, comment_id)

            if not comment:
                raise HTTPException(status_code=404, detail="Comment not found")

            if comment.post_id != post_id:
                raise HTTPException(
                    status_code=400, detail="Comment does not belong to this post"
                )

            # 더티 체킹을 통한 수정
            comment.content = content

        db.refresh(comment)
        return comment

    def delete_comment(self, db: Session, post_id: int, comment_id: int):
        with db.begin():
            comment = comment_repository.find_by_id(db, comment_id)

            if not comment:
                raise HTTPException(status_code=404, detail="Comment not found")

            if comment.post_id != post_id:
                raise HTTPException(
                    status_code=400, detail="Comment does not belong to this post"
                )

            comment_repository.delete(db, comment)

comment_service = CommentService()
```

중복되는 코드는 아래와 같이 함수로 감싸서 재활용할 수 있다.

```python
def _get_verified_comment(self, db: Session, post_id: int, comment_id: int):
    comment = comment_repository.find_by_id(db, comment_id)
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.post_id != post_id:
        raise HTTPException(
            status_code=400, detail="Comment does not belong to this post"
        )

    return comment
```

---

## Router 구현

comments는 특정 post에 종속된 형태, 즉 `/posts/{post_id}/comments` 의 형태이므로 post_router에서 처리한다.

```python
# routers/post_router.py

from mysite4.services.comment_service import comment_service
from mysite4.schemas.comment import CommentCreate, CommentResponse

@router.post(
    "/{post_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_comment(post_id: int, data: CommentCreate, db: Session = Depends(get_db)):
    # 경로에서 받은 post_id를 서비스로 전달한다.
    return comment_service.create_comment(db, post_id, data)
    
@router.put("/{post_id}/comments/{comment_id}", response_model=CommentResponse)
def update_comment(
    post_id: int, comment_id: int, data: CommentCreate, db: Session = Depends(get_db)
):
    updated_comment = comment_service.update_comment(
        db, post_id, comment_id, data.content
    )
    return updated_comment

@router.delete(
    "/{post_id}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_comment(post_id: int, comment_id: int, db: Session = Depends(get_db)):
    comment_service.delete_comment(db, post_id, comment_id)
    return None
```

---

### 게시글 상세 조회에서의 댓글 조회

현재 구조에서 댓글에 대한 조회는 게시글 상세 조회에 포함되어 있으나, 댓글이 많아지게 되면 별도의 API로 만들어 페이지네이션 기능을 추가해야 한다.

---

## Lazy Loading

현재 Post, Comment 두개의 테이블에서 데이터를 가져오지만, JOIN과 연관된 로직은 존재하지 않는다. 이는 `PostDetailResponse` 스키마를 통해 데이터를 반환할 때 SQLAlchemy의 Lazy Loading 메커니즘이 작동하기 때문이다.

Lazy Loading은 연관된 객체를 조회할 때 처음부터 모든 데이터를 가져오지 않고, 실제 그 데이터가 필요한 시점(속성에 접근할 때)에 비로소 추가 SQL 쿼리를 실행하여 불러오는 방식이다.

단, N+1 문제가 발생할 수 있으며, 추후 해결할 예정이다.

