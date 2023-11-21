class ChatIdValidator:
    """ "Проверка ввода chat_id """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        chat_id = dict(value).get(self.field)
        if not chat_id:
            print('chat_id нужен для отправки уведомлений')
        return True
