from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col, when
spark = SparkSession.builder.appName("OddsGoldAnalytics").getOrCreate()
silver_path = "s3a://dataodds/silver/cleaned"
gold_path = "s3a://dataodds/gold/odds_aggregated"




df = spark.read.format("delta").load(silver_path)

# analisa no database se o time está jogando em casa ou fora
df = df.withColumn(
    "home_or_away",
    when(col("team") == col("home_team"), "home").otherwise("away")
)

# agrupa por time, casa de aposta e se esta jogando em casa/fora e calcula a média das odds para cada situaçao
agg = df.groupBy("team", "market_type", "home_or_away").agg(
    avg("odds").alias("avg_odds")
)

# Exibe os resultados
print("database")
agg.show(30, truncate=False)

agg.write.format("delta").mode("overwrite").option("mergeSchema", "true").save(gold_path)
