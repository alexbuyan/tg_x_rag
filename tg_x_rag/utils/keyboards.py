from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def yes_no_keyboard():
    return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='yes'),
                    KeyboardButton(text='no')
                ]
            ],
            resize_keyboard=True
        )