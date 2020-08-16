package com.test.spark

import org.apache.spark.{SparkConf, SparkContext}

object SaveToFile{
	def main(args: Array[String]){
		val conf = new SparkConf
		val sc = new SparkContext(conf)
		
		try {
			//RDD 저장 및 읽어오기
			var testRDD = sc.parallelize(
				Seq(
					(1,"홍길동",30),
					(2,"고길동",40),
					(3,"김길동",50)
				)			
			)	
			//저장
			testRDD.saveAsTextFile("save/rdd")

			//읽어오기
			var testRDD2 = sc.textFile("save/rdd")
			testRDD2.foreach(println)

			//DataFrame 만든다
			val testDF = testRDD.toDF("user_id","name","age")
			
			//저장한다
			val dfWriter = testDF.write
			// parquet, orc, jason...

			dfWriter.format("parquet").save("save/df")

			//저장된 파일에서 데이터를 읽어와 DataFrame을 만든다
			import org.apache.spark.sql.hive.HiveContext
			val sqlContext = new HiveContext(sc)
			import sqlContext.implicits._

			val dfReader = sqlContext.read
			val testDF2 = dfReader.format("parquet").load("save/df")
			testDF2.show


		finally {
			sc.stop()
		}
	}
}