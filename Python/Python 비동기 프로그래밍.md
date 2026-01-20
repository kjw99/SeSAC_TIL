## 비동기 프로그래밍

- 비동기 프로그래밍은 단일 스레드 환경에서 여러 작업을 동시에 처리하기 위한 제어 방식.
- 호출된 함수가 즉시 결과를 반환하지 않더라도 프로세서가 다른 작업을 수행할 수 있도록 제어권을 유지.
    - 1번 → 1번 끝 → 2번 → 2번 끝 이런식이 아니라. 1번 → 2번 → 1번 끝… 이렇게 되도록. 결과를 기다리지 않고 바로바로 실행하는 것.
- 입출력 작업 대기 시간 동안 자원의 유휴 상태를 방지하여 시스템 효율성을 높인다.
- 동기 프로그래밍과 비동기 프로그래밍 비교
    - 동기 프로그래밍은 순차적으로 명령을 실행, 앞선 작업이 완료될 때까지 다음 작업을 시작하지 않음.
    - 비동기 프로그래밍은 작업 완료 여부와 관계 없이 다음 명령 호출. 작업 완료 시점에 콜백이나 이벤트 루프를 통해 결과를 처리함.
- 동기 프로그래밍 방식

```python
import time
import asyncio

# 동기 방식 함수 정의
def fetch_data_sync(name):
    print(f"데이터 조회 시작: {name}")
    time.sleep(2)  # 2초 동안 프로세스 차단
    print(f"데이터 조회 완료: {name}")

# 동기 실행 메커니즘 확인
def run_sync_example():
    start_time = time.time()
    fetch_data_sync("작업1")
    fetch_data_sync("작업2")
    end_time = time.time()
    print(f"동기 총 소요 시간: {end_time - start_time}초")

run_sync_example()
#데이터 조회 시작: 작업1
#데이터 조회 완료: 작업1
#데이터 조회 시작: 작업2
#데이터 조회 완료: 작업2
#동기 총 소요 시간: 4.003570079803467초
```

- 비동기 프로그래밍
    - asyncio.gather에서 gather()가 async를 한번에 실행시키는 함수. 첫 async를 실행시키고 이벤트 루프로 보내고 다음 async를 실행.

```python

# 비동기 방식 함수 정의
async def fetch_data_async(name):
    print(f"데이터 조회 시작: {name}")
    await asyncio.sleep(2)  # 2초 동안 제어권을 이벤트 루프에 반환
    print(f"데이터 조회 완료: {name}")

    
# 비동기 실행 메커니즘 확인
async def run_async_example():
    start_time = time.time()
    # 두 개의 비동기 작업을 동시에 예약
    await asyncio.gather(
        fetch_data_async("작업1"),
        fetch_data_async("작업2")
    )
    end_time = time.time()
    print(f"비동기 총 소요 시간: {end_time - start_time}초")
# 실행 코드
# 비동기 함수의 실행의 asyncio.run()으로 해야하지만, ipynb 또는 colab 환경에서는 이미 이벤트 루프가 돌아가고 있어 대신 await를 활용한다.
# asyncio.run(run_async_example())
await run_async_example()
#데이터 조회 시작: 작업1
#데이터 조회 시작: 작업2
#데이터 조회 완료: 작업1
#데이터 조회 완료: 작업2
#비동기 총 소요 시간: 2.006120204925537초
```

## 코루틴

- 코루틴은 실행을 일시 중단하고 재개할 수 있는 특수한 형태의 함수.
- 파이썬에서는 async def 예약어를 사용하여 정의하며, 호출 시 즉시 실행되지 않고 코루틴 객체를 반환함.
- await가 반드시 필요! 이게 있어야 실행 가능.
    - coro에 async 지정된 함수를 담았는데, 타입을 보면 코루틴 타입이라고 나온다.
    - async가 있으면 함수의 실행 결과는 코루틴이 나옴. 이걸 await 해야지 원래 함수의 실행 결과가 나오게 된다.
    - 그래서 coro 자체를 print하면 정상적인 값이 안나옴.
    - value에 coro를 await 시키고 저장했기 때문에 value를 출력했을 때 정상적인 값이 나온 것.

```python
import asyncio

async def simple_coroutine():
    print("코루틴 실행")
    return "코루틴 반환값"

# 코루틴 객체 생성
coro = simple_coroutine()
print(f"객체 유형: {type(coro)}")

# await 키워드를 통해 코루틴 실행 및 결과 추출

value = await coro
print(value)
#객체 유형: <class 'coroutine'>
#코루틴 실행
#코루틴 반환값
```

## 이벤트 루프

- 이벤트 루프는 비동기 함수들을 관리하고 실행하는 중앙 제어 장치이다.
- 대기 중인 작업들을 모니터링하다가 작업이 완료되면 해당 지점부터 실행을 재개한다.
- 간단하게 생각
    - async << 오래 걸릴수도 있는 작업
    - await << async 작업이 끝나면 실행.
- async 3개를 모아서 한번에 실행시킬 수 있다.

```python
import asyncio

async def main_loop_task():
    loop = asyncio.get_running_loop()
    print(f"현재 실행 중인 이벤트 루프 정보: {loop}")

await main_loop_task()
# Jupyter 환경에서는 이미 이벤트 루프가 실행 중이므로 await로 바로 호출
# 일반 환경에서는 asyncio.run()으로 이벤트루프를 실행한다.
```

## 대기 키워드

- await 키워드는 코루틴의 작업이 완료될 때까지 해당 코루틴의 실행을 일시 정지시킨다.
- 일시 정지된 동안 제어권은 이벤트 루프로 반환되어 다른 비동기 작업이 수행될 수 있다.

```python
import asyncio

async def task_with_delay(seconds):
    print(f"{seconds}초 대기 작업 시작")
    await asyncio.sleep(seconds) # 비차단 대기 수행
    print(f"{seconds}초 대기 작업 종료")
    return seconds

async def execute_tasks():
    # await를 사용한 순차적 비동기 처리
    val1 = await task_with_delay(1)
    val2 = await task_with_delay(1)
    print(f"합계: {val1 + val2}")

await execute_tasks()
```

## 비동기 작업의 병렬 처리

- asyncio.gather는 여러 코루틴을 동시에 이벤트 루프에 등록하여 병렬적으로 실행한다.
- 모든 작업이 완료될 때까지 대기하며, 결과들을 리스트 형태로 반환함.
- `gather(*(fetch_url(u) for u in urls))` 이런 경우 gather 내부의 코드가 다 실행되면 다음 코드로 넘어간다.

```python
import asyncio

async def fetch_url(url):
    print(f"{url} 요청 전송")
    await asyncio.sleep(2) # 네트워크 지연 상황 시뮬레이션
    return f"{url} 데이터"

async def main():
    urls = ["google.com", "naver.com", "daum.net"]
    
    # 여러 코루틴을 생성 후 gather에 전달
    results = await asyncio.gather(*(fetch_url(u) for u in urls))
    
    print(f"수집 결과: {results}")

await main()
```

- 그래서 이렇게 구현하면 비동기 명령어들을 써도 동기처럼 실행됨.

```python

# 코루틴이여도 await를 반복해서 사용하면 동기처럼 실행된다.
async def main():
    urls = ["google.com", "naver.com", "daum.net"]
    
    results = [await fetch_url(u) for u in urls]
#    results = []
#    for u in urls:
#        result = await fetch_url(u)
#        results.append(result)
    
    print(f"수집 결과: {results}")

await main()
```

## 비동기 요청

- aiohttp는 파이썬의 asyncio 라이브러리를 기반으로 하는 비동기 HTTP 클라이언트 및 서버 프레임워크이다.
- 단일 스레드 내에서 이벤트 루프를 통해 다수의 네트워크 요청을 병렬로 처리하여 입출력 대기 시간을 효율적으로 관리한다.

```python
import asyncio
import aiohttp

async def main():
    # ClientSession은 연결 풀을 관리하는 객체이다.
    async with aiohttp.ClientSession() as session:
        # 비동기 context manager를 사용하여 세션을 생성한다.
        pass

await main()
```

## 비동기 클라이언트 요청

- 세션은 뭔가의 리소스를 사용함.
- 그래서 일반 request처럼 한줄 한줄 실행하는 것이 아니라 with ~~ as를 사용함.
- with ~~ as: 이후 들여쓰기를 하면 해당 공간에서는 세션이 살아있음. 들여쓰기 끝난 이후에는 자동으로 리소스의 사용을 멈춤. 세션 사용이 불가능 해짐.
    - with ~ as session: 이렇게 되어 있는 구간에서는 세션 사용이 가능하다는 뜻. 밖으로 나가면 세션 끊김!
    - with as 를 안 쓰면 try ~ finally 구문을 사용하고 finally에서 session.close()로 세션을 닫아줘야 한다.

```python
async def fetch_status(url):
    async with aiohttp.ClientSession() as session:
        # GET 요청을 비동기적으로 수행한다.
        async with session.get(url) as response:
            # 응답 상태 코드를 반환받는다.
            status = response.status
            print(f"상태 코드: {status}")
            return status

await fetch_status("https://jsonplaceholder.typicode.com/posts")
```

- 아래 코드는 위의 비동기적 코드의 동기적 코드 버전.
    - 비동기는 한번에 여러 가지 실행이 가능한데, 동기적으로 사용하면 하나씩 밖에 안됨.

```python
import requests
def fetch_status(url):
    response = requests.get(url)
    status = response.status_code
    print(f"상태 코드: {status}")
    return status

fetch_status("https://jsonplaceholder.typicode.com/posts")
```

## 응답 데이터 처리

- 응답 객체로부터 텍스트, 바이너리, 제이슨 데이터를 비동기적으로 추출한다.
- 데이터 추출 메서드인 text(), json(), read() 역시 코루틴이므로 await 키워드를 사용해야 한다.

```python
async def get_json_data():
    url = "https://jsonplaceholder.typicode.com/posts/1"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            # 응답 본문을 제이슨 형식으로 파싱한다.
            data = await response.json()
            # 특정 키의 값을 출력한다.
            print(f"제목: {data['title']}")

await get_json_data()
```

## 다중 요청 병렬 처리

- gather를 사용하여 여러 개의 aiohttp 요청 태스크를 동시에 실행.
- 동기 방식의 요청과 달리 각 요청의 완료를 기다리지 않고 다음 요청을 바로 수행한다.
- 코드의 실행 과정
    - request_all 함수 실행.
        - 세션을 생성, gather를 통해 tasks를 한번에 실행하려 한다.
        - 이를 위해 tasks를 생성해야 하는데, fetch_url 함수를 통해 생성.

```
async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()

async def request_all(urls):
    async with aiohttp.ClientSession() as session:
        # 각 URL에 대한 요청 코루틴 리스트를 생성한다.
        tasks = [fetch_url(session, url) for url in urls]
        # 모든 태스크를 병렬로 실행하고 결과를 수집한다.
        responses = await asyncio.gather(*tasks)
        print(f"응답 개수: {len(responses)}")

url_list = [
    "https://jsonplaceholder.typicode.com/posts/1", 
    "https://jsonplaceholder.typicode.com/posts/2", 
    "https://jsonplaceholder.typicode.com/posts/3", 
    ]
await request_all(url_list)
```

## 매개변수 및 헤더 전달

- 요청 시 params 인자를 통해 쿼리 스트링을 전달하거나, headers 인자를 통해 HTTP 헤더를 설정.
- 딕셔너리 구조를 활용하여 데이터를 정의한다.

```python
async def search_with_params():
    url = "https://httpbin.org/get"
    # 쿼리 매개변수를 정의한다.
    query_params = {"name": "admin", "id": "123"}
    # 사용자 정의 헤더를 정의한다.
    custom_headers = {"User-Agent": "AiohttpClient/1.0"}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=query_params, headers=custom_headers) as response:
            result = await response.json()
            # 서버에서 수신한 인자 정보를 확인한다.
            print(result["args"])

await search_with_params()
```

## 다중 요청 개수 제한

- 비동기 환경에서 동시에 너무 많은 네트워크 요청을 보낼 경우 서버 측 차단이나 시스템 자원 고갈이 발생할 수 있다.
- asyncio.Semaphore 객체를 사용하여 동시에 실행 가능한 코루틴의 숫자를 제어한다.
- 세마포어도 with 키워드를 통해 사용.

```python
import asyncio
import aiohttp

async def fetch_with_semaphore(semaphore, session, url):
    # 세마포어를 사용하여 동시 실행 숫자를 제한한다.
    async with semaphore:
        async with session.get(url) as response:
            status = response.status
            # 실제 요청이 수행되는 시점을 확인한다.
            print(f"요청 완료: {url} (상태: {status})")
            return await response.text()

async def main():
    urls = [f"https://jsonplaceholder.typicode.com/posts/{i}" for i in range(1, 21)]
    
    # 동시 요청 숫자를 5개로 제한하는 세마포어를 생성한다.
    semaphore = asyncio.Semaphore(5)
    
    async with aiohttp.ClientSession() as session:
        # 모든 요청 태스크를 생성하되, 세마포어에 의해 5개씩 순차적으로 실행된다.
        tasks = [fetch_with_semaphore(semaphore, session, url) for url in urls]
        await asyncio.gather(*tasks)

await main()
```

## 직접 구현하면서 동기, 비동기 비교해보기

- tmdb 데이터 사용.
- 현재 상영 중인 영화 가져오기
    - 동기 방식.
    - request.get() 사용
    
    ```python
    import requests
    from pprint import pprint
    import os
    from dotenv import load_dotenv
    load_dotenv()
    API_KEY = os.getenv('TMDB_API_KEY')
    params = {
        'language' : 'ko-kr',
    }
    headers = {
        "Authorization" : f"Bearer {API_KEY}"
    }
    def get_movie_data(data_url):
        URL = f"https://api.themoviedb.org/3/{data_url}"
        try:
            response = requests.get(URL, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(e)
        return data
        
    data_url = "movie/now_playing"
    data = get_movie_data(data_url)
    data = data["results"]
    max_vote_average = 0
    max_move_id = 0
    max_move = ""
    for result in data:
        
        if max_vote_average < result["vote_average"]:
            max_vote_average = result["vote_average"]
            max_move_id = result["id"]
            max_move = result["title"]
    ```
    
    - 비동기 방식
    - session.get() 사용
    - 비동기 방식으로 한번에 실행하기 위해 세마포어를 통한 숫자 제한과 asyncio.gather() 사용.
    - asyncio.gather()는 인자로 여러개의 코루틴을 받아야 함. 리스트 자체를 받아선 안됨! 그래서 *list명을 사용해서 리스트의 인자를 하나 하나 풀어서 넘겨준 것.
        - *tasks는 python에서 리스트를 풀어서 각각의 요소를 개별 인자로 전달하는 파이썬 문법!
    - 보통 변수 = 함수는 함수를 실행하고 결과 값이 저장됨.
    - 근데 async 함수는 결과로 코루틴 객체를 반환함. 또한, 실행된 상태가 아님! 아직 실행되지 않은 상태. 실행 대기중인 코루틴 객체가 변수에 저장된 상태라는 뜻.
    - await asyncio.gather()를 통해서 코루틴 객체들이 실행되게 된다.
        - tasks안에 있는 모든 코루틴을 이벤트 루프에 등록.
        - 동시 실행!
        - 모든 코루틴이 끝날 때까지 대기!
    
    ```python
    # 1. now_playing을 활용해 데이터 20개 가져오기 (일반 동기 써도 무방함)
    # 2. movie_id 모아놓기
    # 3. 그걸 바탕으로 movie/{movie_id}에 요청 동시에 보내기
    
    import asyncio
    import aiohttp
    from pprint import pprint
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    API_KEY = os.getenv('TMDB_API_KEY')
    params = {
        'language' : 'ko-kr',
    }
    headers = {
        "Authorization" : f"Bearer {API_KEY}"
    }
    
    simple_movies = []
    movies_id = []
    movies_title = []
    movies_vote_average = []
    movies_revenue = []
    
    async def movie_session(session, data_url, params, headers):
        url = f"https://api.themoviedb.org/3/{data_url}"
        async with session.get(url, params = params, headers = headers) as response:
            result = await response.json()        
            return result
    
    async def fetch_with_semaphore(semaphore, session, url, index):
        # 세마포어를 사용하여 동시 실행 숫자를 제한한다.
        async with semaphore:
            async with session.get(url, params = params, headers = headers) as response:
                # status = response.status
                # # 실제 요청이 수행되는 시점을 확인한다.
                # print(f"요청 완료: {url} (상태: {status})")
                result = await response.json()
                movies_revenue[index] = result['revenue']            
    
    async def movie_now():
        async with aiohttp.ClientSession() as session:
            # tmdb에서 now_playing 데이터 가져오기
            result = await movie_session(session, "movie/now_playing", params, headers)
            movie_results = result["results"]
    
            for movie_result in movie_results:
                movies_id.append(movie_result["id"])
                movies_title.append(movie_result["title"])
                movies_vote_average.append(movie_result["vote_average"])
                movies_revenue.append("")
    
    async def main(movies_id):
        
        movie_urls = [f"https://api.themoviedb.org/3/movie/{movie_id}" for movie_id in movies_id]
        
        # 동시 요청 숫자를 5개로 제한하는 세마포어를 생성한다.
        semaphore = asyncio.Semaphore(5)
        
        async with aiohttp.ClientSession() as session:
            # 모든 요청 태스크를 생성하되, 세마포어에 의해 5개씩 순차적으로 실행된다.
            tasks = [fetch_with_semaphore(semaphore, session, url, index) for index, url in enumerate(movie_urls)]
            await asyncio.gather(*tasks)
            
            for i in range(len(movies_id)):
                sub_movie = {
                    "title" : movies_title[i],
                    "vote_average" : movies_vote_average[i],
                    "revenue" : movies_revenue[i]
                }
                simple_movies.append(sub_movie)
            
            pprint(simple_movies)
    
    await movie_now()
    await main(movies_id)
    ```

- 비동기는 결국 외부에 api 요청을 여러 가지 하려는데, 시간이 오래 걸리기 때문에 한번에 하기 위해 사용하는 것!
- 원래는 하나의 요청을 하면 (클라이언트 → 서버) (서버 → 클라이언트) (클라이언트 → 서버) 이런 과정을 거쳐서 동작한다.
    - http는 무상태성, 비연결성의 특징이 있기 때문.
- 이런 과정을 한번만 하고, 이후엔 연결된 채로 (클라이언트 → 서버)의 과정을 한번만 하도록 하는 것이 세션이다.
- 이번엔 공공데이터 포털을 사용해서 데이터를 가져와 봤음.

```python
import requests
from pprint import pprint
import os
from dotenv import load_dotenv
import requests

load_dotenv()

def safe_int(value, default=1000000000):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def data_pull(detail_url, params):
    url = f"http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/{detail_url}"
    response = requests.get(url, params=params)
    data = response.json()
    return data

def sido_real_time_search():
    params = {
        'serviceKey' : data_api_key,
        'sidoName' : sido_name,
        'returnType' : "json",
        'ver' : '1.0',
        'numOfRows' : '100', 
        'pageNo' : '1'
    }
    detail_url = f"getCtprvnRltmMesureDnsty"
    data = data_pull(detail_url, params)
    items = data["response"]["body"]["items"]
    
    pm25_min = 1000000000000000000
    pm25_min_station_name = ""

    for item in items:
        
        pm25 = item["pm25Value"]
        station_name = item["stationName"]
        station_names.append(station_name)
        smart_sido_data[station_name] = item
        pm25 = safe_int(pm25)
        if pm25 < pm25_min:
            pm25_min = pm25
            pm25_min_station_name = station_name
    
    print(pm25_min, pm25_min_station_name)

sido_names = ["전국", "서울", '부산', '대구', 
              '인천', '광주', '대전', '울산', 
              '경기', '강원', '충북', '충남', 
              '전북', '전남', '경북', '경남', 
              '제주', '세종']

def station_real_time_search(station_name, data_term):
    params = {
        'serviceKey' : data_api_key,
        'stationName' : station_name,
        'returnType' : "json",
        'ver' : '1.0',
        'numOfRows' : '10000',
        'pageNo' : '1',
        'dataTerm' : data_term
    }
    detail_url = f"getMsrstnAcctoRltmMesureDnsty"
    data = data_pull(detail_url, params)
    items = data["response"]["body"]["items"]
    
    for item in items:        
        sub_dic = {
            "date_time" : item["dataTime"],
            "pm10_value" : item["pm10Value"],
            "pm25_value" : item["pm25Value"]
        }
        dust_days.append(sub_dic)
    
    for dust_day in dust_days:
        pprint(dust_day)

station_names = []
smart_sido_data = {}
dust_days = []
data_api_key = os.getenv('DATA_GO_API_KEY')
url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty'
print(f"시도명 목록 : {sido_names}")
sido_name = input("원하는 시도명을 입력하세요.")
# sido_name = '서울'
if sido_name in sido_names:
    sido_real_time_search()
else:
    print("잘못된 시도명 입니다.")

pprint(smart_sido_data["강서구"])

print(f"지역 목록 : {station_names}")
station = input("미세농도를 확인할 지역을 입력하세요.")
if station in station_names:
    station_real_time_search(station, "MONTH")
else:
    print("잘못된 지역명 입니다.")
    

```

- 공공 데이터 포털에서는 한번에 100개 이상의 데이터를 가져올 수 있기에 비동기 방식이 아니라 그냥 request를 사용해서 한번에 가져오게 구현함.
- 하지만 서버 입장에서는 이렇게 한번에 대량의 데이터를 가져올 수 있도록 구현하면 좋지 않음. 나중에 구현할 일이 있으면 주의하자!