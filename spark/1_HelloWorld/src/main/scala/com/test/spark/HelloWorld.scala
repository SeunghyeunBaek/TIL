package com.test.spark

import org.apache.spark.{SparkConf, SparkContext}

object HelloWorld{
	def main(args: Array[String]){
		val conf = new SparkConf
		val sc = new SparkContext(conf)
		
		try{
			println("========================")
			println("Hello Word")
			println("========================")			
		
		} finally{
			sc.stop()
		}
		
	}
}
