#!/usr/bin/python

from numpy import *
from Dataset import Dataset

# Bayesian Classifier
# First, we need to build the probability model

d = Dataset("rec.sport.baseball.txt", 
"rec.sport.hockey.txt", cutoff=1000)

#d = Dataset("comp.sys.mac.hardware.txt", "comp.sys.ibm.pc.hardware.txt", cutoff=2000)
(Xtrain, Ytrain, Xtest, Ytest) = d.getTrainAndTestSets(0.8, seed=5)
wordlist = d.getWordList()

def trainNaiveBayes(X, Y):
  # First, count frequencies given the category

  # Each row is a post, and each column is a word
  # To count the number of words from every post, sum up the values from each
  # column for a given category

  # Flattens Y so that it is easier to iterate over
  yFlat = Y.flatten()
  yPos = yFlat == 1
  yNeg = yFlat == -1

  # X.shape[1] returns number of columns for a given matrix
  numColumns = X.shape[1]

  # Indexing with a boolean array like yOne only checks indices that are True
  # For each column, this comprehension adds up values from the rows in that
  # column that match True indices in yPos or yNeg
  def getProb(yVector):
    total = sum( [sum(X[yVector,j]) for j in range(numColumns)] )

    # Need to pad each sum by one, and the total by the number of words, so as
    # to avoid zero probabilities
    total += X.shape[1]
    prob = array([ (sum(X[yVector,j]) + 1) / total for j in range(numColumns)])

    return prob

  probPos = getProb(yPos)
  probNeg = getProb(yNeg)
  
  # Since both of these probabilities have the same denominator, and we only care
  # about which one is greater, we can just drop the denominator entirely

  # The numbers are so small that products become impossible, so we can just
  # keep track of the ratios
  return (probPos,probNeg)

def naiveBayesClassify(probPos, probNeg, X, Y):
  probRatio = array([ probPos[i] / probNeg[i] for i in range(probPos.shape[0]) ])

  # Probabilties for each post
  postProb = []
  for i in range(X.shape[0]):
    # Probabilities for individual words in this post
    wordProb = []

    for j in range(X.shape[1]):
      if(X[i,j]):
        # Append prob to result
        wordProb = wordProb + [probRatio[j]]

    avgRatio = sum(wordProb) / len(wordProb)
    postProb = postProb + [avgRatio]

  estimates = []
  for i in range(len(postProb)):
    if(postProb[i] > 1.0):
      estimates = estimates + [1]
    else:
      estimates = estimates + [-1]

  right = 0
  wrong = 0
  for i in range(Y.shape[0]):
    if(estimates[i] == Y[i]):
      right += 1
    else:
      wrong += 1

  return (right,wrong)

def ridgeTrain(X, Y, l = 1):
  Xt = matrix(X.T)
  return linalg.inv(Xt * matrix(X) + l * identity(X.shape[1])) * Xt * matrix(Y)

def classify(x, w):
  return sign(dot(w, x))

def perceptronTrain(X,Y, l = 1):
  w = random.rand(X.shape[1])
  perfect = False
  iterations = 0
  models = []
  while (not perfect and iterations < 100):
    iterations += 1
    perfect = True
    for i in range(X.shape[0]):
      result = classify(w, X[i])
      if (result != Y[i]):
        perfect = False
        w = w + l * (Y[i] * X[i])
    models = models + [w]
  m = array(models)
  w = array([average(m[:,i]) for i in range(m.shape[1])])
  return (w, iterations)

def l2Error(w,X,Y,columns, l):
   s1 = sum([linalg.norm(Y - dot(w.T,x)) for x in X[:,columns]])
   s2 = l * linalg.norm(w)

   s3 = s1 + s2
   return s3

def error(w, X, Y, columns):
  X = X[:,columns]
  right = 0
  wrong = 0
  for i in range(X.shape[0]):
    result = classify(w,X[i]) 
    if result == Y[i]:
      right += 1
    else:
      wrong += 1
  return wrong

def streamwiseTrain(X, Y, l = 1):
  cols = []
  w = zeros(X.shape[0])
  e = sum([linalg.norm(Y) for x in X])
  for j in range(X.shape[1]):
    newCols = cols + [j]
    w = ridgeTrain(X[:,newCols], Y, l)
    curr = error(w,X,Y,newCols)  + l * linalg.norm(w)
    if curr < e:
      cols = newCols
      e = curr

  return (ridgeTrain(X[:,cols],Y,l),cols)

def stepwiseTrain(X, Y, l = 1, maxFeatures = 25):
  cols = []
  w = zeros(X.shape[0])
  e = sum([linalg.norm(Y) for x in X])
  while len(cols) < maxFeatures:
    best = None
    for j in range(X.shape[1]):
      if j in cols:
        continue
      newCols = cols + [j]
      w = ridgeTrain(X[:,newCols], Y, l)
      curr = error(w,X,Y,newCols) + l * linalg.norm(w)
      if curr < e:
        best = j
        e = curr
    if best == None:
      break
    else:
      cols = cols + [best]
  return (ridgeTrain(X[:,cols],Y,l),cols)

# Pardon the repetition in this function...
def runTests():
  print("\nTraining: Bayes...")
  (probPos,probNeg) = trainNaiveBayes(Xtrain,Ytrain)
  (right,wrong) = naiveBayesClassify(probPos,probNeg,Xtest,Ytest)
  print("Number Correct: " + str(right) + "\n")
  print("Number incorrect: " + str(wrong) + "\n")

if __name__ == "__main__":
  runTests()