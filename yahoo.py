import urllib2

class Yahoo():
    def __init__(self):
        """
        Tools for downloading information from Yahoo finance
        (c) 2012, 2013 Intelligent Planet Ltd
        """
        
        self.verbose = 0
        self.url = 'http://ichart.finance.yahoo.com/table.csv?s=%s.L&amp;a=%s&amp;b=%s&amp;c=%s&amp;d=%s&amp;e=%s&amp;f=%s&amp;g=%s&amp;ignore=.csv'
        #self.url string format - (tick, start_month, start_day, start_year, end_day, end_month, end_year, period (d or w))
        self.url_date = [00, 01, 2005, 31, 11, 2020]    #default for udate in url_build
        
        
    ### intra day & informational
    
    def intra_url(self, tick, prop):    #intra day and information 
        return 'http://download.finance.yahoo.com/d/quotes.csv?s=%s.L&f=%s' % (tick.upper(), prop)
    
    
    def down_http(self, url):    #download data from yahoo
        return urllib2.urlopen(url).read()
        
    
    def intra_ohlcv(self, tick):    #get O H L C V for intra day
        return self.down_http(self.intra_url(tick, 'o0h0g0l1v0')).rstrip('\r\n').split(',')
        
        
    def shares_os(self, tick):    #get shares outstanding
        return int(''.join(self.down_http(self.intra_url(tick, 'j2')).lstrip(' ').rstrip('\r\n').split(',')))
        
    
    ### end of day
    
    def eod_url(self, tick, period, udate):    #historical EOD data - period is w for week or d for day
        return self.url % (tick.upper(), udate[0], udate[1], udate[2], udate[3], udate[4], udate[5], period)
           
           
    def eod_hist(self, tick, period, udate=''):    #download eod data and output as csv tuple
        if not udate: udate = self.url_date
        return self.list_make(self.down_http(self.eod_url(tick, period, udate)).rsplit('\n'))
        
        
    def list_make(self, clist):    #reverse order of list and strip out the header
        out = []
        for item in clist:
            if item and 'Date' not in item:    #header is Date,Open,High,Low,Close,Volume,Adj Close
                res = item.rsplit(',')
                out.insert(0, res[0:6])
        return out
        
        
    def iter_list(self, clist):    #iterate over list
        for item in clist: yield item
                
                
    def iter_day_week(self, clist):    #input daily data list and iterate daily & (created) weekly data in 2 row tuple output
        i = self.iter_list(clist)
        pos = 0 ; vol = [] ; price = [] ; row = ()
        for item in clist:    #stops iterator going off the end of the list and raising a stop error
            if self.verbose > 2: print item
            res = next(i)
            price.append(float(res[2]))    #high
            price.append(float(res[3]))    #low
            vol.append(int(res[5]))
            if pos == 0: open = res[1]
            if pos == 4: 
                row = res[0], open, max(price), min(price), res[4], sum(vol)    #created weekly EOD data
                if self.verbose > 1: print '#####', row
                price = [] ; vol = [] ; pos = -1
                
            if pos == -1: yield item, row
            else: yield item, ()

            pos += 1

        
    def notes(self):
     """
http://download.finance.yahoo.com/d/quotes.csv?s=AFR.L&f=o0h0g0l1v0

Open, high, low, close, vol - 131.60,131.90,129.20,130.00,4155892


http:/finance.yahoo.com/d/quotes.csv?s=AFR.L&f=b2b3d1d2a5b6ghl5k1k3ll1nopp5p6qrr1vy

103.80,103.60,"6/29/2012",-,2,402,10,041,101.20,105.90,"N/A","N/A - <b>103.80</b>",226,600,"Jun 29 - 

<b>103.80</b>",103.80,"AFREN",101.20,103.70,122.35,88.03,"N/A",606.43,"N/A",6713956,N/A

Start - http://download.finance.yahoo.com/d/quotes.csv?s= 

IDs - %40%5EDJI,GOOG

Properties - example name(n), symbol(s), the latest value(l1), open(o) and the close value of the last 

trading day(p)     f=nsl1op

Static part - At the end add the following to the URL - &e=.csv

QuoteProperty

Name     Description     Tag
AfterHoursChangeRealtime     After Hours Change (Realtime)     c8
AnnualizedGain     Annualized Gain     g3
Ask     Ask     a0
AskRealtime     Ask (Realtime)     b2
AskSize     Ask Size     a5
AverageDailyVolume     Average Daily Volume     a2
Bid     Bid     b0
BidRealtime     Bid (Realtime)     b3
BidSize     Bid Size     b6
BookValuePerShare     Book Value Per Share     b4
Change     Change     c1
Change_ChangeInPercent     Change Change In Percent     c0
ChangeFromFiftydayMovingAverage     Change From Fiftyday Moving Average     m7
ChangeFromTwoHundreddayMovingAverage     Change From Two Hundredday Moving Average     m5
ChangeFromYearHigh     Change From Year High     k4
ChangeFromYearLow     Change From Year Low     j5
ChangeInPercent     Change In Percent     p2
ChangeInPercentRealtime     Change In Percent (Realtime)     k2
ChangeRealtime     Change (Realtime)     c6
Commission     Commission     c3
Currency     Currency     c4
DaysHigh     Days High     h0
DaysLow     Days Low     g0
DaysRange     Days Range     m0
DaysRangeRealtime     Days Range (Realtime)     m2
DaysValueChange     Days Value Change     w1
DaysValueChangeRealtime     Days Value Change (Realtime)     w4
DividendPayDate     Dividend Pay Date     r1
TrailingAnnualDividendYield     Trailing Annual Dividend Yield     d0
TrailingAnnualDividendYieldInPercent     Trailing Annual Dividend Yield In Percent     y0
DilutedEPS     Diluted E P S     e0
EBITDA     E B I T D A     j4
EPSEstimateCurrentYear     E P S Estimate Current Year     e7
EPSEstimateNextQuarter     E P S Estimate Next Quarter     e9
EPSEstimateNextYear     E P S Estimate Next Year     e8
ExDividendDate     Ex Dividend Date     q0
FiftydayMovingAverage     Fiftyday Moving Average     m3
SharesFloat     Shares Float     f6
HighLimit     High Limit     l2
HoldingsGain     Holdings Gain     g4
HoldingsGainPercent     Holdings Gain Percent     g1
HoldingsGainPercentRealtime     Holdings Gain Percent (Realtime)     g5
HoldingsGainRealtime     Holdings Gain (Realtime)     g6
HoldingsValue     Holdings Value     v1
HoldingsValueRealtime     Holdings Value (Realtime)     v7
LastTradeDate     Last Trade Date     d1
LastTradePriceOnly     Last Trade Price Only     l1
LastTradeRealtimeWithTime     Last Trade (Realtime) With Time     k1
LastTradeSize     Last Trade Size     k3
LastTradeTime     Last Trade Time     t1
LastTradeWithTime     Last Trade With Time     l0
LowLimit     Low Limit     l3
MarketCapitalization     Market Capitalization     j1
MarketCapRealtime     Market Cap (Realtime)     j3
MoreInfo     More Info     i0
Name     Name     n0
Notes     Notes     n4
OneyrTargetPrice     Oneyr Target Price     t8
Open     Open     o0
OrderBookRealtime     Order Book (Realtime)     i5
PEGRatio     P E G Ratio     r5
PERatio     P E Ratio     r0
PERatioRealtime     P E Ratio (Realtime)     r2
PercentChangeFromFiftydayMovingAverage     Percent Change From Fiftyday Moving Average     m8
PercentChangeFromTwoHundreddayMovingAverage     Percent Change From Two Hundredday Moving Average     m6
ChangeInPercentFromYearHigh     Change In Percent From Year High     k5
PercentChangeFromYearLow     Percent Change From Year Low     j6
PreviousClose     Previous Close     p0
PriceBook     Price Book     p6
PriceEPSEstimateCurrentYear     Price E P S Estimate Current Year     r6
PriceEPSEstimateNextYear     Price E P S Estimate Next Year     r7
PricePaid     Price Paid     p1
PriceSales     Price Sales     p5
Revenue     Revenue     s6
SharesOwned     Shares Owned     s1
SharesOutstanding     Shares Outstanding     j2
ShortRatio     Short Ratio     s7
StockExchange     Stock Exchange     x0
Symbol     Symbol     s0
TickerTrend     Ticker Trend     t7
TradeDate     Trade Date     d2
TradeLinks     Trade Links     t6
TradeLinksAdditional     Trade Links Additional     f0
TwoHundreddayMovingAverage     Two Hundredday Moving Average     m4
Volume     Volume     v0
YearHigh     Year High     k0
YearLow     Year Low     j0
YearRange     Year Range     w0

If you've a tag with 0, like [a0], it doesn't matter if you use [a0] or just [a]. 

http://code.google.com/p/yahoo-finance-managed/wiki/csvQuotesDownload

http://chartapi.finance.yahoo.com/instrument/1.0/^nsei/chartdata;type=quote;range=1d/csv/

   """
   
   
