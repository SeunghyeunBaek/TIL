# Flask와 웹 애플리케이션

* app.run : 사용자의 request를 기다리는 상태
* request : `localhost:5000`/address
* reponse : index, lotto

```python
from flask import Flask
import random

app = Flask(__name__)


# 주소창에 '/'가 있으면 index를 실행한다.
@app.route('/')
def index():
    return '노동왕 워킹'

# 주소창에 'lotto'가 있으면 lotto를 실행한다.
@app.route('/lotto')
def lotto():
    lucky_nums = random.sample(range(1, 46), 6)
    return f'노동왕 워킹 : {lucky_nums}'

if __name__ == '__main__':
    app.run(debug=True)

```

```html
html for돌리기
<u1>
    {% for num in lucky_numbers %} 
    <li>{{num}}</li>
    {% endfor %}
</u1>
```

