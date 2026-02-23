지금 우리 프로젝트에서는 `main.py`에서 이렇게 테이블을 만들고 있다.

```python
# main.py
from database import engine
from mysite4 import models

models.Base.metadata.create_all(bind=engine)
```

이 방식은 테이블이 없으면 새로 만들어주는 코드이다.

테이블에 변경이 있을 경우에는 다음 명령어를 사용하여 DB를 초기화 후 진행하였었다.

```python
models.Base.metadata.drop_all(bind=engine)
```

---

## Alembic

**Alembic**은 SQLAlchemy를 위한 DB 마이그레이션 도구이다.

- 모델을 변경하면 자동으로 변경 사항을 감지해서 마이그레이션 파일을 생성해준다
- 마이그레이션 파일을 실행하면 원래 있던 데이터를 유지하면서 DB 구조를 변경한다
- 이전 버전으로 롤백도 가능하다.

### migration

- DB에서의 마이그레이션은 DB 구조(스키마)를 한 상태에서 다른 상태로 변경하는 작업
또는 DB 구조를 변경하는 작업을 코드로 기록한 것을 의미한다.

### 설치 및 초기 설정

- 설치

```bash
uv add alembic
```

- 프로젝트 루트 디렉토리에서 실행한다.

```bash
uv run alembic init alembic
```

이 명령어를 실행하면 다음과 같은 파일/폴더가 생성된다.

```
fastapi_basic/
├── alembic/                  # Alembic 관련 파일들
│   ├── versions/             # 마이그레이션 파일들이 쌓이는 폴더
│   ├── env.py                # Alembic 설정 (수정 필요)
│   ├── script.py.mako        # 마이그레이션 파일 템플릿
│   └── README
├── alembic.ini               # Alembic 설정 파일 (수정 필요)
├── database.py
├── main.py
└── ...
```

- `alembic.ini` 설정
    
    `alembic.ini` 파일을 열어서 `sqlalchemy.url` 부분을 찾아 비워둔다.
    
    아래 env.py에서 동적으로 설정할 예정이다.
    

```
sqlalchemy.url =
```

- env.py 설정
    
    `alembic/env.py` 파일을 수정해야 한다.
    
    1. **모델 메타데이터** - 우리 모델들을 Alembic이 인식하도록 연결
    2. **DB 연결 URL** - `.env` 파일에서 읽어오기
    

### 모델 메타데이터 연결

- `alembic/env.py`를 열고 상단에 다음을 추가한다.

```python
import os
from dotenv import load_dotenv
from mysite4 import models 
from nplusone.models import DemoUser, DemoComment, DemoPost

# .env 파일 로드
load_dotenv()
```

- `target_metadata` 부분을 찾아서 수정한다.

```python
target_metadata = models.Base.metadata
```

### **DB 연결 URL**

`run_migrations_online()` 함수 안에서 DB URL을 동적으로 설정한다.

기존 코드:

```python
def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
```

수정 후:

```python
def run_migrations_online() -> None:
    # .env에서 DB URL을 가져와서 alembic 설정에 주입
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = os.getenv("DATABASE_URL")

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
```

설정이 잘 되었는지 확인해보자.

```bash
uv run alembic current
```

에러 없이 실행되면 설정이 완료된 것이다. 

---

## 첫 마이그레이션 만들기

### 기존 테이블이 이미 있는 경우

우리 프로젝트는 이미 `create_all()`로 테이블을 만들어 놓은 상태이다.
이 상태에서 Alembic을 처음 도입할 때는 **"현재 DB 상태를 기준점으로 잡는"** 초기 마이그레이션을 만들어야 한다.

- 자동 마이그레이션 생성

```bash
uv run alembic revision --autogenerate -m "init"
```

- revision - 새 마이그레이션 파일을 만든다
- --autogenerate - 모델과 DB를 비교해서 자동으로 변경사항을 감지한다
- -m "init" - 마이그레이션에 붙일 설명 메시지 (commit 메시지처럼)

실행하면 `alembic/versions/` 폴더에 파일이 생성된다.

```
alembic/versions/
└── a1b2c3d4e5f6_init.py
```

- 마이그레이션 기준점 등록

```bash
uv run alembic stamp head
```

- stamp - 마이그레이션을 실제로 실행하지 않고, DB에 "적용 완료" 표시만 남긴다
- head - 가장 최신 마이그레이션을 가리킨다

---

## DB 변경 후 마이그레이션 적용하기

- `mysite4/models/user.py`에 `nickname` 컬럼을 추가한다.

```python

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)

    nickname: Mapped[str | None] = mapped_column(String(50), nullable=True)  # 새로 추가

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    # User가 작성한 Post2 목록 (1:N)
    posts2: Mapped[list["Post2"]] = relationship(back_populates="user")

```

- 마이그레이션을 자동 생성한다.

```bash
uv run alembic revision --autogenerate -m "add nickname to users"
```

- 마이그레이션을 적용한다.

```bash
uv run alembic upgrade head
```

이제 실제 DB의 `users` 테이블에 `nickname` 컬럼이 추가된다. 

기존 데이터는 그대로 유지되면서, 새 컬럼만 추가된다.

- uv 환경에서 했으니까 uv run이 앞에 붙어야 함!

---

## 롤백하기

실수로 잘못된 마이그레이션을 적용했다면, 되돌릴 수 있다.

### 한 단계 되돌리기

```bash
uv run alembic downgrade -1
```

- `1`은 "현재 버전에서 한 단계 이전으로"라는 뜻이다. `downgrade()` 함수가 실행된다.

### 특정 버전으로 되돌리기

```bash
uv run alembic downgrade a1b2c3d4e5f6
```

특정 revision ID를 지정해서 그 시점으로 되돌릴 수 있다.

### 마이그레이션 히스토리 확인

```bash
uv run alembic history
```

모든 마이그레이션의 목록과 순서를 보여준다.

---

## 앞으로의 작업 흐름

- 만약 DB가 이미 존재한다면 아래 명령어를 1회 진행한다.
    1. uv run alembic revision --autogenerate -m "init"
    2. uv run alembic stamp head

- 위의 과정을 거쳤거나 DB가 존재하지 않은 상태였으면
    1. 모델 수정 (Python 코드)
    2. uv run alembic revision --autogenerate -m "변경 설명"
    3. alembic upgrade head
    - 주로 이 방식을 사용하게 될 것임.
    - 플젝 초기에는 DB 변경이 잦으니까 그럴 때는 아예 alembic도 안 쓰다 나중에 안정되면 쓰는 경우도 있다.

# main.py에서 create_all 제거하기

Alembic을 도입했으면, `main.py`에서 `create_all()`을 제거해야 한다.

```python
# main.py 

models.Base.metadata.create_all(bind=engine)  # 이 줄을 제거 또는 주석처리
```