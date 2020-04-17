# HTTPS 와 SSL 인증서

*200416*

*references*

* [생활코딩](https://opentutorials.org/course/228/4894)
* [초보몽키의 개발블로그](https://wayhome25.github.io/cs/2018/03/11/ssl-https/)
* [miguelgrinberg.com](https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https)

## 1. 용어

* HTTP(Hypertext Transfer Protocol)
  * HTML 을 전송하기 위한 전송 규약
  * http://google.com/: google.com 서버 index 페이지를 http 프로토콜로 요청한다
  
* HTTPS(Hypertext Transfer Protocol over Secure Socket Layer)
  * HTML을 전송하기 위한 전송 규약, HTTP에서 보안 기능 추가
    * 발신/수신 데이터 보안
      * 제3자가 발신/수신 데이터 감청, 변조할 수 없음
      * id, pass 등 정보를 암호화해서 전송
    * 도메인 신뢰성 입증
      *  도메인 신뢰성 검증 과정 포함
  
* SSL , TLS
  
  * 같다. 정식명식은 TLS
  
* CA(Certificate authority, Root Certificate)

  * 인증서에 대해 보증을 서주는 기업(Symantec, Comodo, Godaddy, GlobalSign)

* 사설인증기관

  * 공인되지 않은 CA, 본인이 직접 인증서를 만들 경우 본인은 사설인증기관이 된다
  * 사설인증기관의 인증서를 사용할 경우 아래와 같은 경고창 출력

  ![img](https://s3.ap-northeast-2.amazonaws.com/opentutorials-user-file/module/228/1536.gif)

  * 공인CA 인증서를 사용할 경우 아래와 같은 창 출력

  ![img](https://s3.ap-northeast-2.amazonaws.com/opentutorials-user-file/module/228/1537.gif)

## 2. HTTP vs HTTPS

![views](https://i.imgur.com/4GHgl0T.png)

HTTP 는 SSL 레이어 위에서 동작, SSL을 사용하는 HTTP 를 HTTPS 라고 한다.

## 3. SSL 인증서

디지털 인증서는 클라이언트 - 서버 간 통신을 제 3자가 보증해주는 전자 문서다

SSL 인증서는 3가지 기능이 있음

​	1) 발/수신 데이터 노출 방지 

​	2) 서버 신뢰도 보증

​	3) 발/수신 데이터 변조 방지

### 1) 발/수신 데이터 노출 방지

데이터 전송시 암호화함. sender 가 `암호화`한 데이터를 보내면 receiver가 `key `를 통해 `복호화`함.

#### 대칭키 암호화 방식

* sender 와 reciver 가 동일한 `key` 로 암호화/복호화 하는 암호화 방식

* key만 있으면 누구든 복호화할 수 있다.

* ```bash
  echo 'this is the plain text' > plaintext.txt  # plain text 생성
  
  cat plaintext.txt
  
  # plaintext.txt를 des3 방식으로 암호화해서 cipertext.bin에 저장
  openssl enc -e -des3 -salt -in plaintext.txt -out ciphertext.bin;  # key 설정
  openssl enc -d -des3 -in ciphertext.bin -out plaintext.txt  # 복호화
  ```
  

##### 공개키 암호화 방식

* public key, private key로 구성

* public key로 암호화한 파일을 private key로 복호화 할 수 있음(반대도 가능)

* ```bash
  openssl genrsa -out private.pem 1024  # 1024bit 길이의 private key 를 rsa 방식으로 생성
  openssl rsa -in private.pem -out public.pem -outform PEM -pubout  # private key로 public key 생성
  
  ehco 'a secret message' > file.txt  # create file
  # public key로 file.txt 암호화
  openssl rsautl -encrypt -inkey public.pem -pubin -in file.txt -out file.ssl 
  # private key로 file.ssl 복호화
  openssl rsautl -decrypt -inkey private.pem -in file.ssl -out file_dec.txt
  ```

### 2) 서버 신뢰도 입증

#### 인증서 역할

* 클라이언트가 접속한 서버 신뢰도 보증
* public key를 client에게 전송

#### 인증서 내용

CA는 자신의 private key를 이용해 인증서를 암호화, 브라우저는 공인 CA리스트와 각 CA의 공개키 리스트를 알고 있음

* 서비스 정보
  * 인증서를 발급한 CA
  * 도메인
* public key
  * public key 암호화 방법





#### 서버 신뢰도 입증 과정

1. 클라이언트가 서버에 접속 요청
2. 서버가 클라이언트에게 인증서 제공
3. 클라이언트 브라우저는 인증서가 자신의 CA리스트에 포함됐는지 확인
4. 인증서에 해당하는 CA의 public key로 인증서를 복호화
   * 1-4과정을 통과하면 서버를 신뢰할 수 있는 이유
     * 4번 통과 => 해당 인증서는 CA의 private key로 암호화됐음
     * CA의 private key는 CA만 가지고 있기 때문에 인증서는 CA가 발급한 것이 맞음
     * CA가 발급한 인증서를 가지고 있는 도메인은 CA의 검토를 통과한 도메인
     * 따라서 도메인을 신뢰할 수 있음

### 3) 발/수신 데이터 변조 방지

발/수신 데이터는 대칭키 방식으로 암호화

## 4. SSL 통신과정

![views](https://i.imgur.com/YIfy1wK.png)

발/수신 데이터는 대칭키로 암호화, 암호화할 때 사용한 대칭키는 공개키로 암호화

공개키방식은 컴퓨터 자원을 많이 소모, 대칭키 방식은 보안이 취약, 공개키와 대칭키를 함께 활용

통신과정은 아래 세단계로 구성

1) 악수
2) 전송
3) 세션종료 

### 1) 악수(Handshake)

실제 데이터를 전송하기 전 서버-클라이언트가 서로의 정보를 파악하는 과정

SSL통신에서는 악수 과정에서 SSL인증서와 공개키를 주고 받는다

1. Client Hello
   * 클라이언트가 서버에 접속할 때 아래와 같은 데이터를 전송 
     * 클라이언트가 생성한 랜덤 데이터
     * 클라이언트가 사용할 수 있는 암호화 방식
     * 세션아이디: 이미 악수를 한 경우 시간을 절약하기 위해 기존 세션 재활용
2. Server Hello
   * 서버는 Client Hello에 대한 응답으로 아래와 같은 데이터를 전송
     * 서버가 생성한 랜덤 데이터
     * 서버 사용할 수 있는 암호화 방식
       * 클라이언트의 암호화 방식 중 서버가 사용할 수 있는 암호화 방식을 선택해 전달
     * 인증서
3. Client 인증서 검토
   * 서버로부터 받은 인증서가 공인 CA에 의해 발급받은 것인지 확인
   * CA 리스트에 인증서가 없다면 사용자에게 경고 메시지 출력
   * CA 리스트에 인증서가 있다면 CA공개키로 인증서 복호화
   * 클라이언트의 랜덤데이터와 서버의 랜덤데이터를 조합해 키 생성(pre master secret)
   * 인증서의 공개키로 pre master secret 암호화 후 서버로 전송
   * pre master secret => master secret
     * session key 생성(데이터 발/수신시 암호화에 사용할 대칭키)
4. Server
   * pre master secret 를 인증서의 비밀키로 복호화
   * pre master secret => master secret
     * session key 생성(데이터 발/수신 시 암호화에 사용할 대칭키)
5. 악수 종료

### 2) 전송

* 클라이언트와 서버가 데이터를 주고 받는 단계
* 데이터를 session key로 암호화 후 전송
* 속도는 느리지만 안전한 공개키 방식으로 대칭키를 암호화하고, 실제 데이터는 대칭키로 암호화

### 3) 세션종료

* session key 폐기

## 5 인증서 발급

## 6 인증서 구입

```bash
ssl.key  # 비밀키
ssl.crt  # 인증서
ca.pem  # Root CA 인증서
sub.class1.server.ca.pem  # 중계 인증서
```

## 7 웹서버에 인증서 설치

### 인증서 만들기

* rsa: 4096: 4096 bit 길이의 rsa 비밀키
* days: 유효 기간

```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout private_key.pem -days 365
```

```bash
Generating a 4096 bit RSA private key
......................++
.............++
writing new private key to 'key.pem'
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]: KR
State or Province Name (full name) [Some-State]: Seoul
Locality Name (eg, city) []: Gangnam
Organization Name (eg, company) [Internet Widgits Pty Ltd]: MINDS AND COMPANY
Organizational Unit Name (eg, section) []: 
Common Name (e.g. server FQDN or YOUR name) []: BAEK
Email Address []: shbaek@mindslab.ai
```

* 생성파일
  * private_key.pem: 비밀키
  * cert.pem: 인증서

### FLASK

```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return("You called the service with https")

cert_dir = 'cert/'

if __name__ == '__main__':
    app.run(ssl_context=(cert_dir+'cert.pem', cert_dir+'private_key.pem'))
    
# flask run --cert=cert/cert.pem --key=key.pem 
```

### Client

* `verify = False` 를 해야 `bad handshake`오류 무시

```python
import requests

url = 'https://127.0.0.1:5000/'
res = requests.get(url, verify=False)

print(res.text)

### You called the service with https
```























