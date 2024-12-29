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

class ActionGetWordMeaning(Action):
    def name(self) -> Text:
        return "action_get_word_meaning"  # Tên action của bạn

    @sync_to_async
    def get_word_meaning_from_db(self, word_name: str) -> str:
        """Hàm này lấy nghĩa của từ từ cơ sở dữ liệu"""
        try:
            word = Word.objects.get(name__iexact=word_name)  # Tìm từ theo tên (không phân biệt chữ hoa/thường)
            return word.meaning  # Trả về nghĩa của từ
        except Word.DoesNotExist:
            return None  # Nếu không tìm thấy từ, trả về None

    def extract_word_from_question(self, question: str) -> str:
        """Trích xuất từ từ câu hỏi nếu slot không được điền"""
        
        # Tìm từ sau "Từ" trong câu hỏi, ví dụ: "Từ Peach có nghĩa là gì?"
        match = re.search(r"Từ (\w+)", question, re.IGNORECASE)
        if match:
            return match.group(1).strip()

        # Tìm từ trong câu có "có nghĩa là" hoặc "giải thích" (các câu hỏi kiểu khác)
        match = re.search(r"(?:có nghĩa là|giải thích từ)\s([^\s]+)", question, re.IGNORECASE)
        if match:
            return match.group(1).strip()

        return None  # Nếu không tìm thấy từ trong câu, trả về None

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Trước tiên, lấy giá trị của từ trong entities (nếu có)
        word_name = None
        for entity in tracker.latest_message['entities']:
            if entity['entity'] == 'word':  # Tìm entity 'word' trong câu
                word_name = entity['value']
                break

        if not word_name:
            # Nếu không có từ trong entities, trích xuất từ từ câu hỏi của người dùng
            question = tracker.latest_message.get("text", "")
            word_name = self.extract_word_from_question(question)

        if word_name:
            # Nếu đã có từ (từ trong entities hoặc trích xuất từ câu hỏi), lấy nghĩa từ cơ sở dữ liệu
            meaning = await self.get_word_meaning_from_db(word_name)

            if meaning:
                dispatcher.utter_message(
                    text=f"Nghĩa của từ {word_name}: {meaning}."
                )
            else:
                dispatcher.utter_message(response="utter_default")
        else:
            # Nếu không tìm thấy từ trong câu hỏi và entities, yêu cầu người dùng nhập lại
            dispatcher.utter_message(
                response="utter_default"
            )

        return []  # Trả về danh sách rỗng
