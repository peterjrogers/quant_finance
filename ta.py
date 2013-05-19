import math, array, numpy

class Ta():
    def __init__(self):
        
        """
        Technical analysis tools
        (c) 2012, 2013 Intelligent Planet Ltd
        """
        
        self.verbose = 1
        

    def calcema(period, close, lastema, ndigits):
        """
        Exponential Moving Average - EMA
        https://en.wikipedia.org/wiki/Moving_average
        """
        k = 2. / (period + 1.)
        k1 = 1. - k
        return round(((close * k) + (lastema * k1)), ndigits)


    def adi(self, period=7, ndigits=4):
        """
        Average Directional Index
        Developed in 1978 by J. Welles Wilder as an indicator of trend strength in a series of prices.
        http://en.wikipedia.org/wiki/Average_directional_movement_index
        """
        
        #track delta extreme price changes from yesterday
        delta_high = self.high - self.last_high
        delta_low = self.last_low - self.low

           
        #if today's range is within yesterdays then no directional movement occured
        if delta_high < 0 and delta_low < 0: dmpos = dmneg = 0
        if delta_high == delta_low: dmpos = dmneg = 0
           
        #if the range moved up it is a positive DM
        if delta_high > delta_low:
            dmpos = delta_high
            dmneg = 0
           
        #if the range moved down it is a negative DM
        if delta_high < delta_low:
            dmpos = 0
            dmneg = delta_low
           
        #get x period ema of directional movement
        try:
            self.last_admneg = admneg
            self.last_admpos = admpos            
        except:
            self.last_admneg = dmneg
            self.last_admpos = dmpos
        
        self.admneg = self.calcema(period, dmneg, self.last_admneg, ndigits)
        self.admpos = self.calcema(period, dmpos, self.last_admpos, ndigits)
           
        #get true range
        tr = max(self.high - self.low, self.high - self.last_close, self.last_close - self.low)
           
        #get x period ema of true range
        try: self.last_atr = self.atr
        except: self.last_atr = tr
        
        self.atr = self.calcema(self.adi_period, tr, self.last_atr, ndigits)
  
        #get directional index
        self.dipos = round(((self.admpos / self.atr) * 100), ndigits)
        self.dineg = round(((self.admneg / self.atr) * 100), ndigits)
       
        #get directional movement index
        if self.dipos != 0. and self.dineg != 0. :
            dx = ((self.dipos - self.dineg) / (self.dipos + self.dineg)) * 100
        else:
            dx = 0.
                       
        #get x period ema of true range
        try: self.last_adx = self.adx
        except: self.last_adx = dx
        
        self.adx = round(calcema(self.adi_period, dx, self.last_adx), ndigits)
        

    def trendi(self, p1=13, p2=13, ndigits=4):
        """
        Price trend indicator
        """
        
        #calc ema
        try: self.last_trendi_ema = self.trendi_ema
        except: self.last_trendi_ema = self.last_close
        
        self.trendi_ema = calcema(p1, self.close, self.last_trendi_ema, ndigits)
        
        #calc % gap between ema and ohlc
        og = ((self.open - self.trendi_ema) / self.open) * 100
        hg = ((self.high - self.trendi_ema) / self.high) * 100
        lg = ((self.low - self.trendi_ema) / self.low) * 100
        cg = ((self.close - self.trendi_ema) / self.close) * 100
           
        #calc weighted trend indicator
        try: self.last_trend = self.trend
        except: self.last_trend = 0.01
        
        self.trend = round(((og * 0.1) + (hg * 0.2) + (lg * 0.2) + (cg * 0.5)), ndigits)
           
        #get ema of trend
        try: self.last_atrend = self.atrend
        except: self.last_atrend = self.trend
        
        self.atrend = self.calcema(p2, self.trend, self.last_atrend, ndigits)
       
              
    def willr(self, period=13, ndigits=2):
        """
        Williams %R
        A technical analysis oscillator showing the current closing price in relation to the high and low of the past N days.
        It was developed by Larry Williams.
        http://en.wikipedia.org/wiki/Williams_%25R
        """
        
        if len(self.high_list) > period:
            #set slice parameters
            y = len(self.high_list) -1
            x = y - period
           
            #get highest high of period
            slice = self.high_list[x:y]
            slice.append(self.high)
            high = max(slice)
                           
            #get lowest low of period
            slice = self.low_list[x:y]           
            slice.append(self.low)
            low = min(slice)
                           
            #calculate willr - (high range - close) over (high range - low range) * -100
            try: self.last_willr = self.willr
            except: self.last_willr = 0.01
            
            self.willr = round((((high - self.close) / (high - low)) * -100), ndigits)
       
       
    def macd(self, p1=12, p2=26, p3=9, ndigits=4):
        """
        MACD (moving average convergence/divergence)
        A technical analysis indicator created by Gerald Appel in the late 1970s
        It is used to spot changes in the strength, direction, momentum, and duration of a trend in a stock's price.
        http://en.wikipedia.org/wiki/MACD
        """
        #get p1 and p2 ema's
        try:
            self.last_macd_p1_ema = self.macd_p1_ema
            self.last_macd_p2_ema = self.macd_p2_ema
        except:
            self.last_macd_p1_ema = self.last_macd_p2_ema = 0.01
        
        self.macd_p1_ema = self.calcema(p1, self.close, self.last_macd_p1_ema, ndigits)
        self.macd_p2_ema = self.calcema(p2, self.close, self.last_macd_p2_ema, ndigits)
        
        #get macd line
        self.macd_macd = round((self.macd_p1_ema - self.macd_p2_ema), ndigits)
        
        try: self.macd_last_signal = self.macd_signal
        except: self.macd_last_signal = self.macd_macd
           
        #calc a 9 period ema of the fast line to get signal line
        self.macd_signal = self.calcema(self.macd_p3, self.macd_macd, self.macd_last_signal, ndigits)
           
        #subtract signal from macd to obtain histogram
        try: 
            self.x_last_macd_hist = self.last_macd_hist
            self.last_macd_hist = self.macd_hist
        except: self.last_macd_hist = self.x_last_macd_hist = 0.01
        
        self.macd_hist = round((self.macd_macd - self.macd_signal), ndigits)

       
    def pre_ema(self, ndigits=4):
        """
        Preset EMA - Price & Volume
        """
        #check for first iteration with except
        try: 
            self.last_ema_12 = self.ema_12
            self.last_ema_13 = self.ema_13
            self.last_ema_26 = self.ema_26
            self.last_ema_65 = self.ema_65
            self.last_ema_200 = self.ema_200
            self.last_ema_vol = self.ema_vol
        except:
            self.last_ema_12 = self.last_ema_13 = self.last_ema_26 = self.last_ema_65 = self.last_ema_200 = self.last_close
            self.last_ema_vol = self.last_vol
        
        #update ema values
        self.ema_12 = self.calcema(12, self.close, self.last_ema_12, ndigits)
        self.ema_13 = self.calcema(13, self.close, self.last_ema_13, ndigits)
        self.ema_26 = self.calcema(26, self.close, self.last_ema_26, ndigits)
        self.ema_65 = self.calcema(65, self.close, self.last_ema_65, ndigits)
        self.ema_200 = self.calcema(200, self.close, self.last_ema_200, ndigits)
        self.ema_vol = self.calcema(13, self.vol, self.last_ema_vol, 0)    #integer


    def pvc(self, clist, period=20, ndigits=2):
        """
        Price & Volume channel
        Simple high and low channel for input list and period
        """
        if not clist: return
            
        y = len(clist) +1
        if y < period: return

        #set slice
        x = y - period
        slice = clist[x:y]
       
        #get high channel
        high = round((max(slice)), ndigits)
       
        #get low channel
        low = round((min(slice)), ndigits) 
           
        return low, high
       

    def stan_dev(self, ndigits=4):
        """
        Standard Deviation
        Shows how much variation from the average value
        https://en.wikipedia.org/wiki/Standard_Deviation
        """
        try: 
            if self.standev_return_list: pass
        except: self.standev_return_list = []
        
        #calc per interval return
        int_return = self.int_dif(self.close, self.last_close, ndigits)

        #add return to profit list    self.int_profit
        self.standev_return_list.append(int_return)
        
        #calc averge return - xbar
        xbar = sum(self.standev_return_list) / (len(self.standev_return_list))
        
        #get self.xbar - int_return for all data in period
        pos = 0 
        dset = 0.
        for item in self.standev_return_list:
            xminus = self.standev_return_list[pos] - xbar
            xsq = math.pow(xminus, 2)
            dset += xsq
            pos += 1
        
        #get standard deviation (percent)
        self.stdev = round((math.sqrt(dset / pos)), ndigits)
       
       
    def int_dif(self, start, end, ndigits=2):
        """
        Percentage difference between start and end price
        """
        
        return round((((end / start) - 1.) * 100.), ndigits)
       

    def max_drawdown(self):
        """
        Calculate maximum drawdown loss
        percentage equity value loss and duration
        """
        #check for loss and start loss series
        if self.close < self.last_close:
            if self.maxdraw_lock == 0:
                self.maxdraw_start = self.last_close
                self.maxdraw_lock = 1
                self.maxdraw_count = 1
           
        #check for end of loss series
        if self.maxdraw_lock == 1:
            if self.close > self.last_close:    #check if loss ended
                loss = self.int_dif(self.last_close, self.maxdraw_start)
                if loss < self.maxdraw_loss: #check for new maxloss
                    self.maxdraw_loss = loss
                    if self.maxdraw_count > self.maxdraw_time:    #check for higher maxloss duration
                        self.maxdraw_time = self.maxdraw_count
                self.maxdraw_lock = self.maxdraw_count = 0    #reset loss series after profit
            else:
                self.maxdraw_count +=1    #loss series continues
        
      
    def normal_dist(self, int_return, ndigits=2):
        """
        return normal distribution - increase as x times standard deviation - alert on > or < 3.5 x sigma
        """

        return round((int_return / self.stdev), ndigits)
        
        
