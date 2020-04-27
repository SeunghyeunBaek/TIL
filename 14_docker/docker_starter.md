# docker

*references*

*  [pyrasis](http://pyrasis.com/Docker/Docker-HOWTO)
* [pyrasis-가장빨리만나는도커](http://pyrasis.com/private/2014/11/30/publish-docker-for-the-really-impatient-book)

## 시작

```bash
docker pull [container_name]  # container_name 다운로드
docker images  # 이미지 확인
docker run [OPTIONS] IMAGE[:TAG|@DIGEST] [COMMAND] [ARGS]  # 실행


docker pull ubuntu:latest  # 우분투 이미지 다운로드
docker run -i -t --name ub_docker ubuntu /bin/bash  # 도커 실행
docker ps  # 실행중인 도커 확인
docker exec ub_docker echo "hello"  # 도커에서 실행
docker attach ub_docker  # 컨테이너에 접속
docker stop ub_docker  # 도커 정지
docker rm ub_docker  # 도커 삭제
```

## docker run OPTIONS

| 옵션  | 설명                                                   |
| :---- | :----------------------------------------------------- |
| -d    | detached mode 흔히 말하는 백그라운드 모드              |
| -p    | 호스트와 컨테이너의 포트를 연결 (포워딩)               |
| -v    | 호스트와 컨테이너의 디렉토리를 연결 (마운트)           |
| -e    | 컨테이너 내에서 사용할 환경변수 설정                   |
| –name | 컨테이너 이름 설정                                     |
| –rm   | 프로세스 종료시 컨테이너 자동 제거                     |
| -it   | -i와 -t를 동시에 사용한 것으로 터미널 입력을 위한 옵션 |
| –link | 컨테이너 연결 [컨테이너명:별칭]                        |



## Dockerfile

* .dockerignore: 컨텍스트에서 파일이나 디렉토리 제외

* FROM

  * base 이미지 지정
  * `FROM [image]`

* MAINTAINER

  * 이미지 생성자에 대한 정보
  * `MAINTAINER [name]  <[email]>`

* RUN

  * FROM에서 설정한 이미지위에서 스크립트, 명령어 실행

  * 실행 결과는 새이미지로 저장, 실행 내역은 history에 저장

  * ```bash
    RUN ["apt-get", "install", 'y-', 'ngnix'
    ```

* CMD, ENTRYPOINT

  * 컨테이너를 시작했을 때 실행할 명령어

  * ENTRYPOINT 사용시 CMD는 매개변수만 전달

  * ```bash
    ENTRYPOINT ["echo"]
    CMD ["hello"]
    ```

  * 

##