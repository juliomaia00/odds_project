from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col, when
spark = SparkSession.builder.appName("OddsGoldAnalytics").getOrCreate()

silver_path = "s3a://dataodds/silver/cleaned"
gold_path = "s3a://dataodds/gold/odds_aggregated"

df = spark.read.format("delta").load(silver_path)



# define se o time está jogando em casa ou fora
df = df.withColumn(
    "local",
    when(col("team") == col("home_team"), "casa").otherwise("fora")
)

# agrpa por time, casa de aposta e local (casa/fora), e calcula a média das odds
agg = df.groupBy("team", "market_type", "local").agg(
    avg("odds").alias("media_odds")
)

# Renomeia as colunas 
agg = agg.withColumnRenamed("team", "time") \
         .withColumnRenamed("market_type", "casa_de_aposta")

# mostra os dados e faz o carregamento na camada gold
agg.show(30, truncate=False)
agg.write.format("delta").mode("overwrite").option("mergeSchema", "true").save(gold_path)
