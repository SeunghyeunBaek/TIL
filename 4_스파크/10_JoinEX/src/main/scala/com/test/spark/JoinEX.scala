package com.test.spark

import org.apache.spark.{SparkConf, SparkContext}

object JoinEX{
	def main(args: Array[String]){
		val conf = new SparkConf
		val sc = new SparkContext(conf)
		
		try {
			// products.csv, sales-october.csv 파일을 읽어온다
			val sourceRDD1 = sc.textFile("data/products.csv")
			val sourceRDD2 = sc.textFile("data/sales-october.csv")

			//------------------------ RDD ------------------
			// 두 RDD의 기준컬럼이 가장 먼저나오도록 RDD를 설정한다.
			val productsRDD = sourceRDD1.map{record=>
				val sd = record.split(",")
				// 상품 ID, (상품 이름, 가격)
				(sd(0),(sd(1),sd(2).toInt))
			}

			val salesRDD = sourceRDD2.map{record=>
				val sd = record.split(",")
				// 상품ID, (판매ID, 날짜, 개수)
				(sd(2),(sd(0),sd(1),sd(3).toInt))
			}

			//join
			val joinRDD = productsRDD.join(salesRDD)
			joinRDD.foreach{

				case(pid,((name,price),(sid,sdate,amount)))=>
					println(s"고객 ID : ${sid}")
					println(s"상품명 : ${name}")
					println(s"가격 : ${price}원")
					println(s"개수 : ${amount}개")
					println(s"총액 : ${price*amount}원")
					println(s"날짜 : ${sdate}")
					println("=========================================")
			}

			//------------------------ DataFrame 생성 -------------------------
			//sql이나 함수사용을 위해 DataFrame을 생성한다.
			import org.apache.spark.sql.hive.HiveContext
			val sqlContext = new HiveContext(sc)
			import sqlContext.implicits._

			//RDD를 생성한다.
			val productsRDD = sourceRDD1.map{record=>
				val sd = record.split(",")
				(sd(0),sd(1),sd(2).toInt)
			}
			val salesRDD = sourceRDD2.map{record=>
				val sd = record.split(",")
				(sd(0),sd(1),sd(2),sd(3).toInt)
			}

			//DataFrame 생성
			val productsDF = productsRDD.toDF("item_id","item_name","price")
			val salesDF = salesRDD.toDF("s_id","s_date","item_id","amount")

			//------------------------ sql --------------------------------
			//테이블로 등록
			productsDF.registerTempTable("products_table")
			salesDF.registerTempTable("sales_table")

			val joinDF = sqlContext.sql(
				"select t1.item_id, t1.item_name, t2.s_id,t2.s_date, t1.price, t2.amount "+
				"from products_table as t1, sales_table as t2 "+
				"where t1.item_id = t2.item_id"
			)

			joinDF.foreach{row=>
				//val totPrice = row(4).toString.toInt*row(5).toString.toInt
				println(s"구매 ID : ${row(2)}")
				println(s"구매 날짜 : ${row(3)}")
				println(s"상품명 : ${row(1)}")
				//println(s"총액 : ${totPrice}")
			}
			//------------------------함수 ---------------------------------

			val tmpDF = productsDF.join(salesDF, productsDF("item_id")===salesDF("item_id"),"inner")

			val joinDF2 = tmpDF.select("item_name","s_date","amount","price")

			joinDF2.foreach{row=>
				val totPrice = row(2).toString.toInt*row(3).toString.toInt
				println(s"상품명 : ${row(0)}")
				println(s"날짜 : ${row(1)}")
				println(s"총계 : ${totPrice}")
				println("==============================================")

			}



			// DataFrame - 함수

		} finally {
			sc.stop()
		}
	}
}