import json

import telegram


def get_update_obj(request, bot_inst):

    update = json.loads(request.body)
    print(f"update: {update}")
    return telegram.Update.de_json(update, bot_inst)


class IncrementString:
    """
    Appends a number to a string and increments the number
    """
    def __init__(self, string, start_num=0):
        self.string = string
        self.start_num = start_num
        self.next_num = None

    def __call__(self, *args, **kwargs):
        if not self.next_num:
            self.next_num = self.start_num + 1
            new_string = str(self.string + str(self.next_num))
            return new_string
        else:
            self.next_num += 1
            return str(self.string + str(self.next_num))