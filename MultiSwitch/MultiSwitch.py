import threading
# import pygame
import os
import numpy as np
import time
from functionalities.libs import importExport
from libs.IDDU import IDDUItem, IDDUThread

class MultiSwitchItem(IDDUItem):
    # db = 0
    NButtonIncMap = 23
    NButtonDecMap = 22
    NButtonIncValue = 9
    NButtonDecValue = 8

    dcIgnoreList = ['dcHeadlightFlash', 'dcPitSpeedLimiterToggle', 'dcStarter', 'dcTractionControlToggle', 'dcTearOffVisor', 'dcPushToPass', 'dcDashPage']

    def __init__(self):
        IDDUItem.__init__(self)
        MultiSwitchItem.dcConfig = importExport.loadJson(self.db.dir + '/data/configs/multi.json')
        pass

    # @staticmethod
    # def setDB(rtdb):
    #     MultiSwitchItem.db = rtdb
    #     MultiSwitchItem.dcConfig = importExport.loadJson(MultiSwitchItem.db.dir + '/multi.json')

class MultiSwitchThread(MultiSwitchItem, IDDUThread):
    def __init__(self, rate):
        MultiSwitchItem.__init__(self)
        IDDUThread.__init__(self, rate)


class MultiSwitch(MultiSwitchThread):
    mapDDU = {}
    mapIR = {}
    NCurrentMapDDU = 0
    NCurrentMapIR = 0
    NMultiState = 0
    tMultiChange = 0

    def __init__(self, rate):
        MultiSwitchThread.__init__(self, rate)
        self.timeStr = ''
        # test0 = MultiSwitchItem()
        # test = MultiSwitchMap('blah')

        # myJoystick = None
        # pygame.init()
        # SCREEN = pygame.display.set_mode((10, 10))

        # initialize joystick
        # if os.environ['COMPUTERNAME'] == 'MARC-SURFACE':
        #     self.initJoystick('vJoy Device')
        # else:
        #     self.initJoystick('FANATEC ClubSport Wheel Base')

    def run(self):
        mapDDUList = list(self.mapDDU.keys())
        mapIRList = list(self.mapIR.keys())
        while 1:
            if self.db.BMultiInitRequest:
                self.initCar()
                self.db.BMultiInitRequest = False
                
            if self.pygame.display.get_init() == 1:

                # observe input controller
                events = self.pygame.event.get()
                for event in events:

                    # if event.type == pygame.KEYDOWN:
                    #     print(pygame.key.name(event.key))
                    if event.type == self.pygame.JOYBUTTONDOWN:
                        # print(event.type)
                        # print(event)
                        if event.button == 25:
                            if self.db.NDDUPage == 1:
                                self.db.NDDUPage = 2
                            else:
                                self.db.NDDUPage = 1


                        if event.button == self.NButtonIncMap:
                            if self.NMultiState == 0:
                                self.NMultiState = 1
                                self.db.dcChangedItems = [self.mapIRList[self.NCurrentMapIR]]
                            else:
                                if self.NMultiState == 1:
                                    NCurrentMapIR = self.NCurrentMapIR + 1
                                    if NCurrentMapIR > len(self.mapIRList)-1:
                                        NCurrentMapIR = NCurrentMapIR - len(self.mapIRList)

                                    self.NCurrentMapIR = NCurrentMapIR
                                    self.db.dcChangedItems = [self.mapIRList[self.NCurrentMapIR]]
                                elif self.NMultiState == 2:
                                    NCurrentMapDDU = self.NCurrentMapDDU + 1
                                    if NCurrentMapDDU > len(mapDDUList)-1:
                                        NCurrentMapDDU = NCurrentMapDDU - len(mapDDUList)

                                    self.NCurrentMapDDU = NCurrentMapDDU

                                    self.db.dcChangedItems = [self.mapDDUList[self.NCurrentMapDDU]]

                            self.tMultiChange = time.time()
                            self.db.dcChangeTime = time.time()

                            # print('NMultiState: {} - NCurrentMapDDU: {} - NCurrentMapIR: {}'.format(self.NMultiState, self.mapDDUList[self.NCurrentMapDDU], self.mapIRList[self.NCurrentMapIR]))

                        elif event.button == self.NButtonDecMap:
                            if self.NMultiState == 0:
                                self.NMultiState = 2
                                self.db.dcChangedItems = [self.mapDDUList[self.NCurrentMapDDU]]
                            else:
                                if self.NMultiState == 1:
                                    NCurrentMapIR = self.NCurrentMapIR - 1
                                    if NCurrentMapIR < 0:
                                        NCurrentMapIR = len(self.mapIRList) + NCurrentMapIR

                                    self.NCurrentMapIR = NCurrentMapIR

                                    self.db.dcChangedItems = [self.mapIRList[self.NCurrentMapIR]]

                                elif self.NMultiState == 2:
                                    NCurrentMapDDU = self.NCurrentMapDDU - 1
                                    if NCurrentMapDDU < 0:
                                        NCurrentMapDDU = len(mapDDUList) + NCurrentMapDDU

                                    self.NCurrentMapDDU = NCurrentMapDDU

                                    self.db.dcChangedItems = [self.mapDDUList[self.NCurrentMapDDU]]

                                # print('Current map: {} -  {}'.format(self.NCurrentMap, temp[self.NCurrentMap]))

                            self.tMultiChange = time.time()
                            self.db.dcChangeTime = time.time()

                            # print('NMultiState: {} - NCurrentMapDDU: {} - NCurrentMapIR: {}'.format(self.NMultiState, self.mapDDUList[self.NCurrentMapDDU], self.mapIRList[self.NCurrentMapIR]))

                        elif event.button == self.NButtonIncValue:
                            if self.NMultiState == 0:
                                self.mapIR['dcBrakeBias'].increase()
                            else:
                                if self.NMultiState == 1:
                                    self.mapIR[self.mapIRList[self.NCurrentMapIR]].increase()
                                    self.db.dcChangedItems = [self.mapIRList[self.NCurrentMapIR]]
                                elif self.NMultiState == 2:
                                    self.mapDDU[mapDDUList[self.NCurrentMapDDU]].increase()
                                    self.db.dcChangedItems = [self.mapDDUList[self.NCurrentMapDDU]]

                            self.tMultiChange = time.time()
                            self.db.dcChangeTime = time.time()

                            # print('NCurrentMap: {} - MapItem: {} - NMultiState: {}'.format(self.NCurrentMap, temp[self.NCurrentMap], self.NMultiState))

                        elif event.button == self.NButtonDecValue:
                            if self.NMultiState == 0:
                                self.mapIR['dcBrakeBias'].decrease()
                            else:
                                if self.NMultiState == 1:
                                    self.mapIR[self.mapIRList[self.NCurrentMapIR]].decrease()
                                    self.db.dcChangedItems = [self.mapIRList[self.NCurrentMapIR]]
                                elif self.NMultiState == 2:
                                    self.mapDDU[mapDDUList[self.NCurrentMapDDU]].decrease()
                                    self.db.dcChangedItems = [self.mapDDUList[self.NCurrentMapDDU]]

                            self.tMultiChange = time.time()
                            self.db.dcChangeTime = time.time()

                            # print('NCurrentMap: {} - MapItem: {} - NMultiState: {}'.format(self.NCurrentMap, temp[self.NCurrentMap], self.NMultiState))



                # in case of relevant change inrease or decrese value and send
                # if iRacing Control forward command via vjoy

                # execute this loop while iRacing is running
                # print('running')
                # self.j.set_button(1,1)
                # time.sleep(self.rate)
                # self.j.set_button(1,0)
                # time.sleep(self.rate)

                if time.time() > (self.tMultiChange + 2):
                    if not self.NMultiState == 0:
                        self.NMultiState = 0
                        # print('NCurrentMap: {} - MapItem: {} - NMultiState: {}'.format(self.NCurrentMap, temp[self.NCurrentMap], self.NMultiState))


            time.sleep(self.rate)

    # def initJoystick(self, name):
    #     pygame.joystick.init()
    #     print(self.timeStr + ': \t' + str(pygame.joystick.get_count()) + ' joysticks detected:')
    #
    #     desiredJoystick = 9999
    #
    #     for i in range(pygame.joystick.get_count()):
    #         print(self.timeStr + ':\tJoystick ', i, ': ', pygame.joystick.Joystick(i).get_name())
    #         if pygame.joystick.Joystick(i).get_name() == name:
    #             desiredJoystick = i
    #
    #     if not desiredJoystick == 9999:
    #         print(self.timeStr + ':\tConnecting to', pygame.joystick.Joystick(desiredJoystick).get_name())
    #         myJoystick = pygame.joystick.Joystick(desiredJoystick)
    #         myJoystick.get_name()
    #         myJoystick.init()
    #         print(self.timeStr + ':\tSuccessfully connected to', pygame.joystick.Joystick(desiredJoystick).get_name(), '!')
    #     else:
    #         print(self.timeStr + ':\tFANATEC ClubSport Wheel Base not found!')

    def addMapping(self, name='name', minValue=0 , maxValue= 1, step=1):
        if name in self.db.car.dcList:
            self.mapIR[name] = MultiSwitchMapiRControl(name, minValue , maxValue, step)
        else:
            self.mapDDU[name] = MultiSwitchMapDDUControl(name, minValue , maxValue, step)

    def initCar(self):

        IDDUItem.dcConfig = importExport.loadJson(self.db.dir + '/data/configs/multi.json')

        dcList = list(self.db.car.dcList.keys())
        for i in range(0, len(dcList)):

            if not dcList[i] in self.dcIgnoreList:

                if not dcList[i] in self.dcConfig:
                    n = len(self.dcConfig)
                    IDDUItem.dcConfig[dcList[i]] = [2*n, 2*n+1]

                if self.db.car.dcList[dcList[i]][1]:
                    self.addMapping(dcList[i])

        importExport.saveJson(self.dcConfig, self.db.dir + '/data/configs/multi.json')

        self.mapDDUList = list(self.mapDDU.keys())
        self.mapIRList = list(self.mapIR.keys())

class MultiSwitchMapDDUControl(MultiSwitchItem):
    def __init__(self, name, minValue , maxValue, step):
        MultiSwitchItem.__init__(self)
        self.name = name
        self.type = type(self.db.__getattribute__(name))
        if self.type is not bool:
            self.minValue = minValue
            self.maxValue = maxValue
            self.step = step

    def increase(self):
        if self.type is not bool:
            newVal = np.min([self.db.__getattribute__(self.name) + self.step, self.maxValue])
            self.db.__setattr__(self.name, newVal)
        else:
            self.db.__setattr__(self.name, not self.db.__getattribute__(self.name))

        # print('Increase ' + self.name)

    def decrease(self):
        if self.type is not bool:
            newVal = np.max([self.db.__getattribute__(self.name) - self.step, self.minValue])
            self.db.__setattr__(self.name, newVal)
        else:
            self.db.__setattr__(self.name, not self.db.__getattribute__(self.name))

        # print('Decrease ' + self.name)

class MultiSwitchMapiRControl(MultiSwitchItem):
    def __init__(self, name, minValue , maxValue, step):
        MultiSwitchItem.__init__(self)
        self.name = name
        self.type = type(self.db.__getattribute__(name))
        if self.type is not bool:
            self.minValue = minValue
            self.maxValue = maxValue
            self.step = step

    def increase(self):
        self.pressButton(self.dcConfig[self.name][1]+1, 0.05)

    def decrease(self):
        self.pressButton(self.dcConfig[self.name][0]+1, 0.05)
