import json
import re

import telegram


def get_update_obj(request, bot_inst):
    update = json.loads(request.body)
    print(f"update: {update}")
    return telegram.Update.de_json(update, bot_inst)


# Todo: Write tests
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


def markdown_sanitizer(md: str) -> str:
    """
    Escape all Telegram markdown symbols that require escaping.
    P.S. This should only be used on strings you're sure doesn't have
    intentional markdown formatting.
    """
    culprits = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in culprits:
        if char in md and not char.startswith("\\"):
            md = md.replace(char, f"\{char}")

    return md


# class MarkdownSanitizer:
#
#     def __init__(self, md: str):
#         self.md = md
#         self.same_double_tags = ["*", "__", "```", "~", "`"]
#         self.diff_double_tags = [("[", "]"), ("(", ")")]
#         self.culprits = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
#
#     def generate_patterns(self):
#         double_patterns = [rf"^{char}[a-zA-Z0-9]{char}$" for char in self.same_double_tags]
#         diff_double_patterns = [rf"^{start}[a-zA-Z0-9]{end}$" for start, end in self.diff_double_tags]
#         others = ["^*[a-zA-Z0-9]_$"]
#         all_patterns = double_patterns + diff_double_patterns + others
#
#         def re_search_recursive(pattern_list, str_to_search):
#
#             # search_ = re.findall(pattern, str_to_search)
#             # if not search_:
#             #     return pattern
#             #
#             # return re_search_recursive(pattern, pattern)
#
#         search = [re_search_recursive(pat, self.md) for pat in all_patterns]

