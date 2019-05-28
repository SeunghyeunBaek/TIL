package com.test.spark

import org.apache.spark.{SparkConf, SparkContext}

object SparkSQL_join{
	def main(args: Array[String]){
		val conf = new SparkConf
		val sc = new SparkContext(conf)
		
		try {
			// RDD
			// RDD 생성
			// (key,(val1,val2))

			// spark sql 사용을 위한 HiveContext 객체를 생성
			import org.apache.spark.sql.hive.HiveContext
			val sqlContext = new HiveContext(sc)
			// sqlContext 객체를 만들고 import 해야함
			import sqlContext.implicits._

			val sourceRDD1 = sc.textFile("data/dessert-menu.csv")
			val sourceRDD2 = sc.textFile("data/dessert-order.csv")

			val menuRDD = sourceRDD1.map{record =>
				val splittedData = record.split(",")
				(splittedData(0),(splittedData(1),splittedData(2).toInt))
			}

			val orderRDD = sourceRDD2.map{record=>
				val splittedData = record.split(",")
				(splittedData(1),(splittedData(0),splittedData(2).toInt))
			}

			val joinRDD = menuRDD.join(orderRDD)

			joinRDD.foreach{case(id,((name,price),(userid,amount)))=>
				println(s"${userid}는 ${name}(${price}원)을(를) ${amount}개 구매했고 "+
				s"총 구매액은 ${amount*price}원이다")
			}

			// Spark SQL
			val menuRDD = sourceRDD1.map{record=>
				val splittedData = record.split(",")
				(splittedData(0),splittedData(1),splittedData(2).toInt)
			}

			val orderRDD = sourceRDD2.map{record=>
				val splittedData = record.split(",")
				(splittedData(0),splittedData(1),splittedData(2).toInt)

			}

			//데이터 프레임으로 변환
			//Class를 만들지 않고 튜플을 dataFrame으로 만들었다.
			val menuDF = menuRDD.toDF("item_id","name","price")
			val orderDF = orderRDD.toDF("user_id","item_id","amount")

			//Table을 만든다.
			menuDF.registerTempTable("menu_table")
			orderDF.registerTempTable("order_table")

			val joinDF = sqlContext.sql(
				"select t1.name,t1.price,t2.user_id,t2.amount "+
				"from menu_table as t1, order_table as t2 "+
				"where t1.item_id = t2.item_id"
			)

			joinDF.foreach{row=>
				var totPrice = row{1}.toString.toInt*row{2}.toString.toInt
				print(s"${row(3)}은 ${row(0)}을 ${row(3)}개 구매했고, ${totPrice}원을 냈다")
			}

			var joinDF2 = menuDF.join(orderDF,
				menuDF("item_id")==orderDF("item_id"),"inner").select("name","price","user_id","amount")


		} finally {
			sc.stop()
		}
	}
}








