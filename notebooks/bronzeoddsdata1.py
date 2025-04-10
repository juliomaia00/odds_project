from pyspark.sql.functions import explode, col

# Lê  JSON salvo no S3 (camada Bronze Raw)
df = spark.read.option("multiline", "true").json(bronze_raw_path)

flat_df = df.withColumn("bookmakers", explode(col("bookmakers")))
flat_df.show(3, truncate=False)

flat_df.write.format("delta").mode("overwrite").save(bronze_flat_path)
print("ok")