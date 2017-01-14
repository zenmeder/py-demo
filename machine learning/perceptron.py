#encoding:utf-8
import csv
import random
from sklearn.cross_validation import train_test_split  
import numpy as np

def sign(v):
	if(v>0) :
		return 1
	else:
		return -1
csvfile = open('HTRU_2.csv', 'rU')
reader = csv.reader(csvfile)
data = []
tmp = [] 
for line in reader:
	for i in range(8):
		line[i] = float(line[i])
	line[-1] = int(line[-1]);
	tmp = line[:-1]
	if(line[-1]):
		tmp.append(int(1))
	else:
		tmp.append(int(-1))
	data.append(tmp)

TRUE_SAMPLE = []
FALSE_SAMPLE = []
for i in range(len(data)):
	if(data[i][-1] == 1):
		TRUE_SAMPLE.append(data[i])
	else:
		FALSE_SAMPLE.append(data[i])
TX = []
TY = []
for i in range(len(TRUE_SAMPLE)):
	TX.append(TRUE_SAMPLE[i][:-1])
	TY.append(int(1))

FX = []
FY = []
for i in range(len(FALSE_SAMPLE)):
	FX.append(FALSE_SAMPLE[i][:-1])
	FY.append(int(-1))


tx_train, tx_test, ty_train, ty_test = train_test_split(TX, TY, test_size = 0.3)
fx_train, fx_test, fy_train, fy_test = train_test_split(FX, FY, test_size = 0.3)

t_train_data = TRUE_SAMPLE+FALSE_SAMPLE

weight = [0,0,0,0,0,0,0,0]
bias = 0
learning_rate = 0.8

train_num = 1000000

for i in range(train_num):
	train = random.choice(t_train_data)
	x1,x2,x3,x4,x5,x6,x7,x8,y  = train
	predict = sign(weight[0]*x1+
		weight[1]*x2+
		weight[2]*x3+
		weight[3]*x4+
		weight[4]*x5+
		weight[5]*x6+
		weight[6]*x7+
		weight[7]*x8+
		bias)
	if y*predict <=0:
		weight[0] = weight[0] +learning_rate*y*x1
		weight[1] = weight[1] +learning_rate*y*x2
		weight[2] = weight[2] +learning_rate*y*x3
		weight[3] = weight[3] +learning_rate*y*x4
		weight[4] = weight[4] +learning_rate*y*x5
		weight[5] = weight[5] +learning_rate*y*x6
		weight[6] = weight[6] +learning_rate*y*x7
		weight[7] = weight[7] +learning_rate*y*x8
	bias = bias + learning_rate*y
print(weight, bias)
t_count = 0
f_count = 0
for i in range(len(tx_test)):
	t_predict = sign(weight[0]*tx_test[i][0]+
		weight[1]*tx_test[i][1]+
		weight[2]*tx_test[i][2]+
		weight[3]*tx_test[i][3]+
		weight[4]*tx_test[i][4]+
		weight[5]*tx_test[i][5]+
		weight[6]*tx_test[i][6]+
		weight[7]*tx_test[i][7]+
		bias
		)
	if(t_predict==1):
		t_count+=1
print('正例预测正确数：',t_count)
print('测试的正例共有:',len(tx_test))
print('正例预测准确率为：', float(t_count)/len(tx_test))
for i in range(len(fx_test)):
	f_predict = sign(weight[0]*fx_test[i][0]+
		weight[1]*fx_test[i][1]+
		weight[2]*fx_test[i][2]+
		weight[3]*fx_test[i][3]+
		weight[4]*fx_test[i][4]+
		weight[5]*fx_test[i][5]+
		weight[6]*fx_test[i][6]+
		weight[7]*fx_test[i][7]+
		bias
		)
	if(f_predict==(-1)):
		f_count+=1
print('负例预测正确数：',f_count)
print('测试的负例共有:',len(fx_test))
print('负例预测准确率为：', float(f_count)/len(fx_test))


