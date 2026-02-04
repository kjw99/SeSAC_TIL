## 상태 코드 설정

[HTTP 상태 코드 - HTTP | MDN](https://developer.mozilla.org/ko/docs/Web/HTTP/Reference/Status)

- **200 OK**: 조회 성공
- **201 Created**: 생성 성공
- **204 No Content**: 삭제 성공 (반환할 데이터 없음)
- **404 Not Found**: 데이터를 찾을 수 없음

```python
# post_api.py 수정

from fastapi import status

# 데이터 생성의 경우 201 code를 응답한다.
@router.post("", response_model=PostDetailResponse, status_code=status.HTTP_201_CREATED)
def create_post(post_data: PostCreate):
    global post_id
    post_id += 1

    post = Post(post_id, post_data.title, post_data.content)

    posts.append(post)

    return post
    
    
# 데이터 삭제의 경우 204 code를 응답한다.
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    for index, post in enumerate(posts):
        if post.id == id:
            # 204의 경우 return에 데이터를 넣지 않는다.
            return 
    return {"message": "삭제할 대상이 없습니다."}
```

---

## 예외 처리

데이터가 없을 때 단순히 메시지를 보내는 것이 아니라, `HTTPException`을 사용하여 404 상태 코드를 명확히 전달한다.

```python
# post_api.py 수정
from fastapi import HTTPException

@router.get("/{id}", response_model=PostDetailResponse)
def read_post(id: int):
    # 식별자가 일치하는 데이터를 리스트에서 탐색
    for post in posts:
        if post.id == id:
            return post
    raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    for index, post in enumerate(posts):
        if post.id == id:
            posts.pop(index)
            return 
    raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
```