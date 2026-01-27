## Self Join

- 같은 테이블을 자기 자신과 조인하는 방식이며, INNER JOIN, LEFT JOIN 등 모두 사용 가능하다.
- 조직도/계층 구조를 표현할 때, 데이터 비교가 필요할 때,  순위나 그룹 내 비교가 필요할 때 사용될 수 있다.

- 같은 영화에 출연한 배우들
    
    ```sql
    SELECT 
        a.actor_id AS actor_1, 
        b.actor_id AS actor_2, 
        a.film_id
    FROM film_actor a
    JOIN film_actor b ON a.film_id = b.film_id
    WHERE a.actor_id < b.actor_id; 
    ```
    
    - film을 JOIN하여 영화 제목을 추가로 가져올 수 있음
        
        ```sql
        SELECT 
            a.actor_id AS actor_1, 
            b.actor_id AS actor_2, 
            a.film_id,
            f.title
        FROM film_actor a
        JOIN film_actor b ON a.film_id = b.film_id
        JOIN film f ON f.film_id = a.film_id
        WHERE a.actor_id < b.actor_id; -- 자기 자신 제외 및 중복 조합 방지
        ```
        

---

### 댓글 - 대댓글 관계

- 테이블 생성 및 데이터 입력
    
    ```sql
    CREATE TABLE comments (
        id INT PRIMARY KEY,
        content TEXT,
        parent_id INT,
        FOREIGN KEY (parent_id) REFERENCES comments(id)
    );
    
    INSERT INTO comments VALUES
    (1, '안녕하세요', NULL),           -- 원댓글
    (2, '반갑습니다', NULL),           -- 원댓글
    (3, '네 안녕하세요!', 1),          -- 1번 댓글의 대댓글
    (4, '저도 반가워요', 1),           -- 1번 댓글의 대댓글
    (5, '답글 드립니다', 2),           -- 2번 댓글의 대댓글
    (6, '안녕', NULL);                -- 원댓글
    
    -- 댓글과 대댓글을 함께 조회
    SELECT 
        parent.id as parent_id,
        parent.content as parent_content,
        child.id as reply_id,
        child.content as reply_content
    FROM comments parent
    LEFT JOIN comments child ON child.parent_id = parent.id
    WHERE parent.parent_id IS NULL;  -- 원댓글만 기준으로 조회
    
    -- ORIGINAL : 원댓글
    SELECT 
        ORIGINAL.id as ORIGINAL_id,
        ORIGINAL.content as ORIGINAL_content,
        child.id as reply_id,
        child.content as reply_content
    FROM comments ORIGINAL 
    LEFT JOIN comments child ON child.parent_id = ORIGINAL.id
    WHERE ORIGINAL.parent_id IS NULL;  -- 원댓글만 기준으로 조회
    
    ```
    

- 조회
    
    ```sql
    -- 원댓글만 조회
    SELECT 
        ORIGINAL.id as ORIGINAL_id,
        ORIGINAL.content as ORIGINAL_content
    FROM comments ORIGINAL
    WHERE ORIGINAL.parent_id IS NULL;  -- 원댓글만 기준으로 조회
    ```
    
    ```sql
    -- 모든 댓글 조회
    SELECT 
        ORIGINAL.id as ORIGINAL_id,
        ORIGINAL.content as ORIGINAL_content
    FROM comments ORIGINAL ;
    ```
    
    ```sql
    -- 댓글과 대댓글을 함께 조회
    SELECT 
        parent.id as parent_id,
        parent.content as parent_content,
        child.id as reply_id,
        child.content as reply_content
    FROM comments parent
    LEFT JOIN comments child ON child.parent_id = parent.id
    WHERE parent.parent_id IS NULL;  -- 원댓글만 기준으로 조회
    ```