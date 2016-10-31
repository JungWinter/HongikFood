from keyboard import Keyboard


class Message:
    #  Message클래스를 생성할 때 기본적인 틀만 구현하고
    #  값들은 던져주면 알아서 메시지를 리턴한다

    baseKeyboard = {
        "type": "buttons",
        "buttons": Keyboard.buttons,
    }

    baseMessage = {
        "message": {
            "text": "",
        },
        "keyboard": baseKeyboard
    }
    # Uesage : baseMessage["message"].update(baseWeekend)
    baseWeekend = {
        "message_button": {
            "label": "이번주 메뉴 보기",
            "url": "http://apps.hongik.ac.kr/food/food.php"
        }
    }

    def __init__(self):
        self.returnedMessage = None

    def getMessage(self):
        return self.returnedMessage


class HomeMessage(Message):
    def __init__(self):
        self.returnedMessage = Message.baseKeyboard
        homeKeyboard = Keyboard.homeButtons
        self.returnedMessage["buttons"] = homeKeyboard


class FailMessage(Message):
    def __init__(self):
        self.returnedMessage = Message.baseMessage
        message = "오류가 발생하였습니다."
        keyboard = Message.baseKeyboard
        keyboard["buttons"] = Keyboard.homeButtons
        self.returnedMessage["message"]["text"] = message
        self.returnedMessage["keyboard"] = keyboard
