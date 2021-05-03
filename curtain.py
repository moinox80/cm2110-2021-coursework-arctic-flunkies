import time

class Curtain:
    OPEN=1
    CLOSED=0
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

    def __init__(self):
        self.__current_time = self.current_time
        self.__time = self.t
        self.__status = self.CLOSED
        self.__opening_time = self.current_time
        self.__closing_time = self.current_time

    def run_curtain(self):
        if self.__time.tm_hour >= self.__opening_time.tm_hour
        and self.__time.tm_hour < self.__closing_time.tm_hour
        and self.__time.tm_min >= self.__opening_time.tm_min
        and self.__time.tm_min < self.__closing_time.tm_min:
            self.open_curtain()
        else:
            self.close_curtain()

    def set_time_setting(self, setting):
        time_range = setting.split("-")

        if len(time_range) != 2:
            return False
            
        try:
            self.__opening_time = time.strptime(time_range[0], "%H %M")
            self.__closing_time = time.strptime(time_range[1], "%H %M")
        except ValueError:
            return False


    def get_time(self):
        return self.__current_time
    
    def open_curtain(self):
        self.__status = self.OPEN
    
    def close_curtain(self):
        self.__status = self.CLOSED