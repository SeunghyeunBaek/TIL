# 네이버 오픈API

- 오픈 API 사용시 확인해야 할 사항

  - 접속주소

  - 서버로 보낼 주소

  - 응답 결과 양식

  - API Key

    - client ID : IS3OiCTNiOI4ohZPsBRx

    - client Secret : Nxmj3sNiJZ

    - get url : https://openapi.naver.com/v1/search/blog.xml

      - internet explorer 는 query 를 utf-8 로 변환하지 않는다. chrome 으로 테스트해야함

    - Parmeters : [요청변수](<https://developers.naver.com/docs/search/blog/>) 에서 요청 변수 확인

    - API Key 는 요청 예제를 보고 입력한다.

      - ```javascript
        curl  "https://openapi.naver.com/v1/search/blog.xml?query=%EB%A6%AC%EB%B7%B0&display=10&start=1&sort=sim" \
            -H "X-Naver-Client-Id: {애플리케이션 등록 시 발급받은 client id 값}" \
            -H "X-Naver-Client-Secret: {애플리케이션 등록 시 발급받은 client secret 값}" -v
        ```

      - -H : 헤더를 수정해야함. 주소창에서 입력해서 테스트할 수 없음. -H 가 없다면, url 에서 &name = value 형식으로 입력하면 된다.

        - [Postman](<chrome-extension://coohjcphdfgbiolnekdpbcijmhambjff/index.html>) 사용

- 크롬 웹스토어 - Tabbed Postman - Rest Client

  - 헤더 정보 세팅을 할 수 있다.



# google API

google api Maps - [Places](<https://developers.google.com/places/web-service/search>)

