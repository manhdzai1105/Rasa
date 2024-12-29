import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webChat.settings')
import django
django.setup()

from myApp.models import Question  # Import model Question
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher  
from asgiref.sync import sync_to_async

class ActionFetchQuestion(Action):
    def name(self) -> Text:
        return "action_ask_question"

    @sync_to_async
    def get_random_question_from_db(self):
        # Lấy ngẫu nhiên một câu hỏi từ cơ sở dữ liệu
        try:
            question = Question.objects.order_by('?').first()
            return question
        except Exception as e:
            return None

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Lấy các entities từ câu hỏi
        entities = tracker.latest_message['entities']  # Lấy các entities từ câu hỏi

        # Kiểm tra nếu có entity 'question'
        question_entity = next((entity for entity in entities if entity['entity'] == 'question'), None)
        
        if question_entity:
            question_value = question_entity['value']  # Lấy giá trị của entity 'question'

            # Kiểm tra nếu giá trị của entity 'question' là 'câu hỏi'
            if question_value == 'câu hỏi':
                # Đặt câu hỏi khi giá trị của entity là 'câu hỏi'
                dispatcher.utter_message(text="Đây là câu hỏi của tôi dành cho bạn.")
                
                # Lấy câu hỏi ngẫu nhiên từ cơ sở dữ liệu
                try:
                    question = await self.get_random_question_from_db()
                    if question:
                        dispatcher.utter_message(
                            text=f"{question.question_text}\n"
                                 f"{question.option_a}\n"
                                 f"{question.option_b}\n"
                                 f"{question.option_c}"
                        )
                        return [{"event": "slot", "name": "correct_answer", "value": question.correct_answer}]
                    else:
                        dispatcher.utter_message(text="Hiện tại không có câu hỏi nào trong cơ sở dữ liệu.")
                except Exception as e:
                    dispatcher.utter_message(response="utter_default")
            else:
                # Nếu không phải là 'câu hỏi', không làm gì hoặc đưa ra thông báo
                dispatcher.utter_message(text="Entity 'question' không phải là 'câu hỏi'.")
        else:
            dispatcher.utter_message(response="utter_default")

        return []  # Trả về danh sách rỗng nếu không có entity 'question'
