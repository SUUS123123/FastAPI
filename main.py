from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import FileResponse

from app import models
from app.api.v1 import router as api_v1_router
from app.config import APP_TITLE, APP_VERSION, PROJECT_ROOT
from app.database import Base, engine


def upgrade_legacy_customers_schema() -> None:
    with engine.begin() as connection:
        connection.exec_driver_sql("""
            IF COL_LENGTH('dbo.Customers', 'Balance') IS NULL
                ALTER TABLE dbo.Customers ADD Balance FLOAT NOT NULL
                    CONSTRAINT DF_Customers_Balance DEFAULT 0 WITH VALUES
            IF COL_LENGTH('dbo.Customers', 'Role') IS NULL
                ALTER TABLE dbo.Customers ADD Role NVARCHAR(20) NOT NULL
                    CONSTRAINT DF_Customers_Role DEFAULT N'buyer' WITH VALUES
        """)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    Base.metadata.create_all(bind=engine)
    upgrade_legacy_customers_schema()
    yield


app = FastAPI(title=APP_TITLE, version=APP_VERSION, lifespan=lifespan)
app.include_router(api_v1_router)


@app.get("/", include_in_schema=False)
def root() -> FileResponse:
    return FileResponse(
        PROJECT_ROOT / "static" / "index.html",
        headers={"Cache-Control": "no-store, no-cache, must-revalidate"},
    )















