## 🏗️ Arquitetura

O projeto é dividido em três camadas no armazenamento S3

- **Bronze**: Dados crus recebidos da API ([The Odds API](https://the-odds-api.com/)).
- **Silver**: Dados limpos e estruturados, prontos para análise.
- **Gold**: Dados agregados e enriquecidos, usados para insights e visualizações.

---

## 🔁 Pipeline de Dados

1. **Ingestão (Bronze)**
   - Conexão com a The Odds API.
   - Coleta de odds para o campeonato brasileiro.
   - Armazenamento bruto em Delta Lake (`bronze/raw`(json) e `bronze/flattened`).

2. **Transformação (Silver)**
   - Explode nos campos aninhados (JSON).
   - Seleção e limpeza de colunas relevantes:
     - Nome dos times
     - Odds por mercado
     - Casa de aposta
     - Timestamp da coleta

3. **Agregação (Gold)**
   - Cálculo da média das odds por time, mercado e se o jogo é em casa ou fora.
   - Renomeação das colunas.
   - Preparação para análise final e exportação para tabelas no Hive Metastore.
