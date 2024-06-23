from impactUtils.VWAP import VWAP
from impactUtils.TickTest import TickTest

def getImbalance(data, startTS, endTS):
    if startTS is None:
        startTS = 19 * 60 * 60 * 1000 / 2
    if endTS is None:
        endTS = 31 * 60 * 60 * 1000 / 2   # 3:30 PM
    
    tickTest = TickTest()
    classifications = tickTest.classifyAll(data, startTS, endTS)
    imbalance_volume = 0

    for i in range(0, len(classifications)):
        imbalance_volume += classifications[i][2] * data.getSize(i)
    
    imbalance = VWAP(data, startTS, endTS).getVWAP()*imbalance_volume

    return imbalance