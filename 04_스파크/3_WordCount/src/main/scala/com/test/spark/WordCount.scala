package com.test.spark

import org.apache.spark.{SparkConf,SparkContext};

object WordCount{
	def main(args: Array[String]){
		val conf = new SparkConf
		val sc = new SparkContext(conf)
		
		// simple-words.txt 파일에 들어있는 단어들 중
		// 영어와 숫자로만 구성된 단어들의 빈도를 가져온다.
		try{
			//1. simple-words.txt로부터 테이터를 읽어와 RDD를 만든다.
			//spark-shell
			//val textRDD = sc.textFile("data/simple-words.txt")
			//패키징 후 실행
			val textRDD = sc.textFile("../../data/simple-words.txt")
			textRDD.collect.foreach(println)
			//2. 읽어온 데이터들 중 영어단어만 추출한다.
			val wordRDD = textRDD.filter(word=>
				word.matches("""\p{Alnum}+""")
			)
			// wordRDD.collect.foreach(println)
			//3  각 단어의 빈도수를 계산한다.
			//(단어) 형태의 레코드를 (단어,1)로 바꾼다.
			val wordAndOneRDD = wordRDD.map(record=>
				(record,1)
			)
			// wordAndOneRDD.collect.foreach(println)
			// (record,1)에서 record가 같은 것 끼리 모아 Value의
			// 총합을 계산한다.
			val wordCountRDD = wordAndOneRDD.reduceByKey(
				(result,elem)=>
				result+elem
			)
			// wordCountRDD.collect.foreach(println)
			//3. 출력
			val resultRDD = wordCountRDD.map{
				case(key,value)=>
					s"${key}는 ${value}개있다"
			}
			resultRDD.collect.foreach(println)
		} finally{
			sc.stop()
		}
		
	}
}
