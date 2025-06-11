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

## 📥 Installation

### ✅ 使用 submodule clone 本專案（包含資料來源）

```bash
git clone --recurse-submodules https://github.com/your-user/Parking_Info.git
cd Parking_Info
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

🌐 API 來源

- OpenStreetMap：經緯轉換

- [TDX API](https://tdx.transportdata.tw/api-service/swagger/basic/#/CityCarPark/ParkingApi%20ParkingCityAvailability) - 交通部運輸資料平台：查詢即時停車資訊

