class WindowMechanism():

    OPEN=1
    CLOSED=0  
    
    def __init__(self):
        self.__status = self.OPEN
        self.__curtain_status = self.OPEN

    def open_window(self):
        self.__status = self.OPEN
        print("WINDOW OPENED")

    def close_window(self):
        self.__status = self.CLOSED
        print("WINDOW CLOSED")

    def open_curtains(self):
        self.__curtain_status = self.OPEN
        print("CURTAINS OPENED")

    def close_curtains(self):
        self.__curtain_status = self.CLOSED
        print("CURTAINS CLOSED")

    def window_status(self):
        return {
            "window": self.__status,
            "curtains": self.__curtain_status
        }