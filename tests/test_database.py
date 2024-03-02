import sqlalchemy as sql
from airflow.dags.src.database import PostgresDB


def test_postgresdb_create_engine_conn():
    """
    Test case to verify the creation of a SQLAlchemy engine connection.
    """
    host = "localhost"
    user = "test_user"
    password = "test_password"  # pragma: allowlist secret
    port = 5432
    database = "data_apps"

    db = PostgresDB(
        host=host, user=user, password=password, port=port, database=database
    )
    engine_conn = db.create_engine_conn()

    assert isinstance(engine_conn, sql.engine.base.Engine)


def test_postgresdb_url_conn():
    """
    Test case to verify the URL connection string for the PostgreSQL database.
    """
    host = "localhost"
    user = "test_user"
    password = "test_password"  # pragma: allowlist secret
    port = 5432
    database = "data_apps"

    db = PostgresDB(
        host=host, user=user, password=password, port=port, database=database
    )
    assert (
        db.url_conn
        == f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    )
