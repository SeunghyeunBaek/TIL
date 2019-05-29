from flask import Flask, render_template # render_template : return html page
import random
import requests
import json
import numpy as np

app = Flask(__name__)

# 복권 회차에 따라 당첨번호를 출력하는 서비스
@app.route('/')
def index():
    # templates 폴더 안에 html 페이지가 있어야함
    return render_template('./index.html')

# 랜덤 로또 번호 출력
@app.route('/pick_lotto')
def pick_lotto():
    lucky_numbers = random.sample(range(1, 46), 6)
    lucky_numbers.sort()  # list is mutable class, list 원본을 바꾼다. Tuple, str 에는 없다.
    return render_template('./pick_lotto.html', lucky_numbers=lucky_numbers)  # html에 변수 넘기기

# variable routing : 번수처럼 url 값을 입력받는다.
@app.route('/get_win_numbers/<int:round_number>')
def win_num(round_number):
    url = f'https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={round_number}'
    lotto_data = requests.get(url).text
    lotto_json = json.loads(lotto_data)
    # 최대한 fail 일 때 연산을 안하도록 만든다.
    if lotto_json['returnValue'] == 'fail':
        return f'<h1>{round_number}회차는 아직 안열렸다</h1>'
    else:
        # 회차 정보
        round_number = round_number
        round_date = lotto_json['drwNoDate']
        # 당첨 번호
        win_numbers = [value for key, value in lotto_json.items() if 'drwtNo' in key]
        win_numbers.sort()
        # keys = lotto_json.keys()
        # win_number_keys = [num_key for num_key in keys if 'drwt' in num_key]
        # win_numbers = [lotto_json[win_number_key] for win_number_key in win_number_keys]
        # win_numbers.sort()
        bonus_number = lotto_json['bnusNo']  # 보너스 번호
        unlucky_numbers = random.sample(range(1, 46), 6)  # 내가 찍은 숫자
        unlucky_numbers.sort()
        zip_numbers = zip(unlucky_numbers, win_numbers)
        # 등수 산출
        count = len(set(win_numbers).intersection(unlucky_numbers))  # 맞춘 번호 개수
        bonus_count = 1 if bonus_number in unlucky_numbers else 0  # 보너스 번호(맞추면 1 틀리면 0)

        if count == 6:
            rank = 1
        elif count == 5 and bonus_count == 1:
            rank = 2
        elif count == 5:
            rank = 3
        elif count == 4:
            rank = 4
        elif count == 3:
            rank = 5
        else:
            rank = '언랭'

        return render_template('./get_win_numbers.html',
                               win_numbers=win_numbers,
                               bonus_number=bonus_number,
                               rank=rank,
                               count=count,
                               bonus_count=bonus_count,
                               unlucky_numbers=unlucky_numbers,
                               zip_numbers=zip_numbers,
                               round_number=round_number,
                               round_date=round_date)

# 몇개를 사야 1등이 나올까
@app.route('/how_many_lotto/<int:round_number>')
def how_many_lotto(round_number):
    url = f'https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={round_number}'
    lotto_data = requests.get(url).text
    lotto_json = json.loads(lotto_data)
    keys = lotto_json.keys()
    # 회차 정보
    round_number = round_number
    round_date = lotto_json['drwNoDate']
    # 당첨 번호
    win_number_keys = [num_key for num_key in keys if 'drwt' in num_key]
    win_numbers = [lotto_json[win_number_key] for win_number_key in win_number_keys]
    win_numbers.sort()
    bonus_number = lotto_json['bnusNo']  # 보너스 번호
    destiny_count = 0  # 로또를 산 횟수
    win_count = [0, 0, 0, 0, 0]  # 당첨 횟수 1등~5등
    # 가즈아
    while(True):
        # 내가 찍은 숫자
        unlucky_numbers = random.sample(range(1, 46), 6)
        unlucky_numbers.sort()
        # 등수 산출
        count = len(list(set(win_numbers).intersection(unlucky_numbers)))  # 맞춘 수
        bonus_count = 1 if bonus_number in unlucky_numbers else 0  # 보너스 번호

        if count == 6:
            rank = 1
            win_count[0] = win_count[0] + 1
            break
        elif count == 5 and bonus_count == 1:
            rank = 2
            win_count[1] = win_count[1] + 1
        elif count == 5 and bonus_count == 0:
            rank = 3
            win_count[2] = win_count[2] + 1
        elif count == 4:
            rank = 4
            win_count[3] = win_count[3] + 1
        elif count == 3:
            rank = 5
            win_count[4] = win_count[4] + 1
        else:
            rank = -1
        destiny_count = destiny_count + 1

    wasted_money = destiny_count*1000
    return render_template('./how_many_lotto.html',
                           win_numbers=win_numbers,
                           bonus_number=bonus_number,
                           count=count,
                           bonus_count=bonus_count,
                           destiny_count=destiny_count,
                           win_count=win_count,
                           wasted_money=wasted_money,
                           round_number=round_number,
                           round_date=round_date)


if __name__ == '__main__':
    app.run(debug=True)
