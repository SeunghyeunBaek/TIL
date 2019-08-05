## DB

* 데이터베이스 조회: 기존 데이터베이스 목록 출력

`show database`

* 데이터베이스 생성: 새로운 데이터베이스 생성

`create database`

* 데이터베이스 삭제: 데이터베이스 삭제

`drop database`

* 데이터베이스 선택: 사용할 데이터베이스를 선택한다.

`use database`

## Table

* 테이블 조회: 선택한 데이터베이스 테이블 출력

`show tables`

* 테이블 생성: 새로운 테이블 생성

  * 테이블 생성시 사용할 수 있는 자료형 목록

    * varchar(n): 길이가 최대 n인 가변 문자열
    * char(n): 길이가 n인 고정문자열
    * int: 정수
    * float: 실수
    * date: 날짜
    * time: 시간

  * 테이블 구조 정의

    `create table ex_table(id varchar(10), name char(3), age int)`

* 테이블 구조 조회

`desc table_name`

* 테이블 수정: 테이블 구조 변경

`alter table table_name modify_command`

* modify_command
  * 필드추가: `add + 자료형`
  * 필드 자료형 변경: `modiy + 자료형`
  * 필드삭제: `drop column + 필드명` 
  * 기본키 추가: `alter table + 테이블명 + add constraint + 제약조건명 + primary key (필드명)`
    * ex: `alter table ex_table add constraint NOT NULL primary key (id)`
* 검색

`select + 필드명 ... + from 테이블 명 + where 조건` 

## 책

* [칼퇴족 김대리는 알고 나만 모르는 SQL](https://book.naver.com/bookdb/book_detail.nhn?bid=8073252)

## 강좌

* Introduction to SQL for Data Science (Data Camp)
* The SQL Tutorial for Data Analysis (Mode Analytics)

* 