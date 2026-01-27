# WITH 절 (Common Table Expression, CTE)

- WITH 절은 서브쿼리를 별도의 이름으로 정의하고, 이를 메인 쿼리에서 참조하여 사용하는 구문이다.
- 복잡한 쿼리를 논리적인 블록으로 분리하여 가독성을 높이고 코드의 재사용성을 향상시킨다.
- 정의된 CTE는 해당 쿼리가 실행되는 동안에만 임시로 존재하는 가상 테이블 역할을 한다.

---

### 주요 특징 및 장점

- 가독성 향상: 중첩된 서브쿼리를 상단에 선언하여 쿼리의 흐름을 위에서 아래로 읽을 수 있게 만든다.
- 재사용성: 동일한 서브쿼리 블록을 메인 쿼리 내에서 여러 번 참조할 수 있다.
- 계층적 쿼리: RECURSIVE 키워드를 함께 사용하여 조직도나 트리 구조 같은 계층적 데이터를 처리할 수 있다.
- 유지보수 용이: 복잡한 로직이 별도로 분리되어 있어 특정 부분의 수정이 간편하다.

---

### 기본 문법

- 단일 CTE 생성

```sql
WITH cte_name AS (
    SELECT column1, column2
    FROM table_name
    WHERE condition
)
SELECT * FROM cte_name;
```

- 다중 CTE 생성 (쉼표로 구분)

```sql
WITH cte1 AS (
    SELECT id FROM table1
),
cte2 AS (
    SELECT id FROM table2
)
SELECT * FROM cte1
JOIN cte2 ON cte1.id = cte2.id;
```

---

### WITH 절 활용 사례

### 복잡한 중첩 서브쿼리의 구조화

- Action 카테고리에 속한 영화 목록 찾기
- 서브쿼리 버전
    
    ```sql
    SELECT title
    FROM film
    WHERE film_id IN (
        SELECT film_id
        FROM film_category
        WHERE category_id = (
            SELECT category_id
            FROM category
            WHERE name = 'Action'
        )
    );
    ```
    

```sql
WITH action_category AS (
    SELECT category_id
    FROM category
    WHERE name = 'Action'
),
action_films AS (
    SELECT film_id
    FROM film_category
    WHERE category_id = (SELECT category_id FROM action_category)
)
SELECT title
FROM film
WHERE film_id IN (SELECT film_id FROM action_films);

```

### 집계 데이터의 재사용

- 평균 대여료보다 비싼 영화와 그 차액 계산
- 서브쿼리 버전
    
    ```sql
    SELECT f.film_id, f.title, f.rental_rate
    FROM film f
    WHERE f.rental_rate > (
        SELECT AVG(rental_rate)
        FROM film
    )
    ```
    

```sql
WITH rental_stats AS (
    SELECT AVG(rental_rate) AS avg_rate
    FROM film
)
SELECT
    f.title,
    f.rental_rate,
    rs.avg_rate,
FROM film f, rental_stats rs
WHERE f.rental_rate > rs.avg_rate;
```

---

### 서브쿼리(Inline View)와의 차이점

| 구분 | 서브쿼리 (Inline View) | WITH 절 (CTE) |
| --- | --- | --- |
| 가독성 | 쿼리가 깊어질수록 파악이 어려움 | 쿼리 상단에 정의되어 흐름 파악이 쉬움 |
| 재사용성 | 동일한 쿼리를 매번 다시 작성해야 함 | 정의된 이름을 통해 여러 번 참조 가능 |
| 범위 | FROM 절 내부에서만 유효 | 전체 메인 쿼리 문맥에서 유효 |
| 구조 | 비구조적, 중첩적 | 논리적 분리, 구조적 |