import sqlalchemy as sqla


class Database:
    def __init__(
        self, host: str, user: str, password: str, port: str, database: str
    ) -> None:
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.database = database

    def create_engine_conn(self, url_conn: str) -> sqla.engine.base.Engine:
        return sqla.create_engine(url_conn)


class PostgresDB(Database):
    """
    A class representing a PostgreSQL database connection.

    Args:
        host (str): The hostname or IP address of the database server.
        user (str): The username for authenticating with the database server.
        password (str): The password for authenticating with the database server.
        port (int): The port number on which the database server is listening.

    Attributes:
        url_conn (str): The connection URL for the PostgreSQL database.

    Methods:
        create_engine_conn: Creates and returns a SQLAlchemy engine connection.

    """

    def __init__(self, host, user, password, port, database) -> None:
        super().__init__(host, user, password, port, database)
        self.url_conn = f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    def create_engine_conn(self) -> sqla.engine.base.Engine:
        """
        Creates and returns a SQLAlchemy engine connection.

        Returns:
            sqla.engine.base.Engine: The SQLAlchemy engine connection.

        """
        return super().create_engine_conn(self.url_conn)


if __name__ == "__main__":
    pass
