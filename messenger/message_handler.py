def get_db_filename():
    return 'db/messages.db'

class MessageHandler:
    def __init__(self):
        self.db_filename = get_db_filename()
        