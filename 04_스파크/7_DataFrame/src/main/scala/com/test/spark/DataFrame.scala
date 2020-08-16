package com.test.spark

import org.apache.spark.{SparkConf, SparkContext}

object DataFrame{
	def main(args: Array[String]){
		val conf = new SparkConf
		val sc = new SparkContext(conf)
		
		try {
			//DataFrame생성을 위해 데이터를 담는 클래스
			case class Dessert(menuId:String, name:String, print:Int, kcal:Int)
			// 데이터를 담은 RDD를 만든다.
			val dessertRDD = sc.textFile("data/dessert-menu.csv")
			// DataFrame으로 만들기위한 RDD를 만든다.
			val dessertObjRDD = dessertRDD.map{record =>
				// 쉼표단위로 자른다.
				val splittedLine = record.split(",")
				// Dessert 객체로 만든다
				Dessert(splittedLine(0),splittedLine(1),splittedLine(2).toInt,splittedLine(3).toInt)
			}
			//RDD를 DataFrame으로 변환한다.
			val dessertDF = dessertObjRDD.toDF
			//DataFrame의 구조 출력
			//nullable : null값을 할당할 수 있는지 여부. 객체타입에만 null값을 넣을 수 있음
			dessertDF.printSchema
			//DataFrame의 값 출력
			dessertDF.show()
			//DataFrame을 RDD로 변경
			val tmpRDD = dessertDF.rdd
			tmpRDD.foreach(println)

		} finally {
			sc.stop()
		}
	}
}








