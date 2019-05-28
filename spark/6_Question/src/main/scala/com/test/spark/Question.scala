package com.test.spark

import org.apache.spark.{SparkConf, SparkContext}

object Question{
	def main(args: Array[String]){
		val conf = new SparkConf
		val sc = new SparkContext(conf)
		
		try {
			// csv 파일로 부터 RDD를 생성한다.
			val tmpRDD = sc.textFile("data/questionnaire.csv")
			val questionRDD = tmpRDD.map{record=>
				val record2 = record.split(",")
				(record2(0)/10, record2(1),record2(2).toInt)
			}
			// 영속화 : 여러컴퓨터에 분산저장돼있는 정보를 하나의 컴퓨터 메모리에 적재
			questionRDD.cache
			// 전체 평균
			//  행 개수 세기
			// val count = questionRDD.count
			// RDD를 두번 만드는 경우
			// 나이,성별,도수 중 도수 추출
			//val tmpRDD = questionRDD.map{
			//	case(a1,a2,a3) => a3
			//}
			// 전체 도수 합산
			//val total = tmpRDD.sum
			//평균 산출
			//val avg = total/count
			//print(avg)

			// RDD를 한번만 만드는 경우
			//(점수, 1)로 구성된 RDD를 만든다.
			val tmpRDD = questionRDD.map{
				case(age,gender,score) => (score,1)
			}
			// 점수 총합과 개수를 구한다.
			// point1,count1 : 중간결과값
			// point2,count2 : RDD에 저장된 값
			val(totalPoints,counts)=tmpRDD.reduce{
				case((point1,count1),(point2,count2))=>
					(point1+point2,count1+count2)
			}
			//평균을 구한다.

			//나이대별 평균을 구한다.
			val tmpRDD = questionRDD.map{
				case(age,gender,score) =>
					(age,(score,1))
			}
			// 총점과 개수를 계산한다.
			// reduceByKey : age를 기준으로 그룹화, (score,key)가 넘어온다.
			val ageRDD = tmpRDD.reduceByKey{
				case((point1,count1),(point2,count2))=>
					(point1+point2,count1+count2)
			}
			//출력
			println("===============================")
			ageRDD.foreach{
				case(age,(total,counts))=>
					println(s"${age} : ${total.toDouble/counts.toDouble}")
			}
			println("===============================")

			// 공유 변수선언
			// accumulator로 만든 변수는 다른 클러스터에서 사용할 수 있다.
			val numM = sc.accumulator(0, "number of M")
			val numF = sc.accumulator(0, "number of F")
			val totalM = sc.accumulator(0, "total score of M")
			val totalF = sc.accumulator(0,"total score of F")

			questionRDD.foreach{
				case(age,gender,score) =>
					gender match {
						case "M" => 
							numM += 1
							totalM += score
						case "F" => 
							numF += 1
							totalF += score
					}

			}

			val avgM = totalM.value.toDouble/numM.toDouble
			val avgF = totalF.value.toDouble/numM.toDouble
			println(s"남자 : ${avgM}")
			println(s"여자 : ${avgF}")

			//성별 평균
			/*
			val tmpRDD = questionRDD.map{
				case(age,gender,score)=>
					(gender,(score,1))
			}
			val genderRDD = tmpRDD.reduceByKey{
				case((point1,count1),(point2,count2))=>
					(point1+point2,count1+count2)
			}
			//출력
			genderRDD.foreach{
				case(gender,(total,counts))=>
					var gender2 = new String
					gender match{
						case "M" => gender2 = "남자"
						case "F" => gender2 = "여자"
					}
					println("===============================")
					val avg = total.toDouble/counts.toDouble
					println(s"${gender2} : ${avg}")
					println("===============================")
			}
			*/

		} finally {
			sc.stop()
		}
	}
}








