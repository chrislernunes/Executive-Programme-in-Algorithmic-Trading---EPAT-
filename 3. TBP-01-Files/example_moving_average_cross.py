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

import pandas as pd
def initialize(context):
    context.run_once=False # To show if the handle_data has been run in a day
    context.security=symbol('SPY') # Define a security for the following part
    
def handle_data(context, data):
    sTime=get_datetime('US/Eastern') 
    # sTime is the IB server time. 
    # get_datetime() is the build-in fuciton to obtain IB server time 
    if sTime.weekday()<=4:
        # Only trade from Mondays to Fridays
        if sTime.hour==15 and sTime.minute==58 and context.run_once==True:
            # 2 minutes before the market closes, reset the flag
            # get ready to trade
            context.run_once=False
        if sTime.hour==15 and sTime.minute==59 and context.run_once==False:
            # 1 minute before the market closes, do moving average calcualtion
            # if MA(5) > MA(15), then BUY the security if there is no order
            # Keep the long positions if there is a long position
            # if MA(5) < MA(15), clear the position
            hist = data.history(context.security, 'close', 20, '1d')

            mv_5=pd.rolling_mean(hist,5)[-1]            
            mv_15=pd.rolling_mean(hist,15)[-1] 
            if mv_5>mv_15:         
                print(sTime)
                orderId=order_target_percent(context.security, 1.0)
                #order_status_monitor(orderId, target_status='Filled')
            else:
                orderId=order_target_percent(context.security, -1.0)
                #order_status_monitor(orderId, target_status='Filled')
            context.run_once=True