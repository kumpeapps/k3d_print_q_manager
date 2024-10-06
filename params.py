"""Parameters file"""

import setup  # pylint: disable=unused-import, wrong-import-order
import os
import sys
from dotenv import load_dotenv
from infisical_api import infisical_api
from loguru import logger


load_dotenv()
service_token = os.getenv("SERVICE_TOKEN")
app_env = os.getenv("APP_ENV")
creds = infisical_api(
    service_token=service_token, infisical_url="https://creds.kumpeapps.com"
)
log_level = os.getenv("log_level", "INFO")
logger.remove()
logger.add(sys.stderr, level=log_level)


class Params:
    """Parameters"""

    preprod: bool = True if app_env == "dev" else False

    class SQL:
        """SQL Parameters"""

        username = creds.get_secret(  # pylint: disable=no-member
            secret_name="USERNAME", environment=app_env, path="/MYSQL/"
        ).secretValue
        password = creds.get_secret(  # pylint: disable=no-member
            secret_name="PASSWORD", environment=app_env, path="/MYSQL/"
        ).secretValue
        server = creds.get_secret(  # pylint: disable=no-member
            secret_name="SERVER", environment=app_env, path="/MYSQL/"
        ).secretValue
        port = creds.get_secret(  # pylint: disable=no-member
            secret_name="PORT", environment=app_env, path="/MYSQL/"
        ).secretValue
        database = "Automation_PrintQueue"

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

        base_url = creds.get_secret(  # pylint: disable=no-member
            secret_name="BASE_URL", environment=app_env, path="/WEB/"
        ).secretValue


if __name__ == "__main__":
    print(
        """Error: This file is a module to be imported and has no functions
          to be ran directly."""
    )
