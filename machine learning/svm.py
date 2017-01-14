# -*- coding: utf-8 -*-
from sklearn import svm
from sklearn import datasets
import numpy as np
from sklearn.cross_validation import train_test_split  
import csv

def divide(data, label):
    dataT = dataF = labelT = labelF = []
    for i in range(len(label)):
        if(label[i]):
            dataT.append(data[i])
            labelT.append(1)
        else:
            dataF.append(data[i])
            labelF.append(0)
    XT = np.array(dataT)
    YT = np.array(labelT)
    XF = np.array(dataF)
    YF = np.array(labelF)
    xf_train,xf_test,yf_train,yf_test = train_test_split(XF,YF,test_size=0.3)
    xt_train,xt_test,yt_train,yt_test = train_test_split(XT,YT,test_size=0.3)

    return xt_train, xf_train, xf_test, xt_test
def loadDataSet():
    csvfile = open('HTRU_2.csv', 'rU')
    reader = csv.reader(csvfile)
    dataMatIn = []
    labelMat = []
    for line in reader:
        for i in range(8):
            line[i] = float(line[i])
        line[-1] = int(line[-1]);
        dataMatIn.append(line[:-1])
        labelMat.append(line[-1])

    return dataMatIn,labelMat

dataMatIn, labelMat = loadDataSet()
clf = svm.SVC() #定义
xt_train, xf_train, xf_test, xt_test = divide(dataMatIn, labelMat)
clf.fit(dataMatIn,labelMat) #训练
tcount = fcount = 0
for i in range(len(xt_test)):
	if(int(clf.predict(xt_test[i]))):
		tcount+=1
for i in range(len(xf_test)):
	if(int(clf.predict(xf_test[i]) == 0)):
		fcount+=1
print tcount, fcount
