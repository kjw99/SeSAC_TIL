페이지네이션은 데이터베이스에 저장된 수많은 데이터를 한 번에 불러오지 않고, 사용자가 요청한 만큼만 끊어서 보여주는 기술이다. 서버의 부하를 줄이고 클라이언트의 응답 속도를 높이는 데 필수적이다.

### 설치

프로젝트 루트에서 설치한다.

```bash
uv add fastapi-pagination
```

### 기본 설정 및 main.py 등록

이 라이브러리를 사용하기 위해서는 FastAPI 인스턴스에 페이지네이션 기능을 등록해야 한다.

```python
from fastapi import FastAPI
from fastapi_pagination import add_pagination

app = FastAPI()

# 라이브러리가 API 엔드포인트의 쿼리 매개변수를 처리할 수 있도록 등록한다.
add_pagination(app)
```

---

## 활용 코드 예시 및 Query 파라미터

- 반환할 데이터 타입을 `Page`로 감싼다. 기존에 list[UserResponse]를 사용했다면 이를 Page[UserResponse]로 변경한다.
- 함수 내부에서 `paginate()`를 사용하여 데이터를 반환한다. 별도의 계산 로직 없이 데이터 소스(리스트 또는 쿼리)를 통째로 넣으면 된다.
- API 호출 시 기본적으로 사용되는 Query 파라미터는 page와 size이다.
예: /users?page=1&size=1
- 아래 코드만 보면 햇갈릴 수 있는데, paginate()는 repository 쪽에서 해줘야 한다. SQL의 결과를 paginate() 하는 것!
    - 아래 코드는 router, service, repository 구분 없이 한 파일에 다 쑤셔넣은 경우
    - 기존엔 db.scalars~~ 라면, paginate(db, stmt) 이런식으로 쓰자.

- 우리 코드에서는 `repository` 내부의 로직을 다음과 같이 변경한다
    - 기존 방식
        
        ```python
        def get_users(db: Session):
            stmt = select(User).options(selectinload(User.profile))
            return db.scalars(stmt).all()  # 리스트 반환
        ```
        
    - 변경된 방식
        
        ```python
        from fastapi_pagination.ext.sqlalchemy import paginate
        
        def get_users(db: Session):
            stmt = select(User).options(selectinload(User.profile))
            return paginate(db, stmt)  # Page 객체 반환
        ```
        

---

### 응답 데이터 구조

라이브러리를 적용하면 클라이언트는 다음과 같은 구조의 응답을 받게 된다.

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| items | array | 현재 페이지에 포함된 데이터 객체들의 리스트 |
| total | integer | 전체 데이터 개수 |
| page | integer | 현재 페이지 번호 (기본값: 1) |
| size | integer | 한 페이지에 보여줄 데이터의 개수 (기본값: 50) |
| pages | integer | 전체 페이지 개수 |