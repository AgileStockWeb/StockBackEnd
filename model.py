from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from xgboost import XGBRegressor
import yahoo_fin.stock_info as si
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, timedelta

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
        self.Y=self.stock_data['close'].pct_change().shift(-1).dropna()
        self.stock_data=self.stock_data[:-1]
    def choose_normalization(self, method):
        if method == 'standard':
            self.scaler = StandardScaler()
            self.stock_data = self.scaler.fit_transform(self.stock_data)
        elif method == 'min_max':
            self.scaler = MinMaxScaler()
            self.stock_data = self.scaler.fit_transform(self.stock_data)
        else:
            print('沒有做標準化')

    def choose_model(self, model_type):
        if model_type == 'XGB':
            self.model = XGBRegressor()
        elif model_type == 'SVR':
            self.model = SVR(C=0.001,epsilon=0.1,gamma=10,kernel= 'linear')
        elif model_type == 'LM':
            self.model = LinearRegression()
    def train_model(self,i):
        self.model.fit(self.stock_data, self.Y)
        # 假设clf是一个训练好的SVM模型
        joblib.dump(self.model, 'model/'+i+'.pkl')
        return 'model/'+i+'.pkl'
    def pre(self,i, stock_code, stdate,endate,method):
        self.stock_data=adj_value(si.get_data(stock_code+'.TW',  stdate,endate).drop(['ticker'],axis=1).dropna())
        if method == 'standard':
            scaler = StandardScaler()
            pre_data = scaler.fit_transform(self.stock_data)
        elif method == 'min_max':
            scaler = MinMaxScaler()
            pre_data = scaler.fit_transform(self.stock_data)
        else:
            print('沒有標準化')
        model = joblib.load('model/'+i+'.pkl')
        pre = model.predict(pre_data)
        pre=pd.DataFrame(pre)
        pre.index = self.stock_data.index
        pre['pre']=self.stock_data['close']*(1+pre[0])
        pre['pre']=pre['pre'].shift(1)
        pre['trec']=self.stock_data['close']
        pre=pre.drop([0],axis=1).dropna()  
        if len(pre.index)>4:

            custom_ticks = [pre.index[0],pre.index[round(len(pre.index)/4)], 
            pre.index[round(len(pre.index)*2/4)], pre.index[round(len(pre.index)*3/4)]
            , pre.index[round(len(pre.index)*4/4)-1]]
            custom_labels = [str(pre.index[0])[:10],str(pre.index[round(len(pre.index)/4)])[:10]
            , str(pre.index[round(len(pre.index)*2/4)])[:10], str(pre.index[round(len(pre.index)*3/4)])[:10], str(pre.index[round(len(pre.index)*4/4)-1])[:10]]
        else:
            custom_ticks = pre.index
            custom_labels = [str(item)[:10] for item in pre.index]
            
        plt.ylim(min(pre.min())-1,max(pre.max()+1))
        plt.xticks(custom_ticks, custom_labels)
        plt.plot(pre.index, pre['pre'], marker='.', markersize=3, mec='r', mfc='w',label=u'predict')
        plt.plot(pre.index, pre['trec'], marker='.', markersize=3,label=u'True')
        plt.legend() 
        plt.margins(0)
        plt.subplots_adjust(bottom=0.15)
        plt.savefig('jpg/'+i+'.jpg')
        return 'jpg/'+i+'.jpg'

    def pre1(self,i, stock_code,method):
        self.stock_data=adj_value(si.get_data(stock_code+'.TW',  (date.today()- timedelta(days=30))).drop(['ticker'],axis=1).dropna())
        if method == 'standard':
            scaler = StandardScaler()
            pre_data = scaler.fit_transform(self.stock_data)
        elif method == 'min_max':
            scaler = MinMaxScaler()
            pre_data = scaler.fit_transform(self.stock_data)
        else:
            print('沒有標準化')
        model = joblib.load('model/'+i+'.pkl')
        pre = model.predict(pre_data)
        pre=pd.DataFrame(pre)
        pre.index = self.stock_data.index
        pre['pre']=self.stock_data['close']*(1+pre[0])
        return pre['pre'][-1:].values[0]
        
