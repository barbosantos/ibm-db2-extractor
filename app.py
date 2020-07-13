#!/usr/local/bin/python

import configparser
import os
import sys
import logging
import yaml
import ibm_db_dbi
import pandas as pd
import urllib3

import db_utils
from flask import Flask
from gcp_utils import upload_to_bigquery, access_secret_version
from config import tables_to_export

logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


logger = logging.getLogger(__name__)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

@app.route('/')
def main():
    logger.info("Starting DB2 extractor...")

    project_id = os.getenv("GCP_PROJECT")
    secret_id = os.getenv("SECRET_ID")

    db_properties = access_secret_version(project_id, secret_id)
    db_properties = '[db]\n' + db_properties
    config = configparser.RawConfigParser()
    config.read_string(db_properties)

    source_db_host = config.get("db", "source-host")
    source_db_user = config.get("db", "source-user")
    source_db_pass = config.get("db", "source-password")
    source_db_schema = config.get("db", "source-schema")
    source_conn = db_utils.connect_db(source_db_host, source_db_user, source_db_pass)
    conn = ibm_db_dbi.Connection(source_conn)

    bquery_dataset = 'db2-data'
    bquery_dataset = bquery_dataset.replace("-", "_")

    for table_to_export in tables_to_export:
        table = table_to_export["table"]
        source_schema_table = "{}.{}".format(source_db_schema, table)
        columns = table_to_export["columns"]
        where_clause = table_to_export["where_clause"]
        bquery_table_schema = table_to_export["schema_bigquery"]

        sql = "SELECT {} FROM {}".format(columns, source_schema_table)
        if where_clause:
            sql = "{} WHERE {}".format(sql, where_clause)

        logger.info("Running sql: %s", sql)
        conn = ibm_db_dbi.Connection(source_conn)
        # pandas dataframe with the results
        df = pd.read_sql(sql, conn)
        logger.info("Number of rows in dataframe: %s", df.shape[0])
        response = upload_to_bigquery(df, table.lower(), bquery_dataset, bquery_table_schema)
        return response

if __name__ == "__main__":
    try:
        app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
    except:
        print('unable to open port')