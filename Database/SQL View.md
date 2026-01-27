## View

- 뷰는 하나 이상의 테이블을 기반으로 생성된 가상의 테이블이다.
- 실제 데이터를 물리적으로 저장하지 않으며, 정의된 SELECT 쿼리문을 저장하고 있다가 호출 시 실행한다.
- 복잡한 쿼리를 단순화하고 데이터 보안을 강화하는 목적으로 사용된다.
- 베이스 테이블의 데이터가 변경되면 뷰를 통해 보는 데이터도 실시간으로 변경된다.

---

### 주요 특징 및 장단점

- 논리적 독립성: 테이블 구조가 변경되어도 뷰를 사용하는 애플리케이션은 영향을 받지 않을 수 있다.
    - 단, view를 재정의 해야한다.
- 보안성: 특정 컬럼이나 행만을 공개하여 사용자에게 민감한 정보 노출을 방지한다.
- 편의성: 반복되는 복잡한 조인이나 서브쿼리문을 미리 정의해두어 사용 효율을 높인다.
- 제한사항: 인덱스를 직접 가질 수 없으며, 여러 테이블이 조인된 뷰는 삽입, 수정, 삭제 연산에 제약이 많다.

---

### 뷰의 생성 및 관리

- 뷰 생성 (CREATE VIEW)
    
    ```sql
    CREATE VIEW view_name AS
    SELECT column1, column2
    FROM table_name
    WHERE condition;
    ```
    
- 뷰 삭제 (DROP VIEW)
    - 테이블 데이터는 영향을 받지 않는다.
    
    ```sql
    DROP VIEW view_name;
    ```
    

---

### 보안 및 접근 제어

- 고객의 이메일과 활성화 여부만 노출하는 뷰
    - 고객의 결제 정보나 주소 ID 같은 민감한 내부 데이터를 제외하고 마케팅 부서 등에서 활용하기 적합하다.

```sql
CREATE VIEW customer_contact AS
SELECT first_name, last_name, email, activebool
FROM customer;
```

```sql
SELECT * FROM customer_contact
```

### 복잡한 조인 쿼리 단순화

- 대여 기록과 영화 제목을 결합한 뷰
    - 매번 3개의 테이블을 조인할 필요 없이 생성된 뷰를 통해 간단히 대여 현황을 파악할 수 있다.

```sql
CREATE VIEW film_with_category AS
SELECT film.title, category.name
FROM film
JOIN film_category ON film.film_id = film_category.film_id
JOIN category ON category.category_id = film_category.category_id;
```

```sql
SELECT * FROM film_with_category
```