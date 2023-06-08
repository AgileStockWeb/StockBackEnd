from flask import Flask, request, jsonify
from modeldb import *
from resultDB import *
from model import *
from flask_cors import CORS
import uuid
import json

app = Flask(__name__)
CORS(app, origins='*')

@app.route("/api/user/input", methods=["POST"])
def user_input():
    user_input = request.get_json()
    print(user_input)
    # 在 user_input 中加入唯一的 UUID
    user_input['model_id'] = str(uuid.uuid4())


    # 將資料傳給model  
    model = StockPrediction()
    model.input_data(user_input['stock_code'],
                        user_input['start_time'],
                        user_input['end_time'],
                        )
    model.choose_normalization(user_input['data_clean'])
    model.choose_model(user_input['model_type'])
    train_model_path = model.train_model(user_input['model_id'])

    # 印出model估計值
    # model.estimate()

    user_input['model_path'] = train_model_path

    # dict 轉 json
    user_input = json.dumps(user_input)
    
    # 使用資料庫格式並連線
    model_sql = TrainingDataDB(host="127.0.0.1", database="postgres", user="postgres", password="0000")
    
    # 將資料寫入資料庫
    model_sql.get_build_model(json_string=user_input)

    return jsonify({"status": "success"}), 200
    


@app.route("/api/user/show/pretrain_model", methods=["POST"])
def show_pretrain_model():

    # 使用資料庫格式並連線
    model_sql = TrainingDataDB(host="127.0.0.1", database="postgres", user="postgres", password="0000")
    
    # 從資料庫讀取已訓練的模型資料
    pretrain_model_content = model_sql.get_page_data()

    return pretrain_model_content
 

    
@app.route("/api/user/use/pretrain_model/img", methods=["POST"])
def use_pretrain_model_img():
    # 取得使用者點擊的 model_id
    user_select = request.get_json()

    # model回測
    model = StockPrediction()
    jpg_path = model.pre(user_select['model_id'],
                            user_select['stock_code'],
                            user_select['start_time'],
                            user_select['end_time'],
                            user_select['data_clean']
                            )

    # 要回傳資料庫的json
    result_json = {
        "model_id": user_select['model_id'],
        "img_path": jpg_path
    }

    # dict 轉 json
    result_json = json.dumps(result_json)

    print(result_json)
    
    # 使用資料庫格式並連線
    result_sql = ResultDB(host="127.0.0.1", database="postgres", user="postgres", password="0000")
    
    # 將圖片路徑寫入資料庫
    result_sql.set_result_table(result_json)

    return jsonify(jpg_path)

    
@app.route("/api/user/use/pretrain_model/price", methods=["POST"])
def use_pretrain_model_price():
    try:
        # 取得使用者點擊的 model_id
        user_select = request.get_json()

        # model回測
        model = StockPrediction()
        tomorrow_price = model.pre1(user_select['model_id'],
                                    user_select['stock_code'],
                                    user_select['data_clean']
                                    )

        # 要回傳資料庫的json
        result_json = {
           "model_id": user_select['model_id'],
           "tomorrow_price": tomorrow_price
        }

        # dict 轉 json
        result_json = json.dumps(result_json)

        print(result_json)
        
        # 使用資料庫格式並連線
        result_sql = ResultDB(host="127.0.0.1", database="postgres", user="postgres", password="0000")
        
        # 將圖片路徑寫入資料庫
        result_sql.set_result_table_price(result_json)

        return jsonify(tomorrow_price)

    except Exception as e:
        print(e)
        return jsonify({'message': 'Invalid JSON data.'}) 


if __name__ == '__main__':
    app.run()