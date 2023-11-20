
from Database.databaseManager import databaseManager
from Database.Report_DB import Report_DB

class mainDatabase:
    username = "root"
    password = "dorsa-co"
    HOST = "localhost"
    DATABASE_NAME = "test_database"

    def __init__(
        self,
    ):
        self.dbManager = None
        self.__connect__()

        self.Report_DB = Report_DB(self.dbManager)
       

    def __connect__(
        self,
    ):
        self.dbManager = databaseManager(
            self.username, self.password, self.HOST, self.DATABASE_NAME, log_level=1
        )



