import threading
import time
import irsdk

class RTDB:
    def __init__(self):
        timeStr = time.strftime("%H:%M:%S", time.localtime())
        print(timeStr+': RTDB initialised!')

    def initialise(self, data):
        temp = list(data.items())
        for i in range(0,len(data)):
            self.__setattr__(temp[i][0], temp[i][1])

# create thread to update RTDB
class iRThread(threading.Thread):
    def __init__(self, RTDB, keys, rate):
        threading.Thread.__init__(self)
        self.rate = rate
        self.db = RTDB
        self.keys = keys
        self.ir = irsdk.IRSDK()

    def run(self):
        while 1:
            self.db.startUp = self.ir.startup()
            if self.db.startUp:
                for i in range(0, len(self.keys)):
                    self.db.__setattr__(self.keys[i], self.ir[self.keys[i]])
            self.db.timeStr = time.strftime("%H:%M:%S", time.localtime())
            time.sleep(self.rate)