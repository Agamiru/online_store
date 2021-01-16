from .settings import bot, webhook_url





class IncrementString:
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