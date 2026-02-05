## DB 연동

## 준비

database.py를 제외한 코드는 `mysite4` 폴더 내부에 작성한다.

```python
project_root/
├── .env
├── database.py
├── main.py (실행 파일)
└── mysite4/
    ├── models/           - 데이터베이스 테이블과 매핑
    ├── schemas/          - 데이터의 입출력 형식 검증
    ├── repositories/     - 순수한 DB 조작 (SELECT, INSERT)
    ├── services/         - 비즈니스 로직 및 트랜잭션(Commit)
    └── routers/          - API 엔드포인트 관리
```

### Database 생성

`mysite` 데이터베이스를 생성한다.

### Database 연동

- 필요한 라이브러리를 설치한다
    
    `sqlalchemy`는 파이썬 객체와 관계형 데이터베이스 사이를 잇는  표준 ORM 라이브러리이다.
    SQL 쿼리 대신 파이썬 문법만으로 DB를 조작하고 데이터를 안전하게 영구 저장하게 해주는 도구이다.
    
    - sqlalchemy = ORM 역할. 보통 SQL이 있어야 DB와 소통이 가능. 우리는 fastapi를 쓰는 중인데, SQL 없이 python만 가지고 DB와 소통하면 어떨까?. 그래서 나온 개념이 ORM.
    sqlalchemy는 python 문법으로만 db와 소통하도록 도와줌.
    
    ```bash
    uv add sqlalchemy psycopg2-binary python-dotenv
    ```
    
- `.env`파일을 만든 뒤 데이터베이스 연결을 위한 URL을 작성한다.
    
    ```bash
    DATABASE_URL=postgresql://postgres:{비밀번호}@localhost:5432/mysite
    ```
    

- 루트 디렉토리에 `database.py`를 생성한 뒤 설정 코드를 작성한다.
    
    ```python
    import os
    from dotenv import load_dotenv
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, DeclarativeBase
    
    # 환경 변수 로드
    load_dotenv()
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    # DB 엔진 생성
    engine = create_engine(DATABASE_URL)
    
    # 세션 생성기 정의
    # DB와 소통하는 engine을 활용해서 소통하기 위한 공간을 만든다.
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # SQLAlchemy 2.0 스타일의 Base 클래스 선언
    class Base(DeclarativeBase):
        pass
    
    # DB 세션 의존성 주입 함수
    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    ```
    

### 세션 (Session)

세션은 데이터베이스와 상호작용하는 하나의 작업 단위이자 파이썬 객체들의 변경 사항을 추적하는 논리적 영역이다. 데이터베이스에 데이터를 저장하거나 수정할 때 즉시 반영하는 것이 아니라, 세션이라는 '장바구니'에 담아두었다가 마지막에 한꺼번에 확정(Commit)하는 방식으로 동작한다. 이를 통해 여러 작업을 하나의 트랜잭션으로 묶어 처리할 수 있으며 데이터의 일관성을 유지한다.

### 트랜잭션 (Transaction)

트랜잭션은 데이터베이스의 상태를 변화시키기 위해 수행하는 작업의 최소 단위이다. 여러 개의 SQL 명령문을 하나의 묶음으로 처리하여, 모두 성공하거나 혹은 모두 실패하도록 보장한다.

정상 실행시 `COMMIT`을 하여 데이터의 변화를 적용시키고, 문제 발생시 `ROLLBACK`하여 적용시키지 않는다.

DB 트랜잭션의 특징 ACID !

- 원자성 (Atomicity): 트랜잭션 내의 모든 작업은 반드시 전체가 완료되거나, 하나라도 실패하면 전체가 취소되어야 한다. (All or Nothing)
- 일관성 (Consistency): 트랜잭션 완료 후 데이터베이스는 미리 정의된 규칙(제약 조건 등)을 모두 만족하며 유효한 상태를 유지해야 한다.
- 고립성 (Isolation): 동시에 실행되는 트랜잭션들이 서로의 작업 중간 과정에 간섭하지 못하도록 격리한다.
- 지속성 (Durability): 성공적으로 완료된 트랜잭션의 결과는 시스템 장애가 발생하더라도 데이터베이스에 영구적으로 기록된다.

---

## SQLAlchemy 모델 정의

기존 mysite3 `Post` 클래스와는 달리, SQLAlchemy 모델은 데이터베이스에 실제 테이블을 생성할 수 있다.

`schemas`와 분리하여 `models` 폴더를 생성한 후 작성한다.

```python
# models/post.py

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text
from database import Base

class Post(Base):
    __tablename__ = "posts"

    # primary_key는 기본키 설정을, autoincrement는 자동 번호 생성을 의미한다.
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # String(50)은 VARCHAR(50)과 매핑되며, nullable=False는 NOT NULL 제약조건이다.
    title: Mapped[str] = mapped_column(String(50), nullable=False)

    # Text는 길이 제한이 없는 대용량 텍스트 저장에 적합하다.
    content: Mapped[str] = mapped_column(Text, nullable=False)
```

### Mapped와 mapped_column

- Mapped[T]
    
    해당 속성이 파이썬 코드에서 어떤 타입을 가지는지 명시하는 역할을 수행한다. 
    정적 분석 도구가 타입을 정확히 추론할 수 있게 도와주며, 해당 필드가 SQLAlchemy가 관리하는 '매핑된 속성'임을 선언한다.
    
- mapped_column()
    
    실제 데이터베이스 컬럼의 세부적인 성격을 결정한다. 
    데이터베이스 관점에서의 자료형(String, Text 등)이나 제약 조건(Primary Key, Nullable 등)을 설정하는 도구로 사용된다.
    
    - primary_key=True: 행을 식별하는 유일한 기준인 기본키로 설정한다.
    - nullable=False: 빈 값(NULL)을 허용하지 않는 NOT NULL 제약을 추가한다.
    - unique=True: 중복된 값이 들어올 수 없도록 유일성을 보장한다.
    - index=True: 빠른 조회를 위해 해당 컬럼에 인덱스를 생성한다.
    - autoincrement=True: 숫자가 자동으로 1씩 증가하는 자동 생성 기능을 부여한다.
    - default=값: 데이터 생성 시 값이 없으면 파이썬 레벨에서 기본값을 채운다.
    - server_default=값: 데이터베이스 자체에서 기본값을 생성하도록 스키마를 설정한다.
    - ForeignKey("테이블.컬럼"): 다른 테이블과 연결되는 외래키 제약을 설정한다.
    - comment="설명": 데이터베이스 관리 도구에서 볼 수 있는 컬럼 주석을 작성한다.

### 데이터베이스 테이블 생성

작성한 모델을 바탕으로 실제 PostgreSQL 데이터베이스에 테이블을 생성하려면 애플리케이션 실행 시점에 `Base.metadata.create_all` 명령을 실행해야 한다.

```python
# main.py

from fastapi import FastAPI
from database import engine, Base
from mysite4.models.post import Post  # 모델 파일이 import되어야 Base가 인식한다.

# 기존 테이블 지우기
# Base.metadata.drop_all(bind=engine)

# 정의된 모델들을 기반으로 DB에 테이블을 생성한다.
Base.metadata.create_all(bind=engine)

app = FastAPI()
```

- `Base.metadata.create_all`은 테이블이 없으면 생성하고, 테이블이 있으면 아무 동작도 하지 않으며, 기존 테이블에 대한 수정이 불가능하다. 따라서 실제 서비스에서는 사용하지 않는다.
    - 테이블 생성 후에 모델에 컬럼 하나 추가하고 다시 실행을 해도 기존 테이블에 컬럼이 추가되지는 않는다.
    - 아예 테이블 자체를 지우고 다시 생성하면 반영되긴 함.

---

## Pydantic 스키마 정의

클라이언트로부터 입력받을 데이터의 형식과 API가 반환할 응답 형식을 정의한다.

응답에 대한 데이터 모델에서는 SQLAlchemy를 통해 가져온 데이터를 처리하기 위한 설정을 추가한다.

```python
# schemas/post.py

from pydantic import BaseModel, ConfigDict

class PostCreate(BaseModel):
    title: str
    content: str

class PostListResponse(BaseModel):
    id: int
    title: str

    # SQLAlchemy 모델 객체를 Pydantic에서 읽기 위한 설정
    model_config = ConfigDict(from_attributes=True)

class PostDetailResponse(BaseModel):
    id: int
    title: str
    content: str

    model_config = ConfigDict(from_attributes=True)
```

---

## Repository 구현

Repository는 SQLAlchemy의 세션 객체를 전달받아 데이터베이스에 쿼리를 실행한다.

데이터의 최종 확정 권한인 commit은 서비스 계층으로 넘기고, Repository는 순수하게 데이터 조작 명령을 전달하는 역할에 집중한다. 즉, 트랜잭션은 service에서 관리한다.

```python
# repositories/post_repository.py

from sqlalchemy.orm import Session
from sqlalchemy import select
from mysite4.models.post import Post
from mysite4.schemas.post import PostCreate

class PostRepository:
    def save(self, db: Session, new_post: Post):
        # 세션의 작업 목록에 새로운 객체를 추가한다.
        db.add(new_post)
        return new_post

    def find_all(self, db: Session):
        # select 문을 생성하고 scalars를 통해 결과 객체들을 리스트로 가져온다.
        # select * from table
        return db.scalars(select(Post)).all()

    def find_by_id(self, db: Session, id: int):
        # 기본키(Primary Key)를 이용한 조회는 db.get이 가장 빠르고 효율적이다.
        return db.get(Post, id)

    def update(self, db: Session, post: Post, data: PostCreate):
        # 이미 조회된 객체의 속성을 변경하면 세션이 이를 감지한다.
        post.title = data.title
        post.content = data.content
        return post

    def delete(self, db: Session, post: Post):
        # 세션에서 해당 객체를 삭제 대상으로 표시한다.
        db.delete(post)

post_repository = PostRepository()

```

---

## Service 구현

```python
# services/post_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from mysite4.repositories.post_repository import post_repository
from mysite4.models.post import Post
from mysite4.schemas.post import PostCreate

class PostService:
    def create_post(self, db: Session, data: PostCreate):

        new_post = Post(title=data.title, content=data.content)
        
        # 레포지토리에 저장을 요청한다. (아직 DB에 확정된 상태는 아님)
        post_repository.save(db, new_post)
        
        # 서비스 계층에서 트랜잭션을 최종 확정한다.
        db.commit()
        
        # DB에서 생성된 ID 등을 파이썬 객체에 반영한다.
        db.refresh(new_post)
        
        return new_post

    def read_posts(self, db: Session):
        return post_repository.find_all(db)

    def read_post_by_id(self, db: Session, id: int):
        post = post_repository.find_by_id(db, id)
        if not post:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "존재하지 않는 게시글입니다.")
        return post

    def update_post(self, db: Session, id: int, data: PostCreate):
        # 수정할 게시글 존재 여부를 먼저 확인한다.
        post = self.read_post_by_id(db, id)
        
        # 레포지토리를 통해 객체 정보를 수정(더티 체크 대상)한다.
        updated_post = post_repository.update(db, post, data)
        
        # 최종 확정 및 갱신
        db.commit()
        db.refresh(updated_post)
        
        return updated_post

    def delete_post(self, db: Session, id: int):
        post = self.read_post_by_id(db, id)
        
        post_repository.delete(db, post)
        
        # 삭제 트랜잭션을 확정한다.
        db.commit()

post_service = PostService()
```

### 트랜잭션의 경계 설정

서비스 계층의 메서드 하나가 곧 하나의 **트랜잭션 단위**가 된다.

`update_post`내에서 레포지토리를 여러 번 호출하더라도, 마지막에 단 한 번의 `db.commit()`만 수행함으로써 모든 작업이 원자적으로(All or Nothing) 처리되도록 보장한다. 
만약 로직 중간에 예외가 발생하면 `commit`이 호출되지 않으므로 데이터베이스에 불완전한 데이터가 남지 않는다.

ex) 상품 주문 시 `주문` 레코드 생성 → `상품`의 재고 감소라는 2번의 레포지토리 호출이 일어난다.

- db.commit()을 통해 트랜잭션을 종료하여 데이터베이스에 변화내용을 저장한다.
- db.refresh()를 통해 ID, 생성 시간 등 데이터베이스에서 생성되는 새로운 정보를 가져온다.

---

## Router 구현

```python
# routers/post_router.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from mysite4.services.post_service import post_service
from mysite4.schemas.post import PostCreate, PostDetailResponse, PostListResponse

router = APIRouter(prefix="/posts-db", tags=["posts"])

@router.post("", response_model=PostDetailResponse, status_code=status.HTTP_201_CREATED)
def create_post(data: PostCreate, db: Session = Depends(get_db)):
    # Depends(get_db)를 통해 요청마다 새로운 세션을 주입받는다.
    return post_service.create_post(db, data)

@router.get("", response_model=list[PostListResponse])
def read_posts(db: Session = Depends(get_db)):
    return post_service.read_posts(db)

@router.get("/{id}", response_model=PostDetailResponse)
def read_post(id: int, db: Session = Depends(get_db)):
    return post_service.read_post_by_id(db, id)

@router.put("/{id}", response_model=PostDetailResponse)
def update_post(id: int, data: PostCreate, db: Session = Depends(get_db)):
    return post_service.update_post(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_service.delete_post(db, id)
```

### 의존성 주입

어떤 기능을 수행하기 위해 다른 클래스의 인스턴스가 필요할 때 코드 내부에서 직접 객체를 생성해야 한다. 하지만 의존성 주입 방식에서는 해당 객체를 직접 만들지 않고, 외부(프레임워크나 컨테이너)가 생성해준 객체를 전달받아 사용하기만 한다.

FastAPI에서는 `Depends`는 함수를 통해 의존성 주입을 지원한다. 함수가 실행되기 전에 필요한 객체를 미리 준비해주며, 이를 통해 데이터베이스 세션 관리의 효율성을 극대화한다.

- 세션 주입
    
    `db: Session = Depends(get_db)` 코드는 엔드포인트 함수가 호출될 때마다 `database.py`에 정의한 `get_db` 제너레이터를 실행한다.
    
- 자동 자원 해제
    
     get_db 내부의 yield 구문 덕분에 Router의 작업이 끝나고 클라이언트에게 응답이 나가는 순간 finally 블록이 실행되어 세션이 자동으로 닫힌다. 개발자가 직접 세션을 닫는 코드를 작성할 필요가 없다.
    
- 일관된 트랜잭션
    
    하나의 요청 안에서 주입된 db 객체는 서비스와 레포지토리 계층까지 동일하게 전달된다. 이를 통해 전체 비즈니스 로직을 하나의 트랜잭션 범위 안에서 안전하게 처리할 수 있다.
    

---

## 트랜잭션 롤백

롤백은 트랜잭션 도중 오류가 발생했을 때, 해당 트랜잭션 내에서 수행한 모든 데이터 변경 사항을 취소하고 데이터베이스를 이전 상태로 되돌리는 작업이다. 이는 '전부 성공하거나 아니면 아예 수행하지 않는다'는 원자성(Atomicity) 원칙을 실현하는 핵심 기술이다.

```python
class PostService:
    def create_post(self, db: Session, data: PostCreate):
        try:
            new_post = Post(title=data.title, content=data.content)
            post_repository.save(db, new_post)
            
            # 비즈니스 로직 중 강제로 에러가 발생할 경우를 가정
            # if some_error_condition:
            #     raise Exception("데이터 저장 중 오류 발생")

            db.commit()
            db.refresh(new_post)
            return new_post
        except Exception as e:
            # 오류 발생 시 세션에 머물던 변경 사항을 모두 취소한다.
            db.rollback()
            raise e

```

commit과 rollback을 명시하지 않고 컨텍스트 매니저를 활용한 방식의 코드를 활용할 수 있다.

with 을 사용해서 위의 try ~ except 구문을 간편하게 사용. 트랜잭션 구현을 위해 반드시 필요.

```python
class PostService:
    def create_post(self, db: Session, data: PostCreate):
        # begin() 블록 안에서 일어나는 모든 작업은 하나의 트랜잭션이다.
        with db.begin():
            new_post = Post(title=data.title, content=data.content)
            post_repository.save(db, new_post)
            
            # 블록이 끝날 때 성공 시 자동 commit, 실패 시 자동 rollback 된다.
        
        # 블록 외부에서 refresh를 수행하여 최신 데이터를 읽어온다.
        db.refresh(new_post)
        return new_post
```

## ORM (Object-Relational Mapping)

ORM은 객체 지향 프로그래밍 언어와 관계형 데이터베이스(RDBMS) 사이의 서로 다른 데이터 구조를 해결하기 위한 기술이다.
개발자가 복잡한 SQL 쿼리를 직접 작성하는 대신, 파이썬 클래스와 메서드를 이용해 데이터를 다룰 수 있게 돕는 기술이다.

- **생산성 향상**
    
    SQL 문법 대신 익숙한 프로그래밍 언어로 데이터베이스를 조작할 수 있어 개발 속도가 빨라진다.
    
- **유지보수 용이**
    
    데이터베이스 종류가 바뀌더라도 ORM 설정만 변경하면 되므로 코드의 재사용성이 높다.
    
- **직관적인 코드**
    
    비즈니스 로직과 데이터 로직이 분리되어 코드가 훨씬 깔끔해진다.
    

# SQLAlchemy 주요 메서드

## 데이터 생성

- 단일 객체 추가 (add)

```python
new_post = Post(title="첫 번째 글", content="내용입니다")
db.add(new_post)
db.commit()
```

```sql
INSERT INTO posts (title, content) VALUES ('첫 번째 글', '내용입니다') RETURNING posts.id;
```

- 여러 객체 일괄 추가 (add_all)

```python
posts = [
    Post(title="두 번째", content="내용2"),
    Post(title="세 번째", content="내용3")
]
db.add_all(posts)
db.commit()
```

```sql
INSERT INTO posts (title, content) VALUES ('두 번째', '내용2'), ('세 번째', '내용3');
```

## 데이터 조회

- 기본키 기반 조회 (get)
    
    ID가 1인 객체가 이미 세션 메모리(Identity Map)에 있다면 SQL을 실행하지 않고 즉시 반환한다. 메모리에 없을 경우에만 SQL이 실행된다.
    

```python
post = db.get(Post, 1)
```

```sql
SELECT posts.id, posts.title, posts.content FROM posts WHERE posts.id = 1;
```

### stmt와 scalars

SQLAlchemy는 데이터를 바로 가져오는 대신,'무엇을 가져올지 정의하는 단계'와 '실제로 가져와서 변환하는 단계'를 분리한다.

- stmt (Statement) 
SQL 설계도이다. select(Post)와 같이 작성하면 "Post 테이블에서 모든 컬럼을 선택하라"는 문장이 준비되며, 실제 DB에 요청을 보내기 전의 '대기 상태'인 파이썬 객체이다.
- scalars()
    
    DB가 보낸 행(Row) 데이터에서 객체를 골라내는 추출기이다. 
    DB는 보통 `(id, title, content)` 같은 튜플 형태로 데이터를 주는데, `scalars()`를 거치면 우리가 원하는 `Post` 클래스의 인스턴스로 변환된다.
    
- 전체 조회

```python
stmt = select(Post)
posts = db.scalars(stmt).all()
```

```sql
SELECT posts.id, posts.title, posts.content
FROM posts;
```

- 단일 조건 조회

```python
stmt = select(Post).where(Post.id == 1)
post = db.scalars(stmt).first()
```

```sql
SELECT posts.id, posts.title, posts.content
FROM posts
WHERE posts.id = 1
LIMIT 1;
```

- 키워드 검색

```python
stmt = select(Post).where(Post.title.like("%FastAPI%"))
posts = db.scalars(stmt).all()
```

```sql
SELECT posts.id, posts.title, posts.content
FROM posts
WHERE posts.title LIKE '%FastAPI%';
```

- 다중 조건
    - and
    
    ```python
    stmt = select(Post).where(Post.id > 10, Post.title.like("%공부%"))
    posts = db.scalars(stmt).all()
    ```
    
    ```python
    SELECT posts.id, posts.title, posts.content 
    FROM posts 
    WHERE posts.id > 10 AND posts.title LIKE '%공부%';
    ```
    
    - or
    
    ```python
    stmt = select(Post).where(or_(Post.id == 1, Post.title == "공지"))
    posts = db.scalars(stmt).all()
    ```
    
    ```python
    SELECT posts.id, posts.title, posts.content 
    FROM posts 
    WHERE posts.id = 1 OR posts.title = '공지';
    ```
    
- 다중 복잡 조건

```python
stmt = select(Post).where(
    and_(
        Post.id > 10,
        or_(Post.title == "공지", Post.title == "이벤트")
    )
)
posts = db.scalars(stmt).all()
```

```sql
SELECT posts.id, posts.title, posts.content
FROM posts
WHERE posts.id > 10 AND (posts.title = '공지' OR posts.title = '이벤트');
```

- 정렬 조회

```python
stmt = select(Post).order_by(Post.id.desc())
posts = db.scalars(stmt).all()
```

```sql
SELECT posts.id, posts.title, posts.content
FROM posts
ORDER BY posts.id DESC;
```

- 결과 제한

```python
stmt = select(Post).order_by(Post.id.desc()).limit(10)
posts = db.scalars(stmt).all()
```

```sql
SELECT posts.id, posts.title, posts.content
FROM posts
ORDER BY posts.id DESC
LIMIT 10;
```

### 결과 추출 메서드의 종류와 특징

`all()`과 `first()` 외에도 상황에 따라 데이터의 유일성을 검증할 수 있는 다양한 메서드가 존재한다.

| 메서드 | 결과가 없을 때 | 결과가 2개 이상일 때 | 특징 |
| --- | --- | --- | --- |
| **`.all()`** | `[]` (빈 리스트) | 리스트 전체 반환 | 일반적인 목록 조회에 적합 |
| **`.first()`** | `None` 반환 | 첫 번째 것만 반환 | 데이터 존재 여부만 확인할 때 유용 |
| **`.one()`** | **에러 발생** | **에러 발생** | 반드시 정확히 1개여야 하는 고유값 조회 시 사용 |
| **`.one_or_none()`** | `None` 반환 | **에러 발생** | 없거나 하나만 있어야 하는 안전한 단건 조회에 권장 |

## 데이터 수정과 더티 체킹

SQLAlchemy는 객체의 속성 변경을 감지하여 자동으로 `UPDATE` 문을 생성한다.

### 더티 체킹을 통한 수정

```python
# 1. 먼저 데이터를 조회 (Persistent 상태가 됨)
post = db.get(Post, 1)

# 2. 객체의 속성을 변경
post.title = "수정된 제목"

# 3. 커밋 시점에 변경 사항이 감지되어 SQL 실행
db.commit()

```

## 데이터 삭제

- 객체 기반 삭제

```python
post = db.get(Post, 1)
db.delete(post)
db.commit()
```

```sql
DELETE FROM posts WHERE posts.id = 1;
```