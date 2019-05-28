name := "WordCount2"
version := "0.1"
scalaVersion := "2.10.4"
libraryDependencies ++= Seq(
	"org.apache.spark" % "spark-core_2.10" % "2.0.1" % "provided"// provided 컴퓨터 내부에 있는 라이브러리를 설치
)

assemblyOption in assembly := (assemblyOption in assembly).value.copy(includeScala = false)
