from .keyboard import Keyboard
from json import loads, dumps


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
        self.returnedMessage = loads(dumps(Message.baseMessage))

    def updateMessage(self, message):
        self.returnedMessage["message"]["text"] = message

    def updateKeyboard(self, argKeyboard):
        keyboard = Message.baseKeyboard
        keyboard["buttons"] = argKeyboard
        self.returnedMessage["keyboard"] = keyboard

    def add_photo(self, url, width, height):
        photo_message = {
            "photo": {
                "url": "http://www.hongik.ac.kr/front/images/local/header_logo.png",
                "width": 198,
                "height": 45,
            },
        }
        photo_message["photo"]["url"] = url
        photo_message["photo"]["width"] = width
        photo_message["photo"]["height"] = height
        self.returnedMessage["message"].update(photo_message)


class EvaluateMessage(BaseMessage):
    def __init__(self, message, step):
        '''
        step 1 : 식단 평가하기 -> 장소
        step 2 : 장소 -> 시간대
        step 3 : 시간대 -> 점수
        step 4 : 점수 -> 끝
        '''
        super().__init__()
        self.updateMessage(message)
        if step == 1:
            self.updateKeyboard(Keyboard.placeButtons)
        elif step == 2:
            self.updateKeyboard(Keyboard.timeButtons)
        elif step == 3:
            self.updateKeyboard(Keyboard.scoreButtons)
        elif step == 4:
            self.updateKeyboard(Keyboard.homeButtons)
        else:
            raise


class SummaryMenuMessage(BaseMessage):
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
    def returnHomeKeyboard():\
        return Keyboard.homeButtons


class FailMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        self.updateMessage("오류가 발생하였습니다.")
        self.updateKeyboard(Keyboard.homeButtons)


class SuccessMessage(Message):
    def __init__(self):
        self.returnedMessage = "SUCCESS"
