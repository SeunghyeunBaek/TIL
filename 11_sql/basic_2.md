references: [mode](https://mode.com/resources/sql-tutorial/sql-between/)

## Convention

* spaces: SQL treats one space, multiple spaces or a line break as being the same thing`

```sql
SELECT *
  FROM two spaces
 LIMIT one space
 WHERE one sapce
 ORDER BY one space
```



* capitalized: `SELECT`, `FROM`, `WHERE` 

## Limit

```sql
SELECT *
  FROM tutorial.us_housing_units
 LIMIT 100
```

## Logical Operators

- [`LIKE`](https://mode.com/resources/sql-tutorial/sql-like/) 
  - allows you to match similar values, instead of exact values.
  - `Group`은 내장함수 이름이기 떄문에 "group"으로 표기했다.
  -  `%`는 문자열을 나타낸다.
  - `_`는 한글자를 나타낸다.
  - `ILIKE`은 대소문자를 구분하지 않는다.

```sql
--row for wich 'group' starts with 'Snoop' and is followed by any number and selection of charcaters
SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE "group" LIKE "Snoop%"
 
--ignore case
SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE "group" ILIKE 'snoop%'
```

* [`IN`](https://mode.com/resources/sql-tutorial/sql-in-operator/) allows you to specify a list of values you’d like to include.
  * 리스트에 대한 값의 포함 여부를 나타냄

```sql
SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year_rank IN (1, 2, 3)
 
 --문자열은 '' 홑따옴표 사용
 SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE artist IN ('Taylor Swift', 'Usher', 'Ludacris')
```



- [`BETWEEN`](https://mode.com/resources/sql-tutorial/sql-between/) 

  - allows you to select only rows within a certain range.

  ```sql
  SELECT *
    FROM tutorial.billboard_top_100_year_end
   WHERE year_rank BETWEEN 5 AND 10
   
   SELECT *
    FROM tutorial.billboard_top_100_year_end
   WHERE year_rank >= 5 AND year_rank <= 10
  ```

- [`IS NULL`](https://mode.com/resources/sql-tutorial/sql-is-null/) allows you to select rows that contain no data in a given column.

  - `WHERE artist == NULL` 은 사용할 수 없다. NULL로 산술연산 불가능.

```sql
SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE artist IS NULL
```

- [`AND`](https://mode.com/resources/sql-tutorial/sql-and-operator/) allows you to select only rows that satisfy two conditions.
- [`OR`](https://mode.com/resources/sql-tutorial/sql-or-operator/) allows you to select rows that satisfy either of two conditions.
- [`NOT`](https://mode.com/resources/sql-tutorial/sql-not-operator/) allows you to select rows that do not match a certain condition.

## ORDER BY

```sql
--The numbers will correspond to the order in which you list columns in the SELECT clause. 
SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year_rank <= 3
 ORDER BY 2, 1 DESC
```

