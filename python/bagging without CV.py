import csv
from sklearn import svm
import numpy as np
import pickle

def loadTrainingData(train_features_file_name='training_features.csv',
             train_class_file_name='training_class_labels.csv',
             instanceNum=10000, featureNum=3587):
    train_features_file=file(train_features_file_name)
    train_class_file=file(train_class_file_name)
    
    train_features = [[0 for col in range(featureNum)]for row in range(instanceNum)]
    reader = csv.reader(train_features_file)
    row = 0
    for line in reader:
        l = len(line)
        for col in range(l):
            train_features[row][col] = float(line[col])
        row += 1

    train_class = [[0] for row in range(instanceNum)]
    reader = csv.reader(train_class_file)
    row = 0
    for line in reader:
        train_class[row] = float(line[0])
        row += 1
        
    return train_features, train_class


def loadTestingData(test_features_file_name='test_features.csv',
                     testInstanceNum=8132 * 4, featureNum=3587):
    test_features_file = file(test_features_file_name)
    test_features = [[0 for col in range(featureNum)] for row in range(testInstanceNum)]
    reader = csv.reader(test_features_file)
    row = 0
    for line in reader:
        l = len(line)
        for col in range(l):
            test_features[row][col] = line[col]
        row += 1
    return test_features
    
def classify(test_features, svm):
    max_prob = 0
    max_choice = 0
    for j in range(4):
        instance = test_features[j]
        # print svm.predict_proba(instance)
        p = svm.predict_proba(instance)[0][0]
        if p > max_prob:
            max_prob = p
            max_choice = j
    return max_choice


def choose_best(arr):
    best_num = 0
    best_choice = 'A'
    for i in range(4):
        if arr[i] > best_num:
            best_num = arr[i]
            if i == 0:
                best_choice = 'A'
            elif i == 1:
                best_choice = 'B'
            elif i == 2:
                best_choice = 'C'
            else:
                best_choice = 'D'
    return best_choice
    
def bagging_without_CV(train_features, train_class,
          classifierNum=100, classifierSize=500, featureSize=500):
        
    svmList = []
    index = [i for i in range(featureSize)]
    
    for i in range(classifierNum):
        print 'start', i
        np.random.shuffle(index)
        features = []
        class_labels = []
        for j in range(classifierSize):
            features.append(train_features[index[j]])
            class_labels.append(train_class[index[j]])
        current_svm = svm.SVC(probability=True)
        current_svm.fit(features, class_labels)
        svmList.append(current_svm)
        # print svmList[i].support_
    return svmList


def writeSVMList(svmList, fileName='svmList.txt'):
    f = open('svmList.txt', 'wb')
    pickle.dump(svmList, f)
        
def loadSVMList(fileName='svmList.txt'):
    f = open(fileName, 'rb')
    svmList = pickle.load(f)
    return svmList

def classifiyAllInstances(testInstanceNum, svmList, test_features):
    answer = []
    for i in range(testInstanceNum):
        best_answer = [0 for ttt in range(4)]
        print 'start classify'
        for svm in svmList:
            ans = classify(test_features, i, svm)
            best_answer[ans] += 1
        print i
        answer.append(choose_best(best_answer))

    csvfile = file('test_class.csv', 'wb')
    writer = csv.writer(csvfile)
    writer.writerow(['id', 'correctAnswer'])
    for i in range(testInstanceNum):
        writer.writerow([102501 + i, answer[i]])
        print i
    csvfile.close()

def loadAndClassify(svmList, testInstanceNum=8132 * 4, featureNum=3587,
                    test_features_file_name='test_features.csv'):
    test_features_file=file(test_features_file_name)
    reader = csv.reader(test_features_file)
    row = 0
    answer = []
    instances = [[0 for col in range(featureNum)] for c in range(4)]
    for line in reader:
        lineLength = len(line)
        for col in range(lineLength):
            instances[row % 4][col] = line[col]
        row += 1
        if not row % 4 == 0:
            continue
        best_answer = [0 for ttt in range(4)]
        for svm in svmList:
            ans = classify(instances, svm)
            best_answer[ans] += 1
        print row / 4
        answer.append(choose_best(best_answer))
    
    
    csvfile = file('test_class.csv', 'wb')
    writer = csv.writer(csvfile)
    writer.writerow(['id', 'correctAnswer'])
    for i in range(len(answer)):
        writer.writerow([102501 + i, answer[i]])
    csvfile.close()

def train():
    train_features, train_class = loadTrainingData(
                                                   train_features_file_name='train_1000.csv',
                                                   train_class_file_name='training_class_labels.csv',
                                                   instanceNum=10000, featureNum=1000)
    svmList = bagging_without_CV(train_features, train_class, classifierNum=200, classifierSize=500, featureSize=500)
    writeSVMList(svmList)

def test():
    #test_features = loadTestingData()
    svmList = loadSVMList()
    loadAndClassify(svmList, featureNum=1000, test_features_file_name='test_1000.csv')

if __name__ == '__main__':
    train()
    test()
