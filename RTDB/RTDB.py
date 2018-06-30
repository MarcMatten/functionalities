class RTDB:
    def __init__(self):
        print('RTDB initialised!')

    def initialise(self, data):
        temp = list(data.items())
        for i in range(0,len(data)):
            self.__setattr__(temp[i][0], temp[i][1])