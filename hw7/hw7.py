#!/usr/bin/python

from numpy import *
from Dataset import Dataset

# Bayesian Classifier
# First, we need to build the probability model

d = Dataset("rec.sport.hockey.txt", "rec.sport.baseball.txt", cutoff=200)
(Xtrain, Ytrain, Xtest, Ytest) = d.getTrainAndTestSets(0.8, seed=1)
wordlist = d.getWordList()

def trainNaiveBayes(X, Y):
  # First, count frequencies given the category
  print Y
  yFlat = Y.flatten() 
  yOne = yFlat == 1
  yZero = yFlat == 0
  cat1 = array([sum(X[yOne,j]) / sum(yOne) for j in range(X.shape[1])])
  cat2 = array([sum(X[yZero,j]) / sum(Zero) for j in range(X.shape[1])])
  return (cat1, cat2)

def naiveBayesClassify(cat1, cat2, x):
  # Not actually implemented!
  return 1

# trainNaiveBayes(Xtrain,Ytrain)

def ridgeTrain(X, Y, l):
  return linalg.inv(X.T * X + l * identity(X.shape[0])) * X.T * Y

def ridgeClassify(X, w):
  return sum(dot(w, x[i])

def perceptronClassify(w, x):
  return sign(dot(w,x))

def perceptronTrain(X,Y, l = 1):
  w = randomVector(X.shape[0])
  perfect = False
  iterations = 0
  while (not perfect and iterations < 100):
    iterations += 1
    perfect = True
    for i in range(X.shape[1]):
      result = perceptronClassify(w, X[row])
      if (result != Y[row]):
        perfect = False
        w = w + l * (Y[row] * X[row])
  return (w, iterations)

def streamwiseClassify(X, Y, l):
  def error(w,X,y):
    return sum([sum(y - dot(w,x)) + l * sum(w[w != 0]) for x in X])
  cols = []
  w = zeros(X.shape[0])
  e = 1
  for j in range(X.shape[1]):
    newCols = cols + [j]
    w = ridgeTrain(X[:,cols], Y, l)
    curr = error(w,X,y)
    if curr < w:
      cols = newCols
  return ridgeTrain(X[:,cols],Y,l)

def stepwiseClassify(X, Y, l, maxFeatures = 50):
  def error(w,X,y):
    return sum([sum(y - dot(w,x)) + l * sum(w[w != 0]) for x in X])
  cols = []
  w = zeros(X.shape[0])
  e = 1
  bestError = None
  while cols.size < maxFeatures:
    best = None
    for j in (range(X.shape[1]) - cols):
      newCols = cols + [j]
      w = ridgeTrain(X[:,cols], Y, l)
      curr = error(w,X,y)
      if bestError == None or curr < bestError:
        best = j
        bestError = curr 
    if best == None:
      break
    else:
      cols = cols + [best]
  return ridgeTrain(X[:,cols],Y,l)
