## GROUP BY

- GROUP BY는 데이터를 지정된 컬럼 기준으로 그룹화하고, 각 그룹에 대한 집계 함수를 사용할 수 있다.
- GROUP BY가 포함되어 있는 SELECT절에는 GROUP BY에 포함된 컬럼이나 집계 함수만 사용 가능하다.

### 집계 함수

- 집계함수(aggregation function)는 여러 행의 데이터를 요약하여 하나의 결과값을 반환하는 함수이다.

- COUNT() - 행 개수
- SUM() - 합계
- AVG() - 평균
- MIN() - 최소값
- MAX() - 최대값

- 대륙 별 국가 수
    
    ```sql
    SELECT continent, COUNT(*) as country_count
    FROM country
    GROUP BY continent;
    ```
    

- Region 별 국가 평균 인구
    
    ```sql
    SELECT region, AVG(population) as avg_pop
    FROM country
    GROUP BY region;
    ```
    

- 대륙 별 최소 / 최대 인구
    
    ```sql
    SELECT continent,
       MIN(population) as min_pop,
       MAX(population) as max_pop
    FROM country
    GROUP BY continent;
    ```
    

- 대륙 별 인구가 1000만 이상인 국가의 수
    
    ```sql
    SELECT continent, COUNT(*) as big_countries 
    FROM country 
    WHERE Population >= 10000000 
    GROUP BY continent;
    ```
    

## HAVING

- HAVING은 GROUP BY의 결과에 조건을 거는 절이다.
- WHERE는 개별 행 데이터, HAVING은 그룹화된 결과를 필터링한다.
    - 즉, HAVING의 경우 집계함수와 함께 쓰이는 경우가 많다.

- 대륙 별 국가 수가 20개가 넘는 대륙, 국가 수 조회
    
    ```sql
    SELECT continent, COUNT(*) as country_count
    FROM country
    GROUP BY continent
    HAVING COUNT(*) > 20;
    ```
    

- Region 별 평균 인구가 10000000이 넘는 지역, 평균 인구 조회
    
    ```sql
    SELECT region, AVG(population) as avg_pop
    FROM country
    GROUP BY region
    HAVING AVG(population) > 10000000;
    ```
    

- 대륙 별 인구가 1000만 이상인 국가의 수가 10개가 넘는 대륙의 이름과 국가 수 조회
    
    ```sql
    SELECT continent, COUNT(*) as big_countries 
    FROM country 
    WHERE population >= 10000000 
    GROUP BY Continent
    HAVING COUNT(*) > 10;
    ```
    

- 평균 인구수가 10000000 이 넘는 대륙 의 국가 수
    - HAVING절에는 SELECT절에 포함되지 않는 집계함수가 포함될 수 있다.
    
    ```sql
    SELECT Continent, COUNT(*) as country_count
    FROM country
    GROUP BY Continent
    HAVING AVG(Population) > 10000000 ;
    ```