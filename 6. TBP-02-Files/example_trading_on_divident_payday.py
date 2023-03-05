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
Trading on divident payday

Strategy:
The investment universe consists of stocks from NYSE, AMEX and NASDAQ that 
offer company-sponsored DRIPs(Dividend Reinvestment Plans). Each day at close 
investors buy stocks which have dividend payday on next working day and hold 
these stocks for 1 day. Stocks are weighted equally.

Source Paper
http://papers.ssrn.com/sol3/papers.cfm?abstract_id=2172448

Abstract:
On the day that dividends are paid we find a significant positive mean abnormal
 return, followed by a reversal that negates most of this price appreciation. 
 This temporary dividend pay date effect has grown in magnitude since the 1970’s,
 and is concentrated among high dividend yield stocks that offer dividend 
 reinvestment plans (DRIPs). Since the mid-1990s, these stocks yield a mean 
 abnormal return close to 0.5% on the dividend pay date. This temporary 
 inflation is larger in magnitude for stocks subject to greater limits to 
 arbitrage. Quarterly profits from a trading strategy to exploit this anomaly 
 are economically significant, and related to time series movements in market 
 sentiment, transaction costs, the dividend premium, and the VIX. For investors 
 who reinvest their dividends on the pay date, this temporary inflation 
 represents a substantial implicit transaction cost.

DRIP list
https://www-us.computershare.com/Investor/3x/Plans/PlansList.asp?stype=drip
http://www.dripadvice.com/all_plans.html

Dividend Calendar
http://www.nasdaq.com/dividend-stocks/dividend-calendar.aspx?date=2017-Jan-23
'''
from bs4 import BeautifulSoup
from urllib2 import urlopen
import datetime as dt
def get_dividend(adt):
    str_adt= adt.strftime('%Y-%b-%d')
    try:
        url ='http://www.nasdaq.com/dividend-stocks/dividend-calendar.aspx?date=%s' %(str_adt,)
        webpage = urlopen(url)
    except:
        print __name__+'::get_dividend:ERROR'
        exit()
    final=[]
    soup = BeautifulSoup(webpage)
    x=soup.find_all('a')
    for item in x:
        if item.parent.name=='td':
            if 'dividend-history' in item['href']:
                final.append( item['href'].split('/')[-2].upper())
    return final

def initialize(context):
    context.run_once=False # To show if the handle_data has been run in a day
    context.dripList=['VOD', 'VMC', 'WBS', 'WY', 'WGL', 'XYL', 'WM', 'VIA', 'WEC',
                      'NEWP', 'BIDU', 'NFG', 'CASY', 'ARB', 'EGN', 'KSS', 'HRL',
                      'ARI', 'BMY', 'ELN', 'CHL', 'AVLY', 'PSX', 'IBKC', 'HH',
                      'HBNC', 'HARL', 'GFED', 'BHI', 'FOFB', 'FNBN', 'FSGI', 'FPTB',
                      'FXNC', 'FNCB', 'FMFC', 'FKYS', 'FFKY', 'FCCO', 'FCBC', 'FBNC',
                      'FDBC', 'FSBI', 'FMNB', 'FMAO', 'FNB', 'FMBM', 'ESBF', 'ENBP',
                      'EVBS', 'DNBF', 'DIMC', 'CSBB', 'CHBH', 'CNIG', 'CBKM', 'CTWS',
                      'CBIN', 'CMTV', 'CNAF', 'CMOH', 'COH', 'CCNE', 'CSBC', 'COFS',
                      'CHS', 'CVBK', 'CNBC', 'CECB', 'CBTC', 'WABC', 'CBKN', 'WIN',
                      'CAFI', 'DPZ', 'BDGE', 'BORT', 'BNCN', 'BHLB', 'BAYK', 'BMRC', 
                      'BKMU', 'BTFG', 'BSX', 'WHR', 'XRX', 'FUR', 'WSBC', 'WLP', 'WDR',
                      'VFC', 'UNM', 'UHT', 'UBOH', 'UMBF', 'TG ', 'TTO', 'TDW', 'TICC',
                      'PNC', 'MTW', 'FHCO', 'THRD', 'FCAP', 'TIN', 'TDS', 'TTDKY', 
                      'SKT', 'SF', 'STFC', 'S', 'OKSB', 'LNCE', 'SBSI', 'CSX', 'SLM',
                      'SCBT', 'SGK', 'RBCAA', 'RRD', 'PMD', 'PPS', 'GTY', 'PPS', 'PBI',
                      'PLL', 'NOC', 'FFFD', 'FBMI', 'NDSN', 'UFCS', 'NSRGY', 'MYE', 'MVC',
                      'VIVO', 'LPX', 'MBWM', 'ITYBY', 'JKHY', 'ITW', 'HDNG', 'FPFC', 'HQH',
                      'FFCH', 'AKS', 'HOMB', 'FFBC', 'HLAN', 'GEF', 'FDEF', 'GCBC', 'GABC',
                      'GVA', 'NVS', 'GPC', 'GPN', 'WRI', 'CIM', 'EGAS', 'WRE', 'FNFI', 'FMBH', 
                      'EVBN', 'ELY', 'CVS', 'CI', 'ETR', 'DEO', 'BOH', 'FLIC', 'UTL', 'EBTC',
                      'ECL', 'TRST', 'EGLE', 'DGICA', 'DGAS', 'CR', 'CPY', 'ADC', 'CBE', 'PSS', 
                      'CLPHY', 'HME', 'FCF', 'CNL', 'CLF', 'CHCO', 'CL', 'CHK', 'UL', 'UGI', 
                      'CTL', 'DFS', 'CNKA', 'DE', 'M', 'COF', 'DBD', 'JCP', 'CLNH', 'CSL', 
                      'HMIN', 'ESBK', 'HAL', 'GNW', 'GRVY', 'GFI', 'GSK', 'AUBN', 'ARTNA',
                      'TKC', 'WBM', 'GRC', 'LG', 'CAR', 'ANDE', 'STLD', 'AMNB', 'SWK', 'CCL',
                      'TCB', 'SWN', 'SUG', 'SNA', 'SHPGY', 'RBN', 'RF', 'DGX', 'POL', 'PCL', 
                      'PM', 'PTNR', 'ODOP', 'NST', 'NOVS.PK', 'NEE', 'NWL', 'NBBC', 'NHI', 
                      'MOLX', 'MDR', 'MPC', 'MRO', 'CLI', 'LYTS', 'KBALB', 'KEY', 'KMPR', 'KB', 
                      'ITC', 'SFI', 'IIBK', 'HBAN', 'GRT', 'FTR', 'AV', 'MT', 'ABCB', 'AGYS', 
                      'AIR', 'GXP', 'FLO', 'OSK', 'PNW', 'STI', 'MORN', 'BBT', 'SE', 'VTR', 
                      'XEL', 'STJ', 'PPL', 'TRV', 'SWX', 'LUV', 'NVE', 'MDT', 'MDU', 'MKC', 
                      'MMC', 'LRY', 'JCI', 'IMN', 'IDA', 'AWR', 'ACH', 'AWC', 'ATI', 'ALSK', 
                      'AYI', 'HNZ', 'HIW', 'HTCO', 'HCP', 'HWKN', 'HGIC', 'FUL', 'HRB', 'GG', 
                      'GOV', 'GIS', 'GCI', 'FO', 'FCE.A', 'FLS', 'FAF', 'EDE', 'LLY', 'EIX', 
                      'EGP', 'DTE', 'DCI', 'DG', 'DRI', 'CMI', 'CLGX ', 'CAG', 'CWH', 'CMA', 
                      'CMCSK', 'CHE', 'SCHW', 'CBS', 'BGG', 'BRE', 'BRC', 'BOKF', 'BKH', 'BMS', 
                      'AEC', 'ASBC', 'AOS', 'AM', 'ALL', 'APA', 'LNT', 'ALE ', 'AGN', 'ALB', 'AGL', 
                      'YORW', 'WSFS', 'WWE', 'WWD', 'WNS', 'UIL', 'TRMK', 'TRMD', 'TMP', 'TIBB', 
                      'TSCDY', 'TFX', 'TSTY', 'SBBX', 'SUSQ', 'SEOAY', 'STT', 'SPAR', 'SSS', 'SWKS', 
                      'K', 'USB', 'KFT', 'WFC', 'SRE', 'SAP', 'STBA', 'RSO', 'RELV', 'RAS', 'PBIB', 
                      'PMI', 'PEO', 'PNNW', 'BTU', 'PCX', 'NUTR', 'NWN', 'NWBI', 'NRF', 'NSFC', 'NNN', 
                      'MAA', 'MDH', 'MPR', 'MBTF', 'MEE', 'MPET', 'LUX', 'JPST', 'JFBC', 'ISIL', 
                      'TEG', 'INFY', 'IPCC', 'IFNNY', 'IBCP', 'IMPUY', 'IBN', 'CATS', 'HOC', 'GBCI', 
                      'GAM', 'FSP', 'FE', 'FNFG', 'FITB', 'FIATY', 'FRT', 'EFX', 'EDR', 'EMN', 'EML', 
                      'DRE', 'DCOM', 'DTEGY', 'CW', 'CS', 'CBRL', 'CLB', 'CWCO', 'CBU', 'CMCO', 'CRBC', 
                      'CV', 'CARV', 'TAST', 'CRRB', 'CRS', 'LSE', 'CT', 'CAC', 'CWT', 'BRKL', 'BCO', 
                      'BOBE', 'BHB', 'BMI', 'AROW', 'ACI', 'ANH', 'AME', 'AWK', 'ACO', 'AKZOY', 'APD', 
                      'ADX', 'AKR', 'FBR', 'FSS', 'ESS', 'ERIC', 'EPR', 'DPS', 'DEG', 'CYS', 'CTB', 
                      'CLC', 'CIA', 'CPK', 'CHG', 'BCR', 'BPL', 'BC', 'BTH', 'BHP', 'BANR', 'BKSC', 
                      'SNE', 'AIG', 'BASFY.PK', 'UNH', 'VLO', 'DOM', 'COST', 'DUK', 'Pixar DRIP', 
                      'AMZN', 'AVY', 'ING', 'KR', 'TM', 'TGT', 'RDS.A', 'JPM', 'BRK', 'ASH', 'AJC', 
                      'AGNC', 'DRIP Advice Disclaimer', 'AEX', 'HSY', 'YHOO', 'USG', 'TSN', 'THI', 
                      'SJM', 'GT', 'CLX', 'TXN', 'SUN', 'SWY', 'QCOM', 'PGN', 'NOK', 'NKE', 'MAC', 
                      'INTC', 'HRC', 'HOG', 'HBI', 'FDX', 'EQ', 'CHFC', 'CPB', 'BGP', 'BBY', 'BD', 
                      'AIT', 'AOC', 'AMP', 'AET', 'BP', 'BZH', 'ATO', 'CCF', 'BUD', 'DELL', 'YUM', 
                      'C', 'CAT', 'HPQ', 'JNJ', 'MRK', 'DD', 'VZ', 'PG', 'DIS', 'AXP', 'MO', 'T', 
                      'KO', 'MCD', 'PAYX', 'WAG', 'WTR', 'AA', 'MMM', 'PEP', 'LMT', 'PFE', 'CVX', 
                      'COP', 'CSCO', 'SBUX', 'GOOG', 'GE', 'WMT', 'SIRI', 'AAPL', 'MSFT', 'MAT', 
                      'MAR', 'LXBK', 'LOW', 'KYO', 'PHG', 'KMB', 'KSE', 'ICI', 'HD', 'MLHR', 'HR', 
                      'HAS', 'HCM', 'GM', 'F', 'FNM', 'XOM', 'EXC', 'EQR', 'EOP', 'EP', 'EK', 'DPL', 
                      'CCBD', 'CLP', 'CE', 'BAB', 'BXP', 'BA', 'BAX', 'BLL', 'BAC', 'AXA', 'AEP', 
                      'AA', 'ABT', 'IBM']    
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
            dividendList=get_dividend(dt.date.today())

            # check if the stock has DRIP, save them in finalList
            finalList=[]
            for stk in dividendList:
                if stk in context.dripList:
                    finalList.append(stk)
                
            if len(finalList)!=0:
                value=show_account_info('cash')/len(finalList)
                orderIdList=[]
                for stk in dividendList:
                    orderId=order(symbol(stk), value/show_real_time_price(symbol(stk),'ask_price'))
                    orderIdList.append(orderId)
                for orderId in orderIdList:
                    order_status_monitor(orderId, target_status='Filled')
            else:
                close_all_positions()
            context.run_once=True    
     