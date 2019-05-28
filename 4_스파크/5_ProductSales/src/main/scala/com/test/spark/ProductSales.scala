package com.test.spark

import org.apache.spark.{SparkConf, SparkContext}
// HashMap
import scala.collection.mutable.HashMap
// 파일에서 데이터를 읽어오기 위해
import java.io.{BufferedReader, InputStreamReader}
// 파일 시스템 접근을 위해
import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.fs.{FileSystem, Path}

object ProductSales{
	def main(args: Array[String]){
		val conf = new SparkConf
		val sc = new SparkContext(conf)
		
		try {
			// 1. 10월과 11월에 대한 매출 정보를 읽어와
			//    RDD로 만든다.
			val octRDD = sc.textFile("../../data/sales-october.csv")
			// octRDD.collect.foreach(println)
			
			val splitOctRDD = octRDD.map { record =>
				val splitData = record.split(",")
				(splitData(2), splitData(3).toInt)
			}
			// splitOctRDD.collect.foreach(println)
			
			val novRDD = sc.textFile("../../data/sales-november.csv")
			// novRDD.collect.foreach(println)
			
			val splitNovRDD = novRDD.map { record =>
				val splitData = record.split(",")
				(splitData(2), splitData(3).toInt)
			}
			splitNovRDD.collect.foreach(println)
			
			
			// 2. 각 월의 매출 정보를 상품당 총 판매 개수
			//    형태로 계산하여 각각 RDD로 만든다.
			val keyOctRDD = splitOctRDD.reduceByKey(
				(result, elem) =>
				result + elem
			)
			// keyOctRDD.collect.foreach(println)
			
			val keyNovRDD = splitNovRDD.reduceByKey(
				(result, elem) =>
				result + elem
			)
			// keyNovRDD.collect.foreach(println)
			
			// 3. 각 총 매출 현황을 하나의 결과로 통합한다.
			
			// join : 둘 중 한군데라도 없는건 빠진다.
			// leftOuterJoin : 좌측에는 있는 레코드는 모두
			// 가져오고 우측에 없는 것은 None으로 처리된다.
			// rightOuterJoin : 우측에 있는 레코드는 모두
			// 가져오고 좌측에 없는 것은 None으로 처리된다.
			// fullOuterJoin : 좌우측 모두 가져오고 좌우측에
			// 없는 것은 None으로 처리된다.
			val bothRDD = keyOctRDD.join(keyNovRDD)
			// bothRDD.collect.foreach(println)
			
			val totalRDD = bothRDD.map{
				case (productId, (octAmount, novAmount)) =>
				(productId, octAmount + novAmount)
			}
			// totalRDD.collect.foreach(println)
						
			// 4. 상품 정보와 통합된 결과를 합쳐 하나의
			//    최종결과를 가져온다.
			// (상품id, (상품이름, 단가))
			// 상품정보를 가져온다.
			/* 
			val productRDD = sc.textFile("../../data/products.csv")
			// productRDD.collect.foreach(println)
			val keyProductRDD = productRDD.map { record =>
				val splitData = record.split(",")
				(splitData(0), (splitData(1), splitData(2)))
			}
			// keyProductRDD.collect.foreach(println)
			
			// 합친다.
			val resultRDD = keyProductRDD.join(totalRDD)
			// resultRDD.foreach(println)
			val resultRDD2 = resultRDD.map {
				case (id, ((name, price), amount)) =>
				s"${name}은 단가가 ${price}이고 ${amount}만큼 팔렸음"
			}
			resultRDD2.foreach(println)
			*/
			// 데이터를 담을 해시맵 객체를 생성한다.
			val productMap = new HashMap[String, (String, Int)]
			// 파일에 접근할 수 있는 객체를 생성한다.
			val hadoopConf = new Configuration
			val fileSystem = FileSystem.get(hadoopConf)
			// 파일에서 데이터를 읽어올 수 있는 객체를 생성한다
			val inputStream = fileSystem.open(new Path("../../data/products.csv"))
			// 데이터를 문자로 변환해 주는 객체
			val isr = new InputStreamReader(inputStream)
			// 라인단위로 읽어 올수 있는 객체
			val br = new BufferedReader(isr)
			
			// 첫 라인을 읽어온다.
			var line = br.readLine
			
			while(line != null){
				// 쉼표를 기준으로 잘라낸다.
				val splitLine = line.split(",")
				// 해시맵에 담는다.
				productMap(splitLine(0)) = (splitLine(1), splitLine(2).toInt)
				// 다음 줄을 읽어온다.
				line = br.readLine
			}	
			// 파일을 닫는다.
			br.close()
			// println(productMap)
			
			// 브로드캐스트 변수로 만들어준다.
			val bcMap = sc.broadcast(productMap)
			
			// 데이터를 종합하여 출력한다.
			val resultRDD = totalRDD.map {
				case (productId, amount) =>
				// 브로드캐스트 변수에서 해시맵을
				// 가져온다.
				val map2 = bcMap.value
				// 해시맵에서 상품 id에 해당하는
				// 튜플을 가져온다.
				val (name, price) = map2(productId)
				s"${name}의 가격은 ${price}이고 총 ${amount}개 팔렸습니다"
			}
			
			println("==========================")
			resultRDD.foreach(println)
			println("==========================")
		} finally {
			sc.stop()
		}
	}
}








