import numpy as np
from sklearn.datasets import make_blobs
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import log_loss
import csv

def loadData(train_features_file_name='training_features.csv', \
             train_class_file_name='training_class_labels.csv', \
             test_features_file_name='test_features.csv', \
             instanceNum=10000, featureNum=3587):
    train_features_file = file(train_features_file_name)
    train_class_file = file(train_class_file_name)
    test_features_file = file(test_features_file_name)
    train_features = [[0 for col in range(featureNum)]for row in range(instanceNum)]
    reader = csv.reader(train_features_file)
    row = 0
    for line in reader:
        l = len(line)
        for col in range(l):
            train_features[row][col] = line[col]
        row += 1

    train_class = [[0] for row in range(instanceNum)]
    reader = csv.reader(train_class_file)
    row = 0
    for line in reader:
        train_class[row] = line[0]
        row += 1

    testInstanceNum = 8132 * 4
    test_features = [[0 for col in range(featureNum)] for row in range(testInstanceNum)]
    reader = csv.reader(test_features_file)
    row = 0
    for line in reader:
        l = len(line)
        for col in range(l):
            test_features[row][col] = line[col]
        row += 1

    return train_features, train_class, test_features
    
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
    
def SVM(train_features, train_class, test_features,
          classifierNum=100, classifierSize=500,
          testInstanceNum=8132):
    clfList = [[0] for i in range(classifierNum)]
    index = [i for i in range(10000)]

    for i in range(classifierNum):
        clfList[i] = svm.SVC(probability=True)
        np.random.shuffle(index)
        current_train_features = []
        current_train_class = []
        for j in range(classifierSize):
            current_train_features.append(train_features[index[j]])
            current_train_class.append(train_class[index[j]])
        print 'start train'
        clfList[i].fit(current_train_features, current_train_class)
        print i

    answer = []
    for i in range(testInstanceNum):
        best_answer = [0 for ttt in range(4)]
        print i
        for j in range(classifierNum):
            ans = classify(test_features, i, clfList[j])
            best_answer[ans] += 1
        answer.append(choose_best(best_answer))

    csvfile = file('test_class.csv', 'wb')
    writer = csv.writer(csvfile)
    writer.writerow(['id', 'correctAnswer'])
    for i in range(testInstanceNum):
        writer.writerow([102501 + i, answer[i]])
    csvfile.close()

def TrainRandomForest(train_features, train_class):
    instanceNum = len(train_features)
    trainSize = int(instanceNum * 0.8)
    X_train = train_features[0:trainSize]
    y_train = train_class[0:trainSize]
    X_valid = train_features[trainSize+1, instanceNum]
    y_valid = train_class[trainSize+1, instanceNum]
    
    randomForest = RandomForestClassifier(n_estimators=25)
    randomForest.fit(X_train, y_train)
    randomForest_probs = randomForest.predict_proba(X_test)
    sig_randomForest = CalibratedClassifierCV(randomForest, method="sigmoid", cv="prefit")
    sig_randomForest.fit(X_valid, y_valid)


    return randomForest

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
    return svmList

def classifyRandomForest(test_features, randomForest):
    sig_randomForest_probs = sig_randomForest.predict_proba(X_test)
    sig_randomForest_probs = sig_randomForest.predict_proba(X_test)

if __name__ == '__main__':
    train_features, train_class, test_features = loadData(\
                train_features_file_name='training_features.csv', \
                test_features_file_name='test_features.csv')
    randomForest = DoRandomForest(train_features, train_class, test_features)
    
