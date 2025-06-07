# app/linebot/reply_utils.py

from linebot.models import FlexSendMessage

def make_parking_flex_message(parking_list):
    """
    將停車場資料列表轉換成 Flex Message
    每個停車場一個 bubble，最多顯示前三個
    """
    bubbles = []

    for park in parking_list[:3]:
        name = park.get("name", "無名停車場")
        spaces = park.get("available_spaces", "未知")
        lat = park.get("lat")
        lon = park.get("lon")

        maps_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"

        bubble = {
            "type": "bubble",
            "size": "micro",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "text",
                        "text": name,
                        "weight": "bold",
                        "size": "md",
                        "wrap": True
                    },
                    {
                        "type": "text",
                        "text": f"剩餘車位：{spaces}",
                        "size": "sm",
                        "color": "#888888"
                    },
                    {
                        "type": "button",
                        "style": "link",
                        "height": "sm",
                        "action": {
                            "type": "uri",
                            "label": "導航",
                            "uri": maps_url
                        }
                    }
                ]
            }
        }

        bubbles.append(bubble)

    flex_message = {
        "type": "carousel",
        "contents": bubbles
    }

    return FlexSendMessage(alt_text="停車場查詢結果", contents=flex_message)