package com.test.spark

import org.apache.spark.{SparkConf, SparkContext}

object WordCount{
	def main(args: Array[String]){
		val conf = new SparkConf
		val sc = new SparkContext(conf)
		
		try {
			
			
		} finally {
			sc.stop()
		}
	}
}








