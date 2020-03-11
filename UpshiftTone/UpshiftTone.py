# import all required packages
import threading
import time
import winsound


class UpShiftTone(threading.Thread):
    def __init__(self, RTDB, rate):
        threading.Thread.__init__(self)
        self.rate = rate
        self.db = RTDB
        self.FirstRPM = 20000
        self.ShiftRPM = 20000
        self.LastRPM = 20000
        self.BlinkRPM = 20000
        self.DriverCarName = ''
        self.BInitialised = False
        self.IsOnTrack = False
        self.tBeep = 0
        self.BShiftTone = False
        self.oldGear = 0

    def run(self):
        while 1:
            # execute this loop while iRacing is running
            while self.db.startUp:
                if not self.BInitialised or self.db.BUpshiftToneInitRequest:
                    self.initialise()

                # execute this loop while player is on track
                while self.db.IsOnTrack and self.db.ShiftToneEnabled:
                    t = time.time()
                    if self.db.Gear > 0 and self.db.UpshiftStrategy < 4 and self.db.Throttle > 0.9:
                        self.beep(self.db.iRShiftRPM[self.db.UpshiftStrategy])
                    elif self.db.Gear > 0 and self.db.UpshiftStrategy == 4 and self.db.Throttle > 0.9:
                        self.beep2()
                    else:
                        self.db.Alarm[7] = 0
                    
                    if (not self.oldGear == self.db.Gear) and self.BShiftTone:
                        tShiftReaction = max(time.time() - self.tBeep, 0)
                        if tShiftReaction > 1:
                            self.db.tShiftReaction = float('nan')
                        else:
                            self.db.tShiftReaction = tShiftReaction

                    # if not self.oldGear == self.db.Gear:
                    #     if 0 < self.oldGear < self.db.Gear and self.BShiftTone:
                    #         self.db.tShiftReaction = max(min(time.time() - self.tBeep, 2), 0)

                        self.BShiftTone = False

                    if self.db.Gear > 0:
                        self.oldGear = self.db.Gear
                    
                    self.db.tExecuteUpshiftTone = time.time() - t

            self.BInitialised = False

    def beep(self, shiftRPM):
        if self.db.RPM >= shiftRPM and self.db.UserShiftFlag[self.db.Gear - 1] and self.db.Speed > 20:
            self.db.Alarm[7] = 3
            if time.time() > (self.tBeep + 0.75):
                winsound.Beep(500, 150)
                self.tBeep = time.time()
                
                if (not self.BShiftTone) and self.oldGear == self.db.Gear:
                    self.BShiftTone = True
        else:
            self.db.Alarm[7] = 0

    def beep2(self):
        if self.db.RPM >= self.db.UserShiftRPM[self.db.Gear - 1] and self.db.UserShiftFlag[self.db.Gear - 1] and self.db.Speed > 20:
            self.db.Alarm[7] = 3
            if time.time() > (self.tBeep + 0.75):
                winsound.Beep(500, 150)
                self.tBeep = time.time()

                if (not self.BShiftTone) and self.oldGear == self.db.Gear:
                    self.BShiftTone = True
        else:
            self.db.Alarm[7] = 0

    def initialise(self):
        time.sleep(0.1)
        self.tBeep = 0

        # get optimal shift RPM from iRacing and display message
        self.FirstRPM = self.db.DriverInfo['DriverCarSLFirstRPM']
        self.ShiftRPM = self.db.DriverInfo['DriverCarSLShiftRPM']
        self.LastRPM = self.db.DriverInfo['DriverCarSLLastRPM']
        self.BlinkRPM = self.db.DriverInfo['DriverCarSLBlinkRPM']
        self.DriverCarName = self.db.DriverInfo['Drivers'][self.db.DriverInfo['DriverCarIdx']]['CarScreenNameShort']

        print(self.db.timeStr + ':First Shift RPM for', self.DriverCarName, ':', self.FirstRPM)
        print(self.db.timeStr + ':Shift RPM for', self.DriverCarName, ':', self.ShiftRPM)
        print(self.db.timeStr + ':Last Shift RPM for', self.DriverCarName, ':', self.LastRPM)
        print(self.db.timeStr + ':Blink Shift RPM for', self.DriverCarName, ':', self.BlinkRPM)

        self.db.iRShiftRPM = [self.FirstRPM, self.ShiftRPM, self.LastRPM, self.BlinkRPM]

        # play three beep sounds as notification
        winsound.Beep(500, 150)
        time.sleep(0.3)
        winsound.Beep(600, 150)
        time.sleep(0.3)
        winsound.Beep(800, 150)

        self.BInitialised = True
        self.db.BUpshiftToneInitRequest = False
