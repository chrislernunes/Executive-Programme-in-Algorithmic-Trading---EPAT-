% bollinger_5min.m
clear;

[num]=xlsread('C:/Users/Ernest/Dropbox/BacktestWS/ES_2005_2007_5_min.xls');
cl=num(:, end);

lookback=12;
entryZscore=2;
exitZscore=0;

buyEntry=cl <= smartMovingAvg(cl, lookback)-entryZscore*smartMovingStd2(cl, lookback);
sellEntry=cl >= smartMovingAvg(cl, lookback)+entryZscore*smartMovingStd2(cl, lookback);

% buyEntry(isnan(buyEntry))=0;
% sellEntry(isnan(sellEntry))=0;

positionL=NaN(size(cl));
positionL(1)=0;
positionL(buyEntry)=1;
positionS=NaN(size(cl));
positionS(1)=0;
positionS(sellEntry)=-1;

buyExit= cl >= smartMovingAvg(cl, lookback)-exitZscore*smartMovingStd2(cl, lookback);
sellExit= cl <= smartMovingAvg(cl, lookback)+exitZscore*smartMovingStd2(cl, lookback);

% buyExit(isnan(buyExit))=0;
% sellExit(isnan(sellExit))=0;

positionL(buyExit)=0;
positionS(sellExit)=0;


positionL=fillMissingData(positionL);
positionS=fillMissingData(positionS);
position=positionL+positionS;

ret5min=(backshift(1, position).*(cl-backshift(1, cl)))./backshift(1, cl);
ret5min(isnan(ret5min))=0;
% plot(smartcumsum(ret5min));
plot(cumprod(ret5min+1)-1);

annavgret=252*(6.5*12+3)*smartmean2(ret5min)*100
annavgvol=sqrt(252*(6.5*12+3))*smartstd2(ret5min)*100
sharpe=annavgret/annavgvol
[maxDD maxDDD]=calculateMaxDD(smartcumsum(ret5min))

ret5min(isnan(ret5min))=0;
[maxDD maxDDD]=calculateMaxDD(cumprod(1+ret5min)-1)

fprintf(1, '===With transaction costs of 1bps===\n');
tcost=1/10000;

ret5min=(backshift(1, position).*(cl-backshift(1, cl)))./backshift(1, cl)-...
    tcost*abs(position-backshift(1, position));

plot(smartcumsum(ret5min));

annavgret=252*(6.5*12+3)*smartmean2(ret5min)*100
annavgvol=sqrt(252*(6.5*12+3))*smartstd2(ret5min)*100
sharpe=annavgret/annavgvol
[maxDD maxDDD]=calculateMaxDD(smartcumsum(ret5min))

avgNumHoldBars=calculateAvgHoldday(position)

totNumRTtrades=smartsum(abs(position-backshift(1, position)))/2

totRet=smartsum((backshift(1, position).*(cl-backshift(1, cl)))./backshift(1, cl))

avgRTretInBps=totRet/totNumRTtrades*10000