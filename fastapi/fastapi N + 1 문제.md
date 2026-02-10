## N+1 문제

N+1 문제는 데이터베이스 조회 시 발생하는 대표적인 성능 저하 현상이다. 1번의 쿼리로 N개의 데이터를 가져왔을 때, 각 데이터와 연관된 정보를 가져오기 위해 N번의 추가 쿼리가 발생하는 상황을 의미한다.

예를 들어 게시글 목록을 조회하는 상황에서 

- 게시글 10개를 가져오는 쿼리가 1번 실행된다.
- 각 게시글의 작성자 이름을 표시해야 한다면, 10번의 추가 쿼리가 발생하여 총 11번의 쿼리가 실행된다.

데이터가 많아질수록 서버의 응답 속도는 기하급수적으로 느려지게 된다.

---

## 지연 로딩 (Lazy Loading)

지연 로딩은 SQLAlchemy(및 다른 대부분의 ORM)의 기본 동작 방식이다. 연관된 객체가 실제로 참조되는 시점에 데이터베이스에 쿼리를 날려 데이터를 가져온다.

데이터가 정말로 필요한 순간까지 조회를 미루기 때문에 메모리 효율성을 높일 수 있다. 하지만 반복문 안에서 연관 객체에 접근할 경우 N+1 문제를 유발하는 주원인이 된다.

```python
# 게시글을 가져오는 쿼리 1번 실행
posts = db.scalars(select(Post)).all()

# 각 게시글마다 작성자(user)를 조회하는 추가 쿼리 N번 실행
for post in posts:
    print(post.user.name)
```

---

## 즉시 로딩 (Eager Loading)

즉시 로딩은 메인 데이터를 조회할 때 연관된 데이터까지 한꺼번에 가져오는 방식이며, N+1 문제를 방지하기 위해 필수적으로 사용되는 기법이다. 

SQLAlchemy에서는 joinedload와 selectinload 등을 통해 이를 구현한다.

---

### joinedload

joinedload는 SQL의 JOIN 구문을 사용하여 연관된 데이터를 한 번에 가져오는 방식이다.

여러 테이블을 하나의 쿼리로 결합하여 조회한다. 

주로 다대일(N:1) 혹은 일대일(1:1) 관계, 즉 주가 되는 객체와 다른 객체 하나만 연관이 있을 때 효율적이다.

단, 일대다(1:N)관계에서 활용하면 JOIN 결과의 중복 데이터 문제(Cartesian Product)가 발생할 수 있다.

- 게시글 - 유저의 관계와 같은 것. 다대일 인 경우 주가 되는 객체가 “다”에 해당하는 경우 사용.
- select * from post left outer join user on post.user_id = user_id 대충 이런 느낌으로 모든 데이터를 가져옴.
    - joinedload 안 썻을 때는 그냥 post들 가져오고, 각 post의 user 데이터에 접근할 때마다 다시 select 쿼리를 사용하는 식으로 데이터를 가져왔었다.

```python
from sqlalchemy.orm import joinedload

# 한 번의 JOIN 쿼리로 모든 데이터를 가져온다
stmt = select(Post).options(joinedload(Post.user))
posts = db.scalars(stmt).all()
```

여기서 중복 데이터 문제란 post에 대한 comments들이 여러 개가 있을 때, sql의 table 형태로 데이터를 가져오게 되면 post에 대한 데이터가 중복되어서 나타나는 것을 말한다.

---

### selectinload

selectinload는 메인 쿼리를 실행한 후, 연관된 데이터들의 ID를 모아 IN 절을 사용하는 별도의 쿼리를 실행하는 방식이다.

쿼리는 총 2번 발생하지만, 일대다, 다대다 관계 , 즉 주가 되는 객체와 다른 객체 여러 개가 연관이 있을 때 joinedload보다 성능이 우수한 경우가 많다. 

- 1:N, N:M 상황에 사용.
- 메인 쿼리(post) 실행, 데이터 가져올 쿼리(comment) 실행 후 in 절 사용. 총 2번의 쿼리로 데이터를 가져온다.
- select * from post / select * from comment where comment_post_id in (앞의 post에 있는 모든 id)
이런 느낌으로 쿼리가 실행됨.
    - selectinload 없이 하면 메인 쿼리(post) 실행 후 연관된 데이터의 ID와 일치하는 데이터들을 하나 하나 select ~ where 쿼리로 가져온다.

```python
from sqlalchemy.orm import selectinload

# 1. 게시글 조회 쿼리 실행
# 2. 조회된 게시글들의 작성자 ID를 모아 IN 절로 작성자들 조회 쿼리 실행
stmt = select(Post).options(selectinload(Post.comments))
posts = db.scalars(stmt).all()
```

---

### joinedload, selectinload 선택 기준

N+1 문제를 해결하기 위해서는 데이터의 관계에 따라 적절한 로딩 전략을 선택해야 한다.

1. 관계가 다대일(N:1) 혹은 일대일(1:1)인 경우
일반적으로 joinedload가 유리하다. 테이블을 합쳐서 한 번에 가져오는 것이 효율적이기 때문이다.
2. 관계가 일대다(1:N) 혹은 다대다(N:M)인 경우
일반적으로 selectinload가 권장된다. JOIN으로 인해 결과 행이 너무 많아지는 현상을 방지할 수 있다.
3. 비동기 환경
비동기 환경에서는 지연 로딩이 허용되지 않으므로, 연관 데이터가 필요하다면 반드시 즉시 로딩 옵션을 명시해야 한다.

---

## 복합 관계에서의 즉시 로딩 전략

하나의 테이블이 아니라 여러 테이블이 얽혀 있는 복잡한 구조에서는 관계의 방향에 따라 옵션을 나열하거나 연결하여 처리한다.

### 다중 로딩 (Multiple Loading)

하나의 엔티티를 기준으로 서로 다른 연관 엔티티들을 병렬적으로 가져올 때 사용한다. 
.options() 내부에 필요한 로딩 전략을 콤마(,)로 나열한다.

- 게시글을 조회하면서 작성자 정보(N:1)와 댓글 목록(1:N)이 모두 필요한 경우

```python
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

stmt = (
    select(Post)
    .options(
        joinedload(Post.user),       # 경로 1: 작성자 (JOIN)
        selectinload(Post.comments)  # 경로 2: 댓글 목록 (SELECT IN)
    )
)
```

---

### 연쇄 로딩 (Chained Loading)

연관된 엔티티를 거쳐 그 내부에 있는 깊은 단계의 엔티티까지 가져올 때 사용한다. 

마침표(.)를 사용해 로딩 경로를 직렬적으로 연결한다.

- 게시글 -> 작성자 -> 작성자의 프로필(1:1)까지 한꺼번에 필요한 경우

```python
from sqlalchemy.orm import joinedload

# Post에서 User를 거쳐 Profile까지 연속 로딩
stmt = (
    select(Post)
    .options(
        joinedload(Post.user).joinedload(User.profile)    
        # 1단계: 작성자 로드    # 2단계: 해당 작성자의 프로필까지 JOIN
    )
)
```

---

### 복합 활용

위 두 방식을 조합하여 복잡한 객체 그래프를 한 번에 완성한다.

```python
stmt = (
    select(Post)
    .options(
        # 작성자의 프로필까지 깊게 가져오고 (연쇄)
        joinedload(Post.user).joinedload(User.profile),

        # 동시에 댓글들과 그 댓글 작성자까지 가져오기 (다중 + 연쇄)
        selectinload(Post.comments).joinedload(Comment.author)
    )
)
```

---

## Lazy 로딩 방지

비동기 환경이나 엄격한 성능 관리가 필요한 프로젝트에서는 모델 정의 시 lazy loading을 방지하는 옵션을 사용하는 것이 표준이다. 즉시 로딩을 명시하지 않은 연관 데이터에 접근할 때, 지연 로딩을 수행하는 대신 에러를 발생시킨다.

```python
# 모델 정의 시
class Post(Base):
    __tablename__ = "posts"
    # 연관 데이터 접근 시 명시적 로딩이 없으면 에러 발생
    user: Mapped["User"] = relationship("User", lazy="raise_on_sql")
```

- `lazy` 옵션
    - select : 기본값. lazy loading을 허용한다.
    - joined : joinedload를 명시하지 않아도 사용한다.
    - selectin : selectinload를 명시하지 않아도 사용한다.

---

## SQLAlchemy에서의 일반 JOIN

- 데이터를 응답하는 것이 아니라, 단순 필터링(WHERE) 또는 정렬을 할 때는 `joinedload`가 아닌 일반 `join()`을 활용한다.

```python
stmt = (
    select(Post)
    .join(Post.user) # 필터링을 위한 조인
    .where(User.name == "admin")
)
```