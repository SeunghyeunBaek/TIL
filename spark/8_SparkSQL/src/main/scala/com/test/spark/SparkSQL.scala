package com.test.spark

import org.apache.spark.{SparkConf, SparkContext}

object SparkSQL{
	def main(args: Array[String]){
		val conf = new SparkConf
		val sc = new SparkContext(conf)
		
		try {
			//DataFrame생성을 위해 데이터를 담는 클래스
			case class Dessert(menuId:String, name:String, price:Int, kcal:Int, menu_type:String)
			// 데이터를 담은 RDD를 만든다.
			val dessertRDD = sc.textFile("data/dessert-menu.csv")
			// DataFrame으로 만들기위한 RDD를 만든다.
			val dessertObjRDD = dessertRDD.map{record =>
				// 쉼표단위로 자른다.
				val splittedLine = record.split(",")
				// Dessert 객체로 만든다
				Dessert(splittedLine(0),splittedLine(1),splittedLine(2).toInt,splittedLine(3).toInt,splittedLine(4))
			}
			val dessertDF = dessertObjRDD.toDF

			// spark sql 사용을 위한 HiveContext 객체를 생성
			import org.apache.spark.sql.hive.HiveContext

			val sqlContext = new HiveContext(sc)
			// sqlContext 객체를 만들고 import 해야함
			import sqlContext.implicits._

			//1.sql 명령문을 직접이용하는 방법
			//	=> 사용할 DataFrame을 Table로 등록해야한다.
			//2.제공되는 함수를 이용하는 방법

			// DataFrame을 Table로 등록한다.
			dessertDF.registerTempTable("dessert_table")

			println("=========================================")
			println("DataFrame의 모든데이터 가져오기")

			val selectAllDF = sqlContext.sql(
				"select * from dessert_table"
			)
			selectAllDF.show

			val selectAllDF2 = dessertDF.select("*")
			selectAllDF.show

			println("=========================================")
			println("일부 Column의 데이터를 가져온다")

			// RDD map 함수를 통해 원하는 정보만 담긴 RDD를 만드는 것과 동일하다

			val namePriceDF = sqlContext.sql(
				"select name, price from dessert_table"
			)
			namePriceDF.show

			// val namePriceDF2 = sqlContext.select(dessertDF("name"),dessertDF("price"))
			val namePriceDF2 = dessertDF.select($"name",$"price")

			namePriceDF2.show

			println("==========================================")
			println("조건에 맞는 Column만 가져온다")
			//RDD의 filter 함수
			val over5200wonDF = sqlContext.sql(
				"select * from dessert_table where price >= 5200"
			)
			over5200wonDF.show

			val over5200wonDF2 = dessertDF.where("price >= 5200")
			over5200wonDF2.show()
			//val over5200wonDF2 = dessertDF.where($"price" >= 5200)

			//price가 5200 이상인 row의 name,price를 가져온다ㅏ.
			val over5200wonNameDF = sqlContext.sql(
				"select name, price from dessert_table where price >= 5200"
			)
			val over5200wonNameDF2 = dessertDF.select($"name",$"price")
											  .where($"price">=5200)

			println("===============================================")
			println("특정 컬럼을 기준으로 정렬한다")

			//오름 차순 정렬, asc 는 생략가능
			val sortedDF = sqlContext.sql(
				"select name, price from dessert_table "
				+"where price>=5200 "
				+"order by price asc"
			)

			//내림차순 정렬
			val sortedDF2 = sqlContext.sql(
				"select name, price from dessert_table "
				+"where price>=5200 "
				+"order by price desc"
			)

			val sortedDF3 = dessertDF.select($"name",$"price")
									 .where($"price">=5200)
									 .orderBy($"price".asc)

			val sortedDF4 = dessertDF.select($"name",$"price")
						 			 .where($"price">=5200)
						 			 .orderBy($"price".desc)

			println("===============================================")
			println("집계함수")
			// 숫자로 구성된 컬럼만 가능
			// null이 포함된 컬럼은 제외
			val sumDF1 = sqlContext.sql(
				"select sum(price) from dessert_table "
				+"where kcal>=300"
			)

			val sumDF2 = dessertDF.agg(sum($"price"))
								  .where($"kcal">=300)

			//평균 
			//가격이 4000원 이상인 상품들의 평균 칼로리를 구한다.
			val avgDF1 = sqlContext.sql(
				"select avg(kcal) from dessert_table "
				+"where price >= 4000"
			)

			val avgDF2 = dessertDF.where($"price">=4000).agg(avg($"kcal"))

			//최대 최소
			val minMaxDF1 = sqlContext.sql(
				"select max(price), min(price) from dessert_table"
			)
			val minMaxDF2 = dessertDF.agg(max($"price"),min($"price"))

			//상품가격이 3000원 이상인 상품의 수
			val countDF1 = sqlContext.sql(
				"select count(*) from dessert_table where price >=3000"
			)
			val countDF2 = dessertDF.where($"price">=3000)
									.agg(count("*"))

			println("===========================================")
			println("그룹화해서 집계하기")

			//가격 총합,평균,최대,최소,개수를 가져온다.
			val staticsDF1 = sqlContext.sql(
				"select sum(price), avg(price), max(price) "
				+", min(price), count(price) from dessert_table "
			)
			val staticsDF2 = dessertDF.select("price").agg(sum("price"),avg("price"),min("price"),max("price"))

			val groupDF1 = sqlContext.sql(
				"select menu_type, sum(price),avg(price),max(price) "+
				", min(price), count(price) "+
				"from dessert_table "+
				"group by menu_type"
			)

			val groupDF2 = dessertDF.groupBy("menu_type").agg(sum("price"), avg("price"), min("price"), max("price"),count("price"))

			
		} finally {
			sc.stop()
		}
	}
}








