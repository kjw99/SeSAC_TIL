- 알고리즘 : 문제 해결 방법을 정의한 **단계적 절차**.
- 프롬프트 기법 중 CoT 라는게 있음. 단계적으로 설명해달라고 하는 방법. AI를 사용할 때 대충 알려달라고 하는 것 보다 이런 방식으로 자세히 알려달라고 하는게 더 좋음.
- Counter() 함수
    - collections에 있는 함수임. import 필요!
    - **Counter(text) 이런 방식으로 사용. 문자열을 받아서 문자열에 있는 모든 문자를 딕셔너리 형태로 변환하고, 각각 몇개가 있는지 저장함.**
    - key : value 형식으로 변환되기 때문에 “hello” 같은 경우에는 { “h” : 1, “e” : 1, “l” : 2, “o” : 1 } 이런 형식으로 저장됨.
    - 반환값을 변수에 저장한 후 딕셔너리 값을 불러오듯이 counter[’h’] 이렇게 부르면 1이라는 value 값을 받을 수 있음.
- 문자열 뒤집기 간단한 방법.
    - text[::-1] 이렇게 하면 text에 있는 문자열이 뒤집힌다. “12345” → “54321”
- if 조건에 대해.
    - 값이 존재한다 → True.
    - if는 보통 뒤에 조건이 오는데, 조건 대신 if -3, if 5 이런식으로 해도 True 취급으로 된다는 것.
    - 값이 존재하지 않는다면 False인데, 0은 값이 존재하지 않는 취급을 받음.
    - 숫자 외에도 문자열도 가능. ‘abc’, ‘ ‘(공백) 등. 아예 공백도 아니라 ‘’ 이렇게 자리가 없는 경우(빈 문자열) False 취급.
    - if [1, 2, 3] 이런것도 가능. if [] 이런식으로 빈 리스트면 false
    - set, 딕셔너리 등 다 동일함
    - python에서는 된다는 것. 다른 언어는 다름.
- 사소한 or and 작동 방식.
    - A and B의 경우 T T / T F / F T / F F 이런 방식으로 True False 체크를 한다. 그래서 A와 B를 모두 확인해야 함.
    - A or B의 경우 or은 둘 중 하나만 True면 되니까, A가 True면 B는 확인을 안함.
    - 그래서 print(3 or 6 or 9) 이런식으로 출력한다면? 결과값은 3이 나온다.
        - 3에서 이미 True 취급이니까 맨 앞에 3을 결과로 내놓는 식으로 작동.
    - print( (3 or 6 or 9) in [3, 6, 9] ) 이렇게 하면 True가 나오는데, 3 6 9중 하나의 숫자가 리스트에 포함되어 있나요?? 를 따지는게 아니라 3이 리스트에 포함되어 있나요? 를 따지는 것.
        - 그래서 4 or 6 or 9 이렇게 조건을 바꾸면 4 in [3, 6, 9] 를 체크하게 되는 셈이라 False가 나옴.
- 알고리즘 문제들
    - 콜라츠 규칙
        - 주소 : https://dailyalgo.kr/ko/problems/157
        - 로직 : 문제에 써 있는 대로 구현.
        - 최종 코드
        
        ```python
        def solution(n):
            answer = 0
            while(True):        
                if n == 1:
                    break
                elif n % 2 == 0:
                    n = n / 2
                elif n % 2 != 0:
                    n = (n * 3) + 1
                answer += 1
            return answer
        
        ```
        
    - 팰린드롬 수
        - 주소 : https://dailyalgo.kr/ko/problems/158
        - 로직
            1. 주어진 숫자 n을 문자열로 변환.
            2. 이후 문자열의 길이를 파악하고, 1인 경우 무조건 정답이니까 따로 조건 체크. 
            3. 왼쪽, 오른쪽 문자를 하나 하나 비교해서 일치하지 않는 경우가 있으면 False 처리.
            4. 좌 우를 한번에 체크하니까 문자의 길이의 절반 만큼만 반복하면 됨. 그래서 cnt 길이를 절반으로 줄여서 반복 시작.
        - 최종 코드
        
        ```python
        def solution(n):
            answer = True
            text = str(n)
            left = 0
            right = -1
            cnt = len(text)
            if cnt > 1:
                cnt = int(cnt / 2)
            for i in range(cnt):
                if text[left] != text[right]:
                    answer = False
                    break
                left += 1
                right -= 1
            return answer
        
        ```
        
    - 369게임 1
        - 주소 : https://dailyalgo.kr/ko/problems/168
        - 로직 : n 만큼 반복하면서 i를 문자열로 바꾸고 3, 6, 9의 문자가 포함되어 있는지 일일이 체크. 높은 난이도의 문제면 이런 식으로 말고 다른 방법이 필요할 것.
        - 최종 코드
        
        ```python
        def solution(n):
            answer = 0
            for i in range(n + 1):
                if "3" in str(i) or "6" in str(i) or "9" in str(i):
                    answer += 1
                    continue        
            return answer
        
        ```
        
    - 369게임 2
        - 주소 : https://dailyalgo.kr/ko/problems/169
        - 로직
            1. 3333 = count 4 증가. 이런 식이니까 해당 숫자에 3, 6, 9가 얼마나 포함되어 있는지 카운트 해줘야 한다.
            2. collections의 Counter 함수를 사용함.
                1. 매개 변수의 문자열을 하나 하나 분리해서 딕셔너리 형태로 몇 개가 있는지 저장해줌.
            3. 반복문을 돌면서 3, 6, 9 숫자의 개수를 전부 더하며 계산. 
        - 최종 코드
        
        ```python
        from collections import Counter
        
        def solution(n):
            answer = 0
            for i in range(n + 1):
                counter = Counter(str(i))
                answer += counter['3'] + counter['6'] + counter['9']
            return answer
        
        ```
        
    - 최빈값 찾기
        - 주소 : https://dailyalgo.kr/ko/problems/171
        - 로직
            1. numbers 배열에서 어떤 숫자가 가장 많이 나왔는가 를 찾는 문제.
            2. numbers[3] = 5 이런식으로 나온다면, 5를 배열의 하나의 방에 저장해서 lst[5]의 값이numbers에 있는 5의 개수. 이렇게 될 수 있도록 배열을 생성할 것임. 
            3. 숫자의 범위가 -1000 ~ 1000이기 때문에 모든 숫자에 + 1000을 해줘서 0부터 시작하도록 함. 배열의 크기는 2001 (1 ~ 2000 방)
            4. 때문에, 값을 +1 할 때 lst[num + 1000] 이런식으로 + 1000을 해줘야 한다.
            5. 이후 lst의 모든 방을 확인하면서 가장 높은 값이 몇번 방에 있는지 확인.
            6. 해당 방의 번호가 곧 문제에서 요구하는 최빈값이 된다.  
        - 로직 개선
            - 개선 전 코드
            
            ```python
                def solution(numbers):
                answer = 0
                lst = []
                max_number = 0
                max_count = 0
                for _ in range(2001):
                    lst.append(0)
                for num in numbers:
                    lst[num + 1000] += 1
                for i in range(2001):
                    if max_count < lst[i]:
                        max_number = i - 1000
                        max_count = lst[i]
                answer = max_number
                return answer
            ```
            
            - 개선 전 코드에서는 numbers에서 값을 빼와서 +1 하는 과정만 따로 반복을 돌리고, 이후 최빈값 찾는 과정을 거쳤는데, 이 부분을 개선할 수 있음.
            1. 기존의 4번인 값을 +1 하는 과정에서 현재 최빈값의 개수를 비교하고, 서로 동일하면 더 작은 최빈값의 값을 찾아서 더 작은 최빈값으로 갱신.
            2. +1을 했더니, 기존에 있던 최빈값 개수보다 현재 +1한 값이 더 많다면 더 많은 최빈값 개수와 값으로 갱신
            3. 이렇게 변경하면 반복문 하나로 처리가 가능.
            4. 또한, 모든 방을 0으로 초기화하는 과정을 반복문이 아니라 초기값 0 설정 * 2001 이런 식으로 할 수 있음.
            - 추가로 tmp_value 라는 변수를 설정해서 -1000, +1000이 아니라 변수로 -, + 할 수 있도록 수정하면 더 좋다.
        - 최종 코드
        
        ```python
        def solution(numbers):
            answer = 0
            tmp_value = 1000
            lst = [0] * (1000 + tmp_value + 1)
            min_number = 0
            max_count = 0
            # for _ in range(2001):
            #     lst.append(0)
            for num in numbers:
                num = num + tmp_value
                lst[num] += 1
                if max_count == lst[num]:
                    if min_number > num - tmp_value:
                        min_number = num - tmp_value
                if max_count < lst[num]:
                    min_number = num - tmp_value
                    max_count = lst[num]
            answer = min_number
            return answer
        
        ```
        
        - 딕셔너리 사용 버전
        - 로직
            1. 딕셔너리는 { “키” : 값 } 형태로 저장됨. 해당 문제에 사용하기 적합. { “1” : 2, “2” : 1 } 이런식으로 저장하면 되니까.
            2. 빈 딕셔너리를 생성하고 최빈값의 개수를 저장하는 most_common_value_count 변수와 최빈값의 값을 저장하는 most_common_value 변수를 지정.
            3. numbers에서 한 개씩 값 확인
            4. count_dic[num] << 이렇게 저장하면 num이 3인 경우 { “3” : 1 } 이렇게 저장될 것임. 최초에는 .get()함수를 통해 기본값 0이 생성되고, 이후 + 1이 되는 방식. 나중에는 그냥 기존 값 + 1로 연산
            5. 개수를 세면서 최빈값의 데이터도 계속 갱신. 최빈값의 개수가 지금 세고 있는 값이랑 같은 경우 최빈값이 더 작은 쪽으로 갱신.
            6. 지금 센 개수가 지금 가지고 있는 최빈값 개수보다 많으면 최근 데이터로 새롭게 갱신
            7. 이렇게 하면 반복문 하나에서 최빈값에 대한 정보를 다 구할 수 있음.
            8. 추가로 Counter 함수를 사용하면 훨씬 편하게 값을 구할 수 있다. 
        - 최종 코드
        
        ```python
        from collections import Counter
        
        def solution(numbers):
            answer = 0
        
            count_dic = {}
            most_common_value_count = 0
            most_common_value = None
            # 모든 값 확인
            for num in numbers:
                # 개수 세기
                count_dic[num] = count_dic.get(num, 0) + 1
                
                # 최빈값의 개수가 지금 센거랑 같다면 최빈값을 작은 값으로 교체
                if count_dic[num] == most_common_value_count:
                    if most_common_value > num:
                        most_common_value = num
        
                # 지금 센 개수가 지금까지 센 개수보다 많으면 데이터 변경
                if count_dic[num] > most_common_value_count:
                    # 최빈값 개수
                    most_common_value_count = count_dic[num]
                    # 최빈값 값
                    most_common_value = num
            
            # print(Counter(numbers)) # 이거 쓰면 쉬운데 지금은 참고만 하자
                    
            return most_common_value
        ```
        
    - 최소 동전 거스름돈 1
        - 주소 : https://dailyalgo.kr/ko/problems/184
        - 로직
            1. 단위가 큰 동전의 개수부터 파악해야 한다. 1800원은 500원 3개, 100원 3개인데, 100원 18개로도 가능은 하기 때문.
            2. 리스트를 통해 0번 방부터 500원, 100원 … 1원 이런 식으로 순서에 맞게 값을 저장하는방식으로 설계.
            3. coin_size 리스트를 통해 500원, 100원 … 1원 까지 저장하고 해당 리스트의 길이만큼 반복문 시작.
            4. count에 계산하는 동전의 개수를 계속 더한다.
                1. 동전 개수 저장은 현재 남아있는 금액 / n번 동전 이런식으로 계산하고 int() 형변환을 통해 몫만 구하게 함.
                2.  1800 / 500원 이면 3이 나오도록
            5. 이후 현재 남아있는 금액을 최신화하고 계속 반복.
                1. 현재 금액과 n번 동전을 나눠서 남아있는 나머지 부분을 저장하면 현재 남아있는 금액이 된다.
            6. 이후 sum()함수를 통해 coin 리스트의 값을 전부 더하면 끝.
        - 최종 코드
        
        ```python
        def solution(change):
            answer = 0
            count = 0
            coin_size = [500, 100, 50, 10, 5, 1]
            for i in range(len(coin_size)):
                count += int(change / coin_size[i])
                change = change % coin_size[i]
            answer = count
            return answer
        
        ```
        
    - 슬라이딩 윈도우1
        - 주소 : https://dailyalgo.kr/ko/problems/202
        - 로직
            1. 주어진 리스트의 길이와 window가 일치하면 그냥 리스트 전체를 sum()으로 합하면 된다.
            2. 그게 아닌 경우, 리스트의 맨 왼쪽부터 window 길이까지 합을 구한 후. 맨 왼쪽 + 1부터 window 길이 + 1까지의 리스트의 합을 구하면 됨.
            3. 중요한 것은 for 에서 range() 조건을 리스트 길이 - window + 1로 해서 리스트의 범위 밖으로 탐색하지 않도록 하는 것.
        - 중간 코드
        
        ```python
        def solution(numbers, window):
            answer = []
        
            numbers_len = len(numbers)
            if numbers_len == window:
                answer.append(sum(numbers))
            else:
                for i in range(numbers_len - window + 1):
                    answer.append(sum(numbers[i:window + i]))
        
            return answer
        
        ```
        
        - 개선
            - 문제에서는 테스트 케이스의 크기가 작은 경우라서 상관이 없지만, window가 엄청 큰 경우에 기존 코드에서는 연산이 많이 일어나게 됨.
            - 기존 코드는 0 ~ 5까지 더하고, 1 ~ 6까지 더하고 이걸 반복하는데, 이게 사이즈가 5가 아니라 60 80 이렇게 되면??
            - 연산 과정을 잘 살펴보면 중복되는 부분이 있음. 1번 윈도우는 그냥 더해서 계산하고, 2번 윈도우부터는 1번 윈도우에서 중복된 부분을 가져오면 된다.
            - 0 ~ 5 → 1 ~ 6 이때 1 ~ 5까지는 중복되는 영역. 즉, 왼쪽 첫 부분 0을 빼고, 오른쪽에 새로운 부분 6을 더하면 반복할 때마다 2번씩만 연산하면 끝이다.
            1. 첫 부분은 그대로 계산해야 하니까 sum() 함수를 사용해 리스트의 시작 부분부터 window 사이즈 부분까지 더한 값을 total에 저장한다. [ : window ] 사용.
            2. 2번 윈도우부터 반복적인 계산을 시도. 기존 total 값에서 왼쪽 부분을 빼고, 오른쪽 부분을 더함.
            3. 반복문이 0부터 시작하는 이유는 2번 윈도우는 numbers[0] 의 값을 빼줘야 하기 때문. 그래서 자연스럽게 0부터 시작하게 됨.
            4. 더하는 값의 인덱스를 구하는 것은 현재 i와 window를 더해서 위치를 구할 수 있음.
                1. [1, 2, 3, 4, 5], window = 3. 이라고 치면, 1번 윈도우는 1 + 2 + 3
                2. 2번윈도우는 -1 + (1 + 2 + 3) + 4. 이렇게 됨. 1은 [0] 위치에 있고, 4는 [3] 위치에 있음.
            5. 그래서 total을 구하는 식은 total - numbers[i] + numbers[i + window]가 된다.
            6. 반복문의 range() 범위가 중간 코드와 다른 이유는 중간 코드에선 [i : window + i] 이런식으로 윈도우의 값을 구했는데, [ ]에서 마지막 뒷 부분은 제외 처리가 되기 때문임.
                1. [4:7] 이라면 4, 5, 6 이렇게 된다. range(6) 이런 경우도 6은 제외가 됨. 그래서 + 1을 해줘서 numbers 길이가 7이고, window가 3인 경우 최소 4번 index 까지는 오게 해야하기 때문.
                2. 최종 코드에서는 [i + window] 이런 식으로 오른쪽 값을 계산함. 이 경우엔 [6] 이 된다면, 그대로 6번 index의 값을 가져오기에 따로 +1을 해줄 필요가 없다.
        - 최종 코드
        
        ```python
        def solution(numbers, window):
            answer = []
        
            total = sum(numbers[:window])
            answer.append(total)
        
            for i in range(len(numbers) - window):
                total = total - numbers[i] + numbers[i + window]
                answer.append(total)
        
            return answer
        
        ```
        
    - 제거된 수 찾기
        - 주소 : https://dailyalgo.kr/ko/problems/229
        - 로직
            1. 1부터 n까지의 합을 구하기 위해 리스트를 주는데, 그 중에서 특정한 수 하나가 빠져있음.
            2. 이 경우 1부터 n까지 합을 구하고, 리스트에 있는 값의 합을 구해서 빼기 연산을 하면 빠진 숫자가 나오게 된다.
            3. 여기서 n은 주어진 리스트의 길이 + 1일 것임. 숫자 하나가 빠졌다고 하니까.
            4. original_hap에서 range() 부분에 +2를 해둔 이유는 range()는 5를 넣는다 치면 0 1 2 3 4 이렇게 나오기 때문. 그래서 원래 +1을 하는데, 문제를 풀기 위해 +1을 더 해야 한다. 
        - 최종 코드
        
        ```
        def solution(numbers):
            answer = 0
            numbers_len = len(numbers)
            original_hap = sum(range(numbers_len + 2))
            numbers_hap = sum(numbers)
            answer = original_hap - numbers_hap
            return answer
        
        ```
        
        - set 사용한 코드
        - 로직
            - set을 통해 원본 집합과 1개가 빠진 집합을 서로 차집합 연산을 해서 값을 구하는 방법.
        
        ```python
        def solution(numbers):
            answer = 0
            numbers_len = len(numbers)
            numbers_set = set(numbers)
            full_set = set(range(1, numbers_len + 2))
            remain_set = full_set - numbers_set
            answer = remain_set.pop()
            return answer
        ```
        
    - 서브블록 합의 최대와 최소 1
        - 주소 : https://dailyalgo.kr/ko/problems/161
        - 로직
            1. 2 x 2라서 그냥 row, col 부분에 +1 하며 계산함. 사이즈가 커지거나 하면 반복문을 써야 할지도??
            2. 주어진 2차원 배열에서 맨 왼쪽 위부터 시작해서 2 x 2 사이즈의 블럭에 있는 값을 더하고 옆으로 이동해서 또 더하고 이 과정을 반복하는 것.
            3. 그러면서 더한 값의 최대 값과 최소 값을 구하는 문제.
        - 최종 코드
        
        ```python
        def solution(array):
            answer = []
            row_len = len(array) - 1
            col_len = len(array[0]) - 1
            max = -50000000
            min = 50000000
            for i in range(row_len):
                for j in range(col_len):
                    sum = 0
                    sum = array[i][j] + array[i + 1][j] + array[i][j + 1] + array[i + 1][j + 1]
                    if sum > max:
                        max = sum
                    if sum < min:
                        min = sum    
            answer.append(max)
            answer.append(min)
            return answer
        ```