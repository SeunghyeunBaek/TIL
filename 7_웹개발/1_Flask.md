# Flask와 웹 애플리케이션

* app.run : 사용자의 request를 기다리는 상태
* request : `localhost:5000`/address
* reponse : index, lotto

`render_template` : html 반환, 변수를 전달할 수 있음, html은 templates 폴더 안에 있어야함.

`@app.route('/option')` : url로 option을 받으면 다음 함수를 실행

```python
# 랜덤 로또 번호 출력
@app.route('/pick_lotto')
def pick_lotto():
    lucky_numbers = lotto_package.get_unlucky_numbers()
    return render_template('./pick_lotto.html', lucky_numbers=lucky_numbers)  # html에 변수 넘기기

```

`{{var}}` :  .py에서 변수 받기

```html

<table>
    <tr>
        <th style="text-align:center">번호</th>
        <th style="text-align:center">너의 희망</th>
        <th style="text-align:center">적나라한 현실</th>
    </tr>
    {% for idx, unlucky_number, win_number in zip_numbers %}
    <tr>
        <td style="text-align:center">{{idx}}번</td>
        <td style="text-align:center">{{unlucky_number}}</td>
        <td style="text-align:center">{{win_number}}</td>
    </tr>
    {% endfor %}
```

