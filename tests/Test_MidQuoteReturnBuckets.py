import unittest
from taq import MyDirectories
from taq.TAQQuotesReader import TAQQuotesReader
from impactUtils.MidQuoteReturnBuckets import MidQuoteReturnBuckets

# Test MidQuoteReturnBuckets class used to compute
# mid-quote returns of some length of time, e.g. 2 minutes
# or 15 minutes
class Test_MidQuoteReturnBuckets(unittest.TestCase):

    def testName(self):
        startTS = 18 * 60 * 60 * 1000 / 2  # 930AM
        endTS = 16 * 60 * 60 * 1000  # 4PM
        numBuckets = 2
        fileName = MyDirectories.getQuotesDir() + '/20070919/IBM_quotes.binRQ'
        data = TAQQuotesReader( fileName )
        midReturnBuckets = MidQuoteReturnBuckets(data, startTS, endTS, numBuckets)
        self.assertTrue(midReturnBuckets.getN() == 2)
        self.assertAlmostEqual(
            (data.getAskPrice(0) + data.getBidPrice(0) ) / 2,
            midReturnBuckets._startMidQuotes[0]
        )


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
