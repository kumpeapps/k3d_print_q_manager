"""Parameters file"""

import setup  # pylint: disable=unused-import, wrong-import-order
import os
import sys
from dotenv import load_dotenv
from loguru import logger


load_dotenv()
service_token = os.getenv("SERVICE_TOKEN")
app_env = os.getenv("APP_ENV")
log_level = os.getenv("log_level", "INFO")
logger.remove()
logger.add(sys.stderr, level=log_level)


class Params:
    """Parameters"""

    preprod: bool = True if app_env == "dev" else False

    class SQL:
        """SQL Parameters"""

        username = os.getenv("MYSQL_USERNAME", "amech_k3dprintqmanager")
        password = os.getenv("MYSQL_PASSWORD", "")
        server = os.getenv("MYSQL_SERVER", "rw.sql.pvt.kumpedns.us")
        port = os.getenv("MYSQL_PORT", "3306")
        database = os.getenv("MYSQL_DATABASE", "Automation_PrintQueue")

        @staticmethod
        def dict():
            """returns as dictionary"""
            return {
                "username": Params.SQL.username,
                "password": Params.SQL.password,
                "server": Params.SQL.server,
                "port": Params.SQL.port,
                "database": Params.SQL.database,
            }

    class WEB:
        """WEB Parameters"""

        base_url = os.getenv("WEB_BASE_URL", "https://www.kumpe3d.com")
        api_base_url = os.getenv("API_BASE_URL", "https://api.kumpeapps.us")


if __name__ == "__main__":
    print(
        """Error: This file is a module to be imported and has no functions
          to be ran directly."""
    )
