## Subquery

- 서브쿼리는 다른 SQL 쿼리 내부에 포함된 쿼리문이다.
- 메인 쿼리가 실행되기 전에 서브쿼리가 먼저 실행되어 그 결과를 메인 쿼리에서 사용한다.

- 서브쿼리는 괄호 () 안에 작성하며, 단독으로 실행 가능한 완전한 SELECT문이다
- 서브쿼리가 먼저 실행되고 그 결과를 이용해서 메인쿼리가 실행된다.
- 너무 많은 중첩은 성능 저하의 원인이 될 수 있다.
- 조인으로 변환 가능한 경우가 많으며, 보통 조인이 성능상 더 유리하다.

### 위치에 따른 분류

서브쿼리는 SQL 문법 내에서 사용되는 위치에 따라 다음과 같이 분류할 수 있다.

1. 스칼라 서브쿼리 : SELECT 절에서 사용되며 하나의 값만 반환한다.
2. 인라인 뷰: FROM 절에서 사용되며 서브쿼리의 결과를 하나의 테이블처럼 취급한다.
3. 중첩 서브쿼리 : WHERE 절이나 HAVING 절에서 사용되어 조건의 값을 제공한다.

### **스칼라 서브쿼리**

- 서브쿼리의 결과가 단 하나의 값만을 반환한다.
- WHERE 절 등에서 비교 연산자(=, > 등) 사용이 가능하다.
- 주로 집계 함수와 함께 사용된다.

- 평균 인구수보다 인구가 많은 도시들 조회 - `world`
    
    ```sql
    SELECT Name, Population
    FROM city
    WHERE Population > (
        SELECT AVG(Population)
        FROM city
    );
    ```
    

- 가장 많은 인구를 가진 도시의 국가 정보 - `world`
    
    ```sql
    SELECT Name, Population, GNP
    FROM country
    WHERE Code = (
        SELECT CountryCode 
        FROM city 
        ORDER BY Population DESC 
        LIMIT 1
    );
    ```
    

- 평균 대여 금액(rental_rate)보다 비싼 영화를 조회하시오. - `dvdrental`
    
    ```sql
    SELECT f.film_id, f.title, f.rental_rate
    FROM film f
    WHERE f.rental_rate > (
        SELECT AVG(rental_rate)
        FROM film
    )
    ```
    

### 다중행 서브쿼리

- 서브쿼리의 결과가 여러 행을 반환한다.
- IN, ANY, ALL, EXISTS 등의 연산자 사용한다.
    - IN: 목록 중 일치하는 값이 있는지 확인
        - NOT IN : 목록 중 일치하는 값이 없는지 확인
    - ANY: 조건을 만족하는 값이 하나라도 있는지 확인
    - ALL: 모든 값이 조건을 만족하는지 확인
    - EXISTS: 서브쿼리 결과가 존재하는지 확인
        - NOT EXISTS: 서브쿼리 결과가 존재하지 않는지 확인

- 인구 500만 이상인 도시가 있는 국가 찾기 - `world`
    
    ```sql
    SELECT code, name
    FROM country
    WHERE code IN (
        SELECT countrycode 
        FROM city 
        WHERE population >= 5000000
    );
    ```
    

- 적어도 한 번이라도 대여된 적이 있는 영화들 찾기 - `dvdrental`
    
    ```sql
    SELECT f.title 
    FROM film f
    WHERE f.film_id IN (
        SELECT DISTINCT i.film_id
        FROM rental r
        JOIN inventory i ON r.inventory_id = i.inventory_id
    );
    ```
    
    ```sql
    SELECT f.title
    FROM film f
    WHERE EXISTS (
        SELECT 1 
        FROM rental r 
        JOIN inventory i ON r.inventory_id = i.inventory_id
        WHERE i.film_id = f.film_id
    );
    ```
    

- Action 카테고리에 속한 영화들 찾기 - `dvdrental`
    
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
    

### 상관 서브쿼리

- 메인쿼리의 컬럼을 서브쿼리에서 사용한다.
- 메인쿼리와 서브쿼리가 서로 연관되며, 메인쿼리의 각 행마다 서브쿼리가 실행된다.
- 실행 속도가 상대적으로 느릴 수 있다

- 각 국가별 가장 인구가 많은 도시 찾기 - `world`
    
    ```sql
    SELECT c1.name, c1.population, c1.countrycode
    FROM city c1
    WHERE population = (
        SELECT MAX(population)
        FROM city c2
        WHERE c1.countrycode = c2.countrycode
    );
    ```
    
    서브쿼리 내부에서 `city c1`을 활용한다.
    

- 각 고객의 가장 최근 대여 기록 찾기 `dvdrental`
    
    ```sql
    SELECT c.first_name, c.last_name, r.rental_date
    FROM customer c
    JOIN rental r ON c.customer_id = r.customer_id
    WHERE r.rental_date = (
        SELECT MAX(rental_date)
        FROM rental
        WHERE r.customer_id = c.customer_id
    )
    ```
    
    서브쿼리 내부에서 `customer`를 활용한다.