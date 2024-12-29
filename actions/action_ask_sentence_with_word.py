import os
# Thiết lập môi trường Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webChat.settings')
import django
django.setup()

import re
from myApp.models import Word  # Import model Word
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from asgiref.sync import sync_to_async

class ActionGetSentenceWithWord(Action):
    def name(self) -> Text:
        return "action_ask_sentence_with_word"  # Tên action của bạn

    @sync_to_async
    def get_example_sentence_from_db(self, word_name: str) -> str:
        """Hàm này lấy câu ví dụ sử dụng từ từ cơ sở dữ liệu"""
        try:
            word = Word.objects.get(name__iexact=word_name)  # Tìm từ theo tên (không phân biệt chữ hoa/thường)
            return word.example_sentence  # Trả về câu ví dụ sử dụng từ
        except Word.DoesNotExist:
            return None  # Nếu không tìm thấy từ, trả về None

    def extract_word_from_question(self, question: str) -> str:
        """Trích xuất từ từ câu hỏi nếu slot không được điền"""
        
        # Cập nhật biểu thức chính quy để tìm các mẫu câu hỏi khác nhau
        match = re.search(r"(?:Đặt câu với từ|Làm ơn cho tôi một ví dụ với từ)\s([^\s]+)", question, re.IGNORECASE)
        
        if match:
            # Trả về từ mà người dùng yêu cầu, ví dụ: "con chó"
            return match.group(1).strip()  # Lấy từ ví dụ "con chó"

        return None  # Nếu không tìm thấy từ trong câu, trả về None


    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Trước tiên, lấy giá trị của từ trong entities (nếu có)
        word_name = None
        for entity in tracker.latest_message['entities']:
            if entity['entity'] == 'datcau':  # Tìm entity
                break

        if not word_name:
            # Nếu không có từ trong entities, trích xuất từ từ câu hỏi của người dùng
            question = tracker.latest_message.get("text", "")
            word_name = self.extract_word_from_question(question)

        if word_name:
            # Nếu đã có từ (từ trong entities hoặc trích xuất từ câu hỏi), lấy câu ví dụ từ cơ sở dữ liệu
            example_sentence = await self.get_example_sentence_from_db(word_name)

            if example_sentence:
                dispatcher.utter_message(
                    text=f"Ví dụ câu sử dụng từ {word_name}: {example_sentence}."
                )
            else:
                dispatcher.utter_message(response="utter_default")
        else:
            # Nếu không tìm thấy từ trong câu hỏi và entities, yêu cầu người dùng nhập lại
            dispatcher.utter_message(
                response="utter_default"
            )

        return []  # Trả về danh sách rỗng
