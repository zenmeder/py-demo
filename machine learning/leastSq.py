# Required Packages
#encoding:utf-8
import matplotlib.pyplot as plt
import numpy as np
import csv
from sklearn import datasets, linear_model
from scipy.optimize import leastsq
from sklearn.cross_validation import train_test_split  

def func(p,x):
    weight_vector = p
    np.array(weight_vector)
    return np.dot(x,weight_vector)

def error(p,x,y,s):
    print(s)
    return func(p,x)-y 

csvfile = open('HTRU_2.csv', 'rU')
reader = csv.reader(csvfile)
data = []
labels = [] 
for line in reader:
	for i in range(8):
		line[i] = float(line[i])
	line[-1] = int(line[-1]);
	data.append(line[:-1])
	labels.append(line[-1])

dataT = []
labelT = []
dataF = []
labelF = []
for i in range(len(labels)):
	if(labels[i]):
		dataT.append(data[i][:-1])
		labelT.append(data[i][-1])
	else:
		dataF.append(data[i][:-1])
		labelF.append(data[i][-1])
p0=[0,0,0,0,0,0,0]
s="Test the number of iteration"

XT = np.array(dataT)
YT = np.array(labelT)
print(type(XT))
xt_train,xt_test,yt_train,yt_test = train_test_split(XT,YT,test_size=0.3)
resT = leastsq(error,p0,args=(xt_train,yt_train,s))

XF = np.array(dataF)
YF = np.array(labelF)
xf_train,xf_test,yf_train,yf_test = train_test_split(XF,YF,test_size=0.3)
resF = leastsq(error,p0,args=(xf_train,yf_train,s))

print("脉冲星的最小二乘",resT[0])
print("非脉冲星的最小二乘",resF[0])

def distance(type, num, argc):
	sq = 0
	sum = 0
	if(argc):
		xtest = xt_test
		ytest = yt_test
	else:
		xtest = xf_test
		ytest = yf_test
	if(type):
		for i in range(7):
				sq += resT[0][i]*resT[0][i]
		for j in range(7):
			sum += xtest[num][j]* resT[0][j]
		sum -= ytest[num]
		dis = np.abs(sum)/np.sqrt(sq+1)
	else:
		for i in range(7):
				sq += resF[0][i]*resF[0][i]
		for j in range(7):
			sum += xtest[num][j]* resF[0][j]
		sum -= ytest[num]
		dis = np.abs(sum)/np.sqrt(sq+1)
	return dis

t_count = 0
for i in range(len(xt_test)):
	if((distance(1, i,1)-distance(0,i,1))<0):
		t_count+=1
print(t_count, len(xt_test))

f_count = 0
for i in range(len(xf_test)):
	if((distance(0, i,0)-distance(1,i,0))<0):
		f_count+=1
print(f_count, len(xf_test))

print("正例预测正确数：",t_count)
print('测试的正例共有:',len(xt_test))
print('正例预测准确率为：', t_count/len(xt_test))
print('负例预测正确数：',f_count)
print('测试的负例共有:',len(xf_test))
print('负例预测准确率为：', f_count/len(xf_test))
