package com.test.spark

import org.apache.spark.{SparkConf,SparkContext};

object WordCount{
	def main(args: Array[String]){
		val conf = new SparkConf
		val sc = new SparkContext(conf)
		
		try{
			// 1. README.txt 파일을 읽어온다.
			// 한 줄이 레코드 하나를 의미한다.
			val textRDD = sc.textFile("../../data/README.md")
			//textRDD.co`llect.foreach({record=>
			//	println(s"--${record}")
			//})

			// 2. 문자열을 띄어쓰기, 콤마, 마침표를 기준으로 튜플로 만들고
			// 튜플을 다 풀어내 1 차원 RDD를 생성한다(Flatmap)

			val wordRDD = textRDD.flatMap(record=>
				// 띄어쓰기,콤마,마침표를 기준으로 
				// 문자열을 잘라 튜플로 만든다.
				record.split("[ ,.]")
			)

			// 2.1. 문자들 중에 알파벳 숫자만으로 구성된 단어를
			// 추출해 RDD러 만든다.

			val wordRDD2 = wordRDD.filter(word =>
				word.matches("""\p{Alnum}+""")
			)

			wordRDD2.collect.foreach(println)

			// 3. 단어 출현 빈도를 계산한다.
			// 단어-형태를 단어,1 로 변환한다.

			val wordAnd1RDD = wordRDD2.map(record=>
				(record,1)
			)

			val wordAndCountRDD = wordAnd1RDD.reduceByKey(
				(res,el)=>res+el
			)
			// 4. 출현 빈도수를 기준으로 내림차순 정렬한다.
			// 4.1. key와 value의 값을 바꾼다.

			val countAndWordRDD = wordAndCountRDD.map{
				case(key,value)=>
				(value,key)
			}

			// 4.2. 정렬한다.
			val sortedRDD = countAndWordRDD.sortByKey(false)
			sortedRDD.collect.foreach(println)

			// 4.3. 다시 바꾼다.
			val sortedRDD2 = sortedRDD.map{
				case(key,value)=>
				(value,key)
			}

			// 5. 상위 3개를 가져온다.
			val top3Array = sortedRDD2.take(3)

			// 6. 출력한다.
			println("=============================")
			top3Array.foreach(println)
			println("=============================")

			//7.파일로 저장한다.
			val top3RDD = sc.parallelize(top3Array)
			top3RDD.saveAsTextFile("result")
			print("저장완료")

		} finally{
			sc.stop()
		}
		
	}
}
