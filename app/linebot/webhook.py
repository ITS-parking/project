# app/linebot/webhook.py

from flask import Blueprint, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, LocationMessage

from app.linebot.handle import handle_text_message, handle_location_message

import os

linebot_bp = Blueprint('linebot', __name__)

# 載入你的 LINE Channel Access Token 與 Secret（建議用 .env 管理）
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@linebot_bp.route("/callback", methods=["POST"])
def callback():
    # 簽章驗證
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK", 200

# 訊息處理邏輯
@handler.add(MessageEvent, message=TextMessage)
def handle_text(event):
    handle_text_message(event, line_bot_api)

@handler.add(MessageEvent, message=LocationMessage)
def handle_location(event):
    handle_location_message(event, line_bot_api)