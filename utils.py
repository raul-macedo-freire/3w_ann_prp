import pickle
import pandas as pd
import seaborn as sns
import matplotlib as plt
from numpy import ndarray
from os.path import isfile
from pandas import DataFrame
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report,accuracy_score,confusion_matrix




def save_csv_if_doesnt_exist(df:DataFrame,file_name:str,**kwargs):
    if not isfile(file_name):
        df.to_csv(file_name,**kwargs)
    return

def train_and_save_mlp(parameters, X, Y, file_name):
    estimator = MLPClassifier(max_iter=100)
    clf = GridSearchCV(estimator,parameters,n_jobs=-1, cv=5)
    clf.fit(X,Y)

    print(clf.best_params_)
    
    best_model = clf.best_estimator_
    with open(file_name, 'wb') as file:
        pickle.dump(best_model, file)
    return best_model

def train_model_if_doesnt_exist(X:ndarray,Y:ndarray,parameters:dict,file_name:str):
    if not isfile(file_name):
        return train_and_save_mlp(
            parameters, X, Y, file_name
        )
    with open(file_name, 'rb') as f:
        model = pickle.load(f)
    return model

def performance_metrics(Y_true,Y_pred):
    tn, fp, fn, tp = confusion_matrix(Y_true, Y_pred).ravel()
    recall = tp / (tp+fn)
    precision = tp / (tp+fp)
    specificity = tn / (tn+fp)
    accuracy = (tp+tn) / (tp+tn+fp+fn)
    f1_score = tp / (tp + ((fn+fp)/2))
    data = {
        'recall':recall,
        'precision':precision,
        'specificity':specificity,
        'accuracy':accuracy,
        'f1_score':f1_score,
    }
    return pd.DataFrame(data)

def plot_confusion_matrix(observed_data:ndarray,predicted_data:ndarray):
    mat = confusion_matrix(observed_data,predicted_data)
    sns.heatmap(mat.T,square=True,annot=True,fmt='d',linewidths=1)
    plt.xlabel('Observed')
    plt.ylabel('Predict')
    print(classification_report(observed_data,predicted_data))
    print('Accuracy is ',accuracy_score(observed_data,predicted_data))
    return

