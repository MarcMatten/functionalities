# import all required packages
import threading
import time
import winsound

# UpShiftTone Thread
class UpShiftTone(threading.Thread):
    def __init__(self, RTDB, rate):
        threading.Thread.__init__(self)
        self.rate = rate
        self.db = RTDB
        self.ShiftRPM = 20000
        self.initialised = False
        self.fname = "files\Beep.wav"  # path to beep soundfile
        self.IsOnTrack = False

    def run(self):
        while 1:
            # execute this loop while iRacing is running
            while self.db.startUp:
                if not self.initialised:
                    self.initialise()
                # two beeps sounds as notification when entering iRacing
                if self.db.IsOnTrack and not self.IsOnTrack:
                    self.IsOnTrack = True
                    winsound.PlaySound(self.fname, winsound.SND_FILENAME)
                    time.sleep(0.3)
                    winsound.PlaySound(self.fname, winsound.SND_FILENAME)

                # execute this loop while player is on track
                while self.db.IsOnTrack and self.db.ShiftToneEnabled:
                    if self.db.Gear > 0 and self.db.UpshiftStrategy < 4 and self.db.Throttle > 0.9:
                        self.beep(self.db.iRShiftRPM[self.db.UpshiftStrategy])
                    elif self.db.Gear > 0 and self.db.UpshiftStrategy == 4 and self.db.Throttle > 0.9:
                        self.beep2()

                # update flag when leaving track
                if not self.db.IsOnTrack and self.IsOnTrack:
                    self.IsOnTrack = False

            self.initialised = False

    def beep(self, shiftRPM):
        if self.db.RPM >= shiftRPM and self.db.UserShiftFlag[self.db.Gear - 1]:
            winsound.PlaySound(self.fname, winsound.SND_FILENAME)
            time.sleep(0.75)  # pause for 750 ms to avoid multiple beeps when missing shiftpoint

    def beep2(self):
        if self.db.RPM >= self.db.UserShiftRPM[self.db.Gear - 1] and self.db.UserShiftFlag[self.db.Gear - 1]:
            winsound.PlaySound(self.fname, winsound.SND_FILENAME)
            time.sleep(0.75)  # pause for 750 ms to avoid multiple beeps when missing shiftpoint

    def initialise(self):
        time.sleep(0.1)
        # get optimal shift RPM from iRacing and display message
        self.FirstRPM = self.db.DriverInfo['DriverCarSLFirstRPM']
        self.ShiftRPM = self.db.DriverInfo['DriverCarSLShiftRPM']
        self.LastRPM = self.db.DriverInfo['DriverCarSLLastRPM']
        self.BlinkRPM = self.db.DriverInfo['DriverCarSLBlinkRPM']
        self.DriverCarName = self.db.DriverInfo['Drivers'][self.db.DriverInfo['DriverCarIdx']]['CarScreenNameShort']

        # self.db.DriverInfo['Drivers'][self.db.DriverInfo['DriverCarIdx']]['CarScreenNameShort']
        print(self.db.timeStr+':First Shift RPM for', self.DriverCarName, ':', self.FirstRPM)
        print(self.db.timeStr+':Shift RPM for', self.DriverCarName, ':', self.ShiftRPM)
        print(self.db.timeStr+':Last Shift RPM for', self.DriverCarName, ':', self.LastRPM)
        print(self.db.timeStr+':Blink Shift RPM for', self.DriverCarName, ':', self.BlinkRPM)

        self.db.iRShiftRPM = [self.FirstRPM, self.ShiftRPM, self.LastRPM, self.BlinkRPM]

        # play three beep sounds as notification
        winsound.PlaySound(self.fname, winsound.SND_FILENAME)
        time.sleep(0.3)
        winsound.PlaySound(self.fname, winsound.SND_FILENAME)
        time.sleep(0.3)
        winsound.PlaySound(self.fname, winsound.SND_FILENAME)

        self.initialised = True
