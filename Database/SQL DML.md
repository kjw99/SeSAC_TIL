## DML

- Data Manipulation Language, 데이터 조작어
- 데이터를 추가, 조회, 수정, 삭제하는 기본적인 데이터 처리를 담당한다.

---

## INSERT

- 새로운 데이터를 테이블에 추가할 때 사용한다.
- 모든 컬럼의 값을 순서대로 다 적으면 컬럼을 생략할 수 있다.(데이터 2개 넣는 예시)

```sql
INSERT INTO 테이블명 (컬럼1, 컬럼2) VALUES (값1, 값2);
```

```sql
INSERT INTO student (id, name, grade, major) 
VALUES ('2024001', '김철수', 1, '컴퓨터공학');
```

```sql
INSERT INTO student VALUES 
    ('2024002', '이영희', 2, '경영학'),
    ('2024003', '박민수', 3, '물리학');
```

---

## SELECT

- 데이터를 조회할 때 사용한다.
- 모든 필드 조회
    
    ```sql
    SELECT * FROM 테이블명;
    ```
    
- country table에서 모든 필드 조회
    
    ```sql
    SELECT * FROM country;
    ```
    

---

- 특정 필드 조회
    - 컬럼이 띄어쓰기가 있는 경우, `""`로 감싸서 하나의 컬럼명으로 인식하게 한다.
    
    ```sql
    SELECT 테이블명.컬럼명1, 테이블명.컬럼명2 FROM 테이블명;
    ```
    
    - 컬럼을 선택할 때 테이블명을 생략해도 되지만, 생략하지 않는 것이 성능상, 그리고 이후 여러 테이블을 합쳐서 조회할 때 이점이 있다.
        
        ```sql
        SELECT 컬럼명1, 컬럼명2 FROM 테이블명;
        ```
        
    
- country table에서 name, continent 필드 조회

```sql
SELECT name, continent FROM country;
```

---

- alias 설정
    - 테이블명을 축약하여 사용할 수 있다
        
        ```sql
        SELECT t.컬럼명1, t.컬럼명2 FROM 테이블명 AS t;
        SELECT t.컬럼명1, t.컬럼명2 FROM 테이블명 t;
        ```
        
    - 조회 시 컬럼의 이름을 변경할 수 있다.
        
        ```sql
        SELECT t.컬럼명1 AS first, t.컬럼명2 AS second FROM 테이블명 t;
        SELECT t.컬럼명1 first, t.컬럼명2 second FROM 테이블명 t;
        ```
        
    - as는 생략이 가능하다.

```sql
SELECT c.name 국가, c.population 인구 FROM country c;
```

---

- 중복 제거
    
    ```sql
    SELECT DISTINCT 컬럼명 FROM 테이블명;
    ```
    
- country 테이블에서 Continent의 종류 조회
    
    ```sql
    SELECT DISTINCT continent FROM country
    ```
    

### WHERE

- WHERE 절은 데이터를 필터링할 때 사용하는 조건절이다
    
    ```sql
    SELECT * FROM 테이블명 WHERE 조건;
    ```
    

```sql
SELECT * FROM student WHERE grade = 2;
```

- 문자의 경우 `''` (홑따옴표)를 사용한다.

- 비교 연산자
    
    ```sql
    WHERE population > 1000000
    WHERE population >= 1000000
    WHERE population < 1000000
    WHERE population <= 1000000
    WHERE population = 1000000
    WHERE population != 1000000  -- 또는 <>
    ```
    

- 논리 연산자
    
    ```sql
    WHERE population > 1000000 AND continent = 'asia'
    WHERE population > 1000000 OR continent = 'asia'
    WHERE NOT population < 1000000
    ```
    

- 범위
    
    ```sql
    WHERE population BETWEEN 1000000 AND 2000000
    WHERE population NOT BETWEEN 1000000 AND 2000000
    
    WHERE created_at BETWEEN '2024-01-01' AND '2024-12-31'
    ```
    

- 포함
    
    ```sql
    WHERE code IN ('KOR', 'JPN', 'CHN')
    WHERE code NOT IN ('KOR', 'JPN', 'CHN')
    ```
    

- NULL 여부
    
    ```sql
    WHERE LifeExpectancy IS NULL
    WHERE LifeExpectancy IS NOT NULL
    ```
    

- 패턴매칭
    - `%` : 0개 이상의 문자
    - `_` : 1개의 문자
    - `LIKE` 대신 `ILIKE`를 활용하면 대소문자를 구분하지 않는다.
    
    ```sql
    WHERE Name LIKE 'S%'        -- S로 시작
    WHERE Name LIKE '%on'       -- on으로 끝남
    WHERE Name LIKE '%on%'      -- on이 포함
    WHERE Name NOT LIKE 'S%'    -- S로 시작하지 않음
    ```
    

## ORDER BY

- ORDER BY는 결과를 정렬하는 구문이다.

```sql
ORDER BY 컬럼명 [ASC/DESC]
```

- ASC : 오름차순 (기본값, 생략가능)
- DESC: 내림차순

- 인구 많은 순으로 정렬
    
    ```sql
    SELECT name, population 
    FROM city 
    ORDER BY population DESC;
    ```
    

- 국가순으로 정렬 후, 같은 국가 내에서는 인구순 정렬
    - 정렬을 여러 컬럼에 순차적으로 적용 할 수 있다.
    
    ```sql
    SELECT name, countryCode, population 
    FROM city 
    ORDER BY countrycode , population DESC;
    ```
    

- 기본적으로 NULL은 큰 값으로 취급된다. (RDB마다 다를 수 있다.)
    
    ```sql
    SELECT Name, indepyear FROM country 
    ORDER BY indepyear DESC;
    ```
    
    - 다음과 같이 null의 위치를 조정할 수 있다.
        
        ```sql
        SELECT Name, indepyear FROM country 
        ORDER BY indepyear DESC NULLS LAST;
        ```
        
        ```sql
        SELECT Name, indepyear FROM country 
        ORDER BY indepyear ASC NULLS FIRST;
        ```
        

## LIMIT, OFFSET

- 조회 할 레코드들의 개수를 제한한다
    - ORDER BY와 함께 사용한다.

- LIMIT : 갯수
    - 한 페이지에 보여줄 개수
- OFFSET : OFFSET에 해당하는 다음 값 부터
    - (페이지 번호 - 1) * 페이지당 개수

- 인구수 상위 1위 ~ 10위 (1페이지)
    
    ```sql
    SELECT name, population
    FROM city
    ORDER BY population DESC
    LIMIT 5 --OFFSET 0;  
    ```
    

- 인구수 상위 11위 ~ 15위 조회(3페이지)
    
    ```sql
    SELECT name, population
    FROM city
    ORDER BY population DESC
    LIMIT 5 OFFSET 10;  
    ```
    

---

## UPDATE

- 기존 데이터를 수정할 때 사용한다.

```sql
UPDATE 테이블명 SET 컬럼 = 새값 WHERE 조건;
```

```sql
UPDATE student 
SET grade = 2, major = '경제학' 
WHERE id = '2024001';
```

---

## DELETE

- 데이터를 삭제할 때 사용한다.

```sql
DELETE FROM 테이블명 WHERE 조건;
```

```sql
DELETE FROM student 
WHERE id = '2024002';
```

---

<aside>
💡

`UPDATE`와 `DELETE`의 경우 WHERE을 생략하면 테이블 전체가 수정 / 삭제되므로 반드시 조건을 명시해야 한다.

</aside>