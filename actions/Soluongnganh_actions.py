from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
import requests

class ActionSoLuongNganh(Action):
    def name(self) -> str:
        return "action_so_luong_nganh"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain):
        url = "http://127.0.0.1:8000/api/so-luong-nganh/"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            so_luong_nganh = data.get("so_luong_nganh")
            dispatcher.utter_message(f"Trường tuyển sinh {so_luong_nganh} ngành.")
        else:
            dispatcher.utter_message("Xin lỗi, tôi không thể lấy thông tin hiện tại.")
        return []