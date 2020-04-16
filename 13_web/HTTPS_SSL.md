# HTTPS 와 SSL 인증서

*200416*

*references*

* *[생활코딩](https://opentutorials.org/course/228/4894)*

## 용어

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

## HTTP vs HTTPS

![SSL/TLS Protocol Layers - SSL/TLS Overview](https://sites.google.com/site/tlsssloverview/_/rsrc/1337752119392/ssl-tls-protocol-layers/ssllayers.gif)

HTTP 는 SSL 레이어 위에서 동작, SSL을 사용하는 HTTP 를 HTTPS 라고 한다.

## SSL 인증서

디지털 인증서는 클라이언트 - 서버 간 통신을 제 3자가 보증해주는 전자 문서다

### 기능

#### 발/수신 데이터 노출 방지

데이터 전송시 암호화함. sender 가 `암호화`한 데이터를 보내면 receiver가 `key `를 통해 `복호화`함.

* 대칭키 방식

  * sender 와 reciver 가 동일한 `key` 로 암호화/복호화 하는 암호화 방식

  * key만 있으면 누구든 복호화할 수 있다.

  * ```bash
    echo 'this is the plain text' > plaintext.txt  # plain text 생성
    
    cat plaintext.txt
    
    # plaintext.txt를 des3 방식으로 암호화해서 cipertext.bin에 저장
    openssl enc -e -des3 -salt -in plaintext.txt -out ciphertext.bin;  # key 설정
    
    cat cipertext.bin  # 암호 출력
    
    openssl enc -d -des3 -in ciphertext.bin -out plaintext.txt  # 복호화
    ```

  * 

#### 서버 신뢰도 입증

#### 발/수신 데이터 변조 방지

