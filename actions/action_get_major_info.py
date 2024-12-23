import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webChat.settings')
import django
django.setup()

from myApp.models import NganhTuyenSinh
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher  
from asgiref.sync import sync_to_async

class ActionGetMajorInfo(Action):
    def name(self) -> Text:
        return "action_get_major_info"

    @sync_to_async
    def get_major_info_from_db(self, ma_nganh: str):
        # This will be run in a separate thread to avoid blocking the async event loop
        try:
            nganh = NganhTuyenSinh.objects.get(ma_nganh__iexact=ma_nganh.lower())
            return nganh.ten_nganh, nganh.mo_ta
        except NganhTuyenSinh.DoesNotExist:
            return None, None

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Debugging line to check if entity is recognized
        entities = tracker.latest_message['entities']
        print("Extracted entities:", entities)

        # Lấy entity 'ma_nganh' từ câu hỏi của người dùng
        ma_nganh = next(tracker.get_latest_entity_values("ma_nganh"), None)
        
        if ma_nganh:
            # Fetch major information asynchronously
            ten_nganh, mo_ta = await self.get_major_info_from_db(ma_nganh)
            
            if ten_nganh:
                mo_ta = mo_ta if mo_ta else "không có mô tả"
                # Gửi phản hồi về thông tin ngành
                dispatcher.utter_message(
                    text=f"Ngành {ma_nganh} là {ten_nganh}. Mô tả: {mo_ta}."
                )
            else:
                # Gọi utterance khi không tìm thấy ngành
                dispatcher.utter_message(response="utter_no_major_info")
        else:
            dispatcher.utter_message(text="Vui lòng cung cấp mã ngành cần tìm.")

        return []
