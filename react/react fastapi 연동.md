## React + FastAPI 연동

- 지금까지는 외부 API에서 데이터를 가져왔다
- 이번에는 **직접 만든 FastAPI 서버**와 React를 연결하여 Todo 앱을 만들어 본다

---

## FastAPI 서버 만들기

### 프로젝트 생성 및 패키지 설치

- react 프로젝트의 루트가 아닌 상위의 디렉토리(또는 다른 편한 위치)에서 실행한다.

```bash
uv init todo-backend
cd todo-backend
uv add "fastapi[standard]" sqlalchemy psycopg2-binary
```

### DB 생성

- PostgreSQL에 `todo` 데이터베이스를 생성한다

### [main.py](http://main.py/)

```python
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, Mapped, mapped_column, DeclarativeBase, sessionmaker

# --- DB 설정 ---

engine = create_engine("postgresql://postgres:{비밀번호}@localhost:5432/todo")
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

# --- FastAPI 설정 ---

app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 모델 ---

class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    done: Mapped[bool] = mapped_column(default=False)

Base.metadata.create_all(bind=engine)

# --- API ---

@app.get("/todos")
def get_todos(db: Session = Depends(get_db)):
    return db.scalars(select(Todo)).all()

@app.post("/todos")
def create_todo(data: dict, db: Session = Depends(get_db)):
    todo = Todo(text=data["text"])
    with db.begin():
        db.add(todo)
    db.refresh(todo)
    return todo

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, data: dict, db: Session = Depends(get_db)):
    with db.begin():
        todo = db.scalar(select(Todo).where(Todo.id == todo_id))
        todo.text = data["text"]
    db.refresh(todo)
    return todo

@app.put("/todos/{todo_id}/toggle")
def toggle_todo(todo_id: int, db: Session = Depends(get_db)):
    with db.begin():
        todo = db.scalar(select(Todo).where(Todo.id == todo_id))
        todo.done = not todo.done
    db.refresh(todo)
    return todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    with db.begin():
        todo = db.scalar(select(Todo).where(Todo.id == todo_id))
        db.delete(todo)
    return {"message": "삭제 완료"}
```

### 서버 실행

```bash
uv run fastapi dev
```

- `http://localhost:8000/docs`에서 API 문서를 확인할 수 있다

---

## React에서 연동하기

- axios와 useEffect를 사용하여 FastAPI 서버와 통신한다
- 서버 주소: `http://localhost:8000`

### 할 일 목록 가져오기 예시

```jsx
import { useState, useEffect } from "react";
import axios from "axios";

const API_URL = "http://localhost:8000/todos";

const TodoList = () => {
  const [todos, setTodos] = useState([]);

  const fetchTodos = async () => {
    const response = await axios.get(API_URL);
    setTodos(response.data);
  };

  useEffect(() => {
    fetchTodos();
  }, []);

  return (
    <ul>
      {todos.map((todo) => (
        <li key={todo.id}>{todo.text}</li>
      ))}
    </ul>
  );
};

export default TodoList;
```

---

## CORS (Cross-Origin Resource Sharing)

### 출처(Origin)

- **프로토콜 + 도메인 + 포트**를 합친 것을 출처라고 한다

| URL | 출처 |
| --- | --- |
| `http://localhost:5173/about` | `http://localhost:5173` |
| `http://localhost:8000/todos` | `http://localhost:8000` |
- 위 두 URL은 포트가 다르므로 **서로 다른 출처이다.**

### 왜 차단하는가?

- 브라우저는 보안을 위해 **다른 출처로의 요청을 기본적으로 차단**한다 (Same-Origin Policy)
- 예: 악성 사이트가 사용자 브라우저를 통해 은행 API를 몰래 호출하는 것을 방지한다
- React(`localhost:5173`)에서 FastAPI(`localhost:8000`)로 요청하면 출처가 다르므로 차단된다

### CORS 설정

- **서버(FastAPI)** 쪽에서 "이 출처에서 오는 요청은 허용한다"고 설정해야 한다

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

- `allow_origins=["*"]`: 모든 출처에서의 요청을 허용한다
- 이 설정이 없으면 React에서 API 호출 시 에러가 발생한다
- main.py에서 해당 부분 주석을 해제한다.

---

### POST 요청 예시

- 할 일을 추가할 때는 서버가 요구하는 형태에 맞게 데이터를 보내야 한다
- 서버의 `create_todo`는 `data["text"]`로 값을 꺼내므로, **반드시 `{ text: "..." }` 형태로 전달**해야 한다

```jsx
axios.post("http://localhost:8000/todos", { text: "할 일 내용" })
```

- axios의 두 번째 인자로 전달한 객체가 **요청 본문(body)**으로 전송된다
- 서버에서는 이 body를 `data`로 받아 `data["text"]`로 꺼내 사용한다