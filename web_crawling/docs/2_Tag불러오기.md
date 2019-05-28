# 1. 태그 속성 가져오기

*파이썬으로 배우는 웹크롤러*

- 태그는 '태그 이름','속성','문자열' 로 구성됐다.
- 태그 속성 가져오기

```python
html = '''
    <html>
        <head>
            <title>타이틀 태그</title>
        </head>
        <body>
            <p>test1</p>
            <p>test2</p>
            <p>test3</p>
        </body>
    </html>
'''
soup = bs4.BeautifulSoup(html, 'lxml')
# 타이틀 태그 객체
# bs4 로 객체를 만들면 html 태그를 객체로 저장한다.
print(f'태그 : {soup.title}')
print(f'태그 사이의 문자열 : {soup.title.text}')
print(f'태그 이름 : {soup.title.name}')
```

```python
# type, id, class
html = '''
    <html>
        <body>
            <input type = 'text' id = 'test id' class = 'c1 c2'/>
        </body>
    </html>
'''
soup = bs4.BeautifulSoup(html,'lxml')
print(soup.input.attrs) # attrs는 dictionary로 저장됨
print('-'*120)
print(soup.input.attrs['type'])
print(soup.input.attrs['id'])
print(soup.input.attrs['class'])
print('-'*120)
#Dictionary 에 없는 key 값을 참조하면 오류가 난다. get 함수를 쓰면 None 을 반환한다.
#print(soup.input.attrs['non_ex_key'])
print(soup.input.attrs.get('non_ex_key','default value')) #key가 없으면 default value 를 반환함.
```

*190319*

- 영역을 구분하는 태그(p214)
  - div : 영역 구분
  - p : 단락 구분 (div 와 별 차이 없으나 div 보다 단락 간격이 더 크다)
  - span : 개행 안함
  - *div 와 p 모두 css 로 단락 간격을 조절할 수 있다*

- 화면상에 영향을 미치지 않는 태그(div,span)는 영역을 구분하기 위해 사용
- 영역을 구분해 놓은 후에 Style sheet를 활용

- soup.tag.string *vs* soup.tag.text

```python
html = '''
    <p>
        test0
        <span>test1</span>
        <span>test2</span>
        <span>test3</span>
    </p>
'''
soup = bs4.BeautifulSoup(html,'lxml')
print(soup.prettify())
print('--'*40)
print(soup.p.text) # 태그사이에 다른 태그가 있어도 문자열을 모두 가져옴
print('--'*40)
print(soup.p.string) # 태그사이에 다른 태그가 있으면 None을 반환
```

# 2 . 원하는 태그 가져오기(p228)

- find_all('tag') : 태그에 해당하는 객체를 리스트로 반환
  - 입력한 태그가 html 문서내에 없다면 길이가 0인 리스트를 반환

```python
html = '''
    <html>
        <body>
            <p class = 'a1'>p 태그 1</p>
            <p class = 'a2'>p 태그 2</p>
            <p class = 'a1 a2'>p 태그 3</p>
            <ul>
                <li class = 'a1'>항목 1</li>
                <li class = 'a2'>항목 2</li>
                <li class = 'a1 a2'>항목 3</li>
            </ul>
        </body>
    </html>
'''
soup = bs4.BeautifulSoup(html, 'lxml')

#p 태그 모두 가져오기
p_list = soup.find_all('p')
#li 태그 모두 가져오기
li_list = soup.find_all('li')
print(p_list,'\n',li_list)

#tag.text 출력
for p_tag in p_list:
    print(p_tag.text)
for li_tag in li_list:
    print(li_tag.text)
```

- class(css class)에 따라 태그 가져오기
  - css : cascade style sheet, 태그 디자인 속성을 class로 지정함.
  - 같은 css class를 복수의 태그에 적용했을 수도 있다. 이에 원하지 않은 태그도 가져올 수 있다.

```python
# css(cascade style sheet)

# p_tage 중 class가 a1 인 태그를 가져온다.
p_list_a1 = soup.find_all('p',class_ = 'a1')
print(p_list_a1)

# p_tage 중 class가 a2 인 태그를 가져온다.
# find_all 인자 입력 순서는 tag,class_ 순이다.
p_list_a2 = soup.find_all('p','a2')
print(p_list_a2)

# 태그에 관계없이 class 가 a1 인 태그 불러오기
a1_list = soup.find_all(class_='a1')
print(a1_list)

# 태그에 관계없이 class 가 a2 인 태그 불러오기
a1_list = soup.find_all(class_='a2')
print(a1_list)
```

- find('tag') 
  - 맨 처음 나온 tag객체를 반환
  - 해당 태그가 html 문서에 하나밖에 없다면 사용
  - 태그가 없을 경우 None을 반환

```python
html = '''
    <html>
        <body>
            <p class = 'a1' id = 'test1'>p 태그 1</p>
            <p class = 'a1'>p 태그 2</p>
            <p class = 'a2'>p 태그 3</p>
        <body>
    </html>
'''
soup = bs4.BeautifulSoup(html,'lxml')

p_tag = soup.find('p')
print(p_tag) # <p class = 'a1'>p 태그 1</p>
a1 = soup.find(class_='a1')
print(a1) # <p class = 'a1'>p 태그 1</p>
a2 = soup.find(class_='a2')
print(a2) # <p class = 'a2'>p 태그 3</p>
```

- id로 태그 가져오기
  -  id 속성은 중복되지 않는다. find를 활용해 접근할 수 있다.
  - id는 개발자가 특정 태그 하나를 지칭하기 위한 용도로 사용

```python
id_test1 = soup.find(id = 'test1')
print(id_test1)
```

- select
  - tag, class , id 를 문자열로 받아서 결과를 반환한다.
  - 태그가 1개밖에 없어도 list로 반환한다. (cf. find는 str로 반환)
    - tag : 'tag_name'
    - class : '.class_name'
    - id : '#id_name'

```python
p_list = soup.select('p')
a1_list = soup.select('.a1')
test1_list = soup.select('#test1')
p_a1_list = soup.select('p.a1')
```

-  find *vs* select

```python
#find
test1 = soup.find(id = 'test1')
test2 = soup.find(id = 'test2')
test1_p = test1.find('p').text
test2_p = test2.find('p').text

#select
test1_s = soup.select('#test1>p')[0].text
test2_s = soup.select('#test2>p')[0].text
```

