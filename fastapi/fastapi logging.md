## Logging

- 프로그램이 실행되는 동안 일어나는 일들을 기록하는 것

### 로깅이 사용되는 곳

- 장애 원인 파악
    
    에러가 발생했을 때 어디서, 왜 터졌는지 추적할 수 있다
    
- 사용자 문의 대응
    
    "언제, 무슨 요청이 와서, 어떤 결과가 나왔는지" 확인 가능하다
    
- 보안 추적
    
    누가 언제 로그인했는지, 비정상적인 접근이 있었는지 기록
    
- 성능 모니터링
    
    어떤 API가 느린지, 요청이 몰리는 시간대가 언제인지 파악
    
- 디버깅
    
    개발 중에 코드 흐름을 따라가며 변수 값 확인
    

---

## Python logging 기본

### 로그 레벨

Python `logging`에는 5단계의 심각도가 있다.

| 레벨 | 용도 | 예시 |
| --- | --- | --- |
| `DEBUG` | 개발 중 상세 정보 | `logger.debug("SQL 쿼리 결과: ...")` |
| `INFO` | 정상 동작 기록 | `logger.info("로그인 성공: user_id=1")` |
| `WARNING` | 주의가 필요한 상황 | `logger.warning("로그인 실패: 잘못된 비밀번호")` |
| `ERROR` | 에러 발생 | `logger.error("DB 연결 실패")` |
| `CRITICAL` | 치명적 오류 | `logger.critical("서버 시작 불가")` |

로그 레벨을 설정하면, **그 레벨 이상의 로그만 출력**된다.

```python
# INFO로 설정하면 → INFO, WARNING, ERROR, CRITICAL만 출력
# DEBUG는 출력되지 않음
logging.basicConfig(level=logging.INFO)
```

---

## FastAPI에서 로깅 설정하기

- 로깅 설정 파일 만들기
    
    프로젝트 루트에 `logging_config.py` 파일을 만든다.
    

```python
# logging_config.py
import logging

def setup_logging():
    """앱 전체 로깅 설정"""

    # 포맷 설정: 시간 | 레벨 | 모듈명 | 메시지
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)-8s %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 콘솔 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # 루트 로거 설정
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)

    # SQLAlchemy 로그는 WARNING 이상만 (쿼리 로그가 너무 많아서)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
```

- `%(asctime)s` - 로그 발생 시간
- `%(levelname)-8s` - 로그 레벨 (8칸 좌측 정렬)
- `%(name)s` - 로거 이름 (모듈 경로)
- `%(message)s` - 실제 로그 메시지
- `datefmt` - 시간 출력 형식

- main.py에서 로깅 초기화

```python
# main.py
from fastapi import FastAPI
from logging_config import setup_logging

# 앱 시작 시 로깅 설정
setup_logging()

app = FastAPI()
# ... 나머지 코드
```

이제 앱이 시작되면 로깅이 자동으로 활성화된다.

### 서비스 레이어에 로깅 추가하기

- auth_service.py에 로깅 추가
- __name__ ⇒ 파일의 이름이 들어감. (아래 예시에선 auth_service)

```python
# mysite4/services/auth_service.py
import logging

logger = logging.getLogger(__name__)  # 파일 상단에 한 번만 선언

class AuthService:
    def signup(self, db: Session, data: UserCreate) -> User:
        logger.info(f"회원가입 시도: {data.email}")

        existing_user = user_repository.find_by_email(db, data.email)
        if existing_user:
            logger.warning(f"회원가입 실패 - 이메일 중복: {data.email}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="이미 등록된 이메일입니다.",
            )

        hashed_password = self._hash_password(data.password)
        new_user = User(email=data.email, password=hashed_password)
        user_repository.save(db, new_user)
        db.commit()
        db.refresh(new_user)

        logger.info(f"회원가입 성공: user_id={new_user.id}, email={data.email}")
        return new_user

    def login(self, db: Session, data: UserLogin) -> str:
        logger.info(f"로그인 시도: {data.email}")

        user = user_repository.find_by_email(db, data.email)
        if not user:
            logger.warning(f"로그인 실패 - 존재하지 않는 이메일: {data.email}")
            raise HTTPException(...)

        if not self._verify_password(data.password, user.password):
            logger.warning(f"로그인 실패 - 잘못된 비밀번호: {data.email}")
            raise HTTPException(...)

        access_token = self._create_access_token(user.id)
        logger.info(f"로그인 성공: user_id={user.id}")
        return access_token

    def get_current_user(self, db: Session, token: str) -> User:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: int = int(payload.get("sub"))
        except jwt.ExpiredSignatureError:
            logger.warning("토큰 만료됨")
            raise HTTPException(...)
        except jwt.InvalidTokenError:
            logger.warning("유효하지 않은 토큰")
            raise HTTPException(...)

        user = user_repository.find_by_id(db, user_id)
        if not user:
            logger.warning(f"토큰의 user_id에 해당하는 사용자 없음: {user_id}")
            raise HTTPException(...)

        return user
```

- post2_service.py에 로깅 추가

```python
# mysite4/services/post2_service.py
import logging

logger = logging.getLogger(__name__)

class Post2Service:
    def create_post(self, db: Session, data: Post2Create, current_user: User):
        logger.info(f"게시글 작성: user_id={current_user.id}, title={data.title}")
        # ... 기존 로직
        logger.info(f"게시글 작성 완료: post_id={new_post.id}")
        return new_post

    def update_post(self, db: Session, id: int, data: Post2Create, current_user: User):
        post = self.read_post_by_id(db, id)

        if post.user_id != current_user.id:
            logger.warning(
                f"게시글 수정 권한 없음: user_id={current_user.id}, post_id={id}, owner_id={post.user_id}"
            )
            raise HTTPException(...)

        logger.info(f"게시글 수정: post_id={id}, user_id={current_user.id}")
        # ... 기존 로직
        return updated_post

    def delete_post(self, db: Session, id: int, current_user: User):
        post = self.read_post_by_id(db, id)

        if post.user_id != current_user.id:
            logger.warning(
                f"게시글 삭제 권한 없음: user_id={current_user.id}, post_id={id}"
            )
            raise HTTPException(...)

        logger.info(f"게시글 삭제: post_id={id}, user_id={current_user.id}")
        # ... 기존 로직
```

---

## 로그를 파일에 저장하기

콘솔 로그는 서버가 꺼지면 사라진다. 파일에도 저장하면 나중에 확인할 수 있다.

- 파일 핸들러 추가
    
    `logging_config.py`를 수정한다.
    

```python
# logging_config.py
import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    """앱 전체 로깅 설정"""

    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)-8s %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 1. 콘솔 핸들러 (기존과 동일)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # 2. 파일 핸들러 (새로 추가)
    file_handler = RotatingFileHandler(
        filename="app.log",       # 로그 파일 이름
        maxBytes=10 * 1024 * 1024, # 파일 최대 크기: 10MB
        backupCount=5,             # 백업 파일 최대 5개 유지
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    # 루트 로거 설정
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)  # 파일 핸들러 추가

    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("watchfiles").setLevel(logging.WARNING)
```

- RotatingFileHandler란?
    
    일반 `FileHandler`는 로그 파일이 끝없이 커진다. `RotatingFileHandler`는 파일이 지정된 크기에 도달하면 자동으로 새 파일로 전환한다.
    
    ```
    app.log       ← 현재 로그 (최대 10MB)
    app.log.1     ← 이전 로그
    app.log.2     ← 그 이전 로그
    app.log.3     ← ...
    app.log.4
    app.log.5     ← 가장 오래된 로그 (이후 자동 삭제)
    ```
    
    `backupCount=5`이면 최대 5개의 백업 파일을 유지한다.
    

- .gitignore에 로그 파일 추가
    
    로그 파일은 Git에 올리지 않는다.
    

## 현재 코드의 문제점

지금 우리 서비스 레이어 코드를 보자.

```python
# mysite4/services/post2_service.py (현재 코드)
from fastapi import HTTPException, status

class Post2Service:
    def read_post_by_id(self, db: Session, id: int):
        post = post2_repository.find_by_id(db, id)
        if not post:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, "존재하지 않는 게시글입니다."
            )
        return post

    def update_post(self, db: Session, id: int, data: Post2Create, current_user: User):
        post = self.read_post_by_id(db, id)
        if post.user_id != current_user.id:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN, "본인의 게시글만 수정할 수 있습니다."
            )
        ...
```

```python
# mysite4/services/auth_service.py (현재 코드)
from fastapi import HTTPException, status

class AuthService:
    def signup(self, db: Session, data: UserCreate) -> User:
        existing_user = user_repository.find_by_email(db, data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="이미 등록된 이메일입니다.",
            )
        ...
```

### 무엇이 문제인가?

- **서비스 레이어가 HTTP를 알고 있다**
    
    `HTTPException`은 FastAPI(웹 프레임워크)의 개념이다. 서비스 레이어는 비즈니스 로직만 담당해야 하는데, HTTP 상태 코드(404, 403, 409)를 직접 다루고 있다.
    
    ```
    이상적인 계층 분리:
      Router  → HTTP 요청/응답을 처리 (상태 코드, 응답 형식)
      Service → 비즈니스 로직만 담당 (HTTP를 몰라야 함)
      Repository → DB 접근만 담당
    ```
    

- **에러 응답 형식이 제각각**
    
    FastAPI의 `HTTPException`은 기본적으로 이렇게 응답한다.
    
    ```json
    {"detail": "존재하지 않는 게시글입니다."}
    ```
    
    하지만 Pydantic 검증 실패 시에는 완전히 다른 형식으로 응답한다.
    
    ```json
    {
      "detail": [
        {
          "loc": ["body", "email"],
          "msg": "value is not a valid email address",
          "type": "value_error.email"
        }
      ]
    }
    ```
    
    프론트엔드 개발자 입장에서는 에러 응답 형식이 일관되지 않으면 처리하기 어렵다.
    

- **같은 종류의 에러가 여러 곳에 흩어져 있다**
    
    "존재하지 않는 리소스"에 대한 에러가 `post2_service.py`, `post_service.py`, `comment_service.py` 등 여러 파일에 중복되어 있다.
    

---

## 커스텀 예외 클래스 만들기

### 예외 클래스 정의

`mysite4/exceptions.py` 파일을 새로 만든다.

```python
# mysite4/exceptions.py

class AppException(Exception):
    """앱 전체 예외의 부모 클래스"""

    status_code: int = 500  # 기본값: 500 Internal Server Error

    def __init__(self, detail: str):
        self.detail = detail

class NotFoundException(AppException):
    """리소스를 찾을 수 없을 때"""
    status_code = 404

class DuplicateException(AppException):
    """중복된 데이터가 있을 때"""
    status_code = 409

class UnauthorizedException(AppException):
    """인증 실패 (로그인이 안 되었거나 토큰이 유효하지 않을 때)"""
    status_code = 401

class ForbiddenException(AppException):
    """권한 없음 (로그인은 되었지만 해당 작업을 할 권한이 없을 때)"""
    status_code = 403
```

- 이 구조의 장점
    - **의미가 명확함** - `NotFoundException`은 누가 봐도 "없다"는 뜻
    - **재사용 가능** - 어떤 서비스에서든 같은 예외를 사용

---

## 전역 예외 핸들러 등록하기

커스텀 예외가 발생했을 때, FastAPI가 적절한 HTTP 응답으로 변환하도록 핸들러를 등록한다.

### 에러 응답 스키마 정의

먼저, 모든 에러 응답이 따를 통일된 형식을 정한다.

```python
# mysite4/schemas/error.py

from pydantic import BaseModel

class ErrorResponse(BaseModel):
    detail: str

    model_config = {"json_schema_extra": {"examples": [{"detail": "에러 메시지"}]}}
```

### 예외 핸들러 파일 만들기

`mysite4/exception_handlers.py` 파일을 만든다.

```python
# mysite4/exception_handlers.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from mysite4.exceptions import AppException

def register_exception_handlers(app: FastAPI):
    """앱에 예외 핸들러들을 등록하는 함수"""

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
        
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"detail": "서버 내부 오류가 발생했습니다."}
        )
```

### main.py에 등록

```python
# main.py
from fastapi import FastAPI
from mysite4.exception_handlers import register_exception_handlers

app = FastAPI()

# 예외 핸들러 등록
register_exception_handlers(app)

# 라우터 등록
app.include_router(post_router)
# ...
```

### 동작 흐름

```
서비스에서 raise NotFoundException("존재하지 않는 게시글입니다.")
    ↓
NotFoundException은 AppException의 자식이므로, app_exception_handler()가 실행됨
    ↓
exc.status_code = 404, exc.detail = "존재하지 않는 게시글입니다."
    ↓
클라이언트에 JSON 응답 전달: {"detail": "존재하지 않는 게시글입니다."} (404)
```

---

## 서비스 레이어 리팩토링

이제 서비스 레이어에서 `HTTPException` 대신 커스텀 예외를 사용한다.

### post2_service.py 리팩토링

```python
# mysite4/services/post2_service.py

# 수정 전
from fastapi import HTTPException, status

# 수정 후
from mysite4.exceptions import NotFoundException, ForbiddenException

class Post2Service:
    def read_post_by_id(self, db: Session, id: int):
        post = post2_repository.find_by_id(db, id)
        if not post:
            # 수정 전: raise HTTPException(status.HTTP_404_NOT_FOUND, "존재하지 않는 게시글입니다.")
            # 수정 후:
            raise NotFoundException("존재하지 않는 게시글입니다.")
        return post

    def update_post(self, db: Session, id: int, data: Post2Create, current_user: User):
        post = self.read_post_by_id(db, id)

        if post.user_id != current_user.id:
            # 수정 전: raise HTTPException(status.HTTP_403_FORBIDDEN, "본인의 게시글만 수정할 수 있습니다.")
            # 수정 후:
            raise ForbiddenException("본인의 게시글만 수정할 수 있습니다.")

        # ... 나머지 로직 동일

    def delete_post(self, db: Session, id: int, current_user: User):
        post = self.read_post_by_id(db, id)

        if post.user_id != current_user.id:
            raise ForbiddenException("본인의 게시글만 삭제할 수 있습니다.")

        # ... 나머지 로직 동일
```

### auth_service.py 리팩토링

```python
# mysite4/services/auth_service.py

# 수정 전
from fastapi import HTTPException, status

# 수정 후
from mysite4.exceptions import DuplicateException, UnauthorizedException

class AuthService:
    def signup(self, db: Session, data: UserCreate) -> User:
        existing_user = user_repository.find_by_email(db, data.email)
        if existing_user:
            raise DuplicateException("이미 등록된 이메일입니다.")
        # ... 나머지 동일

    def login(self, db: Session, data: UserLogin) -> str:
        user = user_repository.find_by_email(db, data.email)
        if not user:
            raise UnauthorizedException("이메일 또는 비밀번호가 올바르지 않습니다.")

        if not self._verify_password(data.password, user.password):
            raise UnauthorizedException("이메일 또는 비밀번호가 올바르지 않습니다.")

        access_token = self._create_access_token(user.id)
        return access_token

    def get_current_user(self, db: Session, token: str) -> User:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: int = int(payload.get("sub"))
            if user_id is None:
                raise UnauthorizedException("유효하지 않은 토큰입니다.")
        except jwt.ExpiredSignatureError:
            raise UnauthorizedException("토큰이 만료되었습니다.")
        except jwt.InvalidTokenError:
            raise UnauthorizedException("유효하지 않은 토큰입니다.")

        user = user_repository.find_by_id(db, user_id)
        if not user:
            raise UnauthorizedException("사용자를 찾을 수 없습니다.")

        return user
       
```

---

## Pydantic ValidationError 처리

Pydantic 검증 실패(잘못된 이메일 형식, 필수 필드 누락 등)에 대한 에러 응답도 통일할 수 있다.

FastAPI는 Pydantic 에러를 자동으로 422 응답으로 변환하는데, 이 형식을 다음과 같이 커스텀할 수 있다.

- 단, Pydantic 기본 에러 형식은 그대로 쓰는 경우도 많다. 프론트엔드 팀과 합의해서 정하면 된다.

```python
# mysite4/exception_handlers.py

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from mysite4.exceptions import AppException

def register_exception_handlers(app: FastAPI):
    """앱에 예외 핸들러들을 등록하는 함수"""

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_handler(request: Request, exc: RequestValidationError):
        """Pydantic 검증 실패 시 에러 메시지를 간결하게 변환"""
        errors = exc.errors()
        first_error = errors[0]
        field = " → ".join(str(loc) for loc in first_error["loc"])
        message = first_error["msg"]

        return JSONResponse(
            status_code=422,
            content={"detail": f"{field}: {message}"},
        )
        
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unexpected Error: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "서버 내부 오류가 발생했습니다."}
        )        
```

---

## 로깅 추가

```python
# mysite4/exception_handlers.py

# 라이브러리 추가
import logging  

# 로거 생성
logger = logging.getLogger("mysite4")

def register_exception_handlers(app: FastAPI):
    
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        # 비즈니스 예외 로깅 (사용자 실수 등)
        logger.warning(f"Business Exception: {exc.detail} (Path: {request.url.path})")
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_handler(request: Request, exc: RequestValidationError):
        # 유효성 검사 실패 로깅
        logger.info(f"Validation Failed: {request.url.path}")
        errors = exc.errors()
        first_error = errors[0]
        field = " → ".join(str(loc) for loc in first_error["loc"])
        message = first_error["msg"]

        return JSONResponse(
            status_code=422,
            content={"detail": f"{field}: {message}"},
        )
        
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unexpected Error: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "서버 내부 오류가 발생했습니다."}
        )
```

- **`exc_info=True`**
    - `logger.error` 호출 시 이 옵션을 주면 에러가 발생하기까지의 함수 호출 기록(Stack Trace)이 모두 로그에 찍힌다. 
    500 에러가 났을 때 "어느 파일의 몇 번째 줄"에서 터졌는지 바로 알 수 있게 해준다.
    - unhandled_exception_handler()을 사용해서 Exception을 관리하는 경우 반드시 추가해줘야 하는 옵션.
- 예시로 3개 정도만 관리하도록 했지만, exception 사용 방법은 인터넷에 찾아보면 많이 있으니까 참고해보자.