import psycopg2
import os
import json

class PostgreSQLDatabase:
    """              Database 連線基礎操作           """
    #初始化
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.conn = None
        self.cur = None

    #開始連結DB
    def connect(self):
        self.conn = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )
        self.cur = self.conn.cursor()

    #關掉連結
    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
            
            
    """          Table 相關操作               """

    #在當前 database 新增table
    #輸入範例  table_name = 'your_table'  columns = ['id SERIAL PRIMARY KEY', 'name VARCHAR(255)', 'age INTEGER']
    def create_table(self, table, columns):
        column_definitions = ', '.join(columns)
        query = f"CREATE TABLE {table} ({column_definitions})"
        print(query)
        self.cur.execute(query)
        self.conn.commit() #

    #刪除 table
    def drop_table(self, table):
        query = f"DROP TABLE IF EXISTS {table}"
        self.cur.execute(query)
        self.conn.commit() #
    
    #查看當前database 有哪些table
    def get_tables(self):
        query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
        self.cur.execute(query)
        rows = self.cur.fetchall()
        tables = [row[0] for row in rows]
        return tables
    
    #查看 table 欄位
    def get_table_columns(self, table):
        query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}'"
        self.cur.execute(query)
        rows = self.cur.fetchall()
        columns = [row[0] for row in rows]
        return columns
    
    """              資料相關操作               """
    def execute_query(self, query):
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    def execute_update(self, query, values):
        self.cur.execute(query, values)
        self.conn.commit()

    #插入資料
    def insert_data(self, table, columns, values):
        column_names = ', '.join(columns)
        placeholders = ', '.join(['%s'] * len(values))
        query = f"INSERT INTO {table} ({column_names}) VALUES ({placeholders})"
        self.execute_update(query, values)

    #修改資料
    def update_data(self, table, column, value, condition):
        query = f"UPDATE {table} SET {column} = %s WHERE {condition}"
        self.execute_update(query, (value,))
    
    #尋找資料
    def select_data(self, table, columns, condition=None):
        column_names = ', '.join(columns) if columns else '*'
        query = f"SELECT {column_names} FROM {table}"
        if condition:
            query += f" WHERE {condition}"
        return self.execute_query(query)
    
    #刪除資料
    def delete_data(self, table, condition):
        query = f"DELETE FROM {table} WHERE {condition}"
        self.execute_update(query, ())
        
        
    """           匯入/匯出 資料            """        
    # 導入資料  table:匯入當前已存在的table   delimiter:分割資料的分割符號   header:是否要導入第一行     
    def import_data(self, table, file_path, delimiter=',', header=True):
        abs_file_path = os.path.abspath(file_path)
        query = f"COPY {table} FROM '{abs_file_path}' DELIMITER '{delimiter}' CSV {'HEADER' if header else ''}"
        self.execute_update(query, ())

    # 導出資料
    def export_data(self, table, file_path, delimiter=',', header=True):
        abs_file_path = os.path.abspath(file_path)
        query = f"COPY {table} TO '{abs_file_path}' DELIMITER '{delimiter}' CSV {'HEADER' if header else ''}"
        self.execute_update(query, ())
            
    """          執行多個相關的 SQL 操作，以確保它們要麼全部成功提交，要麼全部都不送               """      
    # 开始事务 
    def start_transaction(self):
        self.conn.autocommit = False
        self.cur = self.conn.cursor()

    # 提交事务
    def commit_transaction(self):
        self.conn.commit()
        self.conn.autocommit = True
        self.cur.close()
        self.cur = None

    # 回滚事务
    def rollback_transaction(self):
        self.conn.rollback()
        self.conn.autocommit = True
        self.cur.close()
        self.cur = None


class StockSQL(PostgreSQLDatabase):
    def __init__(self,host, database, user, password):
        super().__init__(host, database, user, password)
    
    def insert_data(self, table, columns, values):
        column_names = ', '.join(columns)
        placeholders = ', '.join(['%s'] * len(values))
        query = f"INSERT INTO {table} ({column_names}) VALUES ({placeholders}) RETURNING model_id"
        self.execute_update(query, values)
        inserted_id = self.cur.fetchone()[0]  # 獲取自動產生的 ID
        self.conn.commit()
        return inserted_id

    #接收到品宏的DATA 要儲存 並傳給學長
    def get_build_model(self, json_string):
        
        table = 'model_build_table'
        columns, values = self.json_processing(json_string)
        
        self.connect()
        self.start_transaction()
        try:
            model_id = self.insert_data(table, columns, values)
            condition = "model_id = {}".format(model_id)
            print(model_id)
            reply_data = self.select_data(table, '*', condition)
            
            
            self.commit_transaction()
            return reply_data
            
        except Exception as e:
            self.rollback_transaction()
            print(f"Transaction rolled back: {str(e)}")

        finally:
            self.close()
    
    @staticmethod
    def json_processing(json_string):
        data = json.loads(json_data)
        columns = list(data.keys())
        values = list(data.values())
        return columns, values
    
