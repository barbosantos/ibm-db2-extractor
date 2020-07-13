import logging
from retry import retry

import ibm_db

logger = logging.getLogger(__name__)

@retry(tries=2, delay=10)
def connect_db(hostname, user, password):
    logger.info("Connecting to DB %s", hostname)
    conn_str = "DATABASE=BLUDB;HOSTNAME={hostname};PORT=50000;PROTOCOL=TCPIP;UID={user};PWD={password}".format(
        hostname=hostname,
        user=user,
        password=password
    )
    return ibm_db.connect(conn_str, "", "")


def exec_sql(conn, sql):
    logger.info("Running sql: %s", sql)
    stmt = ibm_db.exec_immediate(conn, sql)
    logger.info("Number of affected rows: %d", ibm_db.num_rows(stmt))


def fecth_sql(conn, sql):
    logger.info("Running sql: %s", sql)
    stmt = ibm_db.exec_immediate(conn, sql)
    return ibm_db.fetch_assoc(stmt)


def count_rows(conn, table, where_clause=None):
    sql = "SELECT COUNT(*) AS TOTAL FROM {}".format(table)
    if where_clause:
        sql = "{} WHERE {}".format(sql, where_clause)
    result = fecth_sql(conn, sql)
    return result["TOTAL"]
