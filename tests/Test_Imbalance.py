import unittest
import numpy as np
from taq import MyDirectories
from taq.TAQTradesReader import TAQTradesReader
from impactUtils.ImbalanceValue import *

class Test_FirstPriceBuckets(unittest.TestCase):

    def testConstructor(self):
        startTS = None
        endTS = None
        fileName = MyDirectories.getTradesDir() + "/20070919/IBM_trades.binRT"
        data = TAQTradesReader(fileName)

        ibv = getImbalance(data, startTS, endTS)
        self.assertAlmostEqual(ibv,
                               -45224126.44396259)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()