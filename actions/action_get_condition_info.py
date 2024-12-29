import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webChat.settings')
import django
django.setup()

from myApp.models import CauDieuKien
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher  
from asgiref.sync import sync_to_async

class ActionGetConditionInfo(Action):
    def name(self) -> Text:
        return "action_get_condition_info"

    @sync_to_async
    def get_condition_info_from_db(self, condition_name: str):
        # This will be run in a separate thread to avoid blocking the async event loop
        try:
            # Use the condition_name with case insensitivity
            condition = CauDieuKien.objects.get(name__iexact=condition_name.lower())
            return condition.description
        except CauDieuKien.DoesNotExist:
            return None

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Debugging line to check if entity is recognized
        entities = tracker.latest_message['entities']
        print("Extracted entities:", entities)

        # Ensure we are extracting the correct entity from the user input
        condition_name = next(tracker.get_latest_entity_values("name"), None)

        if condition_name:
            # Fetch condition information asynchronously
            description = await self.get_condition_info_from_db(condition_name)
            
            if description:
                # Gửi phản hồi về mô tả câu điều kiện
                dispatcher.utter_message(
                    text=f"Thông tin về {condition_name}: {description}."
                )
            else:
                # Gọi utterance khi không tìm thấy câu điều kiện
                dispatcher.utter_message(response="utter_default")
        else:
            dispatcher.utter_message(response="utter_default")

        return []
