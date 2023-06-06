from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from xgboost import XGBRegressor
import yahoo_fin.stock_info as si
import joblib
import pandas as pd
import matplotlib.pyplot as plt
def adj_value(data):
    data['value']=data['close']/data['adjclose']
    data['open']=data['open']*data['value']
    data['high']=data['high']*data['value']
    data['low']=data['low']*data['value']
    data['close']=data['adjclose']
    return data.drop(['adjclose','value'],axis=1)




class StockPrediction:
    def __init__(self):
        self.stock_data = None
        self.scaler = None
        self.model = None

    def input_data(self, stock_code, stdate,endate):
        # 這裡應該實現一種方法來獲取股票數據
        # 假設你有一個函數叫做 get_stock_data 可以做到這一點
        try:
            self.stock_data = adj_value(si.get_data(stock_code+'.TW',  stdate,endate).drop(['ticker'],axis=1).dropna())
        except:
            self.stock_data = adj_value(si.get_data(stock_code+'.TWO',  stdate,endate).drop(['ticker'],axis=1).dropna())
        self.Y=self.stock_data['close'].pct_change()
        self.trandatax=self.stock_data.iloc[:int(len(self.stock_data)*0.8)][1:]
        self.testatax=self.stock_data.iloc[int(len(self.stock_data)*0.8):]
        self.trandatay=self.Y.iloc[:int(len(self.Y)*0.8)].dropna()
        self.testatay=self.Y.iloc[int(len(self.Y)*0.8):].dropna()
        
    def choose_normalization(self, method):
        if method == 'standard':
            self.scaler = StandardScaler()
        elif method == 'min_max':
            self.scaler = MinMaxScaler()
        else:
            raise ValueError("Unknown normalization method")
        
        self.trandatax = self.scaler.fit_transform(self.trandatax)
        self.testatax = self.scaler.fit_transform(self.testatax)
    def choose_model(self, model_type):
        if model_type == 'XGB':
            self.model = XGBRegressor()
        elif model_type == 'SVR':
            self.model = SVR()
        elif model_type == 'LM':
            self.model = LinearRegression()
        else:
            raise ValueError("Unknown model type")

    def train_model(self,i):
        # 這裡應該實現一種方法來訓練你的模型
        # 你需要先將數據分割成訓練集和測試集
        # 假設你有一個函數叫做 split_data 可以做到這一點
        self.model.fit(self.trandatax, self.trandatay)
        # 假设clf是一个训练好的SVM模型
        joblib.dump(self.model, 'model/'+i+'.pkl')
        return 'model/'+i+'.pkl'
    def estimate(self):    
        print(mean_squared_error(self.model.predict(self.testatax),self.testatay, squared=False))    
    def pre(self,i,method):
        if method == 'standard':
            scaler = StandardScaler()
        elif method == 'min_max':
            scaler = MinMaxScaler()
        else:
            raise ValueError("Unknown normalization method")
        model = joblib.load('model/'+i+'.pkl')
        pre_data = scaler.fit_transform(self.stock_data)
        pre = model.predict(pre_data)
        pre=pd.DataFrame(pre)
        pre.index = self.stock_data.index
        pre['pre']=self.stock_data['close']*(1+pre[0]).shift(1)
        
        pre['trec']=self.stock_data['close']
        pre=pre.drop([0],axis=1).dropna()
        
        plt.plot(pre.index, pre['pre'], mec='r', mfc='w',label=u'predict')
        plt.plot(pre.index, pre['trec'], ms=10,label=u'True')
        plt.legend()  # 讓圖例生效
        plt.margins(0)
        plt.subplots_adjust(bottom=0.15)
        plt.savefig('jpg/'+i+'.jpg')
        plt.show()
        return 'jpg/'+i+'.jpg'
