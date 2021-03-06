# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 11:26:12 2018

@author: Administrator
"""

import matplotlib.pyplot as plt
import trees

decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.6")
arrow_args = dict(arrowstyle="<-")

def plotNode(nodeTxt, centerPt, parentPt, nodeType):
	createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction',\
						 xytext=centerPt, textcoords='axes fraction',\
						 va="center", ha="center", bbox=nodeType, \
						 arrowprops=arrow_args)

def plotMidText(cntrPt, parentPt, txtString):
	xMid = cntrPt[0] + (parentPt[0]-cntrPt[0])/2.0
	yMid = cntrPt[1] + (parentPt[1]-cntrPt[1])/2.0
	createPlot.ax1.text(xMid, yMid, txtString)

def getNumLeafs(myTree):
	numLeafs = 0
	firstStr = myTree.keys()[0]
	secondDict = myTree[firstStr]
	for key in secondDict.keys():
		if type(secondDict[key]).__name__ == 'dict':
			numLeafs += getNumLeafs(secondDict[key])
		else:
			numLeafs += 1
	return numLeafs

def getTreeDepth(myTree):
	maxDepth = 0
	firstStr = myTree.keys()[0]
	secondDict = myTree[firstStr]
	for key in secondDict.keys():
		if type(secondDict[key]).__name__ == 'dict':
			thisDepth = getTreeDepth(secondDict[key]) + 1
		else:
			thisDepth = 1
		if thisDepth > maxDepth:
			maxDepth = thisDepth
	return maxDepth

def plotTree(myTree, parentPt, nodeTxt):
	numLeafs = getNumLeafs(myTree)
	depth = getTreeDepth(myTree)
	firstStr = myTree.keys()[0]
	cntrPt = (plotTree.xoff+(1.0+float(numLeafs))/2.0/plotTree.totalW, \
		   plotTree.yoff)
	plotMidText(cntrPt, parentPt, nodeTxt)
	plotNode(firstStr, cntrPt, parentPt, decisionNode)
	secondDict = myTree[firstStr]
	plotTree.yoff = plotTree.yoff - 1.0/plotTree.totalD
	for key in secondDict.keys():
		if type(secondDict[key]).__name__ == 'dict':
			plotTree(secondDict[key], cntrPt, str(key))
		else:
			plotTree.xoff = plotTree.xoff + 1.0/plotTree.totalW
			plotNode(secondDict[key], (plotTree.xoff, plotTree.yoff),\
				cntrPt, leafNode)
			plotMidText((plotTree.xoff, plotTree.yoff), cntrPt, str(key))
	plotTree.yoff = plotTree.yoff + 1.0/plotTree.totalD
	
def createPlot(inTree):
	fig = plt.figure(1, facecolor='white')
	fig.clf()
	axprops = dict(xticks=[], yticks=[])
	createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
	plotTree.totalW = float(getNumLeafs(inTree))
	plotTree.totalD = float(getTreeDepth(inTree))
	plotTree.xoff = -0.5/plotTree.totalW
	plotTree.yoff = 1.0
	plotTree(inTree, (0.5, 1.0), '')
	plt.show()

myTree = trees.myTree
print myTree
createPlot(myTree)