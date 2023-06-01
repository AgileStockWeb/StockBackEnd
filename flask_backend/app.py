from flask import Flask, request, jsonify
from postgraphql import *
# import AImodel

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 禁止中文转义

def submit2db(data):
    # 建立資料表
    # 增加id欄位
    model_sql = StockSQL(host="127.0.0.1", database="stock_website_database", user="postgres", password="0000")
    training_data = model_sql.get_build_model(data)

    if not isinstance(training_data, dict):
        return jsonify({
            "msg": training_data
        })
    else:
        return training_data

def db2model(training_data):
    AImodel = ...
    # 還要寫expection
    return # result

def model2db():
    ...

@app.route("/submit/train", methods=["POST"])
def submit_training_data():
    try:
        data = request.get_json()
        print(data)
    except Exception as e:
        print(e)
        return jsonify({'error': 'Invalid JSON data.'})
    
    # 要做什麼事
    state = data.get('state')

    if state == 'train':
        training_data = submit2db(data)
        result = db2model(training_data)
        db2model(result)
    elif state == ...:   
        ...

    return jsonify(result)

@app.route("/submit/predict", methods=["POST"])
def submit_predict_data():
    try:
        data = request.get_json()
        print(data)
    except Exception as e:
        print(e)
        return jsonify({'error': 'Invalid JSON data.'})
    
    '''
    從資料庫load訓練好的模型
    需要load model api
    回傳現有的model供選擇
    '''
    predict_md = data.get('model')
    # 呼叫load model api 傳入predict_md 回傳model位置

    

    






        

if __name__ == '__main__':
    app.start()