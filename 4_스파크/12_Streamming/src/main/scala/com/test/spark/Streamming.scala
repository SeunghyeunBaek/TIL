package com.test.spark

import org.apache.spark.{SparkConf, SparkContext}

object Streamming{
	def main(args: Array[String]){
		val conf = new SparkConf
		val sc = new SparkContext(conf)
		
		try {
			import org.apache.spark.streaming.{Seconds, StreamingContext}
			import org.apache.spark.storage.StorageLevel
			import org.apache.log4j.{Level, Logger}
			
			// 로그가 너무 많이 출력되서 좀 줄이는 작업
			// 경고 및 오류메시지만 출력되로록 한다.
			Logger.getRootLogger.setLevel(Level.WARN)
			
			// 스트리밍 객체를 생성한다.
			val ssc = new StreamingContext(sc, Seconds(10))
			
			// ------------ 10초에 한번씩 작업할 내용 ----------
			// 데이터를 전달하는 프로그램에 접속해서 데이터를
			// 받아 온다. 이 데이터는 10초에 한번씩 받아온다.
			
			val lines = ssc.socketTextStream("localhost", 9999, StorageLevel.MEMORY_AND_DISK_SER)
			
			// 띄어쓰를 기준으로 잘내어 1차원으로 만들어준다.
			val temp_word = lines.flatMap(record =>
				record.split(" ")
			)
			// 비어있는 정보는 날린다.
			val words = temp_word.filter(record =>
				record.nonEmpty
			)
			
			// 빈도수 계산을 위해 (단어, 1) 구조로
			// 만든다.
			val pairs = words.map(record =>
				(record, 1)
			)
			
			// 빈도수를 계산한다.
			val wordCounts = pairs.reduceByKey {
				case (result, value) =>
				result + value
			}
			
			// 출력
			wordCounts.print()
			
			// 가동한다
			ssc.start()
			// 처리중 오류가 발생했을 경우 바로 종료
			// 시키지 않고 처리가 완료될 때까지 기다린다.
			ssc.awaitTermination()
			
		} finally {
			sc.stop()
		}
	}
}








