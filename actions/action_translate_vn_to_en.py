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

class ActionTranslateVnToEn(Action):
    def name(self) -> Text:
        return "action_translate_vn_to_en"  # Tên action của bạn

    @sync_to_async
    def get_word_meaning_from_db(self, word_name: str) -> str:
        """Hàm này lấy nghĩa của từ tiếng Việt từ cơ sở dữ liệu"""
        try:
            word = Word.objects.get(meaning__iexact=word_name.lower())  # Tìm từ theo nghĩa (không phân biệt chữ hoa/thường)
            return word.name  # Trả về từ tiếng Anh
        except Word.DoesNotExist:
            return None  # Nếu không tìm thấy từ, trả về None

    def extract_word_from_question(self, question: str) -> str:
        """Trích xuất từ từ câu hỏi nếu slot không được điền"""
        
        # Cập nhật biểu thức chính quy để tìm các mẫu câu hỏi khác nhau
        match = re.search(r"(.*?)\s(dịch sang tiếng Anh là gì|được viết là gì trong tiếng Anh|trong tiếng Anh gọi là gì|trong tiếng Anh là gì|gọi là gì trong tiếng anh|là gì trong tiếng anh)", question, re.IGNORECASE)
        
        if match:
            # Trả về từ trước phần "có nghĩa là gì trong tiếng anh" hoặc các phần tương tự
            return match.group(1).strip() 
        
        return None

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Trước tiên, lấy giá trị của từ trong entities (nếu có)
        word_name = None
        for entity in tracker.latest_message['entities']:
            if entity['entity'] == 'wordvn':  # Tìm entity 'wordvn' trong câu
                word_name = entity['value']
                break

        if word_name:
            # Nếu đã có từ (từ trong entities), lấy nghĩa từ cơ sở dữ liệu
            english_word = await self.get_word_meaning_from_db(word_name)

            if english_word:
                dispatcher.utter_message(
                    text=f"'{word_name}' trong tiếng Anh là: {english_word}."
                )
            else:
                dispatcher.utter_message(response="utter_no_word_translate")  # Thông báo không tìm thấy nghĩa
        else:
            # Nếu không tìm thấy từ trong entities, trích xuất từ từ câu hỏi
            word_name = self.extract_word_from_question(tracker.latest_message['text'])

            if word_name:
                # Nếu trích xuất được từ, lấy nghĩa từ cơ sở dữ liệu
                english_word = await self.get_word_meaning_from_db(word_name)

                if english_word:
                    dispatcher.utter_message(
                        text=f"'{word_name}' trong tiếng Anh là: {english_word}."
                    )
                else:
                    dispatcher.utter_message(response="utter_default")  # Thông báo không tìm thấy nghĩa
            else:
                dispatcher.utter_message(response="utter_default")  # Yêu cầu người dùng nhập lại từ

        return []  # Trả về danh sách rỗng
