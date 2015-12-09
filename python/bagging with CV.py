import csv
from sklearn import svm
import numpy as np
import pickle

def loadTrainingData(train_features_file_name='training_features.csv',
             train_class_file_name='training_class_labels.csv',
             instanceNum=10000, featureNum=3587):
    train_features_file = file(train_features_file_name)
    train_class_file = file(train_class_file_name)
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


def loadTestingData(test_features_file_name = 'test_features.csv',
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
    
def classify(test_features, row, clf):
    max_prob = 0
    max_choice = 0
    for j in range(4):
        instance = test_features[row * 4 + j]
        p = clf.predict_proba(instance)[0][0]
        if p > max_prob:
            max_prob = p
            max_choice = j
    return max_choice

def getTrainingAndTuningSet(classifierNum, features, class_labels, trainingSize, tuningSize):
    randomTrainingFeaturesForEachClassifier = []
    randomTrainingClassLabelForEachClassifier = []
    randomTuningFeaturesForEachClassifier = []
    randomTuningClassLabelForEachClassifier = []

    index = [i for i in range(len(features))]
    
    for i in range(classifierNum):
        np.random.shuffle(index)    
        trainingFeatures = []
        trainingClassLabels = []
        tuningFeatures = []
        tuningClassLabels = []
        for j in range(trainingSize):
            trainingFeatures.append(features[index[j]])
            trainingClassLabels.append(class_labels[index[j]])
        for j in range(tuningSize):
            tuningFeatures.append([features[index[trainingSize + j]]])
            tuningClassLabels.append(class_labels[index[trainingSize + j]])
        
        randomTrainingFeaturesForEachClassifier.append(trainingFeatures)
        randomTrainingClassLabelForEachClassifier.append(trainingClassLabels)
        randomTuningFeaturesForEachClassifier.append(tuningFeatures)
        randomTuningClassLabelForEachClassifier.append(tuningClassLabels)
    
    # print np.shape(randomTrainingFeaturesForEachClassifier)
    # print np.shape(randomTrainingClassLabelForEachClassifier)
    # print np.shape(randomTuningFeaturesForEachClassifier)
    # print np.shape(randomTuningClassLabelForEachClassifier)
    
    return randomTrainingFeaturesForEachClassifier, randomTrainingClassLabelForEachClassifier, \
        randomTuningFeaturesForEachClassifier, randomTuningClassLabelForEachClassifier
        
        
def get_accuracy(svm, tuningFeatures, tuningClassLabels):
    sum = 0.0
    for i in range(len(tuningFeatures)):
        sum += (svm.predict_proba(tuningFeatures[i])[0][0] - tuningClassLabels[i]) ** 2
    return sum / len(tuningFeatures)

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
    
def bagging_with_CV(train_features, train_class,
          classifierNum=100, classifierSize=500,
          testInstanceNum=8132, testFeatureNum=3587,
          trainingSetSize=10, tuningSetSize=2,
          CList=[ 0.01, 0.03, 0.1, 0.3, 1],
          gammaList=[ 0.01, 0.03, 0.1, 0.3, 1]):
    
    trainingFeaturesList, trainingClassList, tuningFeaturesList, tuningClassList = \
     getTrainingAndTuningSet(classifierNum, train_features, train_class, trainingSetSize, tuningSetSize)
    
    svmList = [[0] for i in range(classifierNum)]
    accuracyList = [[[0.0  for g in range(len(gammaList))] for c in range(len(CList))] for t in range(classifierNum)]

    for i in range(classifierNum):
        print 'start', i
        best_accuracy_mean = 0
        best_index = 0
        current_svm_list = [[0] for cnt in range(len(CList) * len(gammaList))]
        
        for ci in range(len(CList)):
            for gi in range(len(gammaList)):
                print ci, gi
                current_index = ci * len(CList) + gi
                current_svm_list[current_index] = svm.SVC(probability=True, C=CList[ci], gamma=gammaList[gi])
                current_svm_list[current_index].fit(trainingFeaturesList[i], trainingClassList[i])
                mean_accuracy = get_accuracy(current_svm_list[current_index], tuningFeaturesList[i], tuningClassList[i])
                accuracyList[i][ci][gi] = mean_accuracy
                if mean_accuracy > best_accuracy_mean:
                    best_accuracy_mean = mean_accuracy
                    best_index = current_index
        svmList[i] = current_svm_list[best_index]
        print 'end', i
        # print svmList[i].support_
    return svmList, accuracyList


def writeSVMList(svmList, fileName='svmList.txt'):
    f = open('svmList.txt', 'wb')
    pickle.dump(svmList, f)
    print 'writer'
    for svm in svmList:
        print svm
    print
        
def loadSVMList(fileName='svmList.txt'):
    f = open(fileName, 'rb')
    svmList = pickle.load(f)
    print 'load'
    for svm in svmList:
        print svm
    print
    return svmList

def writeMeanAccuracy(accuracy, classifierNum=10,
                      CList=[0.01, 0.03, 0.1, 0.3, 1],
                      gammaList=[ 0.01, 0.03, 0.1, 0.3, 1]):
    head = ['C and gamma']
    head.extend(gammaList)
    for i in range(classifierNum):
        csvfile = file('./accuracy/accuracy for SVM' + str(i) + '.csv', 'wb')
        writer = csv.writer(csvfile)
        writer.writerow(head)
        for ci in range(len(CList)):
            row = [CList[ci]]
            print accuracy[i][ci]
            row.extend(accuracy[i][ci])
            writer.writerow(row)
        csvfile.close()

'''
    answer = []
    for i in range(testInstanceNum):
        best_answer = [0 for ttt in range(4)]
        print 'start classify'
        for j in range(classifierNum):
            ans = classify(test_features, i, svmList[j])
            best_answer[ans] += 1
        print i
        answer.append(choose_best(best_answer))

    csvfile = file('test_class.csv', 'wb')
    writer = csv.writer(csvfile)
    writer.writerow(['id','correctAnswer'])
    for i in range(testInstanceNum):
        writer.writerow([102501+i, answer[i]])
        print i
    csvfile.close()
'''

def loadAndClassify(svmList, testInstanceNum=8132 * 4, featureNum=3587,
                    test_features_file_name='test_features.csv'):
    test_features_file = file(test_features_file_name)
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
        print 'start classify'
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
                                                   train_features_file_name='train_500.csv',
                                                   train_class_file_name='training_class_labels.csv',
                                                   instanceNum=10000, featureNum=500)
    svmList, accuracyList = bagging_with_CV(train_features, train_class,
                                            classifierNum=100, trainingSetSize=500,
                                            tuningSetSize=500)
    writeSVMList(svmList)
    writeMeanAccuracy(accuracyList, classifierNum=100)

def test():
    # test_features = loadTestingData()
    svmList = loadSVMList()
    loadAndClassify(svmList, test_features_file_name='test_500.csv',featureNum=500)

if __name__ == '__main__':
    train()
    test()
