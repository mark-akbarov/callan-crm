from telebot import types


class CustomKeyboard:
    def __init__(
            self,
            buttons: list = None,
            *args,
            **kwargs
    ) -> None:
        self.buttons = buttons

    def create(self, *args, **kwargs):
        keyboards = [types.KeyboardButton(text=button, **kwargs) for button in self.buttons]
        return keyboards


yes_no_markup = CustomKeyboard(['Yes, proceed', 'No, change details'])

share_markup = CustomKeyboard(['Share Contact'], request_contact=True)
