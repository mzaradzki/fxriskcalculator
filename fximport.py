

import csv
import urllib

holder = {}

def fxdata(CCY='USD', info=True):
            
    if not(holder.has_key(CCY)):
        fxurl = 'http://sdw.ecb.europa.eu/quickviewexport.do?node=2018794&SERIES_KEY=120.EXR.D.'+CCY+'.EUR.SP00.A&type=csv'
        fxwebpage = urllib.urlopen(fxurl)

        datareader = csv.reader(fxwebpage)
        data = []
        for row in datareader:
            data.append(row)

        data = data[5:560]
        gdata = [] # filter out missing data
        for i in range(len(data)):
            try:
                gdata.append([data[i][0], float(data[i][1])])
            except:
                if info:
                    print data[i]

        holder[CCY] = gdata
    else:
        None
    
    return holder[CCY]

