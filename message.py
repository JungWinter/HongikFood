from keyboard import Keyboard


class Message:
    #  Message클래스를 생성할 때 기본적인 틀만 구현하고
    #  값들은 던져주면 알아서 메시지를 리턴한다

    ex_keyboard = {
        "type": "buttons",
        "buttons": Keyboard.buttons,
    }

    ex_message = {
        "message": {
            "text": "",
        },
        "keyboard": ex_keyboard
    }
    # Uesage : ex_message["message"].update(ex_weekend)
    ex_weekend = {
        "message_button": {
            "label": "이번주 메뉴 보기",
            "url": "http://apps.hongik.ac.kr/food/food.php"
        }
    }
