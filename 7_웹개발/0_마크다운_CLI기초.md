# 마크다운 문서 작성법

`190527`

## 마크다운 작성하기

### 제목 작성

제목은 중요도 순으로 #을 붙인다.

### 리스트 작성

#### 순서가 있는 리스트

1. 앱을 받는다
2. 회원가입한다
3. W카페를 찾는다
4. 커피를 주문한다
5. 알림이 오면 픽업하러 간다

#### 순서가 없는 리스트

* 깃 허브 설치
* 파이썬 설치
* 파이참 설치
* 타이포라 설치

### 일반 문단 작성

배고프다  고배프다 다프고배 고배다프

### 코드 블럭 작성

**동행복권 url**로 복권 당첨 정보 크롤링하기. `crawler.py` 

```python
first_win_amount = []  # 1등 상금
first_winner = []  # 1등 인원
total_amount = []  # 누적 상금
no = []  # 회차
win_no = []  # 로또 당첨 번호
win_date = []  # 발표 날짜

for num in range(1, 800):
    url = f'https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={num}'
    # print(url)
    res = requests.get(url)
    data = res.text
    data_dict = json.loads(data)
    if data_dict['returnValue'] == 'success':
        no.append(data_dict['drwNo'])
        first_win_amount.append(data_dict['firstWinamnt'])
        first_winner.append(data_dict['firstPrzwnerCo'])
        total_amount.append(data_dict['totSellamnt'])
        win_date.append(data_dict['drwNoDate'])
        # 로또 번호
        keys = list(data_dict.keys())
        drwtNos = [key for key in keys if 'drwtNo' in key]
        tmp = [data_dict[drwtNo] for drwtNo in drwtNos]
        win_no.append(tmp)
    else:
        print('return value is False')

# 데이터 프레임 만들기
zip_obj = list(zip(no, win_date, first_win_amount, total_amount, first_winner, win_no))
df_dh = pd.DataFrame(zip_obj, columns=['no', 'date', 'first amount', 'winners', 'total amount', 'win numbers'])
df_dh.to_csv(r'lotto.csv', index=False)  # 저장

print('크롤링 끗')
```
### 표만들기

| Title              | Contents                                                     | Desc               |
| ------------------ | ------------------------------------------------------------ | ------------------ |
| 마크다운 작성하기  | 제목작성, 리스트작성, 일반 문단 작성, 코드블럭 작성, 표만들기 | 마크다운 기본 문법 |
| CLI(터미널 명령어) | CLI 기본 명령어                                              |                    |
| GIT 사용법         |                                                              |                    |

## CLI(터미널 명령어)

### CLI 기본 명령어

```shell
$ pwd # 현재 디렉토리 출력 (pwd : present working directory)
$ ls # 현재 디렉토리 내 폴더,파일 목록 출력 (ls : list segment)
$ mkdir test # test 디랙토리 생성 (mkdir : make directory)
$ rm a.txt # a.txt 파일 삭제(rm : remove)
$ rm -r text # text 디렉토리 삭제(r: recursive)
$ cd test # test 디렉토리로 이동 (cd : change directory)
$ cd .. # 상위 디렉토리로 이동
$ cd - # 이전 디렉토리로 이동
$ cd ~ # 최상위 디렉토리로 이동(~ : root directory)
$ touch a.txt b.txt # a.txt, b.txt 를 생성한다cd 
```
## GIT 기초 명령

``` shell
$ git init # 현재 디렉토리(pwd) 관리자 추가, 디렉토리에 (master)를 출력함
$ rm -r /.git # /.git 을 삭제하면 관리 끝. 빡세게 초기화할 때 사용

$ git remote add 저장소이름 'url' # 원격 리파지토리 설정. url은 리파지토리 주소, origin 은 리파지토리 이름 

$ git add test.md # test.md 파일 추가(사진 프레임 안으로 들어오게 하기)
$ git add . # 해당 디렉토리 모든 파일 추가
$ git commit -m 'MESSAGE' # add된 파일을 모두 커밋

$ git push origin master # 원격 리파지토리에 백업
```



