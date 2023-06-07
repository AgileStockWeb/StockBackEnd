# StockBackEnd
## Require 
- Python 3.7
- Postgresql

## Quick setup Flask
Install python venv and python3.7
```bash
sudo apt install python3.7 python3-venv python3.7-venv
```
Use venv
```bash
python3.7 -m venv py37-venv
```
Into venv
```bash
source py37-venv/bin/activate
```
Install Flask and requirement.txt
```bash
pip3 install -r requirements.txt
```
Run
```bash
flask run
```
Exit venv
```bash
deactivate
```
## Quick Setup Postgresql
DataBase前置安裝
```
安裝POSTGRE:https://www.enterprisedb.com/downloads/postgres-postgresql-downloads   最上面那個15.3版  安裝時密碼預設0000
PY安裝資料庫操作相關套件: pip install psycopg2
```
DataBase建立:

開啟pgadmin4， 並建立DataBase

![image](https://github.com/AgileStockWeb/StockBackEnd/assets/57141904/6a89d772-1b98-46fd-ad1b-ea63111f9dca)

輸入stock_website_database，並點擊SAVE
![image](https://github.com/AgileStockWeb/StockBackEnd/assets/57141904/c9a308c4-a323-4231-a34e-c076d2e124d8)

再來建立TABEL，點擊進入Query Tool

![image](https://github.com/AgileStockWeb/StockBackEnd/assets/57141904/856414a3-69d4-4957-b7ab-e0395245b68d)

輸入SQL指令建，並按送出

![image](https://github.com/AgileStockWeb/StockBackEnd/assets/57141904/ccc1ff95-4198-4467-bb09-d9083ed5c852)


```
TABEL1指令:
CREATE TABLE model_table (model_id TEXT PRIMARY KEY NOT NULL,
						model_name TEXT NOT NULL,
						data_clean TEXT NOT NULL,
					 	start_time TIMESTAMP NOT NULL,
						end_time TIMESTAMP NOT NULL,
						stock_code TEXT NOT NULL,
						technical_indicator TEXT NOT NULL,
						model_path TEXT,
						CONSTRAINT start_end_check CHECK (start_time < end_time));
 
 TABEL2指令:
CREATE TABLE result_table (result_id SERIAL PRIMARY KEY NOT NULL,
             			       jpg_path TEXT,
				       tomorrow_price  float,
               			     model_id TEXT REFERENCES model_table (model_id));
```
有TABLE了

![image](https://github.com/AgileStockWeb/StockBackEnd/assets/57141904/2e7e80ca-48d8-4d48-8a99-4f13a4b65bc2)

最後如何查看資料

如圖所示:

![image](https://github.com/AgileStockWeb/StockBackEnd/assets/57141904/ccd5cf4a-ac52-49c7-b1ce-43ccfc071b87)
