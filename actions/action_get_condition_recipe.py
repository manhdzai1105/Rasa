import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webChat.settings')
import django
django.setup()

from myApp.models import CauDieuKien
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher  
from asgiref.sync import sync_to_async

class ActionGetConditionRecipe(Action):
    def name(self) -> Text:
        return "action_get_condition_recipe"

    @sync_to_async
    def get_condition_recipe_from_db(self, condition_name: str):
        # Truy vấn cơ sở dữ liệu để lấy công thức theo tên câu điều kiện
        try:
            condition = CauDieuKien.objects.get(name__iexact=condition_name.lower())
            return condition.recipe
        except CauDieuKien.DoesNotExist:
            return None

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Lấy entity 'recipe' từ câu hỏi của người dùng
        entities = tracker.latest_message['entities']
        print("Extracted entities:", entities)

        # Lấy entity 'name' (tên câu điều kiện) từ câu hỏi của người dùng
        condition_name = next(tracker.get_latest_entity_values("recipe"), None)

        if condition_name:
            # Fetch công thức của câu điều kiện từ cơ sở dữ liệu một cách bất đồng bộ
            recipe = await self.get_condition_recipe_from_db(condition_name)
            
            if recipe:
                # Gửi phản hồi về công thức câu điều kiện
                dispatcher.utter_message(
                    text=f"Công thức của {condition_name} là: {recipe}."
                )
            else:
                # Gọi utterance khi không tìm thấy công thức của câu điều kiện
                dispatcher.utter_message(response="utter_default")
        else:
            dispatcher.utter_message(response="utter_default")

        return []
