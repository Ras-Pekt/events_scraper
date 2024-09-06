from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from cloud_security.engine import Base


class DBStorage:
    """
    A class to store items in a MySQL database.

    Attributes:
        __engine (Engine): A SQLAlchemy engine to connect to the database
        __session (Session): A SQLAlchemy session to interact with the database

    Methods:
        __init__: Initialize the database connection
        add_item: Add an item to the database
        close: Close the database connection
    """

    __engine = None
    __session = None

    def __init__(self):
        """
        Initialize the database connection.

        args:
            None
        returns:
            None
        """

        MYSQL_USER = getenv("MYSQL_USER")
        MYSQL_PWD = getenv("MYSQL_PWD")
        MYSQL_HOST = "localhost"
        MYSQL_DB = "cloud_security_events"

        self.__engine = create_engine(
            f"mysql+mysqldb://{MYSQL_USER}:{MYSQL_PWD}@{MYSQL_HOST}/{MYSQL_DB}"
        )
        Base.metadata.create_all(self.__engine)

        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()

    def add_item(self, item):
        """
        Add an item to the database.

        args:
            item (object): An item to add to the database
        returns:
            None
        """

        if self.__session:
            self.__session.add(item)
            self.__session.commit()

    def close(self):
        """
        Close the database connection.

        args:
            None
        returns:
            None
        """

        if self.__session:
            self.__session.close()
