import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webChat.settings')
import django
django.setup()

from myApp.models import CauDieuKien
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from asgiref.sync import sync_to_async

class ActionGetConditionTheUse(Action):
    def name(self) -> Text:
        return "action_get_condition_theuse"

    @sync_to_async
    def get_condition_theuse_from_db(self, condition_name: str):
        # This will run in a separate thread to avoid blocking the async event loop
        try:
            # Truy vấn cơ sở dữ liệu để lấy thông tin về cách sử dụng của câu điều kiện
            condition = CauDieuKien.objects.get(name__iexact=condition_name.lower())
            return condition.theuse  # Trả về cách sử dụng của câu điều kiện
        except CauDieuKien.DoesNotExist:
            return None

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Lấy entity 'theuse' từ câu hỏi của người dùng
        entities = tracker.latest_message['entities']
        print("Extracted entities:", entities)

        # Trích xuất tên câu điều kiện từ entities
        condition_name = next(tracker.get_latest_entity_values("theuse"), None)

        if condition_name:
            # Truy vấn cơ sở dữ liệu để lấy thông tin về cách sử dụng của câu điều kiện
            theuse = await self.get_condition_theuse_from_db(condition_name)
            
            if theuse:
                # Gửi phản hồi về cách sử dụng của câu điều kiện
                dispatcher.utter_message(
                    text=f"Cách sử dụng của {condition_name}: {theuse}."
                )
            else:
                # Gọi utterance khi không tìm thấy thông tin
                dispatcher.utter_message(response="utter_default")
        else:
            dispatcher.utter_message(response="utter_default")

        return []
