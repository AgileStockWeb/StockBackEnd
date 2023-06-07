import psycopg2
import json
import os
import datetime
from database import PostgreSQLDatabase
from json_processor import JsonProcessor


class ResultDB(PostgreSQLDatabase):
    def __init__(self,host, database, user, password):
        super().__init__(host, database, user, password)
        self.json_processor = JsonProcessor()
        
    def set_result_table(self,json_string):
        
        table = 'result_table'
        columns, values = self.json_processor.json_processing(json_string)
        
        self.connect()
        self.start_transaction()
        try:
            self.insert_data(table, columns, values)
            self.commit_transaction()

        except Exception as e:
            self.rollback_transaction()
            error_message = (f"Transaction rolled back: {str(e)}")
            print(error_message)
            return error_message

        finally:
            self.close()
            
    def set_result_table_price(self,json_string):
        
        table = 'result_table'
        columns, values = self.json_processor.json_processing(json_string)
        
        self.connect()
        self.start_transaction()
        try:
            model_id = values[columns.index('model_id')]  # 取得要更新的 model_id
            condition =  "model_id = CAST('{}' AS text)".format(model_id)
            values[columns.index('model_id')] = str(model_id)
            self.update_data(table, columns, values, condition)  # 執行資料更新
            self.commit_transaction()

        except Exception as e:
            self.rollback_transaction()
            error_message = (f"Transaction rolled back: {str(e)}")
            print(error_message)
            return error_message

        finally:
            self.close()
    
    
    
    
    def get_all_data(self):
        
        table = 'result_table'
        
        self.connect()
        self.start_transaction()
        
        columns = self.get_table_columns(table)
        query = f"SELECT * FROM {table}"
        data = self.execute_query(query)
        reply_data = self.json_processor.database_to_json(data, columns)
        self.commit_transaction()
        self.close()
        return reply_data
    
if __name__ == '__main__':
    json_data3  = '{"jpg_path": "222","model_id":"1"}'
    json_data4  = '{"tomorrow_price": "222.0","model_id":"1"}'
    result_sql = ResultDB(host="127.0.0.1", database="stock_website_database", user="postgres", password="0000")
    result_sql.set_result_table(json_data3)
    result_sql.set_result_table_price(json_data4)
    print(result_sql.get_all_data())