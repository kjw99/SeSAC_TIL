## DDL

- Data Definition Language, 데이터 정의어
- 데이터베이스 구조를 정의하고 변경하는 명령어이다.

## CREATE (생성)

- 데이터베이스 생성

```sql
CREATE DATABASE 데이터베이스이름;
CREATE DATABASE demodb;
```

- 테이블 생성
    
    ```sql
    CREATE TABLE 테이블명 (
        컬럼명1 데이터타입 [제약조건],
        컬럼명2 데이터타입 [제약조건],
        ...
    );
    ```
    
- 주요 데이터 타입
    - 숫자 타입
        - INT: 정수
        - DECIMAL(전체자리수, 소수자리수): 실수
        - BIGINT: 큰 정수
    - 문자 타입
        - CHAR(길이): 고정 길이 문자
        - VARCHAR(길이): 가변 길이 문자
        - TEXT: 긴 문자열
    - 날짜/시간 타입
        - DATE: 날짜
        - TIME: 시간
        - DATETIME: 날짜와 시간
        - TIMESTAMP: 타임스탬프
- 제약조건
    - PRIMARY KEY: 기본키
        - AUTO_INCREMENT 와 같이 사용
    - NOT NULL: NULL 값 불허용
    - UNIQUE: 중복값 불허용
    - DEFAULT: 기본값 설정
    - FOREIGN KEY: 외래키

```sql
-- 기본적인 테이블 생성
CREATE TABLE student (
    id VARCHAR(7) PRIMARY KEY,
    name VARCHAR(10),
    grade INT, 
    major VARCHAR(20)
);
```

```sql
-- 외래키가 있는 테이블 생성
CREATE TABLE attendance (
    attendance_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
    student_id VARCHAR(7) REFERENCES student(id),    
    date DATE,
    status VARCHAR(10)
);
```

## ALTER (변경)

- 컬럼 추가
    
    ```sql
    ALTER TABLE 테이블명
    ADD 컬럼명 데이터타입 [제약조건];
    ```
    

```sql
ALTER TABLE student 
ADD phone VARCHAR(20);
```

- 컬럼 이름 수정
    
    ```sql
    ALTER TABLE 테이블명 
    RENAME COLUMN 컬럼명 TO 변경할_컬럼명;
    ```
    

```sql
ALTER TABLE student 
RENAME COLUMN phone TO phone_number;
```

- 컬럼 타입 및 제약 조건 수정 (ALTER)
    
    ```sql
    ALTER TABLE 테이블명 
    ALTER COLUMN 컬럼명 TYPE 데이터타입;
    
    ALTER TABLE 테이블명 
    ALTER COLUMN 컬럼명 SET 제약사항;
    ```
    

```sql
ALTER TABLE student 
ALTER COLUMN name TYPE VARCHAR(100);
```

- 컬럼 삭제
    
    ```sql
    ALTER TABLE 테이블명
    DROP COLUMN 컬럼명;
    ```
    
    ```sql
    ALTER TABLE student 
    DROP COLUMN phone_number;
    ```
    

## DROP (삭제)

- 데이터베이스 삭제
    
    ```jsx
    CREATE DATABASE demodb;
    ```
    

- 테이블 삭제
    
    ```sql
    DROP TABLE attendance;
    ```
    

## TRUNCATE (데이터 전체 삭제)

```sql
TRUNCATE TABLE student ;
```