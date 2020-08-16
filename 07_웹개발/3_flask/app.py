from flask import Flask, render_template  # render_template : return html page
import lotto_package  # lotto_package

app = Flask(__name__)

# 복권 회차에 따라 당첨번호를 출력하는 서비스
@app.route('/')
def index():
    # templates 폴더 안에 html 페이지가 있어야함
    return render_template('./index.html')

# 랜덤 로또 번호 출력
@app.route('/pick_lotto')
def pick_lotto():
    lucky_numbers = lotto_package.get_unlucky_numbers()
    return render_template('./pick_lotto.html', lucky_numbers=lucky_numbers)  # html에 변수 넘기기

# 랜덤 추출한 번호와 실제 로또 번호 비교
@app.route('/get_win_numbers/<int:round_number>')
def win_num(round_number):
    win_numbers, bonus_number, round_date = lotto_package.get_lotto_numbers(round_number)
    unlucky_numbers = lotto_package.get_unlucky_numbers()  # 내가 찍은 숫자
    rank, count, bonus_count = lotto_package.get_rank(win_numbers, bonus_number, unlucky_numbers)  # 등수, 번호 맞춘 수, 보너스 번호 맞춤 여부
    zip_numbers = zip(range(1, 7), unlucky_numbers, win_numbers)
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
    win_numbers, bonus_number, round_date = lotto_package.get_lotto_numbers(round_number)
    destiny_count = 0  # 로또를 산 횟수
    win_count = [0, 0, 0, 0, 0]  # 당첨 횟수 1등~5등
    # 가즈아
    while(True):
        # 내가 찍은 숫자
        unlucky_numbers = lotto_package.get_unlucky_numbers()  # 내가 찍은 숫자
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

