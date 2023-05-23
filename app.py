from flask import Flask
from flask_graphql import GraphQLView
import graphene

# 定義可接受的模型類型
class ModelType(graphene.Enum):
    XGB = "XGB"
    LSTM = "LSTM"
    SVR = "SVR"

class ClearType(graphene.Enum):
    REMOVE_NAN = "remove_nan"
    STANDARDIZE = "Standardize"
    MIN_MAX_SCALER = "MinMaxScaler"
    NORMALIZE = "Normalize"

# 建立一個GraphQL Schema
class Query(graphene.ObjectType):
    user_input = graphene.String(
        time=graphene.String(required=True),
        stock_code=graphene.Int(required=True),
        model_type=graphene.Argument(ModelType, required=True, default_value=[ModelType.XGB]),
        clear_type=graphene.List(ClearType, default_value=[ClearType.REMOVE_NAN])
    )

    def resolve_userinput(self, info, time, stock_code, model_type, clear_type):
        # 在這裡可以對使用者輸入進行處理
        return f"Time: {time}, Stock Code: {stock_code}, Model Type: {model_type}, Clear Type: {clear_type}"

schema = graphene.Schema(query=Query)

app = Flask(__name__)

# 設定GraphQL路由
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == '__main__':
    app.run()
