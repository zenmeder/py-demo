#__author__ = "ben"  #coding:utf-8
import numpy as np
import csv
from sklearn.cross_validation import train_test_split  

X1=[]
X2=[]
Y1=[]
Y2=[]

###读入脉冲星的数据
csvfile = open('HTRU_2.csv', 'rU')
reader = csv.reader(csvfile)
for line in reader:
    if line[-1] == "1":
        X1.append(np.array(line).astype("float64")[:-1])
        Y1.append(1)
    else:
        X2.append(np.array(line).astype("float64")[:-1])
        Y2.append(0)

t_xtrain, t_xtest, t_ytrain, t_ytest = train_test_split(X1,Y1, test_size = 0.3)
f_xtrain, f_xtest, f_ytrain, f_ytest = train_test_split(X2,Y2, test_size = 0.3)

ver_t = [0,0,0,0,0,0,0,0]
ver_f = [0,0,0,0,0,0,0,0]
for i in range(len(t_xtrain)):
    for j in range(8):
        ver_t[j] += t_xtrain[i][j]

for i in range(len(f_xtrain)):
    for j in range(8):
        ver_f[j] += f_xtrain[i][j]

for i in range(8):
    ver_t[i] /= len(t_xtrain)
    ver_f[i] /= len(f_xtrain)

print(ver_t)
print(ver_f)

X1 = np.matrix(X1).transpose()
X2 = np.matrix(X2).transpose()

def Rayleigh_quotient(W,X1,X2):
    sigma1 = np.array(X1.mean(1))
    sigma2 = np.array(X2.mean(1))
    cov1 = np.cov(X1)
    cov2 = np.cov(X2)
    Sw = cov1 + cov2
    Sb = np.dot((sigma1 - sigma2),(sigma1-sigma2).T)
    J = np.dot(np.dot(W,Sb),W.T)/np.dot(np.dot(W,Sw),W.T)
    return J


def Query_W(X1,X2):
    sigma1 = np.array(X1.mean(1))
    sigma2 = np.array(X2.mean(1))
    cov1 = np.cov(X1)
    cov2 = np.cov(X2)
    Sw = cov1 + cov2
    W = np.dot(Matrix_Reverse_By_SVD(Sw),(sigma1-sigma2))
    return W
#奇异值分解求逆
def Matrix_Reverse_By_SVD(Sw):
    U,S,V = np.linalg.svd(Sw)
    S_reverse = np.linalg.inv(Sw)
    Sw_reverse = np.dot(np.dot(U,S_reverse),V)
    return Sw_reverse

w = Query_W(X1,X2)
print(w)

def distance(x,y):
    sum=0
    for i in range(len(x)):
        sum+=(y[i]-x[i])*(y[i]-x[i])
    return np.sqrt(sum)

def mul(x,y):
    z=[]
    for i in range(len(x)):
        z.append(x[i]*y[i])
    return z

t_count = 0
for i in range(len(t_xtest)):
    node = mul(t_xtest[i],w)
    dis1 = distance(node, ver_t)
    dis2 = distance(node, ver_f)
    if(dis1<dis2):
        t_count+=1

f_count = 0
for i in range(len(f_xtest)):
    node = mul(f_xtest[i],w)
    dis1 = distance(node, ver_t)
    dis2 = distance(node, ver_f)
    if(dis2>dis1):
        f_count+=1

print('正例预测正确数：',t_count)
print('测试的正例共有:',len(t_xtest))
print('正例预测准确率为：', t_count/len(t_xtest))
print('负例预测正确数：',f_count)
print('测试的负例共有:',len(f_xtest))
print('负例预测准确率为：', f_count/len(f_xtest))


