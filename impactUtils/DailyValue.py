
def getDailyValue(data, startTS, endTS):
    if startTS is None:
        startTS = 19 * 60 * 60 * 1000 / 2
    if endTS is None:
        endTS = 16 * 60 * 60 * 1000

    total_daily_value = 0

    for startI in range(0, data.getN()):
        timestamp = data.getTimestamp(startI)
        if timestamp >= endTS:
            break
        if timestamp < startTS:
            continue

        total_daily_value += data.getSize(startI) * data.getPrice(startI)
    
    return total_daily_value
