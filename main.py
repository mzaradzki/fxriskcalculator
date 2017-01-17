
import os
import webapp2
from math import sqrt, exp, log
from var import covariance
from gaussian import ICNDIST
import copy

from google.appengine.ext.webapp import template


def gaussian(m=0, s=1):
    return lambda x : exp(-(x-m)*(x-m)/s/s)/sqrt(2.*3.1415)


def covar(x,y):
    if False:
        return 1.
    else:
        return covariance(x,y)


CURRENCIES = ['AUD','CAD','CHF','DKK','EUR','GBP','HKD','JPY','NOK','SEK','USD']


def PVol(nets):
    pvar = 0.
    for ccy1 in CURRENCIES:
        for ccy2 in CURRENCIES:
            pvar+= nets[ccy1]*nets[ccy2]*covar(ccy1,ccy2)

    return sqrt(pvar)

def dPVol(ccy, nets):
    cnets = copy.deepcopy(nets)
    bump = max(cnets.values()) * 0.0001
    #
    cnets[ccy] = cnets[ccy] + bump
    pvolup = PVol(cnets)
    #
    cnets[ccy] = cnets[ccy] - 2.*bump
    pvoldown = PVol(cnets)
    return (pvolup-pvoldown)/bump/2.

class MainPage(webapp2.RequestHandler):

    def get(self):
        
        template_values = { 'currencies':CURRENCIES, }
        path = os.path.join(os.path.dirname(__file__), 'form.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):

        assets = {}
        for ccy in CURRENCIES:
            assets[ccy] = float(self.request.get('asset_'+ccy))
        
        liabilities = {}
        for ccy in CURRENCIES:
            liabilities[ccy] = float(self.request.get('liability_'+ccy))

        nets = {}
        for ccy in CURRENCIES:
            nets[ccy] = assets[ccy] - liabilities[ccy]

        pvol = PVol(nets)

        var05 = pvol*ICNDIST(.05)

        G = gaussian(0.,pvol)

        points = []
        for tenX in range(-30,31):
            dico = {'x':pvol*tenX/10., }
            dico['y'] = G(dico['x'])
            if dico['x'] <= var05:
                dico['flagC'] = 'true'
            else:
                dico['flagC'] = 'false'
            dico['flagE'] = dico['flagC']
            points.append(dico)

        table = []
        for ccy in CURRENCIES:
            table.append([ccy, int(assets[ccy]), int(liabilities[ccy]), int(nets[ccy]), int(dPVol(ccy,nets)*var05/pvol*nets[ccy])])
        
        template_values = { 'title':'Portfolio Risk Distribution (5% Annual Risk is '+str(int(var05))+' Euro)', 'label':'probability density', 'points':points, 'table':table, }
        path = os.path.join(os.path.dirname(__file__), 'chart.html')
        self.response.out.write(template.render(path, template_values))


application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
