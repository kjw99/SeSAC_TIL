# **인터넷 강의 사이트에 필요한 데이터 조회**

- 다음 화면을 바탕으로 ERD를 설계하고, 각 화면에 필요한 쿼리문을 작성한다.

### ERD 설계

- draw.io 또는 유사 도구 사용한다.
- 테이블 간 관계 명확히 표시한다.
- 각 컬럼의 데이터 타입과 제약조건 정의한다.
- 인덱스 설계 포함한다.

### 쿼리문 작성

- Notion을 활용해 화면별 필요한 쿼리를 정리한다.

### API 설계

- 각 쿼리에 매칭되는 RESTful한 API를 설계한다.
- resouces를 잘 설명하는 URL을 매핑한다.
- 예시 JSON response를 만든다.
- notion API 문서(복사해옴. 여기다 작성)
    
    [API](https://www.notion.so/2f8df13d6ea081789fe2fcbb9a51f543?pvs=21)
    

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/f2678325-6f7b-4a25-b188-86c42030d6d5/fe75da8d-523f-4023-a294-2c80b95c3edf/image.png)

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/f2678325-6f7b-4a25-b188-86c42030d6d5/3d56e3fe-e526-4f70-b528-88cdd107e294/image.png)

- 메인 페이지
    - 선생님 모음 / 강좌 모음 페이지로 이동하는 버튼
    - 검색창
    - 마이페이지
    - 선생님 목록 일부
    - 강좌(course) 목록 일부

- 선생님 모음 페이지
    - 선생님 세부 페이지
        - 선생님이 진행중인 강좌
        - 선생님이 진행했던 강좌
        - 선생님의 강좌 수강평 모음

- 강좌 모음 페이지
    - 강좌 세부 페이지
        - 공통
            - 강의(lecture) 목록
            - 강좌 수강평
                - 수강평 평점 평균
        - 강좌 신청한 경우
            - 강의별 강의자료
            - 강의별 과제
                - 내 과제 제출 내역(T, F에 준하는 데이터)
            - 강의별 퀴즈
                - 참여 여부 / 점수
            - 강좌별 qna 게시판
                - 게시글
                    - 댓글

- 검색 결과 페이지
    - 검색 결과와 관련된 선생님 목록
    - 검색 결과와 관련된 강좌 목록

- 마이 페이지
    - 내가 신청한 강좌 목록
    - 내가 관심등록한 선생님
    - 내가 관심등록한 강좌
    - 내 게시글 / 댓글 목록

- 게시판
    - 전체 게시판, 질문/답변 게시판, 스터디 모집 게시판
    - 게시글
        - 댓글

- 단,
    - 하나의 화면에서 여러 개의 쿼리를 사용할 수 있다.
    - 검색은 `ILIKE`를 활용하여 구현하며, 특정 Column에 검색어가 포함되어 있는지로 구현한다.
    - `나`에 대한 USER ID는 `ME`를 활용한다.
    

---

### SQL → JSON

SQL의 표 형식 데이터는 JSON의 객체 및 배열 구조로 다음과 같이 치환된다.

- SQL의 단일 레코드는 JSON의 객체({ })에 대응한다.
    - Column Name: JSON의 Key가 된다.
    - Field Value: JSON의 Value가 된다.
    - 단일 테이블 조회 시, 결과 집합은 객체들을 담은 하나의 배열([ ]) 형태로 구성하는 것이 원칙이다.
    - ex) 영화 정보 조회 (단일 table)
    
    ```sql
    SELECT title, description, release_year, rating 
    FROM film 
    ```
    
    ```json
    [
      {
        "title": "ACADEMY DINOSAUR",
        "description": "A Epic Drama of a Feminist And a Mad Scientist who must Battle a Teacher in The Canadian Rockies",
        "release_year": 2006,
        "rating": "PG"
      },
      {
        "title": "ACE GOLDFINGER",
        "description": "A Astounding Epistle of a Database Administrator And a Explorer who must Find a Car in Ancient China",
        "release_year": 2006,
        "rating": "G"
      }
    ]
    ```
    

- 외래키와 중첩 구조
    - 관계형 데이터베이스에서 외래키를 통해 연결된 연관 데이터는 JSON에서 중첩된 객체로 표현하여 데이터 간의 소속 관계를 명확히 한다.
    - 영화와 카테고리 정보 조회 (Join)
        - 영화가 하나의 카테고리를 가진다고 가정.
    
    ```sql
    SELECT 
        f.film_id,
        f.title,
        f.description,
        c.category_id 
        c.name 
    FROM film f
    JOIN film_category fc ON f.film_id = fc.film_id
    JOIN category c ON fc.category_id = c.category_id
    ORDER BY f.film_id ASC
    LIMIT 3;
    ```
    
    ```json
    [
      {
        "film_id": 1,
        "title": "ACADEMY DINOSAUR",
        "description": "A Epic Drama of a Feminist And a Mad Scientist who must Battle a Teacher in The Canadian Rockies",
        "category": {
          "category_id": 6,
          "name": "Documentary"
        }
      },
      {
        "film_id": 2,
        "title": "ACE GOLDFINGER",
        "description": "A Astounding Epistle of a Database Administrator And a Explorer who must Find a Car in Ancient China",
        "category": {
          "category_id": 11,
          "name": "Horror"
        }
      },
      {
        "film_id": 3,
        "title": "ADAPTATION HOLES",
        "description": "A Astounding Reflection of a Lumberjack And a Car who must Sink a Lumberjack in A Baloon",
        "category": {
          "category_id": 6,
          "name": "Documentary"
        }
      }
    ]
    ```
    

- 일대다 관계(1:N)의 배열 처리
    - 하나의 엔티티가 여러 개의 연관 레코드를 가질 때(예: 영화 한 편과 출연 배우들), SQL 결과의 중복 행들을 JSON에서는 단일 객체 내의 배열(Array)로 통합한다.
    - ex) 영화별 출연 배우 목록 조회
    
    ```sql
    SELECT
        f.film_id,
        f.title,
        a.actor_id,
        a.first_name,
        a.last_name
    FROM film f
    JOIN film_actor fa ON f.film_id = fa.film_id
    JOIN actor a ON fa.actor_id = a.actor_id
    ORDER BY f.film_id, a.actor_id;
    
    ```
    
    ```sql
    [
      {
        "film_id": 1,
        "title": "ACADEMY DINOSAUR",
        "actors": [
          {
            "actor_id": 1,
            "name": "PENELOPE GUINESS"
          },
          {
            "actor_id": 10,
            "name": "CHRISTIAN GABLE"
          },
          {
            "actor_id": 20,
            "name": "LUCILLE TRACY"
          }
        ]
      },
      {
        "film_id": 2,
        "title": "ACE GOLDFINGER",
        "actors": [
          {
            "actor_id": 19,
            "name": "BOB FAWCETT"
          },
          {
            "actor_id": 85,
            "name": "MINNIE ZELLWEGER"
          },
          {
            "actor_id": 90,
            "name": "SEAN GUINESS"
          }
        ]
      }
    ]
    
    ```
    

- ex) 고객이 대여한 영화 정보 조회
    
    ```sql
    SELECT c.first_name, c.last_name, f.title, f.rating, cat.name
    FROM customer c
    JOIN rental r ON c.customer_id = r.customer_id
    JOIN inventory i ON r.inventory_id = i.inventory_id
    JOIN film f ON i.film_id = f.film_id
    JOIN film_category fc ON f.film_id = fc.film_id
    JOIN category cat ON fc.category_id = cat.category_id
    ORDER BY c.customer_id
    ```
    
    ```json
    [
      {
        "first_name": "MARY",
        "last_name": "SMITH",
        "rental_films": [
          {
            "title": "PATIENT SISTER",
            "rating": "NC-17",
            "category":
              {
                "name": "Classics"
              }
            
          },
          {
            "title": "TALENTED HOMICIDE",
            "rating": "PG",
            "categories":
              {
                "name": "Sports"
              }
            
          },
          {
            "title": "MUSKETEERS WAIT",
            "rating": "PG",
            "categories":
              {
                "name": "Classics"
              }
           
          }
        ]
      },
      {
        "first_name": "PATRICIA",
        "last_name": "JOHNSON",
        "rental_films": [
          {
            "title": "LOVE SUICIDES",
            "rating": "R",
            "categories":
              {
                "name": "Horror"
              }
          
          }
        ]
      }
    ]
    ```