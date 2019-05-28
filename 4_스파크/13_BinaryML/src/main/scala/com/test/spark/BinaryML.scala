package com.test.spark

import org.apache.spark.{SparkConf, SparkContext}

object BinaryML{
	def main(args: Array[String]){
		val conf = new SparkConf
		val sc = new SparkContext(conf)
		// 2진수 (0, 1)의 and 연산 능력을 갖춘
		// 모델을 만든다.
		// 0 0 => 0
		// 0 1 => 0
		// 1 0 => 0
		// 1 1 => 1
		
		try {
			// 데이터를 가지고 있는 RDD를 만들어준다.
			val binaryRDD = sc.parallelize(
				Seq(
					(0, 0, 0),
					(0, 1, 0),
					(1, 0, 0),
					(1, 1, 1)
				)
			)
			
			binaryRDD.foreach(println)
			
			// 데이터 프레임을 만든다.
			val binaryDF = binaryRDD.toDF("number1", "number2", "result")
			binaryDF.show
			
			// 머신러닝을 위해 데이터를 벡터화한다.
			import org.apache.spark.ml.feature.VectorAssembler
			val assembler = new VectorAssembler()
			// 입력데이터 컬럼을 지정한다.
			assembler.setInputCols(Array("number1", "number2"))
			// 벡터화된 데이터를 담을 컬럼 이름을 지정한다.
			assembler.setOutputCol("binary-features")
			
			val binaryDF2 = assembler.transform(binaryDF)
			binaryDF2.show
			
			// 학습
			import org.apache.spark.ml.classification.LogisticRegression
			
			// 학습 모델을 만든다.
			val lr = new LogisticRegression()
			lr.setMaxIter(10)
			// 입력 데이터 컬럼이름 지정(생략시 features)
			lr.setFeaturesCol("binary-features")
			// 결과 데이터 컬럼이름 지정(생략시 label)
			lr.setLabelCol("result")
			
			// 학습한다.
			val lrModel = lr.fit(binaryDF2)
			
			// 정확도를 확인한다.
			val summary = lrModel.summary
			println(s"정확도 : ${summary.accuracy}")
			
			// 예측결과를 가져온다.		
			val result = lrModel.transform(binaryDF2)
			result.show
			
			val row_list = result.select("result", "prediction")
			
			row_list.foreach{ row =>
				println(s"${row(0)} vs ${row(1)}")
			}
			
		} finally {
			sc.stop()
		}
	}
}
















