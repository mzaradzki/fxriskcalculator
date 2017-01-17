

from fximport import fxdata
from math import log, exp, sqrt


SQUARE = lambda x:x*x


def volatility(ccy='USD'):
    if ccy == 'EUR':
        return 0.
    else:
        ts = fxdata(ccy,False)

        logts = [log(fx) for d, fx in ts]

        rts = [(yafter-ybefore) for ybefore,yafter in zip(logts[0:-1],logts[1:])]

        size = len(rts)

        mean = sum(rts)/size
        
        var = sum(map(SQUARE, rts))/size

        return sqrt(var*255)


def covariance(ccy1='USD', ccy2='JPY'):
    if ccy1 == ccy2:
        return SQUARE(volatility(ccy1))
    elif 'EUR' in [ccy1, ccy2]:
        return 0.
    else:        
        ts1 = fxdata(ccy1,False)
        ts2 = fxdata(ccy2,False)

        logts1 = [log(fx) for d, fx in ts1]
        logts2 = [log(fx) for d, fx in ts2]

        rts1 = [(yafter-ybefore) for ybefore,yafter in zip(logts1[0:-1],logts1[1:])]
        rts2 = [(yafter-ybefore) for ybefore,yafter in zip(logts2[0:-1],logts2[1:])]

        size = len(rts1)

        mean1 = sum(rts1)/size
        mean2 = sum(rts2)/size
        
        var1 = sum(map(SQUARE, rts1))/size
        var2 = sum(map(SQUARE, rts2))/size
        
        return sum([(y1-mean1)*(y2-mean2) for y1,y2 in zip(rts1,rts2)])/size*255


def correlation(ccy1='USD', ccy2='JPY'):
    return covariance(ccy1,ccy2)/(volatility(ccy1)*volatility(ccy2))
