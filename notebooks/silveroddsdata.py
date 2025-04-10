## filtra colunas relevantes que usei para as metricas na gold, padroniza formatos e prepara os dados para análises

from pyspark.sql.functions import explode, col

df = spark.read.format("delta").load(bronze_flat_path)

cleaned = df.select(
    col("id"),
    col("sport_key"),
    col("commence_time"),
    col("home_team"),
    col("away_team"),
    col("bookmakers.title").alias("bookmaker"),
    explode("bookmakers.markets").alias("market")
)

silver_df = cleaned.select(
    "id", "sport_key", "commence_time", "home_team", "away_team", "bookmaker",
    col("market.key").alias("market_type"),
    explode("market.outcomes").alias("outcome")
).select(
    "id", "sport_key", "commence_time", "home_team", "away_team", "bookmaker", "market_type",
    col("outcome.name").alias("team"),
    col("outcome.price").alias("odds")
)

silver_df.write.format("delta").mode("overwrite").save(silver_path)
print("ok")