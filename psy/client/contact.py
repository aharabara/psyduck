class Contact:
    name = None
    nickname = None
    pool = None

    def __init__(self, name:str, nickname:str, pool:int):
        self.nickname = nickname
        self.name = name
        self.pool = pool

    def __str__(self):
        return self.name
