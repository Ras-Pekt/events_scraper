from cloud_security.engine import Base
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
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
        self.__session.add(item)
        self.__session.commit()

    def close(self):
        self.__session.close()
