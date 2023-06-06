import json
from datetime import datetime

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.date().strftime('%Y/%m/%d')  # 只保留日期部分並使用斜線分隔
        return super().default(obj)

class JsonProcessor:
    @staticmethod
    def json_processing(json_string):
        data = json.loads(json_string)
        columns = list(data.keys())
        values = list(data.values())
        return columns, values

    @staticmethod
    def convert_to_dict(columns, data):
        result = []
        for row in data:
            dict_row = {}
            for column, value in zip(columns, row):
                if isinstance(value, datetime):
                    dict_row[column] = value.strftime('%Y/%m/%d')
                else:
                    dict_row[column] = value
            result.append(dict_row)
        return result[0]

    @staticmethod
    def database_to_json(data, columns):
        json_data = []
        for row in data:
            record = {}
            for i, column in enumerate(columns):
                value = row[i]
                if value is None:
                    value = ''
                elif isinstance(value, datetime):
                    value = value.date().strftime('%Y/%m/%d')
                record[column] = value
            json_data.append(record)
        return json.dumps(json_data, cls=DateTimeEncoder)
