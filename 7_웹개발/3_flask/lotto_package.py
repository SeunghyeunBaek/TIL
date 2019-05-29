import requests
import json
import random


def get_lotto_numbers(round_number):
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
    return win_numbers, bonus_number, round_date


def get_unlucky_numbers():
    unlucky_numbers = random.sample(range(1, 47), 6)
    unlucky_numbers.sort()
    return unlucky_numbers


def get_rank(win_numbers, bonus_number, unlucky_numbers):
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
    return rank, count, bonus_count


print(__name__)
