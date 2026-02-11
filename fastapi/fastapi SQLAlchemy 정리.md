## SELECT

```python
from sqlalchemy import select, func, and_, or_, not_

stmt = select(User).where(User.age > 20)
users = db.scalars(stmt).all()
```

### 필터링 / 조건

```python
# 기본 조건
stmt = select(User).where(User.name == "alice")

# 여러 조건 (AND 자동 적용)
stmt = select(User).where(User.age > 20, User.role == "admin")

# 키워드 기반 필터
stmt = select(User).filter_by(name="alice")

# OR / NOT
stmt = select(User).where(or_(User.age < 20, User.age > 60))
stmt = select(User).where(not_(User.is_deleted))

# IN / BETWEEN
stmt = select(User).where(User.id.in_([1, 2, 3]))
stmt = select(User).where(User.age.between(20, 30))

# LIKE (ilike는 대소문자 무시)
stmt = select(User).where(User.name.like("%kim%"))
stmt = select(User).where(User.name.ilike("%kim%"))

# NULL 체크
stmt = select(User).where(User.email.is_(None))
stmt = select(User).where(User.email.is_not(None))
```

### 정렬 / 제한

```python
stmt = select(User).order_by(User.created_at.desc())
stmt = select(User).limit(10).offset(20)
stmt = select(User).distinct()
```

### 그룹핑 / 집계

```python
stmt = select(User.role, func.count()).group_by(User.role)
stmt = select(User.role, func.count()).group_by(User.role).having(func.count() > 1)
```

주요 집계 함수: `func.count()`, `func.sum()`, `func.avg()`, `func.min()`, `func.max()`

---

## JOIN

### 기본 JOIN

```python
# relationship 기반 (ON 절 자동 추론)
stmt = select(User).join(User.addresses)

# 명시적 ON 절
stmt = select(User).join(Address, User.id == Address.user_id)

# LEFT OUTER JOIN
stmt = select(User).outerjoin(Address)
```

### JOIN + WHERE 조합

실무에서 가장 자주 쓰이는 패턴이다. JOIN으로 테이블을 연결한 뒤 WHERE로 필터링한다.

```python
# 특정 도시에 주소를 가진 유저 조회                
stmt = (
    select(User)
    .join(User.addresses)
    .where(Address.city == "Seoul")
)

# JOIN + 여러 조건 조합
stmt = (
    select(User)
    .join(User.addresses)
    .where(
        Address.city == "Seoul",
        User.is_active == True,
    )
)

# LEFT JOIN + NULL 체크 (주소가 없는 유저 찾기)
stmt = (
    select(User)
    .outerjoin(User.addresses)
    .where(Address.id.is_(None))
)

# 여러 테이블 연쇄 JOIN
stmt = (
    select(User)
    .join(User.addresses)
    .join(Address.city_info)
    .where(City.country == "KR")
)
```

> **주의**: `join()` 후 `select(User)`만 하면 User 엔티티만 반환된다. JOIN된 테이블의 컬럼도 함께 가져오려면 `select(User, Address)` 형태로 작성해야 한다.
> 

---

## Eager Loading

N+1 문제를 방지하기 위해 관계 데이터를 미리 로드하는 전략이다.

```python
from sqlalchemy.orm import joinedload, selectinload, contains_eager
```

### joinedload

SQL JOIN을 사용하여 한 번의 쿼리로 관계 데이터를 함께 가져온다. 1:1, N:1 관계에 적합하다.

```python
stmt = select(User).options(joinedload(User.profile))
```

실행되는 SQL:

```sql
SELECT users.*, profiles.*
FROM users LEFT JOIN profiles ON users.id = profiles.user_id
```

### selectinload

별도의 `SELECT ... IN (...)` 쿼리를 실행하여 관계 데이터를 가져온다. 1:N 관계에서 권장되는 전략이다.

```python
stmt = select(User).options(selectinload(User.addresses))
```

실행되는 SQL:

```sql
SELECT * FROM users;
SELECT * FROM addresses WHERE addresses.user_id IN (1, 2, 3, ...);
```

### 중첩 로딩

```python
# User → addresses(selectin) → city(joined) 순서로 중첩 로딩
stmt = select(User).options(
    selectinload(User.addresses).joinedload(Address.city)
)
```

### contains_eager

`joinedload`와 달리, **이미 직접 작성한 JOIN 결과**에서 관계 데이터를 채우는 전략이다.

`joinedload`는 SQLAlchemy가 자동으로 JOIN을 추가하기 때문에, WHERE 조건으로 관계 데이터를 필터링할 수 없다. 반면 `contains_eager`는 개발자가 직접 JOIN과 WHERE를 제어할 수 있다.

```python
# ❌ joinedload: 자동 JOIN이므로 WHERE 필터가 관계 데이터에 적용되지 않는다
stmt = (
    select(User)
    .options(joinedload(User.addresses))
    .where(Address.city == "Seoul")  # 의도대로 동작하지 않음
)

# ✅ contains_eager: 직접 JOIN + WHERE로 필터링된 관계 데이터만 로딩한다
stmt = (
    select(User)
    .join(User.addresses)
    .where(Address.city == "Seoul")
    .options(contains_eager(User.addresses))
)
```

위 코드에서 `contains_eager`를 쓰는 이유는 다음과 같다:

1. `.join(User.addresses)` — 직접 JOIN을 작성하여 WHERE 조건 적용이 가능하다
2. `.where(Address.city == "Seoul")` — JOIN된 데이터를 필터링한다
3. `.options(contains_eager(User.addresses))` — 이미 JOIN으로 가져온 결과를 `user.addresses`에 채워 넣는다

`contains_eager`를 빼면 SQLAlchemy는 JOIN 결과와 relationship을 연결하지 못하고, `user.addresses` 접근 시 별도 쿼리(lazy load)를 다시 실행하게 된다.

---

## 단건 조회 메서드 비교

### `db.get()` — PK 조회 전용

가장 단순한 단건 조회 방법이다. PK로만 조회할 수 있으며, Identity Map(세션 캐시)에 이미 존재하면 DB 쿼리 없이 즉시 반환한다.

```python
user = db.get(User, 1)          # PK가 1인 User 조회
user = db.get(User, (1, "kr"))  # 복합 PK인 경우 튜플로 전달
```

- 결과가 없으면 `None`을 반환한다.
- `select()` 문을 작성할 필요가 없어 PK 단건 조회 시 가장 간결하다.
- 내부적으로 Identity Map을 먼저 확인하므로, 같은 세션 내에서 동일 PK를 반복 조회해도 쿼리가 한 번만 실행된다.

### Result 메서드 비교

 `db.scalars(stmt)` 가 반환하는 `ScalarResult` 에서 호출한다.

| 메서드 | 결과 없음 | 1건 | 2건 이상 |
| --- | --- | --- | --- |
| `first()` | `None` | 반환 | 첫 건만 반환 (에러 없음) |
| `one()` | ❌ `NoResultFound` | 반환 | ❌ `MultipleResultsFound` |
| `one_or_none()` | `None` | 반환 | ❌ `MultipleResultsFound` |

### 실전 선택 가이드

```python
# PK로 단건 조회 (가장 간결, 세션 캐시 활용)
user = db.get(User, 1)

# 임의 조건으로 단건 조회 (PK가 아닌 조건일 때)
user = db.scalar(select(User).where(User.email == "alice@test.com"))

# "정확히 1건이어야 한다" → 없거나 많으면 버그이므로 예외를 던진다
user = db.scalars(stmt).one()

# "0건 또는 1건" → 없을 수 있지만 2건 이상이면 버그다
user = db.scalars(stmt).one_or_none()

# "있으면 첫 번째, 없으면 None" → 여러 건이어도 상관없다
user = db.scalars(stmt).first()

# "전체 목록"
users = db.scalars(stmt).all()
```