"""Print Q Monitor"""

import setup  # pylint: disable=unused-import, wrong-import-order
import sys
import time
import pymysql
from loguru import logger
from params import Params, log_level
import printcommands as pc

logger.remove()
logger.add(sys.stderr, level=log_level)


def monitor():
    """Monitors mySQL database for new print jobs"""
    sql_params = Params.SQL
    kumpe3d_labels_sql = """
                        SELECT 
                            *
                        FROM
                            Automation_PrintQueue.kumpe3d_labels
                        WHERE
                            1 = 1 
                            AND printed = 0;
    """
    kumpe3d_labels_complete_sql = """
                                UPDATE kumpe3d_labels 
                                SET 
                                    printed = 1,
                                    printed_timestamp = now()
                                WHERE
                                    idkumpe3d_labels = %s
    """
    while True:
        db = pymysql.connect(
            db=sql_params.database,
            user=sql_params.username,
            passwd=sql_params.password,
            host=sql_params.server,
            port=3306,
        )
        cursor = db.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute(kumpe3d_labels_sql)
            kumpe3d_labels_printq = cursor.fetchall()
            for print_job in kumpe3d_labels_printq:
                pc.print_product_label(
                    print_job["sku"],
                    print_job["qr_data"],
                    print_job["label_type"],
                    print_job["qty"],
                    print_job["distributor_id"],
                    bool(print_job["enable_print"]),
                )
                cursor.execute(kumpe3d_labels_complete_sql, print_job["idkumpe3d_labels"])
                db.commit()
        except Exception:
            logger.exception("monitor exception")
        cursor.close()
        db.close()
        time.sleep(5)


if __name__ == "__main__":
    monitor()
