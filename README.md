# Parking_Info
> MVP 停車資訊導引系統

## 🔄 專案流程

1. **手機輸入目的地**
2. **Maps API**：將地址轉換為經緯度  
3. **TDX API**：查詢附近停車場剩餘車位與費率資訊  
4. **系統回應**：根據經緯度提供符合條件的停車場  
5. **使用者選擇**：根據剩餘車位或費率做決策  
6. **Maps API**：引導使用者至選定的停車場  

---

## 安裝

### clone 本專案（包含資料來源）

```bash
git clone --recurse-submodules https://github.com/ITS-parking/project.git
cd project
```
若已經 clone 完但未初始化 submodule，可執行：
```bash
git submodule update --init --recursive
```
✅ 安裝依賴
```bash
pip install -r requirements.txt
```
🚀 啟動伺服器：
```
python run.py
```
Swagger UI 文件可於下列位置查看：

http://127.0.0.1:5000/apidocs/

## 功能

### 支援停車場地點

包含以下地區之室內外停車場

| 中文地區名稱    | 英文代碼           |
| --------- | -------------- |
| 臺北市 / 台北市 | Taipei         |
| 桃園市       | Taoyuan        |
| 臺中市 / 台中市 | Taichung       |
| 臺南市 / 台南市 | Tainan         |
| 高雄市       | Kaohsiung      |
| 基隆市       | Keelung        |
| 彰化縣       | ChanghuaCounty |
| 雲林縣       | YunlinCounty   |
| 屏東縣       | PingtungCounty |
| 宜蘭縣       | YilanCounty    |
| 花蓮縣       | HualienCounty  |
| 金門縣       | KinmenCounty   |

### 以下停車場提供預測資料

停車場代碼對照表

| 停車場代碼 | 停車場名稱                     |
|------------|------------------------------|
| 001        | 府前廣場地下停車場            |
| 002        | 松壽廣場地下停車場            |
| 003        | 臺北市災害應變中心地下停車場  |
| 005        | 立農公園地下停車場            |
| 007        | 萬華國中地下停車場            |
| 014        | 興雅國中地下停車場            |
| 018        | 洛陽綜合立體停車場            |
| 028        | 松山高中地下停車場            |
| 030        | 大稻埕公園地下停車場          |

## 🌐 API 來源

- OpenStreetMap - 經緯轉換

- [TDX API](https://tdx.transportdata.tw/api-service/swagger/basic/#/CityCarPark/ParkingApi%20ParkingCityAvailability) - 交通部運輸資料平台：查詢即時停車資訊

- linebot - 使用者介面
