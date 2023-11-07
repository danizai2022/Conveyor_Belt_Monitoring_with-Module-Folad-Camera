
class Report_DB:
    TABLE_NAME = "report46"

    def __init__(self, db_manager):
        self.db_manager = db_manager
        #self.__create_table__()
        self.TABLE_NAME="reports46"

    def __create_table__(
        self,
    ):
        self.db_manager.create_table(self.TABLE_NAME)
        self.db_manager.create_table(self.TABLE_NAME_DEFAULT)

        for col in self.TABLE_COLS:
            self.db_manager.add_column(self.TABLE_NAME, **col)
            self.db_manager.add_column(self.TABLE_NAME_DEFAULT, **col)


    def is_exist(self, application):
        founded_records = self.db_manager.search(
            self.TABLE_NAME, self.PRIMERY_KEY_COL_NAME, application
        )
        if len(founded_records) > 0:
            return True
        return False

    def save(self, data):
        if self.is_exist(data[self.PRIMERY_KEY_COL_NAME]):
            self.db_manager.update_record_dict(
                self.TABLE_NAME,
                data,
                self.PRIMERY_KEY_COL_NAME,
                data[self.PRIMERY_KEY_COL_NAME],
            )
        else:
            self.db_manager.add_record_dict(self.TABLE_NAME, data)


    def get_all_content(self):
         record=self.db_manager.get_all_content(self.TABLE_NAME)
         return record
      
    def remove_record(self,column_name, Select_ID):

        records = self.db_manager.remove_record(self.TABLE_NAME, column_name, Select_ID)
  

    def  search(self,column_name, Select_ID):
         records = self.db_manager.search(self.TABLE_NAME, column_name, Select_ID)
         return records
    

    def search_interval(self,column_name,min_of_interval,max_of_interval):
         records = self.db_manager.search_interval(
                    self.TABLE_NAME,
                   column_name,
                    min_of_interval,
                    max_of_interval,
                )
         return  records
    
    def add_record(self,value):

     self.db_manager.add_record(
                        self.TABLE_NAME,
                        value
                    )