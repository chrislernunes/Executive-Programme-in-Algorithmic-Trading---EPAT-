import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import svm
from sklearn import linear_model


df=pd.read_csv("data.csv")

train_set=df.iloc[:int(len(df)*0.7),:]
test_set=df.iloc[int(len(df)*0.7):,:]

train_col=list(train_set)
train_col.remove('target')
train_col.remove('Date')

train_X=train_set[train_col]
train_y=train_set['target']

test_X=test_set[train_col]
test_y=test_set['target']

print train_X.shape
print train_y.shape
print test_X.shape
print test_y.shape

clf_rfc = RandomForestClassifier(n_estimators=100,max_features=5,max_depth=10, random_state=0)
clf_rfc.fit(train_X,train_y)
print clf_rfc.score(test_X,test_y)

clf_gbc=GradientBoostingClassifier(n_estimators=100, learning_rate=0.1,max_depth=1, random_state=0)
clf_gbc.fit(train_X,train_y)
print clf_gbc.score(test_X,test_y)

clf_svc = svm.SVC()
clf_svc.fit(train_X,train_y)
print clf_svc.score(test_X,test_y)

clf_logisticR= linear_model.LogisticRegression()
clf_logisticR.fit(train_X,train_y)
print clf_logisticR.score(test_X,test_y)

