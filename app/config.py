import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import URL

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


def get_database_url() -> URL:
    query = {
        "driver": os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server"),
        "TrustServerCertificate": os.getenv("DB_TRUST_SERVER_CERTIFICATE", "yes"),
    }
    if os.getenv("DB_TRUSTED_CONNECTION", "yes").lower() in {"yes", "true", "1"}:
        query["trusted_connection"] = "yes"
    else:
        query["UID"] = os.getenv("DB_USER", "sa")
        query["PWD"] = os.getenv("DB_PASSWORD", "")

    return URL.create(
        "mssql+pyodbc",
        host=os.getenv("DB_SERVER", r"localhost\SQLEXPRESS"),
        database=os.getenv("DB_NAME", "ComputerShop"),
        query=query,
    )


DATABASE_URL = get_database_url()
APP_TITLE = os.getenv("APP_TITLE", "Computer Shop API")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
