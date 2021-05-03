class WindowMechanism():
    #Stating attributes
    OPEN=1
    CLOSED=0  
    
    #Initializing attributes
    def __init__(self):
        self.__status = self.OPEN
        self.__curtain_status = self.OPEN

    #Open and close window functions
    def open_window(self):
        self.__status = self.OPEN
        print("WINDOW OPENED")

    def close_window(self):
        self.__status = self.CLOSED
        print("WINDOW CLOSED")

    #Open and close curtain functions
    def open_curtains(self):
        self.__curtain_status = self.OPEN
        print("CURTAINS OPENED")

    def close_curtains(self):
        self.__curtain_status = self.CLOSED
        print("CURTAINS CLOSED")

    #Window status function
    def window_status(self):
        return {
            "window": self.__status,
            "curtains": self.__curtain_status
        }