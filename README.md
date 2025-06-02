# Parking_Info
> MVP  

手機輸入目的地  
   │  
   ▼  
Maps API：將地址轉換為經緯度  
   │  
   ▼  
TDX API：查詢附近停車場剩餘車位與費率資訊  
   │  
   ▼  
系統回應：根據經緯度提供符合條件的停車場  
   │  
   ▼  
使用者選擇：根據剩餘車位或費率做決策  
   │  
   ▼  
Maps API：引導使用者至選定的停車場  
## installation
install dependency
```
pip install -r requirements.txt
```
## execute
compile project
```
python run.py
```
swagger ui
- http://127.0.0.1:5000/apidocs/


## API 

- OpenStreetMap

- [google maps API](https://console.cloud.google.com/google/maps-apis/credentials?project=stately-math-457706-e1)

- [TDX API](https://tdx.transportdata.tw/api-service/swagger/basic/#/CityCarPark/ParkingApi%20ParkingCityAvailability
)


