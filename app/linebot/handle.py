# app/linebot/handle.py

from linebot.models import TextSendMessage
import requests
import re

from app.linebot.reply_utils import make_parking_flex_message



def handle_text_message(event, line_bot_api):
    text = event.message.text.strip()

    # 提供預測資料屬性
    if text == "預測":
        try:
            resp = requests.get("http://localhost:5000/predict/list")
            parking_names = resp.json().get("parking_lots", [])
            if not parking_names:
                reply = TextSendMessage(text="目前沒有可預測的停車場資料")
            else:
                formatted = "\n".join([f"{p['carpark_id']} - {p['carpark_name']}" for p in parking_names])
                reply = TextSendMessage(text=f"📊 可預測停車場：\n{formatted}")
        except Exception as e:
            reply = TextSendMessage(text=f"無法取得預測列表：{str(e)}")
        line_bot_api.reply_message(event.reply_token, reply)
        return
    
    # 預測模型回傳 [名稱or代碼 yyyy-mm-dd HH:MM]
    pattern = r"^(\d{3})\s*-\s*.+?\s+(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2})$"
    match = re.match(pattern, text)
    if match:
        carpark_id, date_part, time_part = match.groups()
        datetime_str = f"{date_part} {time_part}"

        try:
            predict_resp = requests.get("http://localhost:5000/predict/predict", params={
                "carpark_id": carpark_id,
                "date": datetime_str
            })
            result = predict_resp.json()

            if "predicted_availability" in result:
                name = result.get("carpark_name", carpark_id)
                avail = result["predicted_availability"]
                reply = TextSendMessage(
                    text=f"⏰ {datetime_str}\n📍 {name}\n🅿️ 預測可用車位：{avail} 格"
                )
            else:
                reply = TextSendMessage(text=result.get("error", "預測失敗"))

        except Exception as e:
            reply = TextSendMessage(text=f"預測時發生錯誤：{str(e)}")

        line_bot_api.reply_message(event.reply_token, reply)
        return
    
    # 嘗試解析格式：「起點 到 終點」
    if "到" not in text:
        reply = TextSendMessage(text="請使用『起點 到 終點』的格式，例如：台大 到 台北101")
        line_bot_api.reply_message(event.reply_token, reply)
        return

    start, end = [x.strip() for x in text.split("到", 1)]

    # 查詢 geocode（起點與終點經緯度）
    try:
        start_resp = requests.get("http://localhost:5000/maps/geocode", params={"place": start})
        end_resp = requests.get("http://localhost:5000/maps/geocode", params={"place": end})
        start_data = start_resp.json()
        end_data = end_resp.json()

        if "lat" not in end_data or "lat" not in start_data:
            raise Exception("查無起點或終點座標")

        # 拿終點附近停車場資訊（此處用終點經緯度）
        parking_resp = requests.get("http://localhost:5000/tdx/parking", params={
            "lat": end_data["lat"],
            "lon": end_data["lon"]
        })

        parking_list = parking_resp.json().get("parking_lots", [])

        if not parking_list:
            reply = TextSendMessage(text="找不到附近的停車場 🅿️")
        else:
            reply = make_parking_flex_message(parking_list)

    except Exception as e:
        reply = TextSendMessage(text=f"發生錯誤：{str(e)}")
    
    line_bot_api.reply_message(event.reply_token, reply)

def handle_location_message(event, line_bot_api):
    lat = event.message.latitude
    lon = event.message.longitude
    # TODO: 用經緯度查附近停車場、做導航
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f"收到你的位置：{lat}, {lon}")
    )