package com.test.spark

import org.apache.spark.{SparkConf, SparkContext}

object IrisML{
	def main(args: Array[String]){
		val conf = new SparkConf
		val sc = new SparkContext(conf)
		// Iris 데이터를 분류하자~~~
		try {
			// RDD로 읽어오기
			// csv파일에 특성 이름이 있을 경우
			// RDD로 만들면 힘들어 짐요~~~
			// val tempRDD = sc.textFile("data/iris.csv")
			// tempRDD.foreach(println)
			
			// DataFrame으로 읽어오기
			// csv 파일에 특성 이름이 있을 경우
			// DataFrame으로 읽어오면 편합니다~~
			
			import org.apache.spark.sql.hive.HiveContext
			val sqlContext = new HiveContext(sc)
			import sqlContext.implicits._
			
			// csv 파일을 읽어오는 객체추출
			val dfReader = sqlContext.read
			// 읽어올 파일의 양식을 설정한다.
			dfReader.format("csv")
			// 파일의 첫번째 줄을 feature 이름으로 설정한다.
			dfReader.option("header", "true")
			// 각 컬럼의 데이터 타입을 자동으로 설정한다.
			dfReader.option("inferSchema", "true")
			
			// 파일로부터 데이터를 읽어와 DataFrame으로
			// 만든다.
			val tempDF = dfReader.load("data/iris.csv")
			tempDF.show
			
			// 데이터 전처리를 위해 RDD로 변환한다.
			val tempRDD = tempDF.rdd
			
			// 데이터 전처리
			val irisRDD = tempRDD.map{ record =>
				// 꽃 이름 데이터를 변경한다.
				var iris_type = 0
				
				val sepal_width = record(0).toString.toDouble
				val sepal_length = record(1).toString.toDouble
				val petal_width = record(2).toString.toDouble
				val petal_length = record(3).toString.toDouble
				val iris_temp_type = record(4).toString
				
				iris_temp_type match {
					case "Iris-setosa" =>
						iris_type = 0
					case "Iris-versicolor" =>
						iris_type = 1
					case "Iris-virginica" =>
						iris_type = 2
				}
				
				(sepal_width, sepal_length, petal_width, petal_length, iris_type)
			
			}
			
			irisRDD.take(5).foreach(println)
			
			// DataFrame으로 변경한다.
			val irisDF = irisRDD.toDF("sepal-width", "sepal-length", "petal-width", "petal-length", "iris-type")
			irisDF.show
			
			import org.apache.spark.ml.feature.VectorAssembler
			import org.apache.spark.ml.classification.LogisticRegression
			
			// 각 데이터를 벡터화하여 추가된 DF를 구한다.
			val assembler = new VectorAssembler()
			assembler.setInputCols(Array("sepal-width", "sepal-length", "petal-width", "petal-length"))
			assembler.setOutputCol("iris-features")
			
			val irisDataDF = assembler.transform(irisDF)
			irisDataDF.show
			
			// 전체 데이터를 랜덤하게 섞어서 7:3으로 나눈다.
			val (trainData, testData) = {
				val split = irisDataDF.randomSplit(Array(0.7, 0.3))
				(split(0), split(1))
			}
				
			// 영속화
			trainData.cache
			testData.cache
		
			// 학습한다.
			val lr = new LogisticRegression()
			lr.setMaxIter(10)
			lr.setFeaturesCol("iris-features")
			lr.setLabelCol("iris-type")
			
			val model = lr.fit(trainData)
			
			// 정확도 확인
			val summary = model.summary
			print(s"정확도 : ${summary.accuracy}")
			
			// 검증용 데이터를 활용해 예측 결과를
			// 생성한다.
			val result = model.transform(testData)
			
			val row_list = result.select("iris-type", "prediction")
			row_list.foreach{ row =>
				print(s"${row(0)} vs ${row(1)}")
			}
			
		} finally {

			sc.stop()
		}
	}
}








