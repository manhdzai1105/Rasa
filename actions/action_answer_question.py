from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionCheckAnswer(Action):
    def name(self) -> Text:
        return "action_check_answer"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Lấy câu trả lời đúng từ slot
        correct_answer = tracker.get_slot("correct_answer")
        # Lấy entity 'answer' từ câu trả lời của người dùng
        user_answer = next(tracker.get_latest_entity_values("answer"), None)
        
        if correct_answer:
            if user_answer:
                if user_answer.upper() == correct_answer.upper():
                    dispatcher.utter_message(text="Chúc mừng! Bạn đã trả lời đúng. 🎉")
                else:
                    dispatcher.utter_message(text=f"Rất tiếc, đáp án đúng là {correct_answer}.")
            else:
                dispatcher.utter_message(text="Bạn chưa chọn đáp án. Vui lòng thử lại.")
        else:
            dispatcher.utter_message(response="utter_default")
        
        return [SlotSet("correct_answer", None)]
