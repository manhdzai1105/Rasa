import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webChat.settings')
import django
django.setup()

from myApp.models import CauDieuKien
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from asgiref.sync import sync_to_async

class ActionGetConditionExample(Action):
    def name(self) -> Text:
        return "action_get_condition_example"

    @sync_to_async
    def get_condition_example_from_db(self, condition_name: str):
        # This will be run in a separate thread to avoid blocking the async event loop
        try:
            condition = CauDieuKien.objects.get(name__iexact=condition_name.lower())
            return condition.example
        except CauDieuKien.DoesNotExist:
            return None

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Debugging line to check if entity is recognized
        entities = tracker.latest_message['entities']
        print("Extracted entities:", entities)

        # Lấy entity 'example' từ câu hỏi của người dùng
        condition_name = next(tracker.get_latest_entity_values("example"), None)

        if condition_name:
            # Fetch example asynchronously
            example = await self.get_condition_example_from_db(condition_name)
            
            if example:
                # Gửi phản hồi về ví dụ câu điều kiện
                dispatcher.utter_message(
                    text=f"Ví dụ về {condition_name}: {example}."
                )
            else:
                # Gọi utterance khi không tìm thấy ví dụ
                dispatcher.utter_message(response="utter_default")
        else:
            dispatcher.utter_message(response="utter_default")

        return []
