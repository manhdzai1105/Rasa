from rasa_sdk import Action
from rasa_sdk.events import UserUttered
from rasa_sdk.executor import CollectingDispatcher

class ActionDefaultFallback(Action):
    def name(self) -> str:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain) -> list:
        dispatcher.utter_message(text="I'm sorry, I didn't quite get that. Could you please rephrase?")
        return []
