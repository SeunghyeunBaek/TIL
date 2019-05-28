## Spark DataFrame, SparkSQL

**데이터프레임 준비**

```scala
//DataFrame생성을 위해 데이터를 담는 클래스
case class Dessert(menuId:String, name:String, 		           price:Int, kcal:Int)
// 데이터를 담은 RDD를 만든다.
val dessertRDD = sc.textFile("data/dessert-menu.csv")
// DataFrame으로 만들기위한 RDD를 만든다.
val dessertObjRDD = dessertRDD.map{record =>
    // 쉼표단위로 자른다.
    val splittedLine = record.split(",")
    // Dessert 객체로 만든다
    // RDD안의 튜플의 차원은 1이어야한다.
	Dessert(splittedLine(0),splittedLine(1),
    splittedLine(2).toInt,splittedLine(3).toInt)
}
		val dessertDF = dessertObjRDD.toDF
		// spark sql 사용을 위한 HiveContext 객체를 생성
		import org.apache.spark.sql.hive.HiveContext
		val sqlContext = new HiveContext(sc)
		// sqlContext 객체를 만들고 import 해야함
		import sqlContext.implicits._
		// DataFrame을 Table로 등록한다.
		dessertDF.registerTempTable("dessert_table")
```
클레스를 정의하지 않을경우 toDF에서 행이름을 지정할 수 있음

```scala
val menuDF = menuRDD.toDF("item_id","name","price")
val orderDF = orderRDD.toDF("user_id","item_id","amount")
```
**sql 명령문을 이용하는 방법**

`dessertDF.registerTempTable("dessert_table")` 을 사용해야함

```scala
//정렬
val sortedDF = sqlContext.sql(
"select name, price from dessert_table "
+"where price>=5200 "
+"order by price asc"
)
```

```scala
//집계
val sumDF1 = sqlContext.sql(
    "select sum(price) from dessert_table "
    +"where kcal>=300"
)
```
```scala
//groupBy
val groupDF1 = sqlContext.sql(
    "select menu_type, sum(price),avg(price),max(price) "+
    ", min(price), count(price) "+
    "from dessert_table "+
    "group by menu_type"
)
```

**RDD.toDF 함수를 사용하는 방법**

```scala
//정렬
val sortedDF3 = dessertDF.select($"name",$"price")
						 .where($"price">=5200)
						 .orderBy($"price".asc)
```

```scala
//집계
val sumDF2 = dessertDF.where($"kcal">=300).agg(sum($"price"))
```

```scala
//GroupBy
val groupDF2 = dessertDF.groupBy("menu_type").agg(sum("price"), avg("price"), min("price"), max("price"),count("price"))

```

**Join** 

RDD Join 은 (Key,(val1,val2,...)))로 만들어야함

```scala
// RDD
// RDD 생성
// (key,(val1,val2))

val sourceRDD1 = sc.textFile("data/dessert-menu.csv")
val sourceRDD2 = sc.textFile("data/dessert-order.csv")

val menuRDD = sourceRDD1.map{record =>
    val splittedData = record.split(",")
    (splittedData(0),(splittedData(1),splittedData(2).toInt))
}

val orderRDD = sourceRDD2.map{record=>
    val splittedData = record.split(",")
    (splittedData(1),(splittedData(0),splittedData(2).toInt))
}

val joinRDD = menuRDD.join(orderRDD)
joinRDD.foreach{case(id,((name,price),(userid,amount)))=>
    println(s"${userid}는 ${name}(${price}원)을(를) ${amount}개 구매했고 "+ s"총 구매액은 ${amount*price}원이다")
}
```

**spark sql join**

*where 는 key를 지정하는 역할을 한다*where절을 지정하지 않으면  `Detected implicit cartesian product for INNER join between logical plans`에러가 발생한다.

```scala
menuDF.registerTempTable("menu_table")
orderDF.registerTempTable("order_table")

val joinDF = sqlContext.sql(
"select t1.name,t1.price,t2.user_id,t2.amount "+
"from menu_table as t1, order_table as t2 "+
"where t1.item_id = t2.item_id"
)
```
```scala
val menuDF = menuRDD.toDF("item_id","name","price")
val orderDF = orderRDD.toDF("user_id","item_id","amount")

//Table을 만든다.
menuDF.registerTempTable("menu_table")
orderDF.registerTempTable("order_table")

val joinDF = sqlContext.sql(
"select t1.name,t1.price,t2.user_id,t2.amount "+
"from menu_table as t1, order_table as t2 "+
"where t1.item_id = t2.item_id"
)

joinDF.foreach{row=>
var totPrice = row{1}.toString.toInt*row{2}.toString.toInt
print(s"${row(3)}은 ${row(0)}을 ${row(3)}개 구매했고, ${totPrice}원을 냈다")
}

var joinDF2 = menuDF.join(orderDF,
menuDF("item_id")==orderDF("item_id"),"inner").select("name","price","user_id","amount")
```


