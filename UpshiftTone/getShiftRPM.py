import numpy as np
import scipy.signal
import scipy.optimize
import matplotlib.pyplot as plt
from importIBT import importIBT
import tkinter as tk
from tkinter import filedialog


def moving_average(a, n):
    temp = a[-n:]
    temp = np.append(temp, a)
    temp = np.append(temp, a[0:n])
    r = np.zeros(np.size(temp))
    for i in range(0, len(temp)):
        if i < n:
            r[i] = np.mean(temp[0:i + n])
        elif len(temp) < i + n:
            r[i] = np.mean(temp[i - n:])
        else:
            r[i] = np.mean(temp[i - n:n + i])
    return r[n:-n]


def poly2(x, a, b, c):
    return a + b * x + c * np.power(x, 2)


def poly3(x, a, b, c, d):
    return a + b * x + c * np.power(x, 2) + d * np.power(x, 3)


def findIntersection(fun1, fun2, x0):
    return scipy.optimize.fsolve(lambda x: fun1(x) - fun2(x), x0)


def getShiftRPM(path, tReaction):
    # MyChannelMap = {'Speed': ['vCar', 1],  # m/s
    #                 'LapCurrentLapTime': ['tLap', 1],  # s
    #                 'LatAccel': ['gLat', 1],  # m/s²
    #                 'LongAccel': ['gLong', 1],  # m/s²
    #                 'ThrottleRaw': ['rThrottle', 1],  # 1
    #                 'BrakeRaw': ['rBrake', 1],  # 1
    #                 'FuelUsePerHour': ['QFuel', 1 / 3.6],  # l/h --> g/s
    #                 'LapDist': ['sLap', 1],  # m
    #                 'Alt': ['GPSAltitude', 1]  # m,
    #                 }

    d = importIBT(path)

    d['BStraightLine'] = np.logical_and((d['gLat']) < 1, np.abs(d['SteeringWheelAngle']) < 0.03, np.abs(d['vCar']) > 10)
    d['BWOT'] = np.logical_and((d['rThrottle']) > 0.99, np.abs(d['rBrake']) < 0.01)
    d['BCoasting'] = np.logical_and((d['rThrottle']) < 0.01, np.abs(d['rBrake']) < 0.01)
    d['BShiftRPM'] = np.logical_and(d['BStraightLine'], d['BWOT'])
    d['BShiftRPM'] = np.logical_and(d['BShiftRPM'], d['gLong'] > 0.3)

    # minRPM = np.mean(d['RPM'][d['BShiftRPM']])
    minRPM = 2000

    plt.figure()
    plt.grid()
    plt.scatter(d['vCar'][d['BShiftRPM']], d['gLong'][d['BShiftRPM']])
    plt.xlabel('vCar [m/s]')
    plt.ylabel('gLong [m/s²]')
    # plt.legend()
    plt.show(block=False)
    plt.title('Title')
    plt.xlim(0, np.max(d['vCar'][d['BShiftRPM']]) + 5)
    plt.ylim(0, np.max(d['gLong'][d['BShiftRPM']]) + 1)

    d['BGear'] = list()
    d['BRPMRange'] = list()
    gLongPolyFit = list()
    RPMPolyFit = list()
    vCarMin = list()
    vCarMax = list()
    maxRPM = list()

    for i in range(0, np.max(d['Gear'])):
        NGear = i + 1
        d['BGear'].append(np.logical_and(d['BShiftRPM'], d['Gear'] == NGear))

        maxRPM.append(np.max(d['RPM'][d['BGear'][i]]))

        tempBRPMRange = np.logical_and(d['BGear'][i], d['RPM'] > minRPM)
        tempBRPMRange = np.logical_and(tempBRPMRange, d['RPM'] < maxRPM[i])
        tempBRPMRange = np.logical_and(tempBRPMRange, moving_average(d['EngineWarnings'], 6) < 1)

        d['BRPMRange'].append(tempBRPMRange)

        PolyFitTemp, temp = scipy.optimize.curve_fit(poly3, d['vCar'][d['BRPMRange'][i]], d['gLong'][d['BRPMRange'][i]])
        gLongPolyFit.append(PolyFitTemp)

        PolyFitTemp, temp = scipy.optimize.curve_fit(poly2, d['vCar'][d['BRPMRange'][i]], d['RPM'][d['BRPMRange'][i]])
        RPMPolyFit.append(PolyFitTemp)

        vCarMin.append(np.min(d['vCar'][d['BRPMRange'][i]]))
        vCarMax.append(np.max(d['vCar'][d['BRPMRange'][i]]))
        vCar = np.linspace(vCarMin[i] - 10, vCarMax[i] + 10, 100)

        plt.scatter(d['vCar'][d['BRPMRange'][i]], d['gLong'][d['BRPMRange'][i]])
        plt.plot(vCar, poly3(vCar, gLongPolyFit[i][0], gLongPolyFit[i][1], gLongPolyFit[i][2], gLongPolyFit[i][3]))

    vCarShiftOptimal = []
    vCarShiftTarget = []

    for k in range(0, np.max(d['Gear']) - 1):
        f1 = lambda x: poly3(x, gLongPolyFit[k][0], gLongPolyFit[k][1], gLongPolyFit[k][2], gLongPolyFit[k][3])
        f2 = lambda x: poly3(x, gLongPolyFit[k + 1][0], gLongPolyFit[k + 1][1], gLongPolyFit[k + 1][2], gLongPolyFit[k + 1][3])

        result = findIntersection(f1, f2, vCarMax[k])

        vCarShiftOptimal.append(np.min([result[0], vCarMax[k]]))
        vCarShiftTarget.append(vCarShiftOptimal[k] - tReaction * poly3(vCarShiftOptimal[k], gLongPolyFit[k][0], gLongPolyFit[k][1], gLongPolyFit[k][2], gLongPolyFit[k][3]))

        plt.scatter(vCarShiftOptimal[k], f1(vCarShiftOptimal[k]), marker='o', color='black')
        plt.scatter(vCarShiftTarget[k], f1(vCarShiftTarget[k]), marker='o', color='red')

    plt.figure()
    plt.scatter(d['vCar'][d['BShiftRPM']], d['RPM'][d['BShiftRPM']])
    # plt.scatter(d['vCar'][d['BRPMRange']], d['RPM'][d['BRPMRange']])
    plt.grid()
    plt.xlabel('vCar [m/s]')
    plt.xlabel('nMotor [RPM]')
    # plt.legend()
    plt.show(block=False)
    plt.title('Title')
    plt.xlim(0, np.max(d['vCar'][d['BShiftRPM']]) + 5)
    plt.ylim(0, np.max(d['RPM'][d['BShiftRPM']]) + 500)

    nMotorShiftOptimal = []
    nMotorShiftTarget = []

    for i in range(0, np.max(d['Gear'])):
        vCar = np.linspace(vCarMin[i] - 10, vCarMax[i] + 10, 100)
        plt.plot(vCar, poly2(vCar, RPMPolyFit[i][0], RPMPolyFit[i][1], RPMPolyFit[i][2]))

        if i < np.max(d['Gear']) - 1:
            nMotorShiftOptimal.append(poly2(vCarShiftOptimal[i], RPMPolyFit[i][0], RPMPolyFit[i][1], RPMPolyFit[i][2]))
            nMotorShiftTarget.append(poly2(vCarShiftTarget[i], RPMPolyFit[i][0], RPMPolyFit[i][1], RPMPolyFit[i][2]))
            plt.scatter(vCarShiftOptimal[i], nMotorShiftOptimal[i], marker='o', color='black')
            plt.scatter(vCarShiftTarget[i], nMotorShiftTarget[i], marker='o', color='red')

    # plt.savefig('test', dpi=300, facecolor='w', edgecolor='w',
    #             orientation='portrait', papertype='a4', format=None,
    #             transparent=False, bbox_inches=None, pad_inches=0.1,
    #             metadata=None)

    return nMotorShiftOptimal, vCarShiftOptimal, nMotorShiftTarget, vCarShiftTarget


# MyIbtPath = 'C:/Users/Marc/Documents/Projekte/SimRacingTools/FuelSavingOptimiser/porsche718gt4_indianapolis oval 2020-06-17 22-36-30.ibt'
# MyIbtPath = 'M:/07 - SimRacing/Data/bmwz4gt3_indianapolis ovalindypit 2020-01-06 18-29-20.ibt'
# MyIbtPath = 'M:/07 - SimRacing/Data/porsche911cup_indianapolis oval 2020-01-26 15-49-03.ibt'
# MyIbtPath = 'M:/07 - SimRacing/Data/hpdarx01c_indianapolis oval 2020-04-08 20-26-09.ibt'
root = tk.Tk()
root.withdraw()
MyIbtPath = filedialog.askopenfilename(initialdir="C:/Users/Marc/Documents/Projekte/SimRacingTools/FuelSavingOptimiser", title="Select IBT file", filetypes=(("IBT files", "*.ibt"), ("all files", "*.*")))

nMotorShiftOpt, vCarShiftOpt, nMotorShift, vCarShift = getShiftRPM(MyIbtPath, 0.25)

print('vCarShiftOptimal: ', vCarShiftOpt)
print('nMotorShiftOptimal: ', nMotorShiftOpt)
print('vCarShift: ', vCarShift)
print('nMotorShift: ', nMotorShift)

print('Done')
