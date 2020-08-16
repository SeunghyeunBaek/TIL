package com.test.spark

import org.apache.spark.{SparkConf, SparkContext}

object TitanicML{
	def main(args: Array[String]){
		val conf = new SparkConf
		val sc = new SparkContext(conf)
		
		try {
			// csv를 읽어온다.
			val trainRDD = sc.textFile("data/titanic_train.csv")
			trainRDD.take(5).foreach(println)

			//---------------------RDD로 불러오기--------------------------

			// CSV를 RDD로 처리하려면 column name 행을 빼야한다.
			// 최 상단에 있는 문자열 데이터를 가져온다

			/*
			val header_str = trainRDD.first()
			print(header_str)

			// 속성 이름 문자열이 아닌 행들만 가져온다.
			val trainRDD2 = trainRDD.filter{record=> 
				record != header_str
			}

			// 쉼표를 기준으로 구분하고 RDD를 만든다
			val trainRDD3 = trainRDD2.map{record=>
				val sd = record.split(",")
				//sd의 개수, 13 이름 안에 있는 쉼표도 잘린다.
				sd.count
			}
			*/

			// 결론 : 사람 이름에 쉼표가 포함돼 쉼표를 기준으로 잘라내면
			// 데이터 구조가 기존과 달라진다.
			// 데이터가 String으로 변환돼 전처리를 한번 더 해야한다.

			//---------------------DataFrame으로 불러오기------------------

			import org.apache.spark.sql.hive.HiveContext
			val sqlContext = new HiveContext(sc)
			import sqlContext.implicits._

			// csv파일을 읽는 객체
			val dfReader = sqlContext.read
			// 데이터 타입 설정
			dfReader.format("csv")
			// 특성 이름을 파일로부터 읽어와 적용한다
			// option 설정을 안할경우 column name 이 1,2,3 으로 바뀐다.
			dfReader.option("header","true")
			// colunm의 자료형을 자동으로 설정한다. 설정을 안하면 String으로 
			// 변환한다.
			dfReader.option("inferSchema","true")

			//데이터를 읽어와 데이터프레임으로 만든다
			val trainDF1 = dfReader.load("data/titanic_train.csv")
			val testDF1 = dfReader.load("data/titanic_test.csv")

			//결측치를 확인한다.
			val trainTot = trainDF1.count
			val testTot = testDF1.count


			//결측치 확인 함수
			import org.apache.spark.sql.DataFrame

			def checkNull(df:DataFrame): Unit = {
				df.columns.foreach{col=>
					val count = df.select("*").where(s"${col} is null").count
					println(s"${col} : ${count} null values, "+
					s"ratio : ${(count.toFloat/trainTot.toFloat)*100} %")
				}
			}

			// 결측치확인
			checkNull(trainDF1)
			checkNull(testDF1)

			// 나이의 평균을 구한다.
			// meanAge = 29.699
			val meanAge = trainDF1.select(avg("Age")).first().getDouble(0)
			val meanAge_test = testDF1.select(avg("Age")).first().getDouble(0)
			val meanFare_test = testDF1.select(avg("Fare")).first().getDouble(0)


			// DataFrame을 RDD로 변환한다.
			val trainRDD1 = trainDF1.rdd

			//------------------serializable error --------------------------

			/*
			map 함수 밖에서 선언한 변수를(meanAge) 반환값으로 지정하면
			SparkException: Task not serializable 에러발생
			RDD 사용을 지양한다.
			RDD 안에서 선언된 변수는 자동 직렬화된다. 
			RDD 밖에서 선언된 변수는 직렬화되지 않는다. 해결하기 어렵다.
			ex)	(pid,survived,pclass,name,meanAge)
			데이터프레임을 사용할 때는 신경쓸 필요없음
			*/

			/*
			val trainRDD2 = trainRDD1.map{record=>

				val pid = record(0).toString.toInt
				val survived = record(1).toString.toInt
				val pclass = record(2).toString.toInt
				val name = record(3).toString
				//(pid,survived,pclass,name,meanAge) ==> 오류 : meanAge는 직렬화돼있지않다.
			} 
			*/

			//------------------serializable error --------------------------

			// 결측치를 대체할값을 담은 객체를 생성한다.
			// Age 평균, Embarked는 'S'로 대체한다.
			// Any : 모든 형식의 값

			val nullMap = Map[String,Any]("Age" ->meanAge,"Embarked"->"S")
			val nullMap_test = Map[String,Any]("Age" ->meanAge_test,"Embarked"->"S","Fare"->meanFare_test)
			// nulMap을 DataFrame에 적용한다.
			val trainDF2 = trainDF1.na.fill(nullMap)
			val testDF2 = testDF1.na.fill(nullMap_test)

			// 결측치확인
			checkNull(trainDF2)
			checkNull(testDF2)

			/*---------------------String to Int---------------*/

			// StringIndexer : 문자열을 숫자로 변환한다.
			// Python LableEncoder와 같은기능
			import org.apache.spark.ml.feature.StringIndexer

			val indexer1 = new StringIndexer
			// 새로운 col을 추가
			indexer1.setInputCol("Sex")
			indexer1.setOutputCol("Sex_indexed")
			// 새로운 DataFrame을 만든다.

			val indexer2 = new StringIndexer
			indexer2.setInputCol("Embarked")
			indexer2.setOutputCol("Embarked_indexed")

			val trainDF3 = indexer1.fit(trainDF2).transform(trainDF2)
			val trainDF4 = indexer2.fit(trainDF3).transform(trainDF3)

			/*------------------Columns to Vector---------------*/

			// 입력데이터를 벡터화한다.
			import org.apache.spark.ml.feature.VectorAssembler

			// Columns to Vectors
			val assembler = new VectorAssembler
			assembler.setInputCols(Array("Age","SibSp","Parch","Fare","Pclass",
				"Sex_indexed","Embarked_indexed"))
			assembler.setOutputCol("titanic_features")

			val trainDF3 = indexer1.fit(trainDF2).transform(trainDF2)
			val trainDF4 = indexer2.fit(trainDF3).transform(trainDF3)
			val trainDF5 = assembler.transform(trainDF4)

			trainDF5.show

			/*
			------------------------분류모델-----------------------------
			setFeatures와 setLabelCol 을 설정하지 않으면
			입력 : Features, 결과 : Label 인 col을 찾아서 입력한다.
			*/

			import org.apache.spark.ml.classification.LogisticRegression

			val lr = new LogisticRegression
			lr.setMaxIter(10)
			lr.setFeaturesCol("titanic_features")
			lr.setLabelCol("Survived")

			/*
			----------------Pipline을 사용하지 않은 경우---------------
			val trainDF3 = indexer1.fit(trainDF2).transform(trainDF2)
			val trainDF4 = indexer2.fit(trainDF3).transform(trainDF3)
			val trainDF5 = assembler.transform(trainDF4)

			val model = lr.fit(trainDF5)

			// Insample test
			val summary = model.summary
			println(s"${summary.accuracy}")

			// 예측결과를 가져온다.

			val testDF3 = indexer1.fit(testDF2).transform(testDF2)
			val testDF4 = indexer2.fit(testDF3).transform(testDF3)
			val testDF5 = assembler.transform(testDF4)
			val predDF = model.transform(testDF5)

			val row_list = predDF.select("PassengerID","prediction")
			*/

			/*---------------------Pipeline-------------------------*/
			import org.apache.spark.ml.Pipeline

			// 모델을 Array객체에 담는다. Array에 들어간 순서대로 동작한다.
			val lines = Array(indexer1,indexer2,assembler,lr)
			val pipe = new Pipeline
			pipe.setStages(lines)

			//학습한다
			// trainDF2, testDF2 사용
			val pipe_model = pipe.fit(trainDF2)

			// 정확도 측정
			import org.apache.spark.mllib.evaluation.MulticlassMetrics

			// insample test
			val train_result = pipe_model.transform(trainDF2)
			val row_list2 = train_result.select("Survived","prediction")
			
			// y
			val survived_df = row_list2.rdd.map{record=>
				record(0).toString.toDouble
			}

			// y_pred
			val pred_df = row_list2.rdd.map{record =>
				record(1).toString.toDouble
			}

			// 정확도를 계산한다.
			val multi = new MulticlassMetrics(pred_df.zip(survived_df))
			val acc = multi.accuracy
			print(s"accuracy : ${acc}")

			// test data로 예측결과 계산
			val y_pred = pipe_model.transform(testDF2)
			val test_row = y_pred.select("PassengerID","prediction")
			test_row.show


			}

		} finally {
			sc.stop()
		}
	}
}








