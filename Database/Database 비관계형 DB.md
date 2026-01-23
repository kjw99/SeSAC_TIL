## 비관계형 데이터베이스

- NoSQL(Not only SQL)은 전통적인 관계형 데이터베이스의 한계를 극복하기 위해 등장했다.
- 다양한 형태의 데이터를 저장할 수 있으며, 대규모 분산 데이터 처리에 적합하나 정합성이 떨어질 수 있다.

### key-value Database

- key-value 형태로 데이터를 저장한다.
- 매우 빠른 읽기/쓰기 성능을 제공하며 캐싱, 세션 관리, 실시간 분석에 적합하다.
- ex) Redis, Amazon DynamoDB

### Graph Database

- 노드(Entities), 엣지(Relationships) 및 속성(Properties)을 사용하여 데이터 간의 복잡한 관계를 표현한다.
- RDB는 table간의 관계를 나타낸다면, Graph Database는 데이터간의 관계를 나타낸다.
- ex) Neo4j

### Document Database

- JSON과 같은 문서 형식으로 데이터를 저장한다.
- 스키마가 자유로워 다양한 구조의 데이터를 저장할 수 있다.
- 계층적 데이터 구조를 자연스럽게 표현할 수 있다.
- ex) MongoDB

### Wide-Column Database

- 행(Row)마다 다른 컬럼을 가질 수 있으며, 대량의 데이터를 압축하여 저장하고 쿼리하는 데 유리하다.
- 빅데이터 분석, 로그 저장, 타임스리즈 데이터에 접합하다.
- ex) Apache Cassandra