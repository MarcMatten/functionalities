import threading
import time
import irsdk
from libs import Car, Track
import os
from functionalities.libs import importExport


class RTDB:
    def __init__(self):
        timeStr = time.strftime("%H:%M:%S", time.localtime())
        self.initData = list()
        self.queryData = list()
        self.StopDDU = True
        self.StartDDU = False
        self.timeStr = time.strftime("%H:%M:%S", time.localtime())
        print(timeStr + ': RTDB initialised!')

    def initialise(self, data, BQueryData):
        temp = list(data.items())
        for i in range(0, len(data)):
            self.__setattr__(temp[i][0], temp[i][1])
        self.initData.extend(temp)
        if BQueryData:
            self.queryData.extend(list(data.keys()))

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
        snapshotDir = "data/snapshots/"

        if not os.path.exists(snapshotDir):
            os.mkdir(snapshotDir)

        nameStr = time.strftime(snapshotDir + "%Y_%m_%d-%H-%M-%S", time.localtime())+'_RTDBsnapshot'

        variables = list(self.__dict__.keys())
        variables.remove('car')
        variables.remove('track')

        self.car.save(self.dir, nameStr+'_car')
        self.track.save(self.dir, nameStr+'_track')

        self.WeekendInfo['WeekendOptions']['Date'] = str(self.WeekendInfo['WeekendOptions']['Date'])

        data = {}

        for i in range(0, len(variables)):
            data[variables[i]] = self.__getattribute__(variables[i])

        importExport.saveJson(data, nameStr+'.json')

        print(time.strftime("%H:%M:%S", time.localtime()) + ': Saved snapshot: ' + nameStr+'.json')

    def loadSnapshot(self, name):
        path = self.dir + '/data/snapshots/' + name

        self.StopDDU = True
        self.StartDDU = True

        data = importExport.loadJson(path)

        carPath = path + '_car.json'
        self.car = Car.Car('default')
        self.car.load(carPath)

        trackPath = path + '_track.json'
        self.track = Track.Track('default')
        self.track.load(trackPath)
        self.map = self.track.map

        self.initialise(data, False)

        print(time.strftime("%H:%M:%S", time.localtime()) + ': Loaded RTDB snapshot: ' + name +'.json')

    def loadFuelTgt(self, path):  # TODO: does this need to live in here?
        data = importExport.loadJson(path)

        temp = list(data.items())
        for i in range(0, len(data)):
            self.FuelTGTLiftPoints.__setitem__(temp[i][0], temp[i][1])

        print(time.strftime("%H:%M:%S", time.localtime()) + ':\tImported ' + path)


# create thread to update RTDB
class iRThread(threading.Thread):
    def __init__(self, rtdbObj, rate):
        threading.Thread.__init__(self)
        self.rate = rate
        self.db = rtdbObj
        self.ir = irsdk.IRSDK()

    def run(self):
        while 1:
            t = time.perf_counter()
            self.db.startUp = self.ir.startup()
            if self.db.startUp:
                # self.ir.freeze_var_buffer_latest()
                for i in range(0, len(self.db.queryData)):
                    self.db.__setattr__(self.db.queryData[i], self.ir[self.db.queryData[i]])
                # self.ir.unfreeze_var_buffer_latest()

                # Mapping CarIdx for DriverInfo['Drivers']
                self.db.CarIdxMap = [None]*64
                for i in range(0, len(self.db.DriverInfo['Drivers'])):
                    self.db.CarIdxMap[self.db.DriverInfo['Drivers'][i]['CarIdx']] = i

            else:
                self.ir.shutdown()
            self.db.timeStr = time.strftime("%H:%M:%S", time.localtime())
            self.db.tExecuteRTDB = (time.perf_counter() - t) * 1000
            time.sleep(self.rate)
