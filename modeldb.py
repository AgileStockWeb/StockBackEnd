import psycopg2
import json
import os
import datetime
from database import PostgreSQLDatabase
from json_processor import JsonProcessor


class TrainingDataDB(PostgreSQLDatabase):
    def __init__(self,host, database, user, password):
        super().__init__(host, database, user, password)
        self.json_processor = JsonProcessor()
        
    def insert_data(self, table, columns, values):
        column_names = ', '.join(columns)
        placeholders = ', '.join(['%s'] * len(values))
        query = f"INSERT INTO {table} ({column_names}) VALUES ({placeholders})"
        self.execute_update(query, values)
        self.conn.commit()

    #接收到品宏的DATA 要儲存 並傳給學長
    def get_build_model(self, json_string):
        
        table = 'model_table'
        columns, values = self.json_processor.json_processing(json_string)
        
        self.connect()
        self.start_transaction()
        try:
            self.insert_data(table, columns, values)
            #condition = "model_id = {}".format(model_id)
            columns = self.get_table_columns(table)
            #data = self.select_data(table, '*', condition)
            #print(data)
            #reply_data = self.json_processor.database_to_json(columns, data)
            
            self.commit_transaction()
            return json.dumps('{"sucess":"0"}')
        except Exception as e:
            self.rollback_transaction()
            error_message = (f"Transaction rolled back: {str(e)}")
            print(error_message)
            return error_message

        finally:
            self.close()
    
    
    def set_model_path(self, json_string):
        
        table = 'model_table'
        columns, values = self.json_processor.json_processing(json_string)
        
        self.connect()
        self.start_transaction()
        try:
            model_id = values[columns.index('model_id')]  # 取得要更新的 model_id
            condition = "model_id = {}".format(model_id)
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
        table = 'model_table'
        
        self.connect()
        self.start_transaction()
        
        columns = self.get_table_columns(table)
        query = f"SELECT * FROM {table}"
        data = self.execute_query(query)
        reply_data = self.json_processor.database_to_json(data, columns)
        self.commit_transaction()
        self.close()
        return reply_data
    
    def get_page_data(self):
        table = 'model_table'
        
        self.connect()
        self.start_transaction()
        
        columns = ['model_id', 'model_name', 'data_clean', 'start_time', 'end_time', 'stock_code', 'technical_indicator']
        query = f"SELECT * FROM {table}"
        data = self.execute_query(query)
        reply_data = self.json_processor.database_to_json(data, columns)
        self.commit_transaction()
        self.close()
        return reply_data
    
    def find_model_id(self, json_string):
        table = 'model_table'

        columns, values = self.json_processor.json_processing(json_string)
        self.connect()
        self.start_transaction()

        columns = self.get_table_columns(table)
        query = f"SELECT * FROM {table} WHERE model_id = '{values[0]}'"
        data = self.execute_query(query)
        reply_data = self.json_processor.database_to_json(data, columns)
        self.commit_transaction()
        self.close()
        return reply_data
if __name__ == '__main__':
    # 假設這是你的JSON數據
    json_data  = '{"model_id":"8","stock_code":"2303", "start_time":"2020/3/02", "end_time":"2020/03/04", "model_name":"XGB", "data_clean":"dfg", "technical_indicator":"sdfs"}'
    update_data  = '{"model_id":"1" , "model_path": "1514"}'
    model_sql = TrainingDataDB(host="127.0.0.1", database="stock_website_database", user="postgres", password="0000")
    
    tmp = model_sql.get_build_model(json_string=json_data)