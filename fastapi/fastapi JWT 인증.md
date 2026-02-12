## 인증된 사용자만 접근 가능한 API 만들기

로그인 후 받은 토큰으로 "나 로그인한 사용자야"를 증명하는 과정이다.

header를 통해 들어온 token을 디코드하고 서명을 검증한다.

```python
"Authorization : Bearer {token}"
```

### 토큰 검증 로직

JWT를 디코드하여 검증한다.

```python
# services/auth_service.py

    def get_current_user(self, db: Session, token: str) -> User:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: int = int(payload.get("sub"))

            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="유효하지 않은 토큰입니다.",
                )
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="토큰이 만료되었습니다.",
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="유효하지 않은 토큰입니다.",
            )

        user = user_repository.find_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="사용자를 찾을 수 없습니다.",
            )

        return user
```

---

### 재사용 가능한 인증 의존성 - Dependencies

FastAPI의 `Depends`를 활용해서 **어떤 라우터에서든 재사용 가능한 인증 함수**를 만들 수 있다.

- `OAuth2PasswordBearer`
    
    HTTP 요청의 `Authorization` 헤더에서 `Bearer {토큰}` 형식의 토큰을 자동으로 추출한다
    
    - tokenUrl은 Swagger UI에서 사용하는 로그인에 대한 endpoint이다.
    우리는 사용하지 않는 옵션이지만, 필수인자이다.

```python
# mysite4.dependencies.py

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from mysite4.services.auth_service import auth_service
from mysite4.models.user import User

# Authorization 헤더에서 Bearer 토큰을 자동으로 추출한다.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    return auth_service.get_current_user(db, token)
```

---

### Router (인증이 필요한 엔드포인트)

```python
# routers/user_router.py

from fastapi import APIRouter, Depends, status
from mysite4.dependencies import get_current_user
from mysite4.models import User
from mysite4.schemas.user import UserResponse

router = APIRouter(prefix="")

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
```

- main.py에 user_router를 등록한다.

```python
# main.py

from mysite4.routers.user_router import router as user_router # 추가

app = FastAPI()

app.include_router(user_router)  # 추가
```

### 로그인 필수 엔드포인트

- API 엔드포인트에 대해 로그인을 필수로 만들고 싶다면 `Depends(get_current_user)`를 추가해주면 된다.
즉, 해당 엔드포인트는 **토큰이 없으면 접근할 수 없는** 보호된 API가 된다.

```python
@router.post("/some/endpoint")
def some_function(
    data: Schema,
    current_user: User = Depends(get_current_user),  # 이 한 줄 추가
    db: Session = Depends(get_db)
):
    # current_user로 작성자 정보를 활용할 수 있다
    ...
```