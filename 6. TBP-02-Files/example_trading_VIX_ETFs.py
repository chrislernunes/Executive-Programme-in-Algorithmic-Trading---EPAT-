# -*- coding: utf-8 -*-
'''
There is a risk of loss in stocks, futures, forex and options trading. Please
trade with capital you can afford to lose. Past performance is not necessarily 
indicative of future results. Nothing in this computer program/code is intended
to be a recommendation to buy or sell any stocks or futures or options or any 
tradable securities. 
All information and computer programs provided is for education and 
entertainment purpose only; accuracy and thoroughness cannot be guaranteed. 
Readers/users are solely responsible for how they use the information and for 
their results.

If you have any questions, please send email to IBridgePy@gmail.com
'''

'''
Trading VIX ETFs

Strategy:
The investment universe consists of 4 volatility ETNs - XIV, VXX, ZIV, VXZ. 
Investor uses 83 day momentum to rank these ETNs every day. Investor holds ETN 
with the highest past 83-day performance in case that past performance is 
positive. Trading signal is checked on a daily basis and portfolio is 
rebalanced accordingly.

Source Paper
GBerkman, Koch: Drained by DRIPS: The Hidden Cost of Buying on the Dividend Pay Date
http://papers.ssrn.com/sol3/papers.cfm?abstract_id=2172448
'''

def initialize(context):
    context.run_once=False # To show if the handle_data has been run in a day
    context.XIV=symbol('STK,VIX,USD') # Define a security for the following part
    context.VXX=symbol('STK,VXX,USD') # Define a security for the following part
    context.ZIV=symbol('STK,ZIV,USD') # Define a security for the following part
    context.VXZ=symbol('STK,VXZ,USD') # Define a security for the following part
    
def handle_data(context, data):
    sTime=get_datetime() 
    # sTime is the IB server time. 
    # get_datetime() is the build-in fuciton to obtain IB server time 
    if sTime.weekday()<=4:
        # Only trade from Mondays to Fridays
        if sTime.hour==15 and sTime.minute==58 and context.run_once==True:
            # 2 minutes before the market closes, reset the flag
            # get ready to trade
            context.run_once=False
        if sTime.hour==15 and sTime.minute==59 and context.run_once==False:
            # request historical data of 4 ETFs
            hist_XIV = request_historical_data(context.XIV, '1 day', '83 D')
            hist_VXX = request_historical_data(context.VXX, '1 day', '83 D')
            hist_ZIV = request_historical_data(context.ZIV, '1 day', '83 D')
            hist_VXZ = request_historical_data(context.VXZ, '1 day', '83 D')
            diff_XIV = hist_XIV['close'][-1] - hist_XIV['close'][0]
            diff_VXX = hist_VXX['close'][-1] - hist_VXX['close'][0]
            diff_ZIV = hist_ZIV['close'][-1] - hist_ZIV['close'][0]
            diff_VXZ = hist_XIV['close'][-1] - hist_VXZ['close'][0]
            tmp=sorted[[diff_XIV,context.XIV],[diff_VXX,context.VXX],[diff_ZIV,context.ZIV],[diff_VXZ,context.VXZ]]
            if tmp[3][0]>0:
                orderId=order_target(tmp[3][1], 100)
                order_status_monitor(orderId, target_status='Filled')
            else:
                close_all_positions()
            context.run_once=True    
     