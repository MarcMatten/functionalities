import threading
import time
import irsdk
import json
from libs import Car, Track


class RTDB:
    def __init__(self):
        timeStr = time.strftime("%H:%M:%S", time.localtime())
        self.initData = list()
        self.StopDDU = True
        self.StartDDU = False
        self.timeStr = time.strftime("%H:%M:%S", time.localtime())
        print(timeStr + ': RTDB initialised!')

    def initialise(self, data):
        temp = list(data.items())
        for i in range(0, len(data)):
            self.__setattr__(temp[i][0], temp[i][1])
        self.initData.extend(temp)

    def get(self, string):
        return self.__getattribute__(string)

    def reinitialise(self):
        print(time.strftime("%H:%M:%S", time.localtime()) + ': reinitialise RTDB!')
        self.StopDDU = True
        for i in range(0, len(self.initData)):
            self.__setattr__(self.initData[i][0], self.initData[i][1])
        self.timeStr = time.strftime("%H:%M:%S", time.localtime())
        print(time.strftime("%H:%M:%S", time.localtime()) + ': RTDB successfully reinitialised!')
        self.StartDDU = True

    def snapshot(self):
        nameStr = time.strftime('snapshots/' + "%Y_%m_%d-%H-%M-%S", time.localtime())+'_RTDBsnapshot'

        variables = list(self.__dict__.keys())
        variables.remove('car')
        variables.remove('track')

        self.car.saveJson(self.dir, nameStr+'_car')
        self.track.saveJson(self.dir, nameStr+'_track')

        self.WeekendInfo['WeekendOptions']['Date'] = str(self.WeekendInfo['WeekendOptions']['Date'])

        data = {}

        for i in range(0, len(variables)):
            data[variables[i]] = self.__getattribute__(variables[i])

        with open(nameStr+'.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)

        print(time.strftime("%H:%M:%S", time.localtime()) + ': Saved snapshot: ' + nameStr+'.json')

    def loadSnapshot(self, name):
        path = self.dir + '\\snapshots\\' + name

        self.StopDDU = True
        self.StartDDU = True

        with open(path + '.json') as f:
            data = json.loads(f.read())

        carPath = path + '_car.json'
        self.car = Car.Car('default')
        self.car.loadJson(carPath)

        trackPath = path + '_track.json'
        self.track = Track.Track('default')
        self.track.loadJson(trackPath)
        self.map = self.track.map

        self.initialise(data)

        print(time.strftime("%H:%M:%S", time.localtime()) + ': Loaded RTDB snapshot: ' + name +'.json')


# create thread to update RTDB
class iRThread(threading.Thread):
    def __init__(self, rtdbObj, keys, rate):
        threading.Thread.__init__(self)
        self.rate = rate
        self.db = rtdbObj
        self.keys = keys
        self.ir = irsdk.IRSDK()

    def run(self):
        while 1:
            self.db.startUp = self.ir.startup()
            if self.db.startUp:
                self.ir.freeze_var_buffer_latest()
                for i in range(0, len(self.keys)):
                    self.db.__setattr__(self.keys[i], self.ir[self.keys[i]])
                self.ir.unfreeze_var_buffer_latest()
            else:
                self.ir.shutdown()
            self.db.timeStr = time.strftime("%H:%M:%S", time.localtime())
            time.sleep(self.rate)
