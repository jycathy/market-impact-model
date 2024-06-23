from numpy import floor

# This class will be used to build mid-quote return buckets,
# e.g. 2 minute returns
class MidQuoteReturnBuckets(object):
    def __init__(
        self,
        data,  # A TAQQuotesReader object that implements getTimestamp(i), getAskPrice(i), getBidPrice(i), getN()
        startTS,  # In milliseconds from midnight
        endTS,  # In milliseconds from midnight
        numBuckets  # Desired number of return buckets
    ):
        # Save start and end times
        if startTS is None:
            startTS = 19 * 60 * 60 * 1000 / 2
        if endTS is None:
            endTS = 16 * 60 * 60 * 1000
        self._startTS = startTS
        self._endTS = endTS
        bucketLen = (endTS - startTS) / numBuckets

        # Initialize bucket to None
        self._startTimestamps = [None] * numBuckets
        self._endTimestamps = [None] * numBuckets
        self._startMidQuotes = [None] * numBuckets
        self._endMidQuotes = [None] * numBuckets
        self._midReturns = [None] * numBuckets

        # Iterate over buckets, computing and saving
        # each bucket's return and start/end timestamps

        iBucket = -1  # The 0th bucket
        nRecs = data.getN()
        for startI in range(0, nRecs):
            timestamp = data.getMillisFromMidn(startI)
            if timestamp >= endTS:
                break
            if timestamp < startTS:
                continue
            
            newBucket = int(floor((timestamp - startTS) / bucketLen))

            # Save start timestamp and mid-quote price of the bucket
            self._endTimestamps[newBucket] = timestamp
            self._endMidQuotes[newBucket] = ( data.getAskPrice(startI) + data.getBidPrice(startI) ) / 2
            
            if iBucket != newBucket:
                # Save end timestamp and mid-quote price in the bucket
                self._startTimestamps[newBucket] = timestamp
                self._startMidQuotes[newBucket] = ( data.getAskPrice(startI) + data.getBidPrice(startI) ) / 2

                iBucket = newBucket

        for i in range(numBuckets):
            if self._startMidQuotes[i] == None or self._endMidQuotes[i] == None:
                continue
            self._midReturns[i] = (self._endMidQuotes[i] / self._startMidQuotes[i]) - 1.0

    # Get start time stamp of bucket specified by
    # index.
    def getStartTimestamp(self, index):
        return self._startTimestamps[index]

    # Get end time stamp of bucket specified by
    # index.
    def getEndTimestamp(self, index):
        return self._endTimestamps[index]

    # Get the mid-quote return of bucket specified by
    # index.
    def getMidReturn(self, index):
        return self._midReturns[index]

    # Get number of returns.
    def getN(self):
        return len(self._startTimestamps)
