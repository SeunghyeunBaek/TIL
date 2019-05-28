name := "Question"
version := "0.1"
scalaVersion := "2.10.4"
libraryDependencies ++= Seq(
	"org.apache.spark" % "spark-core_2.10" % "2.0.1" % "provided"
)
assemblyOption in assembly := (assemblyOption in assembly).value.copy(includeScala = false)
