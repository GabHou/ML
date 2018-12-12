# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 16:50:58 2018

@author: Administrator
"""

from numpy import *
import operator
import matplotlib
import matplotlib.pyplot as plt

#创建简单数据集
def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group, labels

group,labels = createDataSet()

#KNN算法
def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX, (dataSetSize,1)) - dataSet
    sqDiffMat = diffMat ** 2
    sqDistance = sqDiffMat.sum(axis=1)
    distance = sqDistance ** 0.5
    sortedDistIndicies = distance.argsort()
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    sortedClassCount = sorted(classCount.items(),  key=operator.itemgetter(1),
                              reverse = True)
    return sortedClassCount[0][0]

label = classify0([0,1], group, labels, 2)
print(label)

#读取本地文件并创建矩阵和特征向量
def file2matrix(filename):
    fr = open(filename)
    arrayOLines = fr.readlines()
    numberOfLines = len(arrayOLines)
    returnMat = zeros((numberOfLines, 3))
    classLabelVector = []
    index = 0
    for line in arrayOLines:
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index, :] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    return returnMat, classLabelVector

datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')
print(datingDataMat)
print(datingLabels[0:20])

#画图
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(datingDataMat[:,0], datingDataMat[:,1], 15.0*array(datingLabels), 
		   15.0*array(datingLabels))
plt.show()


def autoNorm(dataSet):
	minValues = dataSet.min(0)
	maxValues = dataSet.max(0)
	ranges = maxValues - minValues
	normDataSet = zeros(shape(dataSet))
	m = dataSet.shape[0]
	normDataSet = dataSet - tile(minValues, (m,1))
	normDataSet = normDataSet/tile(ranges, (m,1))
	return normDataSet, ranges, minValues

normMat, ranges, minValues = autoNorm(datingDataMat)
print(normMat)

def datingClassTest():
	hoRatio = 0.10
	m = normMat.shape[0]
	numTestVecs = int(m*hoRatio)
	errorCount = 0.0
	for i in range(numTestVecs):
		classifierResult = classify0(normMat[i,:], normMat[numTestVecs:m, :],
							   datingLabels[numTestVecs:m], 3)
		print 'the classifier came back with: %d, the real answer is: %d'%(classifierResult, datingLabels[i])
		if(classifierResult != datingLabels[i]):
			errorCount += 1.0
	print 'the total error rate is %f' %(errorCount/float(numTestVecs))
	
datingClassTest()

def classifyPerson():
	resultList = ['not at all', 'in small doses', 'in large doses']
	percentTats = float(raw_input("persentage of time spent playing video games?"))
	ffMiles = float(raw_input("frequent flier miles earand per year?"))
	iceCream = float(raw_input("liters of ice cream consumed per year?"))
	inArr = array([ffMiles, percentTats, iceCream])
	label = classify0((inArr-minValues)/ranges, normMat, datingLabels, 3)
	print 'You will probably like this person: ', resultList[label - 1]
	
classifyPerson()