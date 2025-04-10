from dotenv import load_dotenv
import os

load_dotenv()

aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
odds_api_key = os.getenv("ODDS_API_KEY")

spark._jsc.hadoopConfiguration().set("fs.s3a.access.key", aws_access_key)
spark._jsc.hadoopConfiguration().set("fs.s3a.secret.key", aws_secret_key)
spark._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "s3.amazonaws.com")

# Odds API Config
sport = "soccer_brazil_campeonato"
region = "us"
markets = "h2h,spreads,totals"
odds_format = "decimal"

# S3 paths 
bucket = "dataodds"
bronze_raw_path = f"s3a://{bucket}/bronze/raw/"
bronze_flat_path = f"s3a://{bucket}/bronze/flattened/"
silver_path = f"s3a://{bucket}/silver/cleaned/"
gold_path = f"s3a://{bucket}/gold/aggregated/"