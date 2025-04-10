import requests, json
from datetime import datetime

url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"
params = {
    "apiKey": odds_api_key,
    "regions": region,
    "markets": markets,
    "oddsFormat": odds_format
}


response = requests.get(url, params=params)


if response.status_code != 200:
    raise Exception(f"Erro ao buscar dados: {response.status_code} - {response.text}")


odds_data = response.json()


timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
local_file_path = f"/tmp/odds_{timestamp}.json"
s3_target_path = bronze_raw_path + f"odds_{timestamp}.json"


with open(local_file_path, "w") as f:
    json.dump(odds_data, f, indent=2)

dbutils.fs.cp(f"file:{local_file_path}", s3_target_path)

print(f"Arquivo enviado com sucesso para: {s3_target_path}")