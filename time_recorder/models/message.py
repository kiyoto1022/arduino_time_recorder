class Message:

    def __init__(self, value):
        if len(value) != 0:
            self.user_id = value.replace('\n', '').replace('\r', '').split(',')[0]
            self.entry_exit = value.replace('\n', '').replace('\r', '').split(',')[1]
        else:
            self.user_id = ""
            self.entry_exit = ""

    def is_receive(self):
        if self.user_id == "":
            return False
        return True

    def is_punch_in(self):
        if self.entry_exit == "in":
            return True
        return False

    def is_punch_out(self):
        if self.entry_exit == "out":
            return True
        return False
