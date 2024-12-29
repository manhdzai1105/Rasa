import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webChat.settings')
import django
django.setup()

from myApp.models import Tense  # Import model Tense
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher  
from asgiref.sync import sync_to_async

class ActionGetDefineTense(Action):
    def name(self) -> Text:
        return "action_get_define_tense"

    @sync_to_async
    def get_tense_definition_from_db(self, tense_name: str):
        # Truy vấn cơ sở dữ liệu để lấy định nghĩa của thì theo tên
        try:
            tense = Tense.objects.get(name__iexact=tense_name.lower())
            return tense.define
        except Tense.DoesNotExist:
            return None

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Lấy entity 'tense' từ câu hỏi của người dùng
        entities = tracker.latest_message['entities']
        tense_name = next(tracker.get_latest_entity_values("define_tense"), None)

        if tense_name:
            # Fetch định nghĩa của thì từ cơ sở dữ liệu một cách bất đồng bộ
            tense_definition = await self.get_tense_definition_from_db(tense_name)
            
            if tense_definition:
                # Gửi phản hồi về định nghĩa của thì
                dispatcher.utter_message(
                    text=f"Định nghĩa của thì {tense_name} là: {tense_definition}."
                )
            else:
                # Gọi utterance khi không tìm thấy định nghĩa của thì
                dispatcher.utter_message(response="utter_default")
        else:
            dispatcher.utter_message(response="utter_default")

        return []
