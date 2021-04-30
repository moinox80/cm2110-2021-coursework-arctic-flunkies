import time

class Curtain:
    OPEN=1
    CLOSE=0
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

    def __init__(self):
        self.__current_time = self.current_time
        self.__time = self.t
        self.__open_curtain = self.OPEN
        self.__close_curtain = self.CLOSE

    def run_curtain(self):
        if self.__time.tm_hour > 7 and self.__time.tm_hour < 19:
            return self.__open_curtain
        elif self.__time.tm_hour < 7 and self.__time.tm_hour > 19:
            return self.__close_curtain

    def get_time(self):
        return self.__current_time