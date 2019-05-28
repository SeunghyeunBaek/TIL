package com.test.spark

import org.apache.spark.{SparkConf,SparkContext};
import org.joda.time.{DateTime,DateTimeConstants};
import org.joda.time.format.DateTimeFormat;

object SundayCount{
	def main(args: Array[String]){
		val conf = new SparkConf
		val sc = new SparkContext(conf)
		
		try{
			// 텍스트 파일에서 데이터를 읽어 RDD 객체로 만들어준다.
			val textRDD = sc.textFile("../../data/date.txt")
			// 분산저장된 RDD를 모아서 배열 객체로 만든다.
			//val textArray = textRDD.collect
			// 배열 객체에 담긴 요소들을 출력한다.
			// textArray.foreach(println)

			// string을 yyyyMMdd 형식으로 바꾼다.
			val dateTimeRDD = textRDD.map{dateStr=>
				val pattern = DateTimeFormat.forPattern("yyyyMMdd")
				DateTime.parse(dateStr,pattern);
			}

			// 일요일만 추출한다.
			val sundayRDD = dateTimeRDD.filter{dateTime =>
				dateTime.getDayOfWeek == DateTimeConstants.SUNDAY
			}

			// 일요일 개수를 반환한다.
			val numOfSunday = sundayRDD.count
			println("=========================================")
			println(s"일요일인 날짜의 개수는 ${numOfSunday}개다")
			println("=========================================")

		} finally{
			sc.stop()
		}
		
	}
}
