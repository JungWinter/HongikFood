from .keyboard import Keyboard


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


class BaseMessage(Message):
    def __init__(self):
        super().__init__()
        self.returnedMessage = Message.baseMessage

    def updateMessage(self, message):
        self.returnedMessage["message"]["text"] = message

    def updateKeyboard(self, argKeyboard):
        keyboard = Message.baseKeyboard
        keyboard["buttons"] = argKeyboard
        self.returnedMessage["keyboard"] = keyboard


class SummaryMessage(BaseMessage):
    def __init__(self, message, isToday):
        super().__init__()
        self.updateMessage(message)
        if isToday:
            self.updateKeyboard(Keyboard.todayButtons)
        else:
            self.updateKeyboard(Keyboard.tomorrowButtons)


class HomeMessage(Message):
    def __init__(self):
        self.returnedMessage = Message.baseKeyboard
        homeKeyboard = HomeMessage.returnHomeKeyboard()
        self.returnedMessage["buttons"] = homeKeyboard

    @staticmethod
    def returnHomeKeyboard(self):
        return Keyboard.homeButtons


class FailMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        self.updateMessage("오류가 발생하였습니다.")
        self.updateKeyboard(Keyboard.homeButtons)


class SuccessMessage(Message):
    def __init__(self):
        self.returnedMessage = "SUCCESS"
