import unittest
import numpy as np
from taq import MyDirectories
from taq.TAQTradesReader import TAQTradesReader
from impactUtils.DailyValue import *

class Test_FirstPriceBuckets(unittest.TestCase):

    def testConstructor(self):
        startTS = None
        endTS = None
        fileName = MyDirectories.getTradesDir() + "/20070919/IBM_trades.binRT"
        data = TAQTradesReader(fileName)

        tdv = getDailyValue(data, startTS, endTS)
        self.assertAlmostEqual(np.round(1.043658,4),
                               np.round(tdv/(10**9),4))

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()