import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webChat.settings')
import django
django.setup()

from myApp.models import Tense  # Import model Tense
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher  
from asgiref.sync import sync_to_async

class ActionGetFormulaTense(Action):
    def name(self) -> Text:
        return "action_get_formula_tense"

    @sync_to_async
    def get_tense_formula_from_db(self, tense_name: str):
        # Query the database to get the formula of the tense by its name
        try:
            tense = Tense.objects.get(name__iexact=tense_name.lower())
            return tense.formula
        except Tense.DoesNotExist:
            return None

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the entity 'formula_tense' from the user's question
        tense_name = next(tracker.get_latest_entity_values("formula_tense"), None)

        if tense_name:
            # Fetch the tense formula from the database asynchronously
            tense_formula = await self.get_tense_formula_from_db(tense_name)

            if tense_formula:
                # Định dạng dữ liệu để hiển thị đẹp hơn
                formatted_response = (
                    f"✨ Công thức của **thì {tense_name.capitalize()}** là:\n"
                    f"{tense_formula}"
                )

                dispatcher.utter_message(text=formatted_response)


            else:
                # If no formula is found for the tense, return a response
                dispatcher.utter_message(response="utter_default")
        else:
            dispatcher.utter_message(response="utter_default")

        return []
