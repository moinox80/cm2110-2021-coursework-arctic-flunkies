import time

class Curtain:
    OPEN=1
    CLOSE=0
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    time_1 = 0
    time_2 = 0

    def __init__(self):
        self.__current_time = self.current_time
        self.__time = self.t
        self.__open_curtain = self.OPEN
        self.__close_curtain = self.CLOSE
        self.__time_1 = self.time_1
        self.__time_2 = self.time_2

    def run_curtain(self):
        if self.__time.tm_hour > self.__time_1 and self.__time.tm_hour < self.__time_2:
            return self.__open_curtain
        elif self.__time.tm_hour < self.__time_1 and self.__time.tm_hour > self.__time_2:
            return self.__close_curtain

    def get_time(self):
        return self.__current_time
    
    def set_time_2(self, new_value):
        self.__time_1 = new_value
    
    def set_time_2(self, new_value):
        self.__time_2 = new_value