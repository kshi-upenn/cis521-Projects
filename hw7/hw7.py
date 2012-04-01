#!/usr/bin/python

from numpy import *
from Dataset import Dataset

# Bayesian Classifier
# First, we need to build the probability model

d = Dataset("rec.sport.hockey.txt", "rec.sport.baseball.txt", cutoff=200)
#d = Dataset("comp.sys.mac.hardware.txt", "comp.sys.ibm.pc.hardware.txt", cutoff=2000)
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

def ridgeTrain(X, Y, l = 1):
  Xt = matrix(X.T)
  return linalg.inv(Xt * matrix(X) + l * identity(X.shape[1])) * Xt * matrix(Y)

def ridgeClassify(x, w):
  return sign(dot(w, x))

def perceptronClassify(w, x):
  return sign(dot(w,x))

def perceptronTrain(X,Y, l = 1):
  w = random.rand(X.shape[1])
  perfect = False
  iterations = 0
  models = []
  while (not perfect and iterations < 100):
    iterations += 1
    perfect = True
    for i in range(X.shape[0]):
      result = perceptronClassify(w, X[i])
      if (result != Y[i]):
        perfect = False
        w = w + l * (Y[i] * X[i])
    models = models + [w]
  m = array(models)
  w = array([average(m[:,i]) for i in range(m.shape[1])])
  return (w, iterations)

def streamwiseTrain(X, Y, l = 1):
  def error(w,X,Y):
    return sum([sum(Y - dot(w,x)) + l * sum(w[w != 0]) for x in X])
  cols = []
  w = zeros(X.shape[0])
  e = 1
  for j in range(X.shape[1]):
    newCols = cols + [j]
    print(X[:,newCols])
    w = ridgeTrain(X[:,newCols], Y, l)
    curr = error(w,X,Y)
    if curr < w:
      cols = newCols
  return ridgeTrain(X[:,cols],Y,l)

def stepwiseTrain(X, Y, l = 1, maxFeatures = 50):
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

# (w, iterations) = perceptronTrain(Xtrain, Ytrain)
# w = ridgeTrain(Xtrain, Ytrain)
w = streamwiseTrain(Xtrain, Ytrain)
right = 0
wrong = 0
for i in range(Xtest.shape[0]):
  #result = perceptronClassify(w,Xtest[i])
  result = ridgeClassify(w,Xtest[i]) 
  if result == Ytest[i]:
    right += 1
  else:
    wrong += 1
print("Right: " + str(right) + "; wrong: " + str(wrong))
