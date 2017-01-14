#encoding:utf-8
import numpy as np
import csv
from sklearn.cross_validation import train_test_split  

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

def sigmoid(inX):
    return float(1.0)/(1+np.exp(-inX))

def gradAscent(dataMatIn, classLabels):
    dataMatrix = np.mat(dataMatIn)             #convert to NumPy matrix
    labelMat = np.mat(classLabels).transpose() #convert to NumPy matrix
    
    m,n = np.shape(dataMatrix)
    alpha = 0.001
    maxCycles = 500
    weights = np.ones((n,1))
    
    for k in range(maxCycles):              #heavy on matrix operations
        h = sigmoid(dataMatrix*weights)     #matrix mult
        error = (labelMat - h)              #vector subtraction
        weights = weights + alpha * dataMatrix.transpose()* error #matrix mult
    return weights

def GetResult():
    dataMat,labelMat=loadDataSet()
    weights=gradAscent(dataMat,labelMat)
    print(weights)

    return weights

def plotBestFit(weights):
    dataMat,labelMat=loadDataSet()
    dataArr = array(dataMat)

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

    return xf_test, yf_test, xt_test, yt_test

def count(weights):
    dataMat,labelMat=loadDataSet()
    dataMatrix = np.mat(dataMat) 

    xf_test, yf_test, xt_test, yt_test = divide(dataMat,labelMat)
    for i in range(len(xt_test)):
        print(xt_test[i])
        print(weights)
        sim = sigmoid(xt_test[i]*weights)
        print(sim)

        return 0
     
if __name__=='__main__':
    weights = GetResult()
    count(weights)


