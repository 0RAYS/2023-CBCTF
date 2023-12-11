class secert_flag(str):

    def __repr__(self) -> str:
        return "DELETED"

    def __str__(self) -> str:
        return "DELETED"


class flag_level10:

    def __init__(self, flag: str):
        setattr(self, 'flag_level10', secert_flag(flag))


def get_flag():
    with open('/flag', "r") as f:
        return flag_level10(f.read())