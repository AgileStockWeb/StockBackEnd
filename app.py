from flask import Flask, request, jsonify
import requests
import uuid

app = Flask(__name__)

@app.route("/api/user/input", methods=["POST"])
def user_input():
    try:
        user_input = request.get_json()

        # 在 user_input 中加入唯一的 UUID
        user_input['uuid'] = str(uuid.uuid4())

        # 送要訓練的資料給 db
        database_api_url = 'database URL'  # 替換為資料庫URL
        database_response = requests.post(database_api_url, json=user_input)

        if database_response.status_code == 200:
            # 送要訓練的資料給 model
            model_api_url = 'model URL'  # 替換為model URL
            model_response = requests.post(model_api_url, json=user_input)

            # 根據另一個 API 的回應進行處理
            if model_response.status_code == 200:
                return jsonify({'message': 'success'})
            else:
                return jsonify({'message': 'Error in send user-input to db.'})
        else:
            return jsonify({'message': 'Error in send user-input to database.'})

    except Exception as e:
        print(e)
        return jsonify({'message': 'Invalid JSON data.'})

@app.route("/api/uaer/training_model", methods=["POST"])
def model_output():
    try:
        model_output = request.get_json()
        # 送訓練好的資料回 db
        database_api_url = 'database URL'  # 替換為資料庫URL
        database_response = requests.post(database_api_url, json=model_output)

        if database_response.status_code == 200:
            return jsonify({'message': 'success'})
        else:
            return jsonify({'message': 'Error in send model-output to db.'})
        
    except Exception as e:
        print(e)
        return jsonify({'message': 'Invalid JSON data.'})

@app.route("/api/user/pretrain_model", methods=["POST"])
def user_pretrain_model():
    try:
        database_api_url = 'database URL'  # 替換為資料庫URL
        response = requests.get(database_api_url)

        if response.status_code == 200:
            database_content = response.json()
            return jsonify(database_content)
        else:
            return jsonify({'message': 'Error in request db to UI.'})
        
    except Exception as e:
        print(e)
        return jsonify({'message': 'Invalid JSON data.'})


if __name__ == '__main__':
    app.run()