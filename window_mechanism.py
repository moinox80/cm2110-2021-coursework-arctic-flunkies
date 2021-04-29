
class window_mechanism():

    OPEN=1
    CLOSE=0  
    
    def open_window(self):
        self.__status = self.OPEN
        print("WINDOW OPENED")

    def close_window(self):
        self.__status = self.CLOSE
        print("WINDOW CLOSED")

    def window_status(self):
        if self.__status == 1:
            print("WINDOW IS OPEN")
            return 1
        else: 
            print("WINDOW IS CLOSED")
            return 0