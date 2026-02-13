## 서버에 동시 요청이 들어온다면

### 문제: 동기 서버의 한계

우리가 만든 API에 **100명이 동시에** 요청을 보낸다고 하자.
각 요청이 DB 조회에 100ms가 걸린다면:

- 동기 서버 (요청을 순서대로 처리)
    - 요청 1 → DB 100ms → 응답     (100ms)
    - 요청 2 → DB 100ms → 응답     (200ms)
    - 요청 3 → DB 100ms → 응답     (300ms)
    ...
    - 요청 100 → DB 100ms → 응답   (10,000ms = 10초!)

→ 100번째 사용자는 10초를 기다려야 한다
→ DB 응답을 기다리는 동안 서버는 아무것도 안하고 기다린다.

---

### 해결 방법 1: 스레드 (def)

- 스레드 풀 (동시 처리)
    - Thread 1 → 요청 1 → DB 100ms → 응답
    - Thread 2 → 요청 2 → DB 100ms → 응답     ← 동시에!
    - Thread 3 → 요청 3 → DB 100ms → 응답     ← 동시에!
    - ...
    - Thread 40 → 요청 40 → DB 100ms → 응답   ← 동시에!

→ 40개 요청을 동시에 처리 (100ms에 40개 완료)
→ 나머지 60개는 스레드가 비면 순차 대기

- 장점: 기존 동기 코드 그대로 사용 가능
- 단점: **스레드 수에 한계** (기본 40개), 스레드마다 메모리 소비

### 스레드(Thread)

프로그램 안에서 **독립적으로 실행되는 작업 단위**

- **프로세스**: 프로그램 그 자체 (예: 파이썬 서버 1개)
- **스레드**: 프로세스 안에서 동시에 돌아가는 실행 흐름
- 하나의 프로세스에 여러 스레드를 만들면, 각 스레드가 **동시에 다른 일**을 할 수 있다

### 스레드 풀

```
스레드 풀 (FastAPI가 def를 실행하는 곳):
┌──────────────────────────────┐
│  Thread 1: 요청A의 def 실행   │
│  Thread 2: 요청B의 def 실행   │
│  Thread 3: 요청C의 def 실행   │
│  Thread 4: (대기 중...)       │
│  ...                         │
│  Thread 40: (대기 중...)      │  ← 기본 40개
└──────────────────────────────┘
```

- `def` 엔드포인트는 스레드 풀의 빈 스레드에서 실행된다
- 각 스레드는 독립적이라 `time.sleep()`을 써도 다른 요청에 영향 없다
- 단, 스레드 수(기본 40개)를 초과하면 대기가 발생한다

---

### 해결 방법 2: 이벤트 루프 (async def)

- 이벤트 루프 (1개의 스레드로 전부 처리)
    - 요청 1 → DB 쿼리 보냄 (await) → 기다리지 않고 →
    - 요청 2 → DB 쿼리 보냄 (await) → 기다리지 않고 →
    - 요청 3 → DB 쿼리 보냄 (await) → 기다리지 않고 →
    - ...
    - 요청 100 → DB 쿼리 보냄 (await) →

→ 요청 1의 DB 응답 도착! → 응답 전송
→ 요청 2의 DB 응답 도착! → 응답 전송
...

→ 100개 요청의 DB 쿼리를 거의 동시에 보냄
→ 스레드 1개로 100개 동시 처리 가능!

- 장점: **스레드 1개로 수천 개 동시 처리**, 메모리 효율적
- 단점: 코드에 `await`를 써야 하고, blocking 코드를 쓰면 안 됨
    - blocking 코드 : 대기 / HTTP 요청 / DB 쿼리 등의 IO 작업

---

### 동기 / 비동기의 차이

- 동기(스레드): 대기하는 동안 해당 스레드가 멈춰있음 (점원이 커피 나올 때까지 서서 기다림)
- 비동기(async): 대기하는 동안 다른 요청 처리 (점원이 다음 손님 주문 받음)

---

## FastAPI의 def vs async def

FastAPI는 `def`와 `async def`를 **다르게** 처리한다.

### 실행 방식 차이

- def 엔드포인트
→ FastAPI가 자동으로 스레드 풀에서 실행
→ blocking 코드 써도 OK (다른 요청에 영향 없음)
- async def 엔드포인트:
→ 이벤트 루프에서 직접 실행
→ blocking 코드 쓰면 전체 서버가 멈춤!

### 정리

|  | `def` | `async def` |
| --- | --- | --- |
| 실행 위치 | 스레드 풀 (자동) | 이벤트 루프 (직접) |
| blocking 코드 | OK | **NG** (서버 멈춤) |
| `await` 사용 | 불가 | 가능 |
| 적합한 상황 | 동기 라이브러리 사용 시 | 비동기 라이브러리 사용 시 |

> **규칙: `async def`로 선언했으면 안에서 쓰는 모든 I/O도 async여야 한다.**
> 
> - `time.sleep()` → `asyncio.sleep()`
> - `requests.get()` → `httpx.AsyncClient`
> - sync DB 세션 → async DB 세션

---

## 커넥션 풀이란

### 문제: 매번 DB 연결하면?

- 요청마다 새 연결
    - 요청 → DB 연결 (50ms) → 쿼리 (5ms) → 연결 해제 → 응답
    - 요청 → DB 연결 (50ms) → 쿼리 (5ms) → 연결 해제 → 응답
    
    → 연결/해제 오버헤드가 쿼리보다 10배 크다!
    

### 해결: 커넥션 풀

```
커넥션 풀:
┌─────────────────────────────────┐
│  연결1: (사용중 - 요청A)          │
│  연결2: (사용중 - 요청B)          │
│  연결3: (대기중 - 다음 요청 대기)  │
│  연결4: (대기중)                  │
│  연결5: (대기중)                  │  ← 기본 5개 유지
└─────────────────────────────────┘

요청 → 풀에서 연결 빌려옴 (0ms) → 쿼리 → 연결 반납 → 응답
→ 미리 만들어둔 연결을 재사용해서 빠르다!
```

### SQLAlchemy의 커넥션 풀 설정

```python
# sync
engine = create_engine(
    DATABASE_URL,
    pool_size=5,        # 풀에 유지할 연결 수 (기본 5)
    max_overflow=10,    # pool_size 초과 시 추가 생성 가능한 수 (기본 10)
    pool_timeout=30,    # 연결 대기 최대 시간 (초)
    pool_recycle=1800,  # 연결 재활용 주기 (초) — 오래된 연결 방지
)

# async — 동일한 옵션 사용 가능
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    pool_size=5,
    max_overflow=10,
)
```

### 커넥션 풀 동작 흐름

```
1. 서버 시작 → 엔진이 pool_size(5)개의 연결을 미리 생성

2. 요청 처리:
   요청 A → 풀에서 연결 1번 빌림 → 쿼리 → 반납
   요청 B → 풀에서 연결 2번 빌림 → 쿼리 → 반납

3. 동시 요청이 pool_size를 초과하면:
   → max_overflow까지 임시 연결 추가 생성 (최대 5+10=15개)
   → 요청 완료 후 임시 연결은 제거

4. 15개도 초과하면:
   → pool_timeout(30초) 동안 대기
   → 그래도 안 되면 에러 발생
```

---

## 실습

- 라이브러리 설치
    
    PostgreSQL용 비동기 드라이버를 설치한다.
    

```python
uv add asyncpg
```

### Async SQLAlchemy 설정

비동기 로직을 위한 databse engine을 따로 생성한다.

```python
# async_database.py
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

load_dotenv()

# 드라이버 변경: postgresql:// → postgresql+asyncpg://
SYNC_DATABASE_URL = os.getenv("DATABASE_URL")
ASYNC_DATABASE_URL = SYNC_DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Async 엔진 생성
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)

# Async 세션 생성기
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine, 
    class_=AsyncSession, 
    expire_on_commit=False # async에서는 필수
)

# Async DB 세션 의존성 주입 함수
async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session
```

### async_post_router 구현

```python
# routers/async_post_router.py 

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from async_database import get_async_db
from mysite4.models.post import Post
from mysite4.models.post_tag import PostTag
from mysite4.schemas.post import PostDetailResponse, PostListResponse

router = APIRouter(prefix="/async/posts", tags=["Async Posts (비동기 체험)"])

@router.get("/", response_model=list[PostListResponse])
async def get_posts(db: AsyncSession = Depends(get_async_db)):
    """
    Async 게시글 목록 조회

    쿼리 작성법은 동일하고, await 유무만 다르다!
    """
    stmt = select(Post)
    result = await db.scalars(stmt)
    posts = result.all()
    return posts

@router.get("/{post_id}/lazy", response_model=PostDetailResponse)
async def get_post_lazy(post_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    ❌ lazy loading → async에서는 에러 발생!

    sync에서는 post.comments에 접근하면 자동으로 추가 쿼리가 날아가지만,
    async에서는 이벤트 루프 밖에서 동기 I/O를 할 수 없어서 에러 발생:
    → MissingGreenlet: greenlet_spawn has not been called

    """
    post = await db.get(Post, post_id)

    # 여기서 post.comments에 접근하면 lazy loading 시도 → 에러!
    return post

@router.get("/{post_id}/selectin", response_model=PostDetailResponse)
async def get_post_selectin(post_id: int, db: AsyncSession = Depends(get_async_db)):

    stmt = select(Post).where(Post.id == post_id).options(
        selectinload(Post.comments),
        selectinload(Post.post_tags).selectinload(PostTag.tag),
    )
    result = await db.scalars(stmt)
    post = result.one()
    return post

```

- router를 main.py에 등록한다.

---

### Async에서 lazy loading을 사용할 수 없다.

post.comments에 접근하면 SQLAlchemy가 DB 쿼리를 날려야 하는데,
이건 동기 속성 접근(그냥 .comments)이라 await를 쓸 수 없다.

```python
# Async에서:
post = await db.get(Post, 1)
print(post.comments)  # ← 에러! MissingGreenlet
```

### 해결: Eager Loading

접근하기 **전에** 미리 로드해 놓으면 된다.

```python
# 쿼리 시점에 comments를 함께 가져옴
stmt = select(Post).options(selectinload(Post.comments))
result = await db.scalars(stmt)
post = result.one()

print(post.comments)  # ← 이미 메모리에 있어서 추가 쿼리 없음. OK!
```

## 수정 로직

수정 이후에 응답할 때에도 마찬가지로 데이터를 eager loading해서 가져와야 한다.

```python
# routers/async_post_router.py
from mysite4.schemas.post import PostDetailResponse, PostListResponse, PostCreate

@router.put("/{post_id}/lazy", response_model=PostDetailResponse)
async def update_post_lazy(post_id: int, data: PostCreate, db: AsyncSession = Depends(get_async_db)):
    post = await db.get(Post, post_id)

    post.title = data.title
    post.content = data.content
    await db.commit()

    # 응답 시 comments, tags 접근 → lazy loading → 에러!
    return post

@router.put("/{post_id}/selectin", response_model=PostDetailResponse)
async def update_post_selectin(post_id: int, data: PostCreate, db: AsyncSession = Depends(get_async_db)):

    post = await db.get(Post, post_id)
    post.title = data.title
    post.content = data.content
    await db.commit()

    # commit 후 selectinload로 재조회
    stmt = select(Post).where(Post.id == post_id).options(
        selectinload(Post.comments),
        selectinload(Post.post_tags).joinedload(PostTag.tag),
    )
    result = await db.scalars(stmt)
    post = result.one()
    return post

```

---

## 요약: Async 전환 시 달라지는 것

```
Sync                              Async
────────────────────────────────────────────────────
psycopg2                      →   asyncpg
create_engine                 →   create_async_engine
sessionmaker                  →   async_sessionmaker
Session                       →   AsyncSession
def endpoint                  →   async def endpoint
db.scalars(stmt)              →   await db.scalars(stmt)
lazy loading OK               →   lazy loading NG → eager load 필수
expire_on_commit=True (기본)   →   expire_on_commit=False (필수)
time.sleep / requests         →   asyncio.sleep / httpx.AsyncClient
```

## async - await 사용해야 하는 것

- 클라이언트 - 서버, 서버 - DB 와 같이 서로 통신을 하는 경우에 비동기 처리를 해주면 좋음!
- 즉, 다른 무언가와 통신하는 것이 아닌 서버 내부에서 돌아가는 기능은 비동기 처리를 할 필요가 없다. ex) 비밀번호를 해시 처리해주는 함수
- 함수를 컨트롤 + 클릭으로 타고 들어가보면 async 함수인지 확인이 가능!
- db.add() 의 경우 async 함수가 아닌데, 데이터를 세션에 추가하는 기능이기 때문! 뒤에 commit, refresh 부분이 async 함수!