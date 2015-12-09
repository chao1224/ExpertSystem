import csv
from sklearn import svm
import numpy as np

def loadData(train_features_file=file('training_features.csv'),
             train_class_file=file('training_class_labels.csv'),
             test_features_file=file('test_features.csv'),
             instanceNum = 10000, featureNum = 3587):
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
        instance = test_features[row*4+j]
        p = clf.predict_proba(instance)[0][0]
        if p > max_prob:
            max_prob = p
            max_choice = j
    return max_choice

def choose_best(arr):
    best_num = 0
    best_choice = 'A'
    for i in range(4):
        if arr[i]>best_num:
            best_num = arr[i]
            if i == 0:
                best_choice = 'A'
            elif i==1:
                best_choice = 'B'
            elif i==2:
                best_choice = 'C'
            else:
                best_choice = 'D'
    return best_choice
    
def bagging_SVM(train_features, train_class, test_features,
          classifierNum = 100, classifierSize = 500,
          testInstanceNum = 8132, testFeatureNum = 3587):
    clfList = [[0] for i in range(classifierNum)]
    index = [i for i in range(10000)]

    for i in range(classifierNum):
        clfList[i] = svm.SVC(probability = True)
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
        print 'start classify'
        for j in range(classifierNum):
            ans = classify(test_features, i, clfList[j])
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


if __name__ == '__main__':
    train_features, train_class, test_features = loadData()
    bagging_SVM(train_features, train_class, test_features, classifierSize = 600)
    
