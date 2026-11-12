from google_big_query import carregar_bigquery
from extract_diesel_s10 import extract
from transform_diesel_s10 import transform

df = extract()
df = transform(df)
carregar_bigquery(df)

if __name__ == "__main__":
    main()