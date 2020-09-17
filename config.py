from google.cloud import bigquery
import datetime


# today = datetime.date.today()
# first = today.replace(day=1)
# lastMonth = first - datetime.timedelta(days=1)
# month = lastMonth.month
# year = lastMonth.year

dataset_location = "southamerica-east1"

SCHEMA_IRIS_FLOWER = [
    bigquery.SchemaField(name="SEPAL_LEN", field_type="FLOAT64", mode="NULLABLE"),
    bigquery.SchemaField(name="SEPAL_WID", field_type="FLOAT64", mode="NULLABLE"),
    bigquery.SchemaField(name="PETAL_LEN", field_type="FLOAT64", mode="NULLABLE"),
    bigquery.SchemaField(name="PETAL_WID", field_type="FLOAT64", mode="NULLABLE"),
    bigquery.SchemaField(name="FLOWER_CLASS", field_type="STRING", mode="NULLABLE")
]

tables_to_export = [{
    "table": "IRIS_FLOWER",
    "alias": None,
    "columns": "SEPAL_LEN, SEPAL_WID, PETAL_LEN, PETAL_WID, FLOWER_CLASS",
    "where_clause": "FLOWER_CLASS = 'Iris-setosa' LIMIT 10",
    "schema_bigquery": SCHEMA_IRIS_FLOWER
}]
