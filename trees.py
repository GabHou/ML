# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 17:10:05 2018

@author: Administrator
"""

from math import log
import operator

def calcShannonEnt(dataSet):
	numEntries = len(dataSet)
	labelCounts = {}
	for featVec in dataSet:
		currentLabel = featVec[-1]
		if currentLabel not in labelCounts.keys():
			labelCounts[currentLabel] = 0;
		labelCounts[currentLabel] += 1
	shannonEnt = 0.0
	for key in labelCounts:
		prob = float(labelCounts[key])/numEntries
		shannonEnt -= prob * log(prob, 2)
	return shannonEnt

def splitDataSet(dataSet, axis, value):
	retDataSet = []
	for featureVec in dataSet:
		if(featureVec[axis] == value):
			reduceFeatVec = featureVec[:axis]#注意[]内没有,
			reduceFeatVec.extend(featureVec[axis+1:])
			retDataSet.append(reduceFeatVec)
	return retDataSet

def CreateDataSet():
	dataSet = [[1,1,3,'yes'],
				[1,1,1,'yes'],
				[1,0,1,'no'],
				[0,1,1,'no'],
				[0,0,1,'no']]
	labels = ['no surfacing', 'flippers', 'head']
	return dataSet, labels

dataSet, labels = CreateDataSet()
#print splitDataSet(dataSet, 1, 1)

def ChooseBestFeatureToSplit(dataSet):
	bestInfoGain = 0.0
	bestFeature = -1
	numFeatures = len(dataSet[0]) - 1
	baseEntropy = calcShannonEnt(dataSet)
	for i in range(numFeatures):
		featList = [example[i] for example in dataSet]
		uniqueVals = set(featList)
		newEntropy = 0.0
		for value in uniqueVals:
			subDataSet = splitDataSet(dataSet, i, value)
			prob = len(subDataSet)/float(len(dataSet))
			newEntropy += prob*calcShannonEnt(subDataSet)
		infoGain = baseEntropy - newEntropy
		if(infoGain > bestInfoGain):
			bestInfoGain = infoGain
			bestFeature = i
	if bestFeature == -1:    #如果intfoGain==0怎么办
		return 0
	return bestFeature
	
bestFeature = ChooseBestFeatureToSplit(dataSet)

def majorityCnt(classList):
	classCount = {}
	for vote in classList:
		if vote not in classCount:
			classCount[vote] = 0
		classCount[vote] += 1
	sortedClassCount = sorted(classCount.iteritems(),\
						   key=operator.itemgetter(1), reverse=True)
	return sortedClassCount[0][0]

def createTree(dataSet, labels):
	classList = [example[-1] for example in dataSet]
	if classList.count(classList[0]) == len(classList):
		return classList[0]
	if len(dataSet[0]) == 1:
		return majorityCnt(classList)
	bestFeat = ChooseBestFeatureToSplit(dataSet)
	bestFeatLabel = labels[bestFeat]
	myTree = {bestFeatLabel:{}}
	del(labels[bestFeat])
	featValues = [example[bestFeat] for example in dataSet]
	uniqueVals = set(featValues)
	for value in uniqueVals:
		subLabels = labels[:]
		myTree[bestFeatLabel][value] = createTree(splitDataSet\
				(dataSet, bestFeat, value), subLabels)
	return myTree

myTree = createTree(dataSet, labels)
#print myTree

def classify(inputTree, featLabels, testVec):
	firstStr = inputTree.keys()[0]
	secondDict = inputTree[firstStr]
	featIndex = featLabels.index(firstStr)
	for key in secondDict.keys():
		if testVec[featIndex] == key:
			if type(secondDict[key]).__name__ == 'dict':
				classRet = classify(secondDict[key], featLabels, testVec)
			else:
				classRet = secondDict[key]
	return classRet

print myTree
classRet = classify(myTree, ['no surfacing', 'flippers', 'head'], [1,1,1])
print classRet