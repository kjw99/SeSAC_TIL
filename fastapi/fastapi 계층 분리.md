## 관심사 분리(Separation of Concerns, Soc)

하나의 프로그램을 각각의 독립된 관심사로 분리하는 설계 원칙이다. 프로그램의 각 부분이 단일한 목적을 가지도록 구성한다.

- 장점
    - 코드의 유지보수성 향상: 특정 부분을 수정할 때 다른 부분에 영향을 주지 않음
    - 재사용성 향상: 분리된 각 모듈을 다른 프로젝트에서도 사용 가능
    - 테스트 용이성: 각 부분을 독립적으로 테스트 가능
    - 협업 용이: 개발자들이 각자 맡은 부분을 독립적으로 개발 가능

- 다음 Create 코드를 여러 과정으로 구분할 수 있다.
    
    ```python
    // HTTP Request에 대한 부분
    
    @router.post("", response_model=PostDetailResponse, status_code=status.HTTP_201_CREATED)
    def create_post(post_data: PostCreate):
        global post_id
        post_id += 1
        
        // 비즈니스 로직을 처리하는 부분
        if post_data.title == "":
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "title을 입력하세요")
    
        if post_data.content == "":
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "content를 입력하세요")
    
        // 데이터 생성에 대한 부분
        new_post = Post(post_id, post_data.title, post_data.content)
    
        posts.append(new_post)
    
        return new_post
    
    ```
    

---

## 레이어드 아키텍처 (Layered Architecture)

FastAPI는 특정 구조를 강제하지 않는 자유로운 프레임워크이다. 

하지만 규모가 있는 프로젝트에서는 관심사를 분리하고 유지보수성을 높이기 위해 레이어드 아키텍처를 주로 채택한다. 레이어드 아키텍쳐는 코드를 성격에 따라 층(Layer)으로 나누어 관리하는 설계 패턴이다..

### Presentation Layer (표현 계층)

- 사용자와의 상호작용을 담당한다.
    - 엔드포인트 및 response의 형식을 정한다.
- 데이터를 입력받아 Business Layer에 전달한다.
    - pydantic을 통해 데이터 형식을 검증한다.
- FastAPI에서는 APIRouter가 해당

### Business Layer (비즈니스 계층)

- 비즈니스 로직과 애플리케이션의 핵심 기능을 처리한다.
- 데이터의 유효성을 검증하고 Presentation Layer와 Data Layer를 중계한다.
    - Pydantic이 확인하기 어려운 비즈니스 조건 검사 (예: 중복 아이디 확인, 게시글 수정 권한 체크, 금지어 필터링 등)
- 여러 Repository의 작업을 조합하여 하나의 비즈니스 작업 완성한다.
- 보통 `Service`라고 이름을 붙인다.

### Data Access Layer (데이터 접근 계층)

- 데이터베이스와의 상호작용을 담당한다.
- 데이터를 저장, 조회, 업데이트, 삭제하는 기능을 제공한다.

### 계층 분리의 장점

1. **관심사의 분리 (SoC):** 각 계층은 자신의 역할에만 집중합니다. 예를 들어 Router는 데이터가 DB에 어떻게 저장되는지 알 필요가 없습니다.
2. **유지보수성 향상:** 특정 부분(예: DB를 MySQL에서 PostgreSQL로 교체)을 수정할 때 다른 계층의 코드를 건드릴 필요 없이 해당 계층의 코드만 수정하면 됩니다.
3. **테스트 용이성:** 각 계층을 독립적으로 떼어내어 테스트할 수 있습니다. DB가 준비되지 않아도 서비스 로직만 테스트하는 것이 가능해집니다.
4. **협업 용이:** 기능을 명확히 나눔으로써 여러 개발자가 각자 맡은 레이어를 동시에 개발하기 수월해집니다.