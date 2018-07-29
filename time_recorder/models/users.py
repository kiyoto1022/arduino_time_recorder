from user import *


class Users:
    def __init__(self):
        self.users = {'1': User('1', "user1"), '2': User('2', "user2"), '3': User('3', "user3")}

    def is_member(self, user_id):
        if user_id in self.users:
            return True
        return False

    def get(self, user_id):
        return self.users[user_id]

    def list(self):
        return self.users.values()
